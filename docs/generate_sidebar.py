"""
Build a VitePress sidebar object by walking the writeups/ and notes/ folders.

Run from the docs directory (next to writeups/, notes/, .vitepress/):

    python generate_sidebar.py

By default it rewrites `.vitepress/config.mts` with the new sidebar. Use
`--print` to only emit JSON to stdout (no file write), or `--root <path>` to
target a different docs root.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from urllib.parse import quote


def read_title(md_path: Path) -> str:
    """Return the first Markdown heading in the file, ignoring front matter."""
    try:
        with md_path.open("r", encoding="utf-8") as handle:
            in_frontmatter = False
            for raw_line in handle:
                line = raw_line.strip()
                if line == "---":
                    in_frontmatter = not in_frontmatter
                    continue
                if in_frontmatter:
                    continue
                if line.startswith("#"):
                    return line.lstrip("#").strip()
    except OSError:
        pass
    return md_path.stem.replace("-", " ").strip() or md_path.stem


def parse_date_str(raw: str) -> Optional[datetime]:
    """Parse a date string using common formats; return None if unrecognized."""
    raw = raw.strip().strip("'\"")
    if not raw:
        return None
    formats = [
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%m-%d-%Y",
        "%m/%d/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def extract_frontmatter(md_path: Path) -> Dict[str, object]:
    """
    Return metadata from YAML front matter: tags (list[str]) and date (datetime|None).
    """
    tags: List[str] = []
    date: Optional[datetime] = None
    try:
        with md_path.open("r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError:
        return {"tags": tags, "date": date}

    if not lines or lines[0].strip() != "---":
        return {"tags": tags, "date": date}

    # Capture lines until closing '---'
    frontmatter: List[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        frontmatter.append(line.rstrip("\n"))

    in_tags = False
    for line in frontmatter:
        stripped = line.strip()

        if in_tags:
            if stripped.startswith("-"):
                item = stripped.lstrip("-").strip().strip("'\"")
                if item:
                    tags.append(item)
                continue
            else:
                in_tags = False  # fall through to process other keys

        if stripped.startswith("tags:"):
            # could be tags: ["a", "b"] or start of block
            if "[" in stripped:
                inline = stripped.split("tags:", 1)[1]
                inline = inline.strip().lstrip("[").rstrip("]")
                for part in inline.split(","):
                    item = part.strip().strip("'\"")
                    if item:
                        tags.append(item)
            else:
                in_tags = True
            continue

        if stripped.startswith("date:") and date is None:
            raw_date = stripped.split("date:", 1)[1].strip()
            parsed = parse_date_str(raw_date)
            if parsed:
                date = parsed
    return {"tags": tags, "date": date}


def pick_display_tags(tags: Iterable[str]) -> List[str]:
    """Return matching tags (capitalized) in preferred order; can be multiple."""
    preferred = ["web", "pwn", "rev", "crypto", "forensics", "hardware", "iot"]
    lower_tags = [t.lower() for t in tags]
    found: List[str] = []
    for pref in preferred:
        if pref in lower_tags:
            found.append(pref.capitalize())
    return found


def _is_list_item(line: str) -> bool:
    stripped = line.lstrip()
    if not stripped:
        return False
    if stripped.startswith(("-", "*")):
        return True
    # numbered list: "1.", "12)", "1)"
    if stripped[0].isdigit():
        for sep in (".", ")"):
            if sep in stripped:
                prefix = stripped.split(sep, 1)[0]
                if prefix.isdigit():
                    return True
    return False


def _is_fence(line: str) -> bool:
    return line.strip().startswith("```")


def cleanup_writeup_markdown(md_path: Path) -> bool:
    """
    Remove blank lines that sit directly between list items to tidy spacing.
    Returns True if a change was made.
    """
    try:
        lines = md_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return False

    if not lines:
        return False

    new_lines: List[str] = []
    changed = False

    for idx, line in enumerate(lines):
        if not line.strip() and idx > 0 and idx + 1 < len(lines):
            prev = lines[idx - 1]
            nxt = lines[idx + 1]
            prev_is_special = _is_list_item(prev) or _is_fence(prev)
            next_is_special = _is_list_item(nxt) or _is_fence(nxt)
            # Only strip if both sides are list items or code fences
            if prev_is_special and next_is_special:
                changed = True
                continue
        new_lines.append(line)

    if changed:
        md_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return changed


def build_writeups_sidebar(writeups_root: Path) -> List[Dict]:
    """Construct sidebar items from writeups/<year>/<event>/<challenge>/writeup.md."""
    years: List[Dict] = []

    year_dirs = [d for d in writeups_root.iterdir() if d.is_dir()]
    year_dirs.sort(
        key=lambda d: int(d.name) if d.name.isdigit() else d.name, reverse=True
    )

    for year_dir in year_dirs:
        events: List[Dict] = []

        event_dirs = [d for d in year_dir.iterdir() if d.is_dir()]
        for event_dir in event_dirs:
            challenges_raw: List[Dict] = []
            for challenge_dir in event_dir.iterdir():
                if not challenge_dir.is_dir():
                    continue

                writeup_file = challenge_dir / "writeup.md"
                if not writeup_file.exists():
                    continue

                meta = extract_frontmatter(writeup_file)
                text = read_title(writeup_file)
                tags = pick_display_tags(meta.get("tags", []))
                if tags:
                    text = f"{text} ({', '.join(tags)})"
                link = "/".join(
                    [
                        "",
                        "writeups",
                        quote(year_dir.name, safe=""),
                        quote(event_dir.name, safe=""),
                        quote(challenge_dir.name, safe=""),
                        "writeup",
                    ]
                )
                challenges_raw.append(
                    {
                        "text": text,
                        "link": link,
                        "_date": meta.get("date"),
                        "_name": challenge_dir.name.lower(),
                    }
                )

            if not challenges_raw:
                continue

            challenges_raw.sort(key=lambda c: c["_name"])
            challenges_raw.sort(
                key=lambda c: c["_date"] or datetime.min, reverse=True
            )
            challenges = [{"text": c["text"], "link": c["link"]} for c in challenges_raw]

            event_date = max(
                (c["_date"] for c in challenges_raw if c["_date"] is not None),
                default=None,
            )

            events.append(
                {
                    "text": event_dir.name,
                    "collapsed": True,
                    "items": challenges,
                    "_date": event_date,
                    "_name": event_dir.name.lower(),
                }
            )

        if not events:
            continue

        events.sort(key=lambda e: e["_name"])
        events.sort(key=lambda e: e["_date"] or datetime.min, reverse=True)

        cleaned_events = [
            {"text": e["text"], "collapsed": e["collapsed"], "items": e["items"]}
            for e in events
        ]

        years.append({"text": year_dir.name, "items": cleaned_events})

    return years


def build_notes_sidebar(notes_root: Path) -> List[Dict]:
    """Construct sidebar items from notes/*.md."""
    items: List[Dict] = []

    for note_file in sorted(notes_root.glob("*.md")):
        text = read_title(note_file)
        link = f"/notes/{note_file.stem}"
        items.append({"text": text, "link": link})

    if not items:
        return []

    return [{"text": "Notes", "items": items}]


def cleanup_all_writeups(writeups_root: Path) -> None:
    """Clean up list spacing inside every writeup.md under writeups_root."""
    for year_dir in writeups_root.glob("*"):
        if not year_dir.is_dir():
            continue
        for event_dir in year_dir.glob("*"):
            if not event_dir.is_dir():
                continue
            for challenge_dir in event_dir.glob("*"):
                if not challenge_dir.is_dir():
                    continue
                md_path = challenge_dir / "writeup.md"
                if md_path.exists():
                    cleanup_writeup_markdown(md_path)


def generate_sidebar(root: Path) -> Dict[str, List[Dict]]:
    writeups_root = root / "writeups"
    notes_root = root / "notes"

    sidebar: Dict[str, List[Dict]] = {}

    if writeups_root.exists():
        cleanup_all_writeups(writeups_root)
        sidebar["/writeups/"] = build_writeups_sidebar(writeups_root)
    if notes_root.exists():
        sidebar["/notes/"] = build_notes_sidebar(notes_root)

    return sidebar


def format_sidebar_for_config(sidebar: Dict[str, List[Dict]]) -> str:
    """Render the sidebar dictionary into a TypeScript-friendly block."""
    json_str = json.dumps(sidebar, indent=4)
    lines = json_str.splitlines()
    if not lines:
        return "        sidebar: {},\n\n"

    lines[0] = f"        sidebar: {lines[0]}"
    for i in range(1, len(lines)):
        lines[i] = "        " + lines[i]
    return "\n".join(lines) + ",\n\n"


def replace_sidebar_block(config_text: str, sidebar: Dict[str, List[Dict]]) -> str:
    """
    Replace the existing sidebar block in config.mts with the generated one.

    The replacement is bounded from the start of the 'sidebar:' line to the
    line before the next 'search:' block. This assumes the config keeps the
    same ordering (sidebar then search) which matches the current repo.
    """
    marker = "\n        search:"
    start = config_text.find("        sidebar:")
    if start == -1:
        raise ValueError("sidebar property not found in config.mts")

    end = config_text.find(marker, start)
    if end == -1:
        raise ValueError("search block marker not found after sidebar in config.mts")

    new_block = format_sidebar_for_config(sidebar)
    return config_text[:start] + new_block + config_text[end:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate VitePress sidebar data.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Docs root containing writeups/ and notes/ (default: script directory)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to .vitepress/config.mts (default: <root>/.vitepress/config.mts)",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print sidebar JSON instead of writing to config.mts.",
    )
    args = parser.parse_args()

    sidebar = generate_sidebar(args.root)
    if args.print:
        print(json.dumps(sidebar, indent=4))
        return

    config_path = (
        args.config
        if args.config is not None
        else args.root.joinpath(".vitepress", "config.mts")
    )

    try:
        config_text = config_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Failed to read {config_path}: {exc}")

    try:
        new_content = replace_sidebar_block(config_text, sidebar)
    except ValueError as exc:
        raise SystemExit(f"Could not update sidebar: {exc}")

    try:
        config_path.write_text(new_content, encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Failed to write {config_path}: {exc}")

    print(f"Updated sidebar in {config_path}")


if __name__ == "__main__":
    main()
