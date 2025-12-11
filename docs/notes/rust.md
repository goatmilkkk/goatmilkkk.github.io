# Rust

| Term    | Description                                       |
| ------- | ------------------------------------------------- |
| cargo   | Rust's project manager (think pip/go command)     |
| crate   | a Rust package (compiles into a a binary/library) |
| modules | code files/folders in a crate (e.g. `.rs`)        |

## Rust Commands

```rust
cargo add hex // adds hex crate to .toml
cargo run
```

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

## Rust Functions

> Findings from comparing Rust source code against IDA's decompilation of it (ABI lowering)

| Argument | Description               | Comments                                                     |
| -------- | ------------------------- | ------------------------------------------------------------ |
| 1        | return value pointer      | click on argument after stepping over the function call (instead of rdi) |
| 2        | calling object            | *only exists when there's a method call                      |
| 3        | actual Rust function args | -                                                            |

```rust
// Rust source
cipher = Aes256Gcm::new(key);
cipher.decrypt(nonce, ciphertext.as_ref()); // method call

// decompiled Rust
<aes_gcm::AesGcm<Aes,NonceSize,TagSize> as crypto_common::KeyInit>::new(cipher, &key);
<Alg as aead::Aead>::decrypt(ret_val, cipher, nonce, ct); // cipher is the calling object
```

### Return Value

- Sometimes it points to a string directly

- Other times it points to a struct like:

  ```c
  ret_val {
  	int count;
  	void* data; // deref to get useful data
  }
  ```

## Rust Paths

- `crate::module::type::function`
- `crate::type::function`
- `crate::function`

## Other

- https://research.checkpoint.com/2023/rust-binary-analysis-feature-by-feature/
- https://github.com/h311d1n3r/Cerberus