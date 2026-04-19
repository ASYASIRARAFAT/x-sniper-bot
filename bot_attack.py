import asyncio
import random
import hashlib
import sys
import os
import requests
from telethon import TelegramClient, events, errors

# --- 🎨 ANSI কালার প্যালেট ---
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
R = '\033[91m'  # Red
C = '\033[96m'  # Cyan
W = '\033[0m'   # White
B = '\033[1m'   # Bold

# --- 🖼️ প্রফেশনাল ব্যানার ফাংশন ---
def show_banner():
    os.system('clear')
    banner = f"""
{C}{B}  __  __      _____ _   _ _____ _____  ______ _____  
  \\ \\/ /     / ____| \\ | |_   _|  __ \\|  ____|  __ \\ 
   \\  /_____| (___ |  \\| | | | | |__) | |__  | |__) |
   /  \\______|___ \\| . ` | | | |  ___/|  __| |  _  / 
  / /\\ \\     ____) | |\\  |_| |_| |    | |____| | \\ \\ 
 /_/  \\_\\   |_____/|_| \\_|_____|_|    |______|_|  \\_\\
                                                      
{Y}         [+] Version: 2.0 | High Speed Snipping [+]
{G}         [+] Developer: ASYASIRARAFAT           [+]
{C}=============================================================
|               {W}PREMIUM TELEGRAM SNIPER TOOL{C}                |
=============================================================
    """
    print(banner)

def show_menu():
    print(f"{G}[ 1 ] {W}Start Sniper Attack")
    print(f"{G}[ 2 ] {W}Check Hardware ID (HWID)")
    print(f"{G}[ 3 ] {W}Update Tool (Git Pull)")
    print(f"{G}[ 4 ] {W}About Developer")
    print(f"{R}[ X ] {W}Exit Tool")
    print(f"{C}-------------------------------------------------------------{W}")

# --- 🔐 সিকিউরিটি ও অ্যাপ্রুভাল সিস্টেম ---
RAW_LINK = "https://raw.githubusercontent.com/ASYASIRARAFAT/x-sniper-bot/main/approved.txt"
FB_LINK = "https://www.facebook.com/Yasir.Arafat.Hacker.Official"

def get_hwid():
    try:
        import subprocess
        cpu_info = subprocess.check_output('uname -a', shell=True).decode()
        user_name = os.popen('whoami').read().strip()
        combined = cpu_info + user_name
        return hashlib.sha256(combined.encode()).hexdigest()[:12].upper()
    except:
        return "UNKNOWN-DEV-ID"

def verify_user():
    show_banner() # <--- এখানে ব্যানার কল করা হয়েছে
    user_id = get_hwid()
    hyperlink = f"\x1b]8;;{FB_LINK}\x1b\\{FB_LINK}\x1b]8;;\x1b\\"
    
    print(f"\n{Y}🔍 Checking Authorization...{W}")
    print(f"🔑 Your HWID: {user_id}")
    
    try:
        response = requests.get(RAW_LINK)
        if user_id in response.text:
            print(f"{G}✅ Access Granted! Welcome to X-Sniper.{W}\n")
            show_menu() # <--- এখানে মেনু কল করা হয়েছে
            
            # মেনু অপশন হ্যান্ডেল করা
            choice = input(f"{C}root@x-sniper:~# {W}").strip()
            if choice == '1':
                return True
            elif choice == '2':
                print(f"{Y}Your HWID: {user_id}{W}")
                sys.exit()
            elif choice == '3':
                print(f"{Y}Updating...{W}")
                os.system('git pull')
                sys.exit()
            elif choice == '4':
                print(f"{G}Developer: ASYASIRARAFAT\nFacebook: {FB_LINK}{W}")
                sys.exit()
            elif choice.lower() == 'x':
                sys.exit()
            else:
                print(f"{Y}Starting Sniper Engine...{W}")
                return True
        else:
            print(f"{R}" + "-" * 45 + f"{W}")
            print(f"{R}❌ ACCESS DENIED! (অ্যাক্সেস রিজেক্ট করা হয়েছে){W}")
            print(f"{Y}👉 Your ID: {user_id}{W}")
            print(f"{R}" + "-" * 45 + f"{W}")
            print("অ্যাপ্রুভালের জন্য নিচে দেওয়া লিঙ্কে ক্লিক করুন:")
            print(f"🔗 Facebook: {hyperlink}")
            sys.exit()
    except:
        print(f"{R}⚠️ Connection Error! Please check your internet.{W}")
        sys.exit()

# ভেরিফিকেশন রান করা
verify_user()

# --- ⚙️ কনফিগারেশন লোডার ---
CONFIG_FILE = "config.txt"
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                return int(lines[0]), lines[1]
    
    print(f"\n{C}--- 🛠️ Initial Setup ---{W}")
    api_id = input("Enter API ID: ")
    api_hash = input("Enter API Hash: ")
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{api_id}\n{api_hash}")
    return int(api_id), api_hash

# সেশন স্টার্ট
API_ID, API_HASH = load_config()
BOT = 'XPrepaidsExchangeBot'
client = TelegramClient('sniper_session', API_ID, API_HASH)

# --- গ্লোবাল স্টেট ও বাকি লজিক (আপনার আগের কোড) ---
target_bin = None
target_bal = None
wait_seconds = 0
is_ready = False
is_attacking = False
stop_flag = False
last_button_msg = None
click_lock = asyncio.Lock()
REFRESH_KEYS = ["Refresh", "🔄", "Reload", "Update"]

def reset_all():
    global target_bin, target_bal, wait_seconds, is_ready, is_attacking, stop_flag, last_button_msg
    target_bin = target_bal = None
    wait_seconds = 0
    is_ready = is_attacking = False
    stop_flag = True
    last_button_msg = None
    print(f"\n{Y}🛑 স্ট্যান্ডবাই মোড...{W}")

reset_all()

# [বাকি সব ফাংশন যেমন আছে তেমনই থাকবে...]
def is_latest_listing_menu(msg):
    if not msg or not msg.buttons or not msg.text: return False
    if "Main Listings" not in msg.text and "Total Cards" not in msg.text: return False
    return any(any(k in b.text for k in REFRESH_KEYS) for row in msg.buttons for b in row)

def find_purchase_btn(msg):
    if not msg or not msg.buttons: return None
    t_bin = target_bin.replace(' ', '').lower()
    t_bal = target_bal.replace(' ', '').lower()
    BAD_SIGNS = ["🅶", "🅿️", "🔄", "used", "relister"]
    flat_buttons = [btn for row in msg.buttons for btn in row]
    found_index = None
    for i, btn in enumerate(flat_buttons):
        text = btn.text.replace(' ', '').replace('$', '').lower()
        if t_bin in text and t_bal in text:
            is_bad = any(sign in btn.text for sign in BAD_SIGNS)
            if is_bad:
                print(f"{Y}⚠️ পুরনো কার্ড ইগনোর করা হলো: {btn.text}{W}")
                continue
            found_index = i
            print(f"{G}✨ ফ্রেশ কার্ড পাওয়া গেছে! বাটন: {btn.text}{W}")
            break
    if found_index is None: return None
    for btn in flat_buttons[found_index:]:
        if "purchase" in btn.text.lower(): return btn
    return None

async def double_click_purchase(btn):
    global is_attacking
    is_attacking = False
    print(f"\n{R}🔥 TARGET LOCKED!{W}")
    async with click_lock:
        for i in range(2):
            try:
                print(f"{G}⚡ Click {i+1}{W}")
                await btn.click()
                await asyncio.sleep(0.4)
            except errors.FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except: pass
    print(f"{G}✅ DONE{W}")
    reset_all()

async def trigger_refresh():
    if stop_flag or not is_attacking or not last_button_msg: return
    buttons = [b for row in last_button_msg.buttons for b in row if any(k in b.text for k in REFRESH_KEYS)]
    if not buttons: return
    btn = random.choice(buttons)
    print(f"{C}🔄 Refreshing...{W}")
    async with click_lock:
        try: await btn.click()
        except: pass

async def init_scan():
    global last_button_msg
    async for msg in client.iter_messages(BOT, limit=10):
        if is_latest_listing_menu(msg):
            last_button_msg = msg
            print(f"{G}✅ Latest menu locked (ID: {msg.id}){W}")
            btn = find_purchase_btn(msg)
            if btn: await double_click_purchase(btn)
            else: await trigger_refresh()
            return

@client.on(events.NewMessage(outgoing=True, chats=BOT))
async def command(event):
    global target_bin, target_bal, wait_seconds, is_ready, is_attacking, stop_flag
    txt = event.raw_text.lower().strip()
    if txt.startswith("buy"):
        try:
            _, b, bal, wait = txt.split()
            target_bin, target_bal, wait_seconds = b, bal, int(wait)
            is_ready, stop_flag = True, False
            print(f"{G}🎯 টার্গেট সেট: BIN {b} | Bal {bal}{W}")
        except: print(f"{R}❌ ফরম্যাট: buy 511332xx 1.49 2{W}")
    elif txt == "confirm" and is_ready:
        print(f"{Y}⏳ Waiting {wait_seconds}s{W}")
        await asyncio.sleep(wait_seconds)
        is_attacking = True
        print(f"{R}🚀 STARTED{W}")
        await init_scan()
    elif txt == "stop": reset_all()

@client.on(events.NewMessage(chats=BOT))
@client.on(events.MessageEdited(chats=BOT))
async def handler(event):
    global last_button_msg
    if stop_flag or not is_attacking: return
    msg = event.message
    if not is_latest_listing_menu(msg): return
    if last_button_msg and msg.id < last_button_msg.id: return
    last_button_msg = msg
    btn = find_purchase_btn(msg)
    if btn: await double_click_purchase(btn)
    else:
        await asyncio.sleep(random.uniform(0.5, 1.0))
        await trigger_refresh()

async def main():
    await client.start()
    print(f"\n{G}🤖 Sniper Running and Secure...{W}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
