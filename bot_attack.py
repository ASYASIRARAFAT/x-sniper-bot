import asyncio, random, hashlib, sys, os, requests, re
from telethon import TelegramClient, events, errors

# --- 🎨 ANSI কালার প্যালেট ---
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
{Y}         [+] Version: 3.0 | Master Precision [+]
{G}         [+] Developer: ASYASIRARAFAT           [+]
{C}============================================================={W}""")

def show_menu():
    print(f"{G}[ 1 ] {W}Start Sniper Attack\n{G}[ 2 ] {W}Check HWID\n{G}[ 3 ] {W}Update Tool\n{R}[ X ] {W}Exit")
    print(f"{C}-------------------------------------------------------------{W}")

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
    print(f"{Y}🔍 ভেরিফাই করা হচ্ছে...{W}\n🔑 HWID: {uid}")
    try:
        res = requests.get(RAW_LINK, timeout=10).text
        if uid in res:
            print(f"{G}✅ Access Granted!{W}")
            show_menu()
            opt = input(f"{C}root@x-sniper:~# {W}")
            if opt == '1': return True
            else: sys.exit()
        else:
            print(f"{R}❌ Access Denied!{W}\nID: {uid}")
            sys.exit()
    except: sys.exit()

if not verify(): sys.exit()

# --- ⚙️ ইঞ্জিন সেটআপ ---
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
            print(f"{G}🎯 Target Set: {b} | {bal}{W}")
        except: print(f"{R}Error: buy bin bal wait{W}")
    elif t == "confirm":
        print(f"{Y}⏳ Waiting {wait_seconds}s...{W}")
        await asyncio.sleep(wait_seconds)
        is_attacking = True
        print(f"{R}🚀 ATTACK STARTED!{W}")

@client.on(events.NewMessage(chats='XPrepaidsExchangeBot'))
@client.on(events.MessageEdited(chats='XPrepaidsExchangeBot'))
async def handler(e):
    global is_attacking
    if stop_flag or not is_attacking or not e.message.buttons: return
    if "Main Listings" not in e.message.text and "Total Cards" not in e.message.text: return
    
    msg = e.message
    if not target_bin or not target_bal: return
    
    t_bin = target_bin.lower()
    target_balance = round(float(target_bal), 2)
    BAD = ["🅶", "🅿️", "🔄", "used", "relister"]
    btn_to_click = None

    # --- 🔥 ROW-BASED LASER MATCHING (100% Safe) ---
    for row in msg.buttons:
        # বর্তমান Row-এর সব টেক্সট চেক করা
        for i, b in enumerate(row):
            txt = b.text.lower()
            
            if t_bin in txt:
                if any(x in txt for x in BAD): continue
                
                # ব্যালেন্স ম্যাচিং
                nums = [round(float(n), 2) for n in re.findall(r"\d+\.\d+", txt)]
                if any(abs(n - target_balance) <= 0.01 for n in nums):
                    print(f"{G}🎯 PERFECT ROW MATCH: {b.text}{W}")
                    
                    # ওই একই Row-তে Purchase বাটন খোঁজা
                    for pb in row:
                        if "purchase" in pb.text.lower():
                            btn_to_click = pb
                            break
                    if btn_to_click: break
        if btn_to_click: break

    # --- ⚡ EXECUTION ---
    if btn_to_click:
        async with click_lock:
            print(f"{R}🔥 TARGET LOCKED!{W}")
            for _ in range(2):
                await btn_to_click.click()
                await asyncio.sleep(0.1)
        print(f"{G}✅ SUCCESS!{W}")
        is_attacking = False
    else:
        # নেভিগেশন ও রিফ্রেশ
        flat = [b for r in msg.buttons for b in r]
        next_btn = next((b for b in flat if "Next" in b.text or "▶️" in b.text), None)
        if next_btn:
            print(f"{C}⏭️ Next Page...{W}")
            await next_btn.click()
        else:
            ref = next((b for b in flat if any(k in b.text for k in ["Refresh", "🔄", "Reload"])), None)
            if ref: 
                await asyncio.sleep(random.uniform(0.1, 0.3))
                await ref.click()

async def main():
    await client.start()
    print(f"{G}🤖 Sniper v3.0 Master Engine Live.{W}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
