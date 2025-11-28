## Rust Terminologies

| Term    | Description                                       |
| ------- | ------------------------------------------------- |
| cargo   | Rust's project manager (think pip/go command)     |
| crate   | a Rust package (compiles into a a binary/library) |
| modules | code files/folders in a crate (e.g. `.rs`)        |

## Rust Strings

> https://nikhilh-20.github.io/blog/luna_ransomware/#rust-strings

- Not null-terminated

| Type            | String Slice (&str)                                          | String                                                       |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Struct          | struct str {<br />    QWORD val;<br />    QWORD len;<br />}; | struct String {<br />    QWORD val;<br />    QWORD len;<br />    QWORD cap; // realloc if exceeds cap |
| Size            | 16 bytes                                                     | 24 bytes                                                     |
| Memory Location | stack/heap                                                   | heap                                                         |
| Mutability      | immutable                                                    | mutable                                                      |

## Rust Tools

- [rustbininfo](https://github.com/N0fix/rustbininfo)

```bash
pipx install rustbininfo
rbi [-f] ./file
```

