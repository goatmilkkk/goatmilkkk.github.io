---
tags: ["rev", "anti-analysis"]
date: 14-12-2025
---

# ez-flag-checker

This was a relatively simple challenge in SECCON, but for some reason Claude MCP wasn't able to solve it, so I had to manually do so. Since the encryption scheme was a XOR operation that reuses the same key, my solution was to patch my input to be my expected output instead.

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  uint8_t encrypted_output[32]; // [rsp+20h] [rbp-130h] BYREF
  char buf[264]; // [rsp+40h] [rbp-110h] BYREF
  unsigned __int64 v6; // [rsp+148h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  printf("Enter flag: ");
  if ( fgets(buf, 256, stdin) )
  {
    buf[strcspn(buf, "\n")] = 0;
    if ( strlen(buf) == 26 && !strncmp(buf, "SECCON{", 7u) && buf[25] == 125 )
    {
      sigma_encrypt(&buf[7], encrypted_output, 0x12u); // here
      if ( !memcmp(encrypted_output, expected_output, 0x12u) )
      {
        puts("correct flag!");
        result = 0;
      }
      else
      {
        puts("wrong :(");
        result = 1;
      }
        
     ...
         
}    
```
```c
void __cdecl sigma_encrypt(const char *user_input, uint8_t *out, size_t len)
{
  int i; // [rsp+30h] [rbp-30h]
  uint32_t w; // [rsp+34h] [rbp-2Ch]
  size_t i_0; // [rsp+38h] [rbp-28h]
  uint8_t key_bytes[24]; // [rsp+40h] [rbp-20h]
  unsigned __int64 v7; // [rsp+58h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  for ( i = 0; i <= 3; ++i )
  {
    w = sigma_words[i];
    key_bytes[4 * i] = w;
    key_bytes[4 * i + 1] = BYTE1(w);
    key_bytes[4 * i + 2] = BYTE2(w);
    key_bytes[4 * i + 3] = HIBYTE(w);
  }
  for ( i_0 = 0; i_0 < len; ++i_0 )
    out[i_0] = (i_0 + key_bytes[i_0 & 0xF]) ^ user_input[i_0];
  if ( v7 != __readfsqword(0x28u) )
    (MEMORY[0x7FFFF7D365C0])();
}
```

After the CTF, someone mentioned that this was because of some `reloc` stuff that patches the state that generates the XOR key at runtime. By setting a hardware breakpoint on `sigma_words`, we are able to pinpoint the cause behind this :)

Turns out in the ELF relocation table, there was a monkey patch that patches the memory location at `0x4014` to `3320626Eh` by 'relocating' it, pretty neat trick!

```c
LOAD:0000555555554668 ; ELF RELA Relocation Table
LOAD:0000555555554668                 Elf64_Rela <4008h, 8, 4008h> ; R_X86_64_RELATIVE +4008h
LOAD:0000555555554680                 Elf64_Rela <3F98h, 100000006h, 0> ; R_X86_64_GLOB_DAT __libc_start_main
LOAD:0000555555554698                 Elf64_Rela <3FA0h, 200000006h, 0> ; R_X86_64_GLOB_DAT strncmp

...

LOAD:0000555555554800                 dq 4014h                ; r_offset ; // here
LOAD:0000555555554808                 dq 20h                  ; r_info
LOAD:0000555555554810                 dq 3320626Eh            ; r_addend

...

LOAD:0000555555554818 LOAD            ends
```
```c
// https://man7.org/linux/man-pages/man5/elf.5.html
00000000 struct Elf64_Rela {                                      
00000000     unsigned __int64 r_offset; // addr to patch
00000008     unsigned __int64 r_info; // R_X86_64_SIZE32, writes low 32 bits
00000010     __int64 r_addend; // value to patch at addr 
00000018 };
```

