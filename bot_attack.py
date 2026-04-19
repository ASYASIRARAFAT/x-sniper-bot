import asyncio
import random
import hashlib
import sys
import os
import requests
from telethon import TelegramClient, events, errors



import os

# টার্মিনাল কালার কোড
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
WHITE = '\033[0m'
BOLD = '\033[1m'

def show_banner():
    os.system('clear') # স্ক্রিন পরিষ্কার করবে
    banner = f"""
{CYAN}{BOLD}
  __   __      _____ _   _ _____ _____  ______ _____  
  \ \ / /     / ____| \ | |_   _|  __ \|  ____|  __ \ 
   \ V /_____| (___ |  \| | | | | |__) | |__  | |__) |
    > <______|  ___\| . ` | | | |  ___/|  __| |  _  / 
   / ^ \     |____  | |\  |_| |_| |    | |____| | \ \ 
  /_/ \_\    |_____/|_| \_|_____|_|    |______|_|  \_\
                                                      
{YELLOW}         [+] Version: 2.0 | Powered by YASIR ARAFAT [+]
{GREEN}         [+] Developer: ASYASIRARAFAT           [+]
{CYAN}=============================================================
|               {WHITE}Welcome to High-Speed Sniper Tool{CYAN}           |
=============================================================
    """
    print(banner)

def show_menu():
    print(f"{GREEN}[ 1 ] {WHITE}Start Sniper Attack")
    print(f"{GREEN}[ 2 ] {WHITE}Update Tool")
    print(f"{GREEN}[ 3 ] {WHITE}Check My HWID")
    print(f"{GREEN}[ 4 ] {WHITE}Contact Admin")
    print(f"{RED}[ X ] {WHITE}Exit Bot")
    print(f"{CYAN}============================================================={WHITE}\n")

# --- এটি আপনার verify_user() ফাংশনের ঠিক আগে কল করুন ---
show_banner()
show_menu()




# --- 🔐 সিকিউরিটি ও অ্যাপ্রুভাল সিস্টেম ---
# আপনার গিটহাবের RAW লিঙ্ক এবং ফেসবুক লিঙ্ক
RAW_LINK = "https://raw.githubusercontent.com/ASYASIRARAFAT/x-sniper-bot/main/approved.txt"
FB_LINK = "https://www.facebook.com/Yasir.Arafat.Hacker.Official"

def get_hwid():
    try:
        # টার্মাক্স ও উইন্ডোজের জন্য ইউনিক আইডি তৈরির চেষ্টা
        import subprocess
        cpu_info = subprocess.check_output('uname -a', shell=True).decode()
        user_name = os.popen('whoami').read().strip()
        combined = cpu_info + user_name
        return hashlib.sha256(combined.encode()).hexdigest()[:12].upper()
    except:
        return "UNKNOWN-DEV-ID"

def verify_user():
    user_id = get_hwid()
    # হাইপারলিঙ্ক ফরম্যাট (টার্মিনাল সাপোর্ট করলে নীল দেখাবে)
    hyperlink = f"\x1b]8;;{FB_LINK}\x1b\\{FB_LINK}\x1b]8;;\x1b\\"
    
    print(f"\n🔍 Checking Authorization...")
    print(f"🔑 Your HWID: {user_id}")
    
    try:
        response = requests.get(RAW_LINK)
        if user_id in response.text:
            print("✅ Access Granted! Welcome to X-Sniper.")
            return True
        else:
            print("-" * 45)
            print("❌ ACCESS DENIED! (অ্যাক্সেস রিজেক্ট করা হয়েছে)")
            print(f"👉 Your ID: {user_id}")
            print("-" * 45)
            print("অ্যাপ্রুভালের জন্য নিচে দেওয়া লিঙ্কে ক্লিক করুন:")
            print(f"🔗 Facebook: {hyperlink}")
            print("-" * 45)
            sys.exit()
    except:
        print("⚠️ Connection Error! Please check your internet (GitHub Access required).")
        sys.exit()

# ভেরিফিকেশন রান করা
verify_user()

# --- ⚙️ কনফিগারেশন লোডার (ইউজার তার নিজের আইডি দিবে) ---
CONFIG_FILE = "config.txt"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                return int(lines[0]), lines[1]
    
    print("\n--- 🛠️ Initial Setup ---")
    api_id = input("Enter API ID: ")
    api_hash = input("Enter API Hash: ")
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{api_id}\n{api_hash}")
    return int(api_id), api_hash

API_ID, API_HASH = load_config()
BOT = 'XPrepaidsExchangeBot'

client = TelegramClient('sniper_session', API_ID, API_HASH)

# --- 🎯 গ্লোবাল স্টেট ---
target_bin = None
target_bal = None
wait_seconds = 0
is_ready = False
is_attacking = False
stop_flag = False
last_button_msg = None
click_lock = asyncio.Lock()
REFRESH_KEYS = ["Refresh", "🔄", "Reload", "Update"]

# --- রিসেট ---
def reset_all():
    global target_bin, target_bal, wait_seconds
    global is_ready, is_attacking, stop_flag, last_button_msg
    target_bin = target_bal = None
    wait_seconds = 0
    is_ready = is_attacking = False
    stop_flag = True
    last_button_msg = None
    print("\n🛑 স্ট্যান্ডবাই মোড...")

reset_all()

# --- মেনু চেক ---
def is_latest_listing_menu(msg):
    if not msg or not msg.buttons or not msg.text: return False
    if "Main Listings" not in msg.text and "Total Cards" not in msg.text: return False
    return any(any(k in b.text for k in REFRESH_KEYS) for row in msg.buttons for b in row)

# --- ✅ ADVANCED FRESH CARD FINDER (Anti-Used Filter) ---
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
                print(f"⚠️ পুরনো কার্ড ইগনোর করা হলো: {btn.text}")
                continue
            found_index = i
            print(f"✨ ফ্রেশ কার্ড পাওয়া গেছে! বাটন: {btn.text}")
            break

    if found_index is None: return None
    for btn in flat_buttons[found_index:]:
        if "purchase" in btn.text.lower(): return btn
    return None

# --- ডাবল ক্লিক ---
async def double_click_purchase(btn):
    global is_attacking
    is_attacking = False
    print("\n🔥 TARGET LOCKED!")
    async with click_lock:
        for i in range(2):
            try:
                print(f"⚡ Click {i+1}")
                await btn.click()
                await asyncio.sleep(0.4)
            except errors.FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except: pass
    print("✅ DONE")
    reset_all()

# --- রিফ্রেশ ---
async def trigger_refresh():
    if stop_flag or not is_attacking or not last_button_msg: return
    buttons = [b for row in last_button_msg.buttons for b in row if any(k in b.text for k in REFRESH_KEYS)]
    if not buttons: return
    btn = random.choice(buttons)
    print("🔄 Refreshing...")
    async with click_lock:
        try: await btn.click()
        except: pass

# --- ইনিশিয়াল স্ক্যান ---
async def init_scan():
    global last_button_msg
    async for msg in client.iter_messages(BOT, limit=10):
        if is_latest_listing_menu(msg):
            last_button_msg = msg
            print(f"✅ Latest menu locked (ID: {msg.id})")
            btn = find_purchase_btn(msg)
            if btn: await double_click_purchase(btn)
            else: await trigger_refresh()
            return

# --- কমান্ড হ্যান্ডলার ---
@client.on(events.NewMessage(outgoing=True, chats=BOT))
async def command(event):
    global target_bin, target_bal, wait_seconds, is_ready, is_attacking, stop_flag
    txt = event.raw_text.lower().strip()
    if txt.startswith("buy"):
        try:
            _, b, bal, wait = txt.split()
            target_bin, target_bal, wait_seconds = b, bal, int(wait)
            is_ready, stop_flag = True, False
            print(f"🎯 টার্গেট সেট: BIN {b} | Bal {bal}")
        except: print("❌ ফরম্যাট: buy 511332xx 1.49 2")
    elif txt == "confirm" and is_ready:
        print(f"⏳ Waiting {wait_seconds}s")
        await asyncio.sleep(wait_seconds)
        is_attacking = True
        print("🚀 STARTED")
        await init_scan()
    elif txt == "stop": reset_all()

# --- মেইন হ্যান্ডলার ---
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

# --- রান ---
async def main():
    await client.start()
    print("\n🤖 Sniper Running and Secure...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
