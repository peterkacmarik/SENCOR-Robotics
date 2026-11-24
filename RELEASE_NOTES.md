# Release notes — source patch only

This "release" intentionally contains **no APK binary**. It provides the reproducible source
patch for SENCOR Robotics **5.0.7** that fixes:

- startup crash on MIUI/HyperOS (POCO, Android 14) caused by `Window.getInsetsController()`
  being called before `DecorView` exists;
- 319 missing Slovak/Czech translations (`CL_*`, `CT_*`, `CWF_*`, `FUN_*`, `LG_*`, `MA_*`, ...) that appeared as raw keys in the UI.

Clone the repo, supply your own legally obtained original APK (SHA256
`D4B325BEAE61B487BE24F138FEBAA24A13DF05FD55A09F7598F3FE0CFB392598`), then follow `BUILD.md`.

The build script verifies the APK signature and prints the resulting SHA256. With the pinned
tool versions (JDK 17, android-35, build-tools 36.0.0, apktool 3.0.2), all ZIP entries of the
result are byte-identical to the tested build; only the signing timestamp differs.

See `DISCLAIMER.md` before use. Not affiliated with the vendor.
