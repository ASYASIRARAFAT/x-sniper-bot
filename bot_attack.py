import asyncio, random, hashlib, sys, os, requests, re, time
from telethon import TelegramClient, events, errors

# --- 🎨 কালার ও অ্যানিমেশন ---
G, Y, R, C, W, B = '\033[92m', '\033[93m', '\033[91m', '\033[96m', '\033[0m', '\033[1m'

def slow_print(text, speed=0.002):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(speed)
    print()

def show_banner():
    os.system('clear')

    print(f"""{C}{B}
╔══════════════════════════════════════════════════════╗
║                    X-SNIPER v3.0                     ║
║              Telegram Auto Sniper Engine             ║
╚══════════════════════════════════════════════════════╝
{W}
{Y}   ██╗  ██╗ ███████╗███╗   ██╗██╗██████╗ ███████╗
   ╚██╗██╔╝ ██╔════╝████╗  ██║██║██╔══██╗██╔════╝
    ╚███╔╝  █████╗  ██╔██╗ ██║██║██████╔╝█████╗  
    ██╔██╗  ██╔══╝  ██║╚██╗██║██║██╔═══╝ ██╔══╝  
   ██╔╝ ██╗ ███████╗██║ ╚████║██║██║     ███████╗
   ╚═╝  ╚═╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝
{W}
{C}══════════════════════════════════════════════════════
{G} [1] Start Sniper Engine
{G} [2] Check Hardware ID
{G} [3] Update Tool
{G} [4] Contact Developer
{R} [X] Exit
{C}══════════════════════════════════════════════════════
""")

# --- 🔐 সিকিউরিটি ---
RAW_LINK = "https://raw.githubusercontent.com/ASYASIRARAFAT/x-sniper-bot/main/approved.txt"
def get_hwid():
    try:
        cpu = os.popen('uname -a').read()
        user = os.popen('whoami').read()
        return hashlib.sha256((cpu + user).encode()).hexdigest()[:12].upper()
    except: return "9FDF6C1387E7"

def verify():
    show_banner()
    uid = get_hwid()
    slow_print(f"{Y}🔍 Authorization: Checking HWID...{W}")
    print(f"🔑 ID: {uid}")
    try:
        res = requests.get(RAW_LINK, timeout=10).text
        if uid in res:
            slow_print(f"{G}✅ ACCESS GRANTED! Welcome, Commander.{W}")
            opt = input(f"\n{C}root@x-sniper:~# {W}").strip()
            if opt == '1': return True
            elif opt == '3':
                print(f"{Y}Updating...{W}")
                os.system('git pull')
                sys.exit()
            else: sys.exit()
        else:
            print(f"{R}❌ ACCESS DENIED! Contact Admin.{W}")
            sys.exit()
    except: sys.exit()

if not verify(): sys.exit()

# --- ⚙️ কনফিগ ও ইঞ্জিন ---
API_ID, API_HASH = 30150082, 'd80dc83628969f279e4d1fde7599283e'
client = TelegramClient('sniper_session', API_ID, API_HASH)
target_bin = target_bal = None
wait_seconds = 0
is_attacking = stop_flag = False
click_lock = asyncio.Lock()

@client.on(events.NewMessage(outgoing=True, chats='XPrepaidsExchangeBot'))
async def cmd(e):
    global target_bin, target_bal, wait_seconds, is_attacking, stop_flag
    t = e.raw_text.lower().strip()
    if t.startswith("buy"):
        try:
            _, b, bal, w = t.split()
            target_bin, target_bal, wait_seconds = b, bal, int(w)
            stop_flag = False
            print(f"{G}🎯 TARGET LOCKED: {b} | Bal: {bal}{W}")
        except: print(f"{R}❌ Error! Correct: buy bin bal wait{W}")
    elif t == "confirm":
        print(f"{Y}⏳ Waiting {wait_seconds}s for Refresh...{W}")
        await asyncio.sleep(wait_seconds)
        is_attacking = True
        print(f"{R}🚀 ENGINE ACTIVATED!{W}")

@client.on(events.NewMessage(chats='XPrepaidsExchangeBot'))
@client.on(events.MessageEdited(chats='XPrepaidsExchangeBot'))
async def handler(e):
    global is_attacking
    if stop_flag or not is_attacking or not e.message.buttons: return
    if "Main Listings" not in e.message.text: return
    
    msg = e.message
    if not target_bin or not target_bal: return
    
    t_bin = target_bin.lower()
    target_balance = round(float(target_bal), 2)
    BAD = ["🅶", "🅿️", "🔄", "used", "relister"]
    btn_to_click = None

    # --- 🔥 ROW-BASED ACCURATE MATCHING ---
    for row in msg.buttons:
        for i, b in enumerate(row):
            txt = b.text.lower()
            if t_bin in txt:
                if any(x in txt for x in BAD): continue
                
                nums = [round(float(n), 2) for n in re.findall(r"\d+\.\d+", txt)]
                if any(abs(n - target_balance) <= 0.01 for n in nums):
                    print(f"{G}🎯 PERFECT MATCH: {b.text}{W}")
                    for pb in row:
                        if "purchase" in pb.text.lower():
                            btn_to_click = pb
                            break
                    if btn_to_click: break
        if btn_to_click: break

    # --- ⚡ INSTANT EXECUTION ---
    if btn_to_click:
        async with click_lock:
            print(f"{R}🔥 TARGET LOCKED! CLICKING...{W}")
            for _ in range(2):
                await btn_to_click.click()
                await asyncio.sleep(0.05) # Optimized Latency
        print(f"{G}✅ MISSION ACCOMPLISHED!{W}")
        is_attacking = False
    else:
        flat = [b for r in msg.buttons for b in r]
        next_btn = next((b for b in flat if any(k in b.text for k in ["Next", "▶️"])), None)
        if next_btn:
            await next_btn.click()
        else:
            ref = next((b for b in flat if any(k in b.text for k in ["Refresh", "🔄", "Reload"])), None)
            if ref: await ref.click()

async def main():
    await client.start()
    print(f"\n{G}🤖 X-Sniper v3.0 Master Engine is Online.{W}")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
