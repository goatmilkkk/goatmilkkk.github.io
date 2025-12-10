# SEH

> based on Itanium ABI C++ exceptions

Error handling works as such:

1. Run code in the `try` block
2. If an error gets thrown, control will be passed to the `catch` block

When control is passed over, a few things occur:

1. Find matching exception handler
2. Unwind stack
    - Pop frames
    - Run destructors
    - Restore required registers (for execution of `catch` block)

The binary will store metadata for stack unwinding in the `.eh_frame` section:

```bash
readelf -wf main 2>/dev/null
```

