# Pump Guardian

> TUI water valve control program where the goal is to input the correct sequence of twelve commands

## Remote Debugging

```bash
wsl -d Ubuntu-24.04
bash
lsb_release -a

sudo cp linux_server /usr/local/bin/
sudo chmod +x /usr/local/bin/linux_server

cd ~/bins/pump-guardian/
chmod u+x ./pump
linux_server ./pump
```

## Triage

- Initial triage reveals that the water valve control program is compiled using Rust:

![image-20251125231709281](images/image-20251125231709281.png)

## Analysis

Since the binary is very large, contains framework code and is coded in Rust, we have to filter out the noise and reduce the scope of our analysis:

- Is it possible to skip to the get_flag function directly?
- Else, pinpoint where the comparison against the twelve commands is made

I used MCP to speed up the analysis process with the following prompt:

```
scope: pump-guardian folder

objective: figure out the correct sequence of twelve commands in order to get the flag

analyze binary, rename variables and functions, comment
```

```
call    validate_command_exists; 
...
movzx   r15d, dx // bp AFTER this insn!
```

```
[mappings]
7391 start 
2748 stop 
1f3e flow 
9122 speed 
eefa manual
```

```
Apparently the commands are two-byte IDs

[heap]:0000555555642090 dw 2748h stop             
[heap]:0000555555642092 dw 7391h start
[heap]:0000555555642094 dw 0EEFAh auto
[heap]:0000555555642096 dw 0EEFAh auto
[heap]:0000555555642098 dw 2748h stop
[heap]:000055555564209A dw 1F3Eh flow
[heap]:000055555564209C dw 9122h speed
[heap]:000055555564209E dw 7391h start
[heap]:00005555556420A0 dw 2748h stop
[heap]:00005555556420A2 dw 1F3Eh flow
[heap]:00005555556420A4 dw 9122h speed
[heap]:00005555556420]A6 dw 7391h start // enter commands from bottom to top, params not impt based on testing
```

```
honestly the AI  inaccurate, so it's important to test & verify yourself:
- validatate_command_exists was more of a encrypt_command function

Claude identified the comparison at line 1968: if ( *(v352 + 2 * v358) == v356 )
-> Comparison doesn't change no matter what command I entered so it's probably wrong
-> Went to trace backwards from v356 and got the full EXPECTED_COMMANDS_ARRAY
```

Honestly, I only managed to solve this challenge because of MCP and a lot of guessing so the writeup is really bad. Not sure if there's a better/proper way to reverse this.

Flag: `ACS{R4taTu1i_Is_a_B2sT!!!}` -> https://ratatui.rs/

