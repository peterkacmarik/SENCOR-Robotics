# Build instructions

## Prerequisites

| Tool | Tested version | Notes |
|---|---|---|
| Python | 3.10+ | orchestration + ZIP rewrite |
| JDK | 17 | `javac` must be on PATH (or pass `--javac`) |
| Android SDK platform | `android-35` | `platforms/android-35/android.jar` |
| Android build-tools | `36.0.0` | `d8`, `zipalign`, `apksigner` |
| apktool | 3.0.2 | `apktool` on PATH (or pass `--apktool`) |
| Original APK | 5.0.7 | SHA256 `D4B325BE...` (see README) |

The script auto-detects tools from `--sdk` / `ANDROID_HOME`, but **pin them explicitly** to get
byte-identical output (newer d8 produces different bytecode for the same Java source).

## Steps

1. Obtain the original APK legally and verify it:

```powershell
Get-FileHash "SENCOR+Robotics_5.0.7_APKPure.apk" -Algorithm SHA256
# D4B325BEAE61B487BE24F138FEBAA24A13DF05FD55A09F7598F3FE0CFB392598
```

2. Create your own keystore:

```powershell
keytool -genkeypair -keystore my.keystore -storepass CHANGE_ME -keypass CHANGE_ME `
  -alias fix -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=My Sencor Fix"
```

3. Build:

```powershell
$SDK = "$env:LOCALAPPDATA\Android\Sdk"
python scripts/build_fixed_apk.py `
  --apk "SENCOR+Robotics_5.0.7_APKPure.apk" `
  --keystore my.keystore --storepass CHANGE_ME --keyalias fix `
  --outdir out --sdk $SDK `
  --android-jar "$SDK\platforms\android-35\android.jar" `
  --d8 "$SDK\build-tools\36.0.0\d8.bat" `
  --zipalign "$SDK\build-tools\36.0.0\zipalign.exe" `
  --apksigner "$SDK\build-tools\36.0.0\apksigner.bat"
```

The script prints `SHA256:` of the result and runs `apksigner verify` at the end.

4. Verify the ZIP contents did not change unexpectedly:

```powershell
python -c "import zipfile,hashlib,sys; a=zipfile.ZipFile('SENCOR+Robotics_5.0.7_APKPure.apk'); b=zipfile.ZipFile('out/SENCOR-Robotics-5.0.7-fixed.apk'); print('new entries:', sorted(set(b.namelist())-set(a.namelist()))); print('changed:', [n for n in a.namelist() if n in b.namelist() and hashlib.md5(a.read(n)).hexdigest()!=hashlib.md5(b.read(n)).hexdigest()])"
# expected: new entries = ['classes6.dex']
#           changed = ['AndroidManifest.xml'] (+ META-INF signature files)
```

5. Install:

```powershell
adb uninstall com.sencor.senc
adb install -g -r out\SENCOR-Robotics-5.0.7-fixed.apk
```

If some `CWF_*` keys still appear as raw text, switch the app language once (EN → SK/CS) to
force the language map to reload.

## What the script does

1. `apktool d -s` – decodes the original manifest/resources (dex files are only copied).
2. Injects `com.sencor.fix.EarlyDecorProvider` into the text manifest.
3. Rebuilds a resource-only APK with apktool just to obtain the compiled binary manifest.
4. Compiles `fix_src/.../EarlyDecorProvider.java` with `javac` + `d8`.
5. ZIP rewrite of the original APK: replaces `AndroidManifest.xml`, appends `classes6.dex`,
   keeps every other entry byte-identical (`resources.arsc` stays STORED).
6. `zipalign` + `apksigner sign` + `apksigner verify`.

## Optional tools

`tools/generate_provider.py` and `tools/patch_localization.py` regenerate the provider source
and the translation tables. They expect an apktool-decoded `decoded/assets/` directory in the
workspace root. You do **not** need them for a normal build — the generated Java source is
already included in `fix_src/`.
