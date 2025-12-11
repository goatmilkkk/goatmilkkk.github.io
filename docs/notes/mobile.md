### Mobile

> https://www.notion.so/goatmilkk/Mobile-5c861906257f44c085804a86ca230f50

| Component | Description              | Relevant Info                                                | Analogy         |
| --------- | ------------------------ | ------------------------------------------------------------ | --------------- |
| Activity  | Each activity = 1 screen | - entry point is `MainActivity`<br />- can call directly if it has `<exported>` | web page        |
| Intent    | Send a message           | - consists of fields like `<action>`, `<data>`, `<category>` | client request  |
| Receiver  | Listen for broadcasts    | - app-wide/system-wide broadcasts                            | server listener |

### ItsOnFire (Flare-on 10)

- Android stores strings in `res/values/strings.xml`

### BrainCalc (Python in Android)

- Observe in Manifest `package` and `MainActivity` to find the flag

### Apkocalypse (APK Patching)

- Use `apk.sh` to help patch

  - remove the obsolete flag `--use-aapt2` in `apk.sh`
  - rename `<apk_dir>` to `file` before building

  ```
  ./apk.sh decode <apk_name>
  ./apk.sh build <apk_dir>
  ```

- `Android Studio` to emulate

  - View APK files via `adb shell` (ALT + F12 for Terminal)

  - Get phone architecture via `adb shell getprop ro.product.cpu.abi`

### Androbro (JNI Dynamic Registration, Frida hooking)

- Set-up `frida-server`

  ```python
  # Match architecture (add ADB to path `%userprofile%\AppData\Local\Android\sdk\platform-tools`)
  adb shell getprop ro.product.cpu.abi
  
  # Download from https://github.com/frida/frida/releases (pip install frida==16.2.1 frida-tools==12.3.0)
  adb push frida-server-16.2.1-android-x86 /data/local/tmp/frida-server
  adb shell chmod 755 /data/local/tmp/frida-server
  
  # Run frida-server (as root)
  adb shell "su 0 /data/local/tmp/frida-server &"
  
  # Restart frida-server
  adb shell ps | grep frida
  adb shell "su 0 kill -9 <pid>"
  ```

- Load `frida` scripts

  ```javascript
  // load script at startup
  frida -U -f com.defensys.androbro -l C:\Users\twist\Downloads\hook.js 
  
  // load script after attaching (put script in cmd dir first)
  frida -U -f com.defensys.androbro
  %load hook.js 
  
  // hook strcmp (very noisy)
  frida-trace -U -i strcmp -f com.defensys.androbro
  ```

- Broadcast Intent

  ```bash
  // broadcast Intent to Receiver (-a is action, -es is extra string)
  adb shell am broadcast -a "THE_TRIGER"
  adb shell am broadcast -a "THE_UNLOCKER" --es key "6a209693a9acaf10dcd2e425bab62a5e48698b7fc3"
  ```

- Challenge Notes

  ```
  **(&qword_E88FC - 154) -> key [make as struct???]
  setup with THE_TRIGER, THE_UNLOCKER -> to activate, unlock
  get the key and stuff
  ```

### PricelessL3ak (Trigger Exports, Intents)

- Launch Exported Activity

  - What flag
    - FLAG_ACTIVITY_NEW_TASK = 0x10000000 (this is automatically set)
    - FLAG_ACTIVITY_SINGLE_TOP = 0x20000000
  - What password
    - it's cooked (need reverse VM) .-.

  ```bash
  // trigger onCreate
  adb shell am start -n ctf.l3akctf.pricelessl3ak/.h1832fla12 -a "BINGO"
  
  // trigger onNewIntent
  adb shell am start -n ctf.l3akctf.pricelessl3ak/.h1832fla12 -a "BANGO" -f 0x30000000 --es f "217sd87as" 
  ```