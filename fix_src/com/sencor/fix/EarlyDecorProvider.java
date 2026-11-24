package com.sencor.fix;

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

public final class EarlyDecorProvider extends ContentProvider {

    private static final String[] KEYS = {
        "CWF_APPLocationNotOpen",
        "CWF_AddDeviceFailt",
        "CWF_AddDeviceSuccessFul",
        "CWF_AddManully",
        "CWF_AnotherWayDistributeNetwork",
        "CWF_AutoFind",
        "CWF_BluetoothConnectingPleaseDoNotLeave",
        "CWF_BluetoothTurnedOnCanBeSearchedDevice",
        "CWF_ConfirmLeave",
        "CWF_ContactUs",
        "CWF_ContinueSearch",
        "CWF_CurrentConnectionWiFiStrength",
        "CWF_DeviceAdding",
        "CWF_DeviceConnectingPleaseDoNotLeave",
        "CWF_DeviceConnectingWiFi",
        "CWF_DeviceaNme",
        "CWF_ErrorCode",
        "CWF_ErrorNotice101600And101602And101603",
        "CWF_ErrorNotice101601And60101",
        "CWF_ErrorNotice101601And60102",
        "CWF_ErrorNotice101601And61605",
        "CWF_ErrorNotice101602And61609And101617And61709And999103",
        "CWF_ErrorNotice101617And61701And61706",
        "CWF_ErrorNotice101617And61702",
        "CWF_ErrorNotice101617And61703",
        "CWF_ErrorNotice61701",
        "CWF_ErrorNotice61702",
        "CWF_ErrorNotice61703",
        "CWF_ErrorNotice61704",
        "CWF_ErrorNotice6221",
        "CWF_FailedConnectDevicePleaseFollowInstructionsBelow",
        "CWF_FindNotDeviceNoticeMsg",
        "CWF_GPSNotOpen",
        "CWF_GPSOrAPPLocationNotOpen",
        "CWF_GoToAdd",
        "CWF_MacAddress",
        "CWF_NeedLacationPermissionsUseSearchWiFiList",
        "CWF_NewDevice",
        "CWF_NoWiFiXXXIsFound",
        "CWF_PleaseConfirmWhetherWifiIsNoPassword",
        "CWF_PleaseConnectFamilyWiFiFirst",
        "CWF_PleaseConnectHomeWIFI",
        "CWF_PleaseOpenBluetoothPermissions",
        "CWF_PleaseOpenLocationPermissions",
        "CWF_PleaseOpenWifiPermissions",
        "CWF_PleaseUseManualSelectionToBind",
        "CWF_Strong",
        "CWF_Strongest",
        "CWF_SubmitFeedback",
        "CWF_ThePhoneCannotAccessInternetPleaseConnectHomeWIFI",
        "CWF_TimeOutNoFindDevice",
        "CWF_ViewSolution",
        "CWF_WIN_DeviceConnectAPP",
        "CWF_WIN_DeviceConnectWiFi",
        "CWF_Weak",
        "CWF_WiFiPasswordCannotExceed64Digits",
        "CWF_WiFiPasswordIsSpaced",
        "CWF_WindowCleanMachine"
    };
    private static final String[] SK = {
        "Povolenie pr\u00edstupu k polohe pre aplik\u00e1ciu nie je zapnut\u00e9",
        "Zariadenie sa nepodarilo prida\u0165",
        "Zariadenie bolo \u00faspe\u0161ne pridan\u00e9",
        "Prida\u0165 ru\u010dne",
        "Sk\u00fa\u0161am in\u00fd sp\u00f4sob pripojenia zariadenia k aplik\u00e1cii",
        "Automatick\u00e9 vyh\u013eadanie",
        "Prip\u00e1ja sa cez Bluetooth, neop\u00fa\u0161\u0165ajte pros\u00edm t\u00fato obrazovku",
        "Zariadenie mo\u017eno n\u00e1js\u0165 cez Bluetooth. Povo\u013ete Wi-Fi a pr\u00edstup k polohe v nastaveniach.",
        "Potvr\u010fte odchod",
        "Kontaktujte n\u00e1s",
        "Pokra\u010dova\u0165 v h\u013eadan\u00ed",
        "Aktu\u00e1lna sila sign\u00e1lu Wi-Fi:",
        "Prid\u00e1vam zariadenie...",
        "Zariadenie sa prip\u00e1ja. Aby sa \u00faspe\u0161ne pripojilo k aplik\u00e1cii, zosta\u0148te na tejto obrazovke.",
        "Zariadenie sa prip\u00e1ja k Wi-Fi...",
        "N\u00e1zov zariadenia",
        "K\u00f3d chyby",
        "Zariadenie sa nepodarilo pripoji\u0165. Skontrolujte jeho nap\u00e1janie a re\u0161tartujte ho.",
        "Pripojenie zlyhalo. Re\u0161tartujte zariadenie a sk\u00faste znova.",
        "Pripojenie zlyhalo. Skontrolujte pripojenie k Wi-Fi a sk\u00faste znova.",
        "Pripojenie zlyhalo. Zariadenie je mo\u017eno pripojen\u00e9 k in\u00e9mu telef\u00f3nu.",
        "Chyba pripojenia k zariadeniu. Sk\u00faste znova alebo kontaktujte podporu.",
        "Chyba pripojenia. Skontrolujte sie\u0165 a sk\u00faste znova.",
        "Chyba pripojenia zariadenia. Sk\u00faste znova.",
        "Chyba pripojenia zariadenia. Re\u0161tartujte ho a sk\u00faste znova.",
        "Zariadenie sa nepodarilo pripoji\u0165. Sk\u00faste znova.",
        "Zariadenie je pripojen\u00e9 k in\u00e9mu telef\u00f3nu. Ukon\u010dte toto pripojenie.",
        "Chyba pripojenia k zariadeniu. Skontrolujte Wi-Fi.",
        "Chyba komunik\u00e1cie so zariaden\u00edm. Sk\u00faste znova.",
        "Chyba siete. Sk\u00faste znova.",
        "Zariadenie sa nepodarilo pripoji\u0165. Postupujte pod\u013ea pokynov ni\u017e\u0161ie.",
        "Zariadenie sa nena\u0161lo: 1. Ak nie je pripojen\u00e9 k in\u00e9mu telef\u00f3nu, re\u0161tartujte ho a sk\u00faste znova. 2. Ak je pripojen\u00e9 k in\u00e9mu telef\u00f3nu, ukon\u010dte tam pripojenie a sk\u00faste znova.",
        "GPS nie je zapnut\u00e9",
        "GPS alebo pr\u00edstup aplik\u00e1cie k polohe nie je zapnut\u00fd",
        "Prejs\u0165 na pridanie",
        "MAC adresa:",
        "Aplik\u00e1cia zhroma\u017e\u010fuje \u00fadaje o polohe na zobrazenie zoznamu Wi-Fi, aj ke\u010f je zatvoren\u00e1 alebo sa nepou\u017e\u00edva.",
        "Nov\u00e9 zariadenie",
        "Nena\u0161la sa sie\u0165 Wi-Fi XXX?",
        "Heslo Wi-Fi je pr\u00e1zdne. Overte, \u010di va\u0161a dom\u00e1ca sie\u0165 Wi-Fi nem\u00e1 heslo.",
        "Najprv sa pripojte k dom\u00e1cej sieti Wi-Fi.",
        "Pripojte sa k dom\u00e1cej sieti Wi-Fi",
        "Zapnite Bluetooth",
        "Povo\u013ete pr\u00edstup k polohe",
        "Povo\u013ete pr\u00edstup k Wi-Fi",
        "Pre zariadenia bez podpory Bluetooth pou\u017eite polo\u017eku Prida\u0165 ru\u010dne.",
        "Siln\u00e9",
        "Norm\u00e1lne",
        "Odosla\u0165 sp\u00e4tn\u00fa v\u00e4zbu",
        "Telef\u00f3n nem\u00e1 pr\u00edstup na internet. Pripojte sa k dom\u00e1cej sieti Wi-Fi s internetom.",
        "\u010cas h\u013eadania vypr\u0161al, zariadenie sa nena\u0161lo",
        "Zobrazi\u0165 rie\u0161enie",
        "Robot sa prip\u00e1ja k aplik\u00e1cii",
        "Robot sa prip\u00e1ja k Wi-Fi",
        "Slab\u00e9",
        "Heslo Wi-Fi nem\u00f4\u017ee presiahnu\u0165 32 znakov",
        "Heslo Wi-Fi obsahuje medzeru. Skontrolujte heslo.",
        "\u010cisti\u010d okien"
    };
    private static final String[] CS = {
        "Povolen\u00ed p\u0159\u00edstupu k poloze pro aplikaci nen\u00ed zapnut\u00e9",
        "Za\u0159\u00edzen\u00ed se nepoda\u0159ilo p\u0159idat",
        "Za\u0159\u00edzen\u00ed bylo \u00fasp\u011b\u0161n\u011b p\u0159id\u00e1no",
        "P\u0159idat ru\u010dn\u011b",
        "Zkou\u0161\u00edm jin\u00fd zp\u016fsob p\u0159ipojen\u00ed za\u0159\u00edzen\u00ed k aplikaci",
        "Automatick\u00e9 vyhled\u00e1v\u00e1n\u00ed",
        "P\u0159ipojuje se p\u0159es Bluetooth, neopou\u0161t\u011bjte pros\u00edm tuto obrazovku",
        "Za\u0159\u00edzen\u00ed lze naj\u00edt p\u0159es Bluetooth. Povolte Wi-Fi a p\u0159\u00edstup k poloze v nastaven\u00ed.",
        "Potvr\u010fte odchod",
        "Kontaktujte n\u00e1s",
        "Pokra\u010dovat v hled\u00e1n\u00ed",
        "Aktu\u00e1ln\u00ed s\u00edla sign\u00e1lu Wi-Fi:",
        "P\u0159id\u00e1v\u00e1m za\u0159\u00edzen\u00ed...",
        "Za\u0159\u00edzen\u00ed se p\u0159ipojuje. Aby se \u00fasp\u011b\u0161n\u011b p\u0159ipojilo k aplikaci, z\u016fsta\u0148te na t\u00e9to obrazovce.",
        "Za\u0159\u00edzen\u00ed se p\u0159ipojuje k Wi-Fi...",
        "N\u00e1zev za\u0159\u00edzen\u00ed",
        "K\u00f3d chyby",
        "Za\u0159\u00edzen\u00ed se nepoda\u0159ilo p\u0159ipojit. Zkontrolujte jeho nap\u00e1jen\u00ed a restartujte jej.",
        "P\u0159ipojen\u00ed selhalo. Restartujte za\u0159\u00edzen\u00ed a zkuste to znovu.",
        "P\u0159ipojen\u00ed selhalo. Zkontrolujte p\u0159ipojen\u00ed k Wi-Fi a zkuste to znovu.",
        "P\u0159ipojen\u00ed selhalo. Za\u0159\u00edzen\u00ed m\u016f\u017ee b\u00fdt p\u0159ipojeno k jin\u00e9mu telefonu.",
        "Chyba p\u0159ipojen\u00ed k za\u0159\u00edzen\u00ed. Zkuste to znovu nebo kontaktujte podporu.",
        "Chyba p\u0159ipojen\u00ed. Zkontrolujte s\u00ed\u0165 a zkuste to znovu.",
        "Chyba p\u0159ipojen\u00ed za\u0159\u00edzen\u00ed. Zkuste to znovu.",
        "Chyba p\u0159ipojen\u00ed za\u0159\u00edzen\u00ed. Restartujte jej a zkuste to znovu.",
        "Za\u0159\u00edzen\u00ed se nepoda\u0159ilo p\u0159ipojit. Zkuste to znovu.",
        "Za\u0159\u00edzen\u00ed je p\u0159ipojeno k jin\u00e9mu telefonu. Ukon\u010dete toto p\u0159ipojen\u00ed.",
        "Chyba p\u0159ipojen\u00ed k za\u0159\u00edzen\u00ed. Zkontrolujte Wi-Fi.",
        "Chyba komunikace se za\u0159\u00edzen\u00edm. Zkuste to znovu.",
        "Chyba s\u00edt\u011b. Zkuste to znovu.",
        "Za\u0159\u00edzen\u00ed se nepoda\u0159ilo p\u0159ipojit. Postupujte podle pokyn\u016f n\u00ed\u017ee.",
        "Za\u0159\u00edzen\u00ed se nena\u0161lo: 1. Pokud nen\u00ed p\u0159ipojeno k jin\u00e9mu telefonu, restartujte jej a zkuste to znovu. 2. Pokud je p\u0159ipojeno k jin\u00e9mu telefonu, ukon\u010dete tam p\u0159ipojen\u00ed a zkuste to znovu.",
        "GPS nen\u00ed zapnut\u00e9",
        "GPS ani p\u0159\u00edstup aplikace k poloze nen\u00ed zapnut\u00fd",
        "P\u0159ej\u00edt na p\u0159id\u00e1n\u00ed",
        "MAC adresa:",
        "Aplikace shroma\u017e\u010fuje \u00fadaje o poloze pro zobrazen\u00ed seznamu Wi-Fi, i kdy\u017e je zav\u0159en\u00e1 nebo se nepou\u017e\u00edv\u00e1.",
        "Nov\u00e9 za\u0159\u00edzen\u00ed",
        "Nena\u0161la se s\u00ed\u0165 Wi-Fi XXX?",
        "Heslo Wi-Fi je pr\u00e1zdn\u00e9. Ov\u011b\u0159te, zda va\u0161e dom\u00e1c\u00ed s\u00ed\u0165 Wi-Fi nem\u00e1 heslo.",
        "Nejd\u0159\u00edve se p\u0159ipojte k dom\u00e1c\u00ed s\u00edti Wi-Fi.",
        "P\u0159ipojte se k dom\u00e1c\u00ed s\u00edti Wi-Fi",
        "Zapn\u011bte Bluetooth",
        "Povolte p\u0159\u00edstup k poloze",
        "Povolte p\u0159\u00edstup k Wi-Fi",
        "Pro za\u0159\u00edzen\u00ed bez podpory Bluetooth pou\u017eijte polo\u017eku P\u0159idat ru\u010dn\u011b.",
        "Siln\u00e9",
        "Norm\u00e1ln\u00ed",
        "Odeslat zp\u011btnou vazbu",
        "Telefon nem\u00e1 p\u0159\u00edstup k internetu. P\u0159ipojte se k dom\u00e1c\u00ed s\u00edti Wi-Fi s internetem.",
        "\u010cas hled\u00e1n\u00ed vypr\u0161el, za\u0159\u00edzen\u00ed se nena\u0161lo",
        "Zobrazit \u0159e\u0161en\u00ed",
        "Robot se p\u0159ipojuje k aplikaci",
        "Robot se p\u0159ipojuje k Wi-Fi",
        "Slab\u00e9",
        "Heslo Wi-Fi nem\u016f\u017ee p\u0159es\u00e1hnout 32 znak\u016f",
        "Heslo Wi-Fi obsahuje mezeru. Zkontrolujte heslo.",
        "\u010cisti\u010d oken"
    };

    private static void injectLanguage(Context ctx) {
        try {
            String lang = ctx.getResources().getConfiguration().locale.getLanguage().toLowerCase();
            String[] vals = lang.equals("cs") ? CS : SK;
            Class<?> cls = Class.forName("com.baole.blap.tool.LanguageParserTool");
            Field f = cls.getField("languageMap");
            Map map = (Map) f.get(null);
            int added = 0;
            for (int i = 0; i < KEYS.length; i++) {
                Object cur = map.get(KEYS[i]);
                if (cur == null || cur.toString().length() == 0) {
                    map.put(KEYS[i], vals[i]);
                    added++;
                }
            }
            if (added > 0) Log.i("DecorFix", "localization injected " + added + " for " + lang);
        } catch (Throwable t) {
            Log.w("DecorFix", "localization inject failed", t);
        }
    }

    @Override
    public boolean onCreate() {
        Context ctx = getContext();
        try {
            Application app = (Application) ctx.getApplicationContext();
            app.registerActivityLifecycleCallbacks(new Application.ActivityLifecycleCallbacks() {
                @Override
                public void onActivityPreCreated(Activity activity, Bundle savedInstanceState) {
                    try { activity.getWindow().getDecorView(); } catch (Throwable t) { }
                    injectLanguage(activity);
                }

                @Override public void onActivityCreated(Activity a, Bundle b) { }
                @Override public void onActivityStarted(Activity a) { injectLanguage(a); }
                @Override public void onActivityResumed(Activity a) { injectLanguage(a); }
                @Override public void onActivityPaused(Activity a) { }
                @Override public void onActivityStopped(Activity a) { }
                @Override public void onActivitySaveInstanceState(Activity a, Bundle b) { }
                @Override public void onActivityDestroyed(Activity a) { }
            });
            Log.i("DecorFix", "installed");
        } catch (Throwable t) {
            Log.w("DecorFix", "hook failed", t);
        }
        return true;
    }

    @Override public Cursor query(Uri uri, String[] p, String s, String[] a, String sort) { return null; }
    @Override public Cursor query(Uri uri, String[] p, Bundle a, CancellationSignal c) { return null; }
    @Override public String getType(Uri uri) { return null; }
    @Override public Uri insert(Uri uri, ContentValues v) { return null; }
    @Override public int delete(Uri uri, String s, String[] a) { return 0; }
    @Override public int update(Uri uri, ContentValues v, String s, String[] a) { return 0; }
    @Override public AssetFileDescriptor openAssetFile(Uri uri, String mode) throws FileNotFoundException { throw new FileNotFoundException(); }
}
