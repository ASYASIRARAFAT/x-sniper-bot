import asyncio, random, hashlib, sys, os, requests
from telethon import TelegramClient, events, errors

# --- 🎨 কালার ও ব্যানার ---
G, Y, R, C, W, B = '\033[92m', '\033[93m', '\033[91m', '\033[96m', '\033[0m', '\033[1m'

def show_banner():
    os.system('clear')
    print(f"""{C}{B}
  __  __      _____ _   _ _____ _____  ______ _____  
  \\ \\/ /     / ____| \\ | |_   _|  __ \\|  ____|  __ \\ 
   \\  /_____| (___ |  \\| | | | | |__) | |__  | |__) |
   /  \\______|___ \\| . ` | | | |  ___/|  __| |  _  / 
  / /\\ \\     ____) | |\\  |_| |_| |    | |____| | \\ \\ 
 /_/  \\_\\   |_____/|_| \\_|_____|_|    |______|_|  \\_\\
{Y}         [+] Version: 2.0 | High Speed Snipping [+]
{G}         [+] Developer: ASYASIRARAFAT           [+]
{C}============================================================={W}""")

def show_menu():
    print(f"{G}[ 1 ] {W}Start Sniper Attack\n{G}[ 2 ] {W}Check HWID\n{G}[ 3 ] {W}Update Tool\n{R}[ X ] {W}Exit")
    print(f"{C}-------------------------------------------------------------{W}")

# --- 🔐 সিকিউরিটি ---
RAW_LINK = "https://raw.githubusercontent.com/ASYASIRARAFAT/x-sniper-bot/main/approved.txt"
FB_LINK = "https://www.facebook.com/Yasir.Arafat.Hacker.Official"

def get_hwid():
    try:
        import subprocess
        cpu = subprocess.check_output('uname -a', shell=True).decode()
        user = os.popen('whoami').read().strip()
        return hashlib.sha256((cpu + user).encode()).hexdigest()[:12].upper()
    except: return "9FDF6C1387E7"

def verify_user():
    show_banner()
    uid = get_hwid()
    print(f"{Y}🔍 Checking Authorization...{W}\n🔑 HWID: {uid}")
    try:
        res = requests.get(RAW_LINK)
        if uid in res.text:
            print(f"{G}✅ Access Granted!{W}")
            show_menu()
            opt = input(f"{C}root@x-sniper:~# {W}")
            if opt == '1': return True
            else: sys.exit()
        else:
            print(f"{R}❌ ACCESS DENIED!{W}\nID: {uid}\nContact: {FB_LINK}")
            sys.exit()
    except: sys.exit()

verify_user()

# --- ⚙️ কনফিগ ও স্নিপার লজিক ---
API_ID, API_HASH = 30150082, 'd80dc83628969f279e4d1fde7599283e'
client = TelegramClient('sniper_session', API_ID, API_HASH)
target_bin = target_bal = None
wait_seconds = 0
is_attacking = stop_flag = False
last_button_msg = None
click_lock = asyncio.Lock()

@client.on(events.NewMessage(outgoing=True, chats='XPrepaidsExchangeBot'))
async def cmd(e):
    global target_bin, target_bal, wait_seconds, is_attacking, stop_flag
    t = e.raw_text.lower()
    if t.startswith("buy"):
        try:
            _, b, bal, w = t.split()
            target_bin, target_bal, wait_seconds = b, bal, int(w)
            stop_flag = False
            print(f"{G}🎯 Target Set: {b} | {bal}{W}")
        except: print(f"{R}Format: buy bin bal wait{W}")
    elif t == "confirm":
        await asyncio.sleep(wait_seconds)
        is_attacking = True
        print(f"{R}🚀 ATTACK STARTED{W}")

@client.on(events.NewMessage(chats='XPrepaidsExchangeBot'))
@client.on(events.MessageEdited(chats='XPrepaidsExchangeBot'))
async def handler(e):
    global last_button_msg
    if not is_attacking or not e.message.buttons: return
    msg = e.message
    if "Main Listings" not in msg.text: return
    last_button_msg = msg
    
    # বাটন খোঁজা
    t_bin, t_bal = target_bin.lower(), target_bal.lower()
    btn_to_click = None
    flat = [b for r in msg.buttons for b in r]
    
    for i, b in enumerate(flat):
        txt = b.text.lower()
        if t_bin in txt and t_bal in txt:
            for pb in flat[i:]:
                if "purchase" in pb.text.lower():
                    btn_to_click = pb
                    break
    
    if btn_to_click:
        async with click_lock:
            for _ in range(2):
                await btn_to_click.click()
                await asyncio.sleep(0.3)
        print(f"{G}✅ TARGET HIT!{W}")
    else:
        # রিফ্রেশ লজিক
        ref = [b for r in msg.buttons for b in r if "Refresh" in b.text or "🔄" in b.text]
        if ref: await random.choice(ref).click()

async def main():
    await client.start()
    print(f"{G}🤖 Sniper Engine Live...{W}")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
