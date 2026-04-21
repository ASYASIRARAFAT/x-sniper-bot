import asyncio, hashlib, sys, os, requests, re, time
from telethon import TelegramClient, events, errors
from datetime import datetime

# --- 🎨 COLORS ---
G, Y, R, C, W, B = '\033[92m', '\033[93m', '\033[91m', '\033[96m', '\033[0m', '\033[1m'

# --- 🔐 SECURITY CONFIG ---
RAW_LINK = "https://raw.githubusercontent.com/ASYASIRARAFAT/x-sniper-bot/main/approved.txt"

def get_hwid():
    try:
        # Termux/Linux এর জন্য ইউনিক আইডি জেনারেট করা
        cpu = os.popen('uname -a').read()
        user = os.popen('whoami').read()
        return hashlib.sha256((cpu + user).encode()).hexdigest()[:12].upper()
    except:
        return "9FDF6C1387E7"

# --- 🛠 UI & LOGGING ---
def ui_header():
    os.system('clear')
    print(f"{C}{B}╔══════════════════════════════════════════════════════════╗")
    print(f"║                      {W}{B}X-SNIPER v21.0{C}{B}                      ║")
    print(f"║             {Y}SECURED MULTI-TARGET SNIPER ENGINE{C}{B}           ║")
    print(f"║             {G}Developed By: Yasir Arafat{C}{B}                   ║")
    print(f"╚══════════════════════════════════════════════════════════╝{W}")

def log(msg, type="info"):
    now = datetime.now().strftime("%H:%M:%S")
    if type == "success": print(f"{G}[{now}] [✔] {msg}{W}")
    elif type == "error": print(f"{R}[{now}] [✘] {msg}{W}")
    elif type == "target": print(f"{C}[{now}] [🎯] {msg}{W}")
    elif type == "wait": print(f"{Y}[{now}] [•] {msg}{W}")
    else: print(f"{W}[{now}] [ℹ] {msg}{W}")

# --- 🛡️ VERIFICATION ENGINE ---
def verify_user():
    uid = get_hwid()
    log(f"Checking HWID: {uid}", "wait")
    try:
        res = requests.get(RAW_LINK, timeout=10).text
        if uid in res:
            log("Access Granted! Welcome Commander.", "success")
            time.sleep(1)
            return True
        else:
            log("Access Denied! Hardware ID not registered.", "error")
            print(f"{Y}\nYour ID: {uid}{W}")
            print(f"{C}Contact Yasir Arafat to register your HWID.{W}")
            return False
    except:
        log("Connection Error! Unable to verify ID.", "error")
        return False

# --- ⚙️ CONFIGURATION (API Details) ---
def load_config():
    if os.path.exists("config.txt"):
        with open("config.txt", "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(lines) >= 2:
                try:
                    return int(lines[0]), lines[1]
                except ValueError:
                    log("Invalid data in config.txt! Re-configuring...", "error")
    
    ui_header()
    log("Configuration not found! Enter API details:", "wait")
    
    # ইনপুট নেওয়ার সময় strip() ব্যবহার করা হয়েছে যাতে স্পেস না থাকে
    api_id_input = input(f"{C}Enter API ID: {W}").strip()
    api_hash_input = input(f"{C}Enter API Hash: {W}").strip()
    
    with open("config.txt", "w") as f:
        f.write(f"{api_id_input}\n{api_hash_input}")
    
    return int(api_id_input), api_hash_input

# কনফিগারেশন লোড করা হচ্ছে
try:
    API_ID, API_HASH = load_config()
except ValueError:
    log("API ID অবশ্যই একটি সংখ্যা হতে হবে!", "error")
    exit()

BOT = 'XPrepaidsExchangeBot'
client = TelegramClient('v21_session', API_ID, API_HASH)

# --- GLOBAL STATE ---
targets = [] 
is_attacking = False
click_lock = asyncio.Lock()

# --- MATCHING ENGINE ---
def find_target_btn(msg):
    if not msg or not msg.buttons: return None
    BAD_SIGNS = ["🅶", "🅿️", "used", "relister", "❌"]
    flat_buttons = [btn for row in msg.buttons for btn in row]

    for target in targets:
        t_bin = target['bin'].lower()
        t_bal = target['bal'].replace('$', '').lower()
        
        found_index = None
        for i, btn in enumerate(flat_buttons):
            btn_txt = btn.text.replace(' ', '').replace('$', '').lower()
            if t_bin in btn_txt and t_bal in btn_txt:
                if any(sign in btn.text for sign in BAD_SIGNS): continue
                found_index = i
                log(f"Match Found: {btn.text}", "success")
                break

        if found_index is not None:
            for btn in flat_buttons[found_index:]:
                if "purchase" in btn.text.lower(): return btn
    return None

# --- EXECUTION ---
async def attack(btn):
    global is_attacking
    log("TARGET SPOTTED! EXECUTING PURCHASE...", "target")
    async with click_lock:
        for i in range(2):
            try:
                await btn.click()
                log(f"Click {i+1} Sent", "success")
                await asyncio.sleep(0.3)
            except Exception as e: log(f"Error: {e}", "error")
    is_attacking = False 
    log("Attack Cycle Finished.", "info")

# --- COMMANDS ---
@client.on(events.NewMessage(outgoing=True, chats=BOT))
async def command(event):
    global targets, is_attacking
    txt = event.raw_text.lower().strip()

    if txt.startswith("buy"):
        try:
            parts = txt.split()
            # buy bin bal wait (wait logic handled in confirm)
            targets.append({'bin': parts[1], 'bal': parts[2], 'wait': int(parts[3])})
            log(f"Target Added: {parts[1]} (${parts[2]})", "target")
        except: log("Format: buy 511332 10.45 0", "error")

    elif txt == "confirm":
        if not targets:
            log("No targets set!", "error")
            return
        
        # শেষের টার্গেটের ওয়েট টাইম ব্যবহার করা হবে
        wait = targets[-1]['wait']
        log(f"Engine starting in {wait}s...", "wait")
        await asyncio.sleep(wait)
        
        is_attacking = True
        ui_header()
        log(f"HUNTING MODE: TRACKING {len(targets)} TARGETS", "success")

    elif txt == "clear":
        targets = []
        is_attacking = False
        log("Targets cleared and engine stopped.", "error")

# --- MAIN HANDLER ---
@client.on(events.NewMessage(chats=BOT))
@client.on(events.MessageEdited(chats=BOT))
async def handler(event):
    if not is_attacking or not event.message.buttons: return
    
    msg_text = event.message.text
    if "listings" not in msg_text.lower() and "total cards" not in msg_text.lower():
        return

    btn = find_target_btn(event.message)
    if btn:
        await attack(btn)

# --- START ---
async def main():
    ui_header()
    # সিকিউরিটি চেক সবার আগে
    if not verify_user():
        sys.exit()
        
    log("Connecting to Telegram...", "wait")
    await client.start()
    ui_header()
    log("X-Sniper v21.0 is Ready.", "success")
    log(f"HWID: {get_hwid()}", "info")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
