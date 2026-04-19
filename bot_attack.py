import asyncio, random, hashlib, sys, os, requests, re, time
from telethon import TelegramClient, events, errors
from datetime import datetime

# --- 🎨 PRO COLORS ---
G, Y, R, C, W, B = '\033[92m', '\033[93m', '\033[91m', '\033[96m', '\033[0m', '\033[1m'

# --- 🛠️ UI & LOGGING SYSTEM ---
def ui_header():
    os.system('clear')
    print(f"{C}{B}╔══════════════════════════════════════════════════════════╗")
    print(f"║                      {W}{B}X-SNIPER v3.5{C}{B}                       ║")
    print(f"║             {Y}PREMIUM TELEGRAM SNIPER ENGINE{C}{B}               ║")
    print(f"║             {G}Developed By: Yasir Arafat{C}{B}                   ║")
    print(f"╚══════════════════════════════════════════════════════════╝{W}")

def log(msg, type="info"):
    now = datetime.now().strftime("%H:%M:%S")
    if type == "success": print(f"{G}[{now}] [✔] {msg}{W}")
    elif type == "error": print(f"{R}[{now}] [✘] {msg}{W}")
    elif type == "wait": print(f"{Y}[{now}] [•] {msg}{W}")
    elif type == "target": print(f"{C}[{now}] [🎯] {msg}{W}")
    else: print(f"{W}[{now}] [ℹ] {msg}{W}")

# --- 🔐 SECURITY & AUTHORIZATION ---
RAW_LINK = "https://raw.githubusercontent.com/ASYASIRARAFAT/x-sniper-bot/main/approved.txt"

def get_hwid():
    try:
        # Generate a unique ID based on device info
        cpu = os.popen('uname -a').read()
        user = os.popen('whoami').read()
        return hashlib.sha256((cpu + user).encode()).hexdigest()[:12].upper()
    except: 
        return "9FDF6C1387E7"

def verify():
    ui_header()
    uid = get_hwid()
    log(f"Checking Hardware ID: {uid}", "wait")
    try:
        # Check if the HWID exists in the approved list
        res = requests.get(RAW_LINK, timeout=10).text
        if uid in res:
            log("Access Granted! Welcome Commander.", "success")
            time.sleep(1)
            return True
        else:
            log(f"Access Denied! ID: {uid} is not authorized.", "error")
            print(f"{Y}\nContact Yasir Arafat for Activation.{W}")
            return False
    except Exception as e:
        log(f"Connection Error: {e}", "error")
        return False

# --- ⚙️ BOT CONFIGURATION ---
# Replace these with your own API details if needed
API_ID, API_HASH = 30150082, 'd80dc83628969f279e4d1fde7599283e'
client = TelegramClient('sniper_session', API_ID, API_HASH)

target_bin = None
target_bal = None
wait_seconds = 0
is_attacking = False
click_lock = asyncio.Lock()

# --- 📩 TELEGRAM COMMAND HANDLER ---
@client.on(events.NewMessage(outgoing=True, chats='XPrepaidsExchangeBot'))
async def cmd(e):
    global target_bin, target_bal, wait_seconds, is_attacking
    t = e.raw_text.lower().strip()
    
    # Format: buy bin balance wait_time
    if t.startswith("buy"):
        try:
            parts = t.split()
            if len(parts) >= 4:
                _, b, bal, w = parts
                target_bin, target_bal, wait_seconds = b, bal, int(w)
                log(f"TARGET LOCKED: {b} | Balance: ${bal}", "target")
            else:
                log("Usage: buy 435880 10 5", "error")
        except Exception as ex: 
            log(f"Input Error: {ex}", "error")
        
    elif t == "confirm":
        if target_bin:
            log(f"Waiting {wait_seconds}s before scan starts...", "wait")
            await asyncio.sleep(wait_seconds)
            is_attacking = True
            ui_header()
            log("SNIPER ENGINE ACTIVATED - READY TO STRIKE", "success")
            print(f"{C}────────────────────────────────────────────────────────────{W}")
        else:
            log("Error: Please set a target first using 'buy'.", "error")

# --- ⚡ THE SNIPER ENGINE ---
@client.on(events.NewMessage(chats='XPrepaidsExchangeBot'))
@client.on(events.MessageEdited(chats='XPrepaidsExchangeBot'))
async def handler(e):
    global is_attacking
    # Validation: Bot is attacking, has buttons, and is in the correct menu
    if not is_attacking or not e.message.buttons: return
    if "Main Listings" not in e.message.text: return
    
    msg = e.message
    if not target_bin or not target_bal: return
    
    t_bin = str(target_bin).lower()
    target_balance = round(float(target_bal), 2)
    BAD = ["🅶", "🅿️", "used", "relister"]
    btn_to_click = None

    # --- ROW-BASED ACCURATE MATCHING ---
    for row in msg.buttons:
        for b in row:
            txt = b.text.lower()
            # BIN Matching
            if t_bin in txt:
                # Filter out bad cards
                if any(x in txt for x in BAD): continue
                
                # Balance Matching (Regex for float numbers)
                nums = [round(float(n.replace(',', '')), 2) for n in re.findall(r"\d+\.\d+", txt)]
                if any(abs(n - target_balance) <= 0.01 for n in nums):
                    log(f"MATCH FOUND: {b.text}", "success")
                    # Finding the associated 'Purchase' button in the same row
                    for pb in row:
                        if "purchase" in pb.text.lower():
                            btn_to_click = pb; break
                    if btn_to_click: break
        if btn_to_click: break

    # --- INSTANT EXECUTION ---
    if btn_to_click:
        async with click_lock:
            log(f"TARGET DETECTED! Clicking Purchase...", "wait")
            # Double click for safety
            try:
                await btn_to_click.click()
                await asyncio.sleep(0.05) 
                await btn_to_click.click()
                log("MISSION ACCOMPLISHED! Card Captured.", "success")
                is_attacking = False # Stop engine after success
                print(f"{C}────────────────────────────────────────────────────────────{W}")
            except Exception as ex:
                log(f"Click Error: {ex}", "error")

# --- 🚀 STARTING THE TOOL ---
async def main():
    # Security Check
    if not verify(): 
        sys.exit()
        
    log("Starting Telegram Session...", "wait")
    await client.start()
    ui_header()
    log("X-Sniper Master Engine is Online.", "success")
    log("Developed By: Yasir Arafat", "info")
    log("Waiting for 'buy' command in Telegram Bot...", "info")
    
    # Keep the script running
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print(f"\n{R}Tool Stopped By User.{W}")
