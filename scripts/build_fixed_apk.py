#!/usr/bin/env python3
"""Build a fixed APK from a legally obtained SENCOR Robotics 5.0.7 APK.

The script only changes two things in a byte-preserving ZIP rewrite:
  1. AndroidManifest.xml  - declares com.sencor.fix.EarlyDecorProvider
  2. adds classes6.dex     - the compiled fix provider

No assets, resources, or original dex files are modified (important: the
iJiami packer detects such changes and kills the app).

Usage:
  python scripts/build_fixed_apk.py \
      --apk "C:\\path\\SENCOR+Robotics_5.0.7_APKPure.apk" \
      --keystore "C:\\path\\my.keystore" \
      --storepass "secret" --keyalias "fix" \
      --outdir out
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

PROVIDER_LINE = (
    '        <provider android:authorities="com.sencor.senc.earlydecor" '
    'android:exported="false" android:initOrder="9999" '
    'android:name="com.sencor.fix.EarlyDecorProvider"/>\n'
)
ANCHOR = '        <provider android:authorities="com.sencor.senc.FileProvider"'
SIG_SUFFIX = ('.RSA', '.SF', '.MF')


def run(cmd, **kwargs):
    print('+ ' + ' '.join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True, **kwargs)


def find_tool(name, override, sdk):
    if override:
        return override
    found = shutil.which(name)
    if found:
        return found
    if sdk and name in ('d8', 'zipalign', 'apksigner'):
        tools = os.path.join(sdk, 'build-tools')
        if os.path.isdir(tools):
            versions = sorted(os.listdir(tools), reverse=True)
            for v in versions:
                for suffix in ('.exe', '.bat', ''):
                    candidate = os.path.join(tools, v, name + suffix)
                    if os.path.isfile(candidate):
                        return candidate
    raise SystemExit(f'Tool not found: {name}. Pass --{name.replace("-", "_")} explicitly.')


def find_android_jar(sdk, override):
    if override:
        return override
    platforms = os.path.join(sdk, 'platforms')
    if os.path.isdir(platforms):
        import re
        def plat_num(s):
            m = re.search(r'(\d+(?:\.\d+)?)', s.split('-', 1)[-1])
            return float(m.group(1)) if m else 0.0
        versions = sorted((p for p in os.listdir(platforms) if p.startswith('android-')),
                          key=plat_num, reverse=True)
        for v in versions:
            jar = os.path.join(platforms, v, 'android.jar')
            if os.path.isfile(jar):
                return jar
    raise SystemExit('android.jar not found. Pass --android-jar.')


def patch_manifest_text(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    if 'com.sencor.fix.EarlyDecorProvider' in text:
        print('manifest already patched')
        return
    if ANCHOR not in text:
        raise SystemExit('Manifest anchor not found - unexpected APK version.')
    text = text.replace(ANCHOR, PROVIDER_LINE + ANCHOR, 1)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    print('manifest patched')


def build_res_only(decoded, tmp, apktool):
    """Compile the edited text manifest back to binary form (no dex touched)."""
    res_only = os.path.join(tmp, 'res-only')
    if os.path.exists(res_only):
        shutil.rmtree(res_only)
    shutil.copytree(decoded, res_only)
    for root, _, files in os.walk(res_only):
        for f in files:
            if f.startswith('classes') and f.endswith('.dex'):
                os.remove(os.path.join(root, f))
    out = os.path.join(tmp, 'res-only.apk')
    run([apktool, 'b', '-f', res_only, '-o', out])
    with zipfile.ZipFile(out) as z:
        return z.read('AndroidManifest.xml')


def compile_provider(fix_src, tmp, javac, d8, android_jar):
    classes = os.path.join(tmp, 'classes')
    dexdir = os.path.join(tmp, 'dex')
    os.makedirs(dexdir, exist_ok=True)
    javafile = os.path.join(fix_src, 'com', 'sencor', 'fix', 'EarlyDecorProvider.java')
    run([javac, '-source', '8', '-target', '8', '-bootclasspath', android_jar,
         '-d', classes, javafile])
    inputs = [
        os.path.join(classes, 'com', 'sencor', 'fix', 'EarlyDecorProvider.class'),
        os.path.join(classes, 'com', 'sencor', 'fix', 'EarlyDecorProvider$1.class'),
    ]
    run([d8, '--lib', android_jar, '--output', dexdir] + inputs)
    return open(os.path.join(dexdir, 'classes.dex'), 'rb').read()


def assemble(original, manifest_bin, provider_dex, out):
    with zipfile.ZipFile(original) as zin, zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for i in zin.infolist():
            name = i.filename
            if name.startswith('META-INF/') and name.endswith(SIG_SUFFIX):
                continue
            data = manifest_bin if name == 'AndroidManifest.xml' else zin.read(name)
            zi = zipfile.ZipInfo(name, date_time=i.date_time)
            zi.compress_type = zipfile.ZIP_STORED if name == 'resources.arsc' else zipfile.ZIP_DEFLATED
            zi.external_attr = i.external_attr
            zout.writestr(zi, data)
        zout.writestr('classes6.dex', provider_dex)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apk', required=True)
    ap.add_argument('--keystore', required=True)
    ap.add_argument('--storepass', required=True)
    ap.add_argument('--keypass', default=None)
    ap.add_argument('--keyalias', required=True)
    ap.add_argument('--outdir', default='out')
    ap.add_argument('--sdk', default=os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT'))
    ap.add_argument('--android-jar')
    for t in ('apktool', 'javac', 'd8', 'zipalign', 'apksigner'):
        ap.add_argument('--' + t, default=None)
    args = ap.parse_args()

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sdk = args.sdk
    apktool = find_tool('apktool', args.apktool, sdk)
    javac = find_tool('javac', args.javac, sdk)
    d8 = find_tool('d8', args.d8, sdk)
    zipalign = find_tool('zipalign', args.zipalign, sdk)
    apksigner = find_tool('apksigner', args.apksigner, sdk)
    android_jar = find_android_jar(sdk, args.android_jar)

    tmp = tempfile.mkdtemp(prefix='sencor-fix-')
    try:
        decoded = os.path.join(tmp, 'decoded')
        run([apktool, 'd', '-s', '-f', '-o', decoded, args.apk])
        patch_manifest_text(os.path.join(decoded, 'AndroidManifest.xml'))
        manifest_bin = build_res_only(decoded, tmp, apktool)
        provider_dex = compile_provider(os.path.join(repo, 'fix_src'), tmp, javac, d8, android_jar)

        unsigned = os.path.join(tmp, 'unsigned.apk')
        aligned = os.path.join(tmp, 'aligned.apk')
        assemble(args.apk, manifest_bin, provider_dex, unsigned)
        run([zipalign, '-f', '-p', '4', unsigned, aligned])

        final = os.path.join(os.path.abspath(args.outdir), 'SENCOR-Robotics-5.0.7-fixed.apk')
        os.makedirs(os.path.dirname(final), exist_ok=True)
        run([apksigner, 'sign', '--ks', args.keystore,
             '--ks-pass', 'pass:' + args.storepass,
             '--key-pass', 'pass:' + (args.keypass or args.storepass),
             '--v1-signing-enabled', 'true', '--v2-signing-enabled', 'true',
             '--out', final, aligned])
        run([apksigner, 'verify', final])
        print('\nBuilt: ' + final)
        print('SHA256: ' + sha256(final))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
