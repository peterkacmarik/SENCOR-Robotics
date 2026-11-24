<div align="center">

# SENCOR Robotics 5.0.7 — Fix Patch

*Reproducible startup and Slovak/Czech localization fix. Source patch only — no APK is distributed here.*

![Android](https://img.shields.io/badge/Android-5.0.7-3DDC84?style=flat-square&logo=android&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![JDK](https://img.shields.io/badge/JDK-17-orange?style=flat-square)
![APK](https://img.shields.io/badge/APK-not_included-red?style=flat-square)

[Overview](#overview) • [Why](#why) • [Prerequisites](#prerequisites) • [Build](#build) • [Install](#install) • [Supported models](#supported-robot-models) • [Limitations](#limitations)

</div>

> [!IMPORTANT]
> This repo contains **only the patch source and build scripts**. You must provide your own,
> legally obtained copy of `SENCOR+Robotics_5.0.7_APKPure.apk`. No APK, signing key, or decompiled
> vendor code is included.

## Overview

A minimal, reproducible patch for **SENCOR Robotics 5.0.7** (`com.sencor.senc`) that fixes two
problems in the original app:

- **Startup crash on MIUI / HyperOS** (POCO `munch_eea`, Android 14): `LogoActivity` called
  `Window.getInsetsController()` before the `DecorView` existed, causing an immediate
  `NullPointerException` and force-stop.
- **Missing SK/CS translations**: 319 keys (`CL_*`, `CT_*`, `CWF_*`, `FUN_*`, `LG_*`, `MA_*`, ...)
  had empty values in the built-in language packs, so the UI showed raw keys such as
  `CWF_AutoFind` or `CL_MAP_CleanMode`.

The patch adds a small `ContentProvider` that pre-creates the decor view before any activity's
`onCreate()` and injects the missing translations at runtime.

## Why

| Problem | Root cause | Fix |
| --- | --- | --- |
| App force-stops on launch | `DecorView` is not created yet when system-bar colors are applied | `getWindow().getDecorView()` in `onActivityPreCreated` |
| Raw translation keys in UI | Empty values in `sk` / `cs-cz` language packs | Runtime injection into `LanguageParserTool.languageMap` |
| Rebuilding normally breaks the app | The iJiami packer detects modified assets/dex and kills the process | ZIP-level rewrite: manifest + one new dex only |

> [!NOTE]
> Only `AndroidManifest.xml` and a new `classes6.dex` change. Assets, resources, and all original
> dex files stay byte-identical — this is what keeps the packer from rejecting the build.

## Prerequisites

| Tool | Tested version |
| --- | --- |
| Python | 3.10+ |
| JDK | 17 (`javac` on PATH) |
| Android SDK platform | `android-35` (`android.jar`) |
| Android build-tools | `36.0.0` (`d8`, `zipalign`, `apksigner`) |
| apktool | 3.0.2 |
| Original APK | 5.0.7, SHA256 `D4B325BEAE61B487BE24F138FEBAA24A13DF05FD55A09F7598F3FE0CFB392598` |

## Build

<details open>
<summary><b>Windows (PowerShell)</b></summary>

```powershell
# 1. Create your own signing key (first time only)
keytool -genkeypair -keystore my.keystore -storepass CHANGE_ME -keypass CHANGE_ME `
  -alias fix -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=My Sencor Fix"

# 2. Build from your own original APK
$SDK = "$env:LOCALAPPDATA\Android\Sdk"
python scripts/build_fixed_apk.py `
  --apk "C:\path\SENCOR+Robotics_5.0.7_APKPure.apk" `
  --keystore my.keystore --storepass CHANGE_ME --keyalias fix --outdir out `
  --sdk $SDK `
  --android-jar "$SDK\platforms\android-35\android.jar" `
  --d8 "$SDK\build-tools\36.0.0\d8.bat" `
  --zipalign "$SDK\build-tools\36.0.0\zipalign.exe" `
  --apksigner "$SDK\build-tools\36.0.0\apksigner.bat"
```

> [!TIP]
> Pin the tool versions as shown. Newer `d8` versions produce different bytecode and break
> byte-for-byte reproducibility. See [BUILD.md](BUILD.md) for verification commands.

</details>

## Install

> [!WARNING]
> The patched APK is signed with **your** key, not the vendor's. Android requires uninstalling the
> original first, which deletes local app data. You will need to log in again.

```powershell
adb uninstall com.sencor.senc
adb install -g -r out\SENCOR-Robotics-5.0.7-fixed.apk
```

If some labels still appear as raw keys, switch the app language once (EN → SK/CS) to force the
language map to reload.

## Supported robot models

The app supports **manual add** (Add device → *Add manually*, key `CWF_AddManully`) when automatic
discovery or BLE pairing does not find the robot:

| Model | Model | Model |
| --- | --- | --- |
| SRV 8250BK | SRV 4200BK | SRV 9200BK |
| SRV 9250BK | SRV 6250BK | SRV 4250SL |
| SRV 4000GD | | |

## Limitations

- Targets **version 5.0.7 only**; other versions have different bytecode and manifests.
- FCM push notifications may not work with a different signing certificate; Play Protect may warn
  about a sideloaded app.
- Tested with a newly created account. Some older accounts failed to log in regardless of this
  patch (server/account-side issue).
- No robot hardware test was performed as part of this project.

## Legal

This project is **not affiliated with SENCOR, Baole/YouRen, or hctrobot**. It contains no APK and no
decompiled vendor code. Only the patch code here is covered by the repository license. You are
responsible for owning the original app and for complying with local law and the vendor's terms.
See [DISCLAIMER.md](DISCLAIMER.md).

> [!NOTE]
> Slovensky: repo obsahuje **len patch**, nie APK. Získaj legálne originálnu APK verzie 5.0.7,
> zostav podľa [BUILD.md](BUILD.md) a nainštaluj. Podpis sa líši, preto treba pôvodnú appu najprv
> odinštalovať.
