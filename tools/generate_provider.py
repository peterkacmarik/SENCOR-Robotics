import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from translations_all import T

keys = sorted(T)
sk = [T[k][0] for k in keys]
cs = [T[k][1] for k in keys]

def jarr(items):
    return "{\n" + ",\n".join("        " + json.dumps(s, ensure_ascii=True) for s in items) + "\n    }"

java = f'''package com.sencor.fix;

import android.app.Activity;
import android.app.Application;
import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.CancellationSignal;
import android.util.Log;

import java.io.FileNotFoundException;
import java.lang.reflect.Field;
import java.util.Map;

public final class EarlyDecorProvider extends ContentProvider {{

    private static final String[] KEYS = {jarr(keys)};
    private static final String[] SK = {jarr(sk)};
    private static final String[] CS = {jarr(cs)};

    private static void injectLanguage(Context ctx) {{
        try {{
            String lang = ctx.getResources().getConfiguration().locale.getLanguage().toLowerCase();
            String[] vals = lang.equals("cs") ? CS : SK;
            Class<?> cls = Class.forName("com.baole.blap.tool.LanguageParserTool");
            Field f = cls.getField("languageMap");
            Map map = (Map) f.get(null);
            int added = 0;
            for (int i = 0; i < KEYS.length; i++) {{
                Object cur = map.get(KEYS[i]);
                if (cur == null || cur.toString().length() == 0) {{
                    map.put(KEYS[i], vals[i]);
                    added++;
                }}
            }}
            if (added > 0) Log.i("DecorFix", "localization injected " + added + " for " + lang);
        }} catch (Throwable t) {{
            Log.w("DecorFix", "localization inject failed", t);
        }}
    }}

    @Override
    public boolean onCreate() {{
        Context ctx = getContext();
        try {{
            Application app = (Application) ctx.getApplicationContext();
            app.registerActivityLifecycleCallbacks(new Application.ActivityLifecycleCallbacks() {{
                @Override
                public void onActivityPreCreated(Activity activity, Bundle savedInstanceState) {{
                    try {{ activity.getWindow().getDecorView(); }} catch (Throwable t) {{ }}
                    injectLanguage(activity);
                }}

                @Override public void onActivityCreated(Activity a, Bundle b) {{ }}
                @Override public void onActivityStarted(Activity a) {{ injectLanguage(a); }}
                @Override public void onActivityResumed(Activity a) {{ injectLanguage(a); }}
                @Override public void onActivityPaused(Activity a) {{ }}
                @Override public void onActivityStopped(Activity a) {{ }}
                @Override public void onActivitySaveInstanceState(Activity a, Bundle b) {{ }}
                @Override public void onActivityDestroyed(Activity a) {{ }}
            }});
            Log.i("DecorFix", "installed");
        }} catch (Throwable t) {{
            Log.w("DecorFix", "hook failed", t);
        }}
        return true;
    }}

    @Override public Cursor query(Uri uri, String[] p, String s, String[] a, String sort) {{ return null; }}
    @Override public Cursor query(Uri uri, String[] p, Bundle a, CancellationSignal c) {{ return null; }}
    @Override public String getType(Uri uri) {{ return null; }}
    @Override public Uri insert(Uri uri, ContentValues v) {{ return null; }}
    @Override public int delete(Uri uri, String s, String[] a) {{ return 0; }}
    @Override public int update(Uri uri, ContentValues v, String s, String[] a) {{ return 0; }}
    @Override public AssetFileDescriptor openAssetFile(Uri uri, String mode) throws FileNotFoundException {{ throw new FileNotFoundException(); }}
}}
'''

os.makedirs("fix_src/com/sencor/fix", exist_ok=True)
open("fix_src/com/sencor/fix/EarlyDecorProvider.java", "w", encoding="utf-8").write(java)
print("generated", len(keys), "keys")
