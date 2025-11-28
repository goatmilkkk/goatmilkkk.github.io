---
tags: ["reverse", "php", "hooking"]
date: 2-11-2025
---

# Matryoshka

> Deobfuscate the huge PHP code to get the flag!

We were given a PHP script containing many layers of obfuscated code, all executed using `eval`. Hence, the best way that I could think of to handle this was to hook onto the PHP functions and print its arguments.

Before we proceed, let's cover a few terminologies:

- Zend Engine: VM that runs PHP
- [uopz](https://github.com/krakjoe/uopz): Exposes user operations for Zend Engine
  - This is what we will be using to hook onto the PHP functions
    - Note that this doesn't work for `eval` since that's a special language construct (i.e. not a function)

    ```bash
    # https://github.com/krakjoe/uopz/blob/master/INSTALL.md
    sudo apt-get install php8.1 php8.1-dev
    sudo pecl install uopz
    ```

Now all we have to do is (slowly) write a hooking script to solve this. Final solve script:

```php
<?php
// php harness.php round_11.php > round_12.php

const PHP_HEADER  = "<?php ";
const PHP_TRAILER = " ?>";

$result = NULL;

function add_tags($string) {
    return PHP_HEADER . $string . PHP_TRAILER;
}

function is_ascii(string $s): bool {
    return preg_match('/^[\x20-\x7E]+$/', $s) === 1;
}

function remove_hooks() {
    uopz_unset_hook("hex2bin");
    uopz_unset_hook("base64_decode");
    uopz_unset_hook("gzinflate");
}

uopz_set_hook("hex2bin", function ($string) use (&$result) {
    $out = hex2bin($string);
    if (is_ascii($out)) {
        if ($out[0] === '"') { // hex string "\x2f\x20 ..."
            $result = PHP_HEADER . "stripcslashes(" . $out . ")" . PHP_TRAILER; // stripcslashes adds " to result which is undesirable
        } else {
            $result = add_tags($out);
        }
    }
    //print substr($out, 0, 20);
});

uopz_set_hook("base64_decode", function ($string) use (&$result) {
    $out = base64_decode($string);
    if (is_ascii($out)) {
        if ($out[0] === '"') { // hex string "\x2f\x20 ..."
            $result = PHP_HEADER . "stripcslashes(" . $out . ")" . PHP_TRAILER;
        } else {
            $result = add_tags($out);
        }
    }
    //print substr($out, 0, 20);
});

uopz_set_hook("gzinflate", function ($string) use (&$result) {
    //remove_hooks();
    $out = gzinflate($string);
    $result = add_tags($out);
});

uopz_set_hook("gzuncompress", function ($string) use (&$result) {
    //remove_hooks();
    $out = gzuncompress($string);
    $result = add_tags($out);
});

uopz_set_hook("stripcslashes", function ($string) use (&$result) {
    $out = stripcslashes($string);
    $result = add_tags($out);
});

include($argv[1]);

echo $result; // If there are multiple hooks triggered in one run, override with the latest result. Doing it this way allows us to skip some of the middle layers too :)

?>
```

