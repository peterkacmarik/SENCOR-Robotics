# SENCOR Robotics 5.0.7 — startup & localization fix

**Source patch only. No APK is distributed in this repository.**

This repo contains a reproducible patch that you apply to **your own, legally obtained**
`SENCOR+Robotics_5.0.7_APKPure.apk`. It fixes two problems found in the original app:

1. **Startup crash on MIUI / HyperOS (POCO, Android 14)** – `LogoActivity.initSystemBarColor()`
   called `Window.getInsetsController()` before the `DecorView` existed → `NullPointerException`
   and an immediate force-stop. A small `ContentProvider` pre-creates the decor view.
2. **Missing Slovak/Czech translations** – 319 keys (`CL_*`, `CT_*`, `CWF_*`, `FUN_*`, `LG_*`, `MA_*`, ...) had empty values in the built-in
   language packs, so the app displayed raw keys (`CWF_AutoFind`, `CWF_AddManully`, ...).
   The provider injects the missing translations at runtime into `LanguageParserTool.languageMap`.

Only two things change in the APK: `AndroidManifest.xml` (adds the provider) and a new
`classes6.dex`. Assets, resources and all original dex files stay byte-identical — important,
because the iJiami packer kills the app if assets are modified.

## Tested original

| | |
|---|---|
| Package | `com.sencor.senc` |
| Version | 5.0.7 (1781494036) |
| Original SHA256 | `D4B325BEAE61B487BE24F138FEBAA24A13DF05FD55A09F7598F3FE0CFB392598` |
| Tested devices | POCO `munch_eea` / Android 14 (MIUI), AVD Android 15 |

## Quick start

```powershell
# 1. Create your own signing key (first time only)
keytool -genkeypair -keystore my.keystore -storepass CHANGE_ME -keypass CHANGE_ME `
  -alias fix -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=My Sencor Fix"

# 2. Build (pin tools for byte-identical output - see BUILD.md)
python scripts/build_fixed_apk.py --apk "C:\path\SENCOR+Robotics_5.0.7_APKPure.apk" `
  --keystore my.keystore --storepass CHANGE_ME --keyalias fix --outdir out `
  --sdk "$env:LOCALAPPDATA\Android\Sdk" `
  --android-jar "$env:LOCALAPPDATA\Android\Sdk\platforms\android-35\android.jar" `
  --d8 "$env:LOCALAPPDATA\Android\Sdk\build-tools\36.0.0\d8.bat" `
  --zipalign "$env:LOCALAPPDATA\Android\Sdk\build-tools\36.0.0\zipalign.exe" `
  --apksigner "$env:LOCALAPPDATA\Android\Sdk\build-tools\36.0.0\apksigner.bat"

# 3. Install (different signature => uninstall original first, data will be lost)
adb uninstall com.sencor.senc
adb install -g -r out\SENCOR-Robotics-5.0.7-fixed.apk
```

Full details: [BUILD.md](BUILD.md).

## Known limitations

- The app is signed with **your** key, not the vendor's: Google Play/FCM push may not work,
  Play Protect may warn, and you must uninstall the original before installing.
- The patch targets **version 5.0.7 only**; other versions have different bytecode/manifest.
- Tested with a newly created account. Some old accounts failed to log in regardless of this
  patch (server-side/account issue).
- No robot hardware test was performed here.

## Reproducibility

With the pinned tool versions above, a rebuild produced **byte-identical ZIP entries** to the
tested APK; only the signing-block timestamp differs. `apksigner verify` passes (v1/v2/v3).

## Legal

This project is **not affiliated with SENCOR, Baole/YouRen or hctrobot**. It contains no APK and
no decompiled vendor code. Only the patch code in this repo is licensed under [MIT](LICENSE).
You are responsible for owning the original app and for complying with local law and the
vendor's terms. See [DISCLAIMER.md](DISCLAIMER.md).

---

Slovensky: toto repo obsahuje **len opravu (patch)**, nie APK. Stiahni si legálne originálnu APK
verzie 5.0.7, spusti build script podľa `BUILD.md` a nainštaluj výsledok. Podpis sa líši od
výrobcu, preto treba pôvodnú appu najprv odinštalovať.
