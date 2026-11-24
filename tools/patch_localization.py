import json, os, sys

PREFIX = "e79b44b1cf0f4a0bac8f6596eb98cea2"
ASSETS = os.path.join("decoded", "assets")

T = {
"CWF_APPLocationNotOpen": ("Povolenie prístupu k polohe pre aplikáciu nie je zapnuté", "Povolení přístupu k poloze pro aplikaci není zapnuté"),
"CWF_AddDeviceFailt": ("Zariadenie sa nepodarilo pridať", "Zařízení se nepodařilo přidat"),
"CWF_AddDeviceSuccessFul": ("Zariadenie bolo úspešne pridané", "Zařízení bylo úspěšně přidáno"),
"CWF_AddManully": ("Pridať ručne", "Přidat ručně"),
"CWF_AnotherWayDistributeNetwork": ("Skúšam iný spôsob pripojenia zariadenia k aplikácii", "Zkouším jiný způsob připojení zařízení k aplikaci"),
"CWF_AutoFind": ("Automatické vyhľadanie", "Automatické vyhledávání"),
"CWF_BluetoothConnectingPleaseDoNotLeave": ("Pripája sa cez Bluetooth, neopúšťajte prosím túto obrazovku", "Připojuje se přes Bluetooth, neopouštějte prosím tuto obrazovku"),
"CWF_BluetoothTurnedOnCanBeSearchedDevice": ("Zariadenie možno nájsť cez Bluetooth. Povoľte Wi-Fi a prístup k polohe v nastaveniach.", "Zařízení lze najít přes Bluetooth. Povolte Wi-Fi a přístup k poloze v nastavení."),
"CWF_ConfirmLeave": ("Potvrďte odchod", "Potvrďte odchod"),
"CWF_ContactUs": ("Kontaktujte nás", "Kontaktujte nás"),
"CWF_ContinueSearch": ("Pokračovať v hľadaní", "Pokračovat v hledání"),
"CWF_CurrentConnectionWiFiStrength": ("Aktuálna sila signálu Wi-Fi:", "Aktuální síla signálu Wi-Fi:"),
"CWF_DeviceAdding": ("Pridávam zariadenie...", "Přidávám zařízení..."),
"CWF_DeviceConnectingPleaseDoNotLeave": ("Zariadenie sa pripája. Aby sa úspešne pripojilo k aplikácii, zostaňte na tejto obrazovke.", "Zařízení se připojuje. Aby se úspěšně připojilo k aplikaci, zůstaňte na této obrazovce."),
"CWF_DeviceConnectingWiFi": ("Zariadenie sa pripája k Wi-Fi...", "Zařízení se připojuje k Wi-Fi..."),
"CWF_DeviceaNme": ("Názov zariadenia", "Název zařízení"),
"CWF_ErrorCode": ("Kód chyby", "Kód chyby"),
"CWF_ErrorNotice101600And101602And101603": ("Zariadenie sa nepodarilo pripojiť. Skontrolujte jeho napájanie a reštartujte ho.", "Zařízení se nepodařilo připojit. Zkontrolujte jeho napájení a restartujte jej."),
"CWF_ErrorNotice101601And60101": ("Pripojenie zlyhalo. Reštartujte zariadenie a skúste znova.", "Připojení selhalo. Restartujte zařízení a zkuste to znovu."),
"CWF_ErrorNotice101601And60102": ("Pripojenie zlyhalo. Skontrolujte pripojenie k Wi-Fi a skúste znova.", "Připojení selhalo. Zkontrolujte připojení k Wi-Fi a zkuste to znovu."),
"CWF_ErrorNotice101601And61605": ("Pripojenie zlyhalo. Zariadenie je možno pripojené k inému telefónu.", "Připojení selhalo. Zařízení může být připojeno k jinému telefonu."),
"CWF_ErrorNotice101602And61609And101617And61709And999103": ("Chyba pripojenia k zariadeniu. Skúste znova alebo kontaktujte podporu.", "Chyba připojení k zařízení. Zkuste to znovu nebo kontaktujte podporu."),
"CWF_ErrorNotice101617And61701And61706": ("Chyba pripojenia. Skontrolujte sieť a skúste znova.", "Chyba připojení. Zkontrolujte síť a zkuste to znovu."),
"CWF_ErrorNotice101617And61702": ("Chyba pripojenia zariadenia. Skúste znova.", "Chyba připojení zařízení. Zkuste to znovu."),
"CWF_ErrorNotice101617And61703": ("Chyba pripojenia zariadenia. Reštartujte ho a skúste znova.", "Chyba připojení zařízení. Restartujte jej a zkuste to znovu."),
"CWF_ErrorNotice61701": ("Zariadenie sa nepodarilo pripojiť. Skúste znova.", "Zařízení se nepodařilo připojit. Zkuste to znovu."),
"CWF_ErrorNotice61702": ("Zariadenie je pripojené k inému telefónu. Ukončte toto pripojenie.", "Zařízení je připojeno k jinému telefonu. Ukončete toto připojení."),
"CWF_ErrorNotice61703": ("Chyba pripojenia k zariadeniu. Skontrolujte Wi-Fi.", "Chyba připojení k zařízení. Zkontrolujte Wi-Fi."),
"CWF_ErrorNotice61704": ("Chyba komunikácie so zariadením. Skúste znova.", "Chyba komunikace se zařízením. Zkuste to znovu."),
"CWF_ErrorNotice6221": ("Chyba siete. Skúste znova.", "Chyba sítě. Zkuste to znovu."),
"CWF_FailedConnectDevicePleaseFollowInstructionsBelow": ("Zariadenie sa nepodarilo pripojiť. Postupujte podľa pokynov nižšie.", "Zařízení se nepodařilo připojit. Postupujte podle pokynů níže."),
"CWF_FindNotDeviceNoticeMsg": ("Zariadenie sa nenašlo: 1. Ak nie je pripojené k inému telefónu, reštartujte ho a skúste znova. 2. Ak je pripojené k inému telefónu, ukončte tam pripojenie a skúste znova.", "Zařízení se nenašlo: 1. Pokud není připojeno k jinému telefonu, restartujte jej a zkuste to znovu. 2. Pokud je připojeno k jinému telefonu, ukončete tam připojení a zkuste to znovu."),
"CWF_GPSNotOpen": ("GPS nie je zapnuté", "GPS není zapnuté"),
"CWF_GPSOrAPPLocationNotOpen": ("GPS alebo prístup aplikácie k polohe nie je zapnutý", "GPS ani přístup aplikace k poloze není zapnutý"),
"CWF_GoToAdd": ("Prejsť na pridanie", "Přejít na přidání"),
"CWF_MacAddress": ("MAC adresa:", "MAC adresa:"),
"CWF_NeedLacationPermissionsUseSearchWiFiList": ("Aplikácia zhromažďuje údaje o polohe na zobrazenie zoznamu Wi-Fi, aj keď je zatvorená alebo sa nepoužíva.", "Aplikace shromažďuje údaje o poloze pro zobrazení seznamu Wi-Fi, i když je zavřená nebo se nepoužívá."),
"CWF_NewDevice": ("Nové zariadenie", "Nové zařízení"),
"CWF_NoWiFiXXXIsFound": ("Nenašla sa sieť Wi-Fi XXX?", "Nenašla se síť Wi-Fi XXX?"),
"CWF_PleaseConfirmWhetherWifiIsNoPassword": ("Heslo Wi-Fi je prázdne. Overte, či vaša domáca sieť Wi-Fi nemá heslo.", "Heslo Wi-Fi je prázdné. Ověřte, zda vaše domácí síť Wi-Fi nemá heslo."),
"CWF_PleaseConnectFamilyWiFiFirst": ("Najprv sa pripojte k domácej sieti Wi-Fi.", "Nejdříve se připojte k domácí síti Wi-Fi."),
"CWF_PleaseConnectHomeWIFI": ("Pripojte sa k domácej sieti Wi-Fi", "Připojte se k domácí síti Wi-Fi"),
"CWF_PleaseOpenBluetoothPermissions": ("Zapnite Bluetooth", "Zapněte Bluetooth"),
"CWF_PleaseOpenLocationPermissions": ("Povoľte prístup k polohe", "Povolte přístup k poloze"),
"CWF_PleaseOpenWifiPermissions": ("Povoľte prístup k Wi-Fi", "Povolte přístup k Wi-Fi"),
"CWF_PleaseUseManualSelectionToBind": ("Pre zariadenia bez podpory Bluetooth použite položku Pridať ručne.", "Pro zařízení bez podpory Bluetooth použijte položku Přidat ručně."),
"CWF_Strong": ("Silné", "Silné"),
"CWF_Strongest": ("Normálne", "Normální"),
"CWF_SubmitFeedback": ("Odoslať spätnú väzbu", "Odeslat zpětnou vazbu"),
"CWF_ThePhoneCannotAccessInternetPleaseConnectHomeWIFI": ("Telefón nemá prístup na internet. Pripojte sa k domácej sieti Wi-Fi s internetom.", "Telefon nemá přístup k internetu. Připojte se k domácí síti Wi-Fi s internetem."),
"CWF_TimeOutNoFindDevice": ("Čas hľadania vypršal, zariadenie sa nenašlo", "Čas hledání vypršel, zařízení se nenašlo"),
"CWF_ViewSolution": ("Zobraziť riešenie", "Zobrazit řešení"),
"CWF_WIN_DeviceConnectAPP": ("Robot sa pripája k aplikácii", "Robot se připojuje k aplikaci"),
"CWF_WIN_DeviceConnectWiFi": ("Robot sa pripája k Wi-Fi", "Robot se připojuje k Wi-Fi"),
"CWF_Weak": ("Slabé", "Slabé"),
"CWF_WiFiPasswordCannotExceed64Digits": ("Heslo Wi-Fi nemôže presiahnuť 32 znakov", "Heslo Wi-Fi nemůže přesáhnout 32 znaků"),
"CWF_WiFiPasswordIsSpaced": ("Heslo Wi-Fi obsahuje medzeru. Skontrolujte heslo.", "Heslo Wi-Fi obsahuje mezeru. Zkontrolujte heslo."),
"CWF_WindowCleanMachine": ("Čistič okien", "Čistič oken"),
}


def patch(lang, index):
    path = os.path.join(ASSETS, f"{PREFIX}_{lang}.json")
    raw = open(path, encoding="utf-8").read()
    data = json.loads(raw)
    changed = 0
    for k, pair in T.items():
        if not data.get(k):
            data[k] = pair[index]
            changed += 1
    out = os.path.join("patched_assets", f"{PREFIX}_{lang}.json")
    os.makedirs("patched_assets", exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(lang, "filled", changed, "keys ->", out)


patch("sk", 0)
patch("cs-cz", 1)
