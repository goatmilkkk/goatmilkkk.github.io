# ex-cute

> cpp-exception based stack vm

## Analysis

<u>chain_exceptions</u>

- dynamic control flow: calculate next target func
- increase offset by rbx (how does rbx get set?)
- why does rsp increase by 0x10? is this consistent?

```python
while:
    calculate_target_func(const)
    try:
        target()
    catch:
        rbx += ?
        rsp += ?
```

### target_func(s)
```c
push    rbx
...  # sus code here! (extract out)
mov     edi, 10h
...
throw(rdi)  # pass control flow back to chain_exceptions with new rbx!
```

## Methodology

### Extract VM Operations

- need to figure out order of target funcs called
- stack-based -> hard to static since i couldn't figure out how rbp/rsp get incremented -> lets dynamic

- bp each useful instruction operation
  - write pseudocode for operations
  - keep track of arguments

### Deobfuscate Instructions

- Tell AI to analyze stage 1 first, since it's simple per-byte encryption

  - From there, figure out what we can remove to deobfuscate

    1. find user input in the extracted vm insns

    2. trace operations that act on it