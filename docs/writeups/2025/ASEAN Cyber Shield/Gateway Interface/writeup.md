---
tags: ["pwn", "iot", "mips"]
date: 04-12-2025
---

# Gateway Interface

> router pwn

## Setup

Copy dependencies in Docker file
```bash
chmod u+x gateway-server
export QEMU_LD_PREFIX=/usr/mipsel-linux-gnu
qemu-mipsel-static -g 23946 gateway-server
```
## Triage

Router barely has any defensive mechanisms:
```python
$ checksec gateway-server
Arch:       mips-32-little
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX unknown - GNU_STACK missing
PIE:        No PIE (0x400000)
Stack:      Executable
RWX:        Has RWX segments
```
## Analysis

- Identify vuln using MCP
  - Stack overflow in `gi::ApplyWifiConfig` via `memmove` with improper bounds check
    ```c
    v15 = "ssid=";
    parse_data(n, data1, data0, 5u, "ssid=");
    ssid_size = n[0];
    ssid = n[1];
    v15 = "key=";
    size = 4;
    parse_data(v16, v18, v19, 4u, "key=");
    v6 = v16[0];
    v7 = v16[1];
    if ( ssid_size >= 2 )
    {
        memmove(buf, ssid, ssid_size); // overflow here!
        LABEL_3:
        v8 = v6 < 2;
        goto LABEL_4;
    }
    ```
- Figure out how to trigger vuln
  - `x-ref` ->`POST /cgi-bin/wifi`
    ````c
    if ( !std::string::compare(a1 + 4, "POST") && !std::string::compare(a1 + 76, "/cgi-bin/wifi") )
    {
        ...
        if ( v35 )
            gi::SetUserCmd(v35 + 28);
        sub_407534(&buf);
        if ( buf != v74 )
            operator delete(buf, 4 * v72);
        v36 = gi::ApplyWifiConfig(&v78); 
    	...
    }
    ````
- Exploit the vuln!
  - write shellcode on stack
    - craft shellcode using [assembler](https://shell-storm.org/online/Online-Assembler-and-Disassembler/)
    - nops + shellcode
