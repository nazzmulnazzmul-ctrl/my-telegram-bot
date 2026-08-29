import logging
import random
import json
import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

TOKEN = '8691358188:AAEX8tXrMfzYxu34QmHUCHyq7Y93x67gvwc'
NAGAD_NUMBER = '01903895955'

TELEGRAM_GROUP_LINK = 'https://t.me/+L7lcQOWFURY2Yjdl'
TELEGRAM_SUPPORT_LINK = 'https://t.me/+R4i0RKeXkR8zM2Zl'
WHATSAPP_REFER_LINK = 'https://chat.whatsapp.com/HdipEsS46HQ4efOR0jMRwj?s=cl&p=a&mlu=0'

DATA_FILE = 'users_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

user_data_db = load_data()

def get_user(user_id):
    str_id = str(user_id)
    if str_id not in user_data_db:
        user_data_db[str_id] = {
            "balance": 0.0,
            "completed_captchas": 0,
            "wrong_captchas": 0,
            "status": "Inactive",
            "current_captcha": None,
            "withdraw_step": False
        }
        save_data(user_data_db)
    return user_data_db[str_id]

def get_main_keyboard():
    keyboard = [
        [KeyboardButton("💵 Withdraw"), KeyboardButton("💸 Earn")],
        [KeyboardButton("🆔 Account"), KeyboardButton("🔗 Refer & Earn")],
        [KeyboardButton("👥 Group"), KeyboardButton("💬 Support & LIVE Chat")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ইনলাইন বাটন তৈরির ফাংশন (যেগুলো নিচে ক্লিক করার অপশন দেখাবে)
def get_inline_keyboard():
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw"), InlineKeyboardButton("💸 Earn", callback_data="earn")],
        [InlineKeyboardButton("🆔 Account", callback_data="account"), InlineKeyboardButton("🔗 Refer & Earn", callback_data="refer")],
        [InlineKeyboardButton("👥 Group", callback_data="group"), InlineKeyboardButton("💬 Support & LIVE Chat", callback_data="support")]
    ])
    return markup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id)
    
    welcome_text = (
        "🇷🇺 রাশিয়ার ২ ক্যাপচা ভেরিফাই আর্নিং সাইটে আপনাকে স্বাগতম 🇷🇺\n"
        "আপনি এখন থেকে যে ক্যাপচা টাইপ করে ইনকাম করবেন সেগুলো রাশিয়ার বিভিন্ন ওয়েবসাইটে ভেরিফাই করে ✅。\n\n"
        "এখন ইনকাম শুরু করতে চাইলে নিচের বাটনগুলোতে ক্লিক করুন 👇"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

# ইনলাইন বাটনে ক্লিক করলে রেসপন্স করার ফাংশন
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    u_data = get_user(user.id)
    data = query.data

    if data == "withdraw":
        u_data['current_captcha'] = None
        u_data['withdraw_step'] = True
        save_data(user_data_db)
        await query.message.reply_text("📱 **Type Your Number (Valid Number)** 👇", parse_mode='Markdown', reply_markup=get_main_keyboard())

    elif data == "earn":
        u_data['withdraw_step'] = False
        letters = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        numbers = "".join(random.choices("0123456789", k=2))
        captcha_code = letters + numbers
        u_data['current_captcha'] = captcha_code
        save_data(user_data_db)
        
        captcha_text = (
            f"💰 **Earn**\n\n"
            f"🔤 **Type The Captcha Text Here 👇**\n\n"
            f"👉 `{captcha_code}`\n\n"
            f"(এই লেখাটি হুবহু চ্যাটে টাইপ করে পাঠান)"
        )
        await query.message.reply_text(captcha_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

    elif data == "account":
        u_data['current_captcha'] = None
        u_data['withdraw_step'] = False
        save_data(user_data_db)
        account_text = (
            f"🆔 **User Id:** `{user.id}`\n"
            f"📍 **Location:** Bangladesh 🇧🇩\n"
            f"💰 **Balance:** {u_data['balance']} TK\n"
            f"👥 **Referrals:** 0\n"
            f"✅ **Total Complete Captchas:** {u_data['completed_captchas']}\n"
            f"❌ **Total Wrong Captchas:** {u_data['wrong_captchas']}\n\n"
            f"📌 **Status:** {u_data['status']} 🔴\n"
            f"💸 **Pay 1$ = 125 TK For Activation Fee**"
        )
        await query.message.reply_text(account_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

    elif data == "refer":
        refer_text = (
            f"🔗 **Your Refer & Earn:**\n\n"
            f"আপনার বন্ধুদের সাথে শেয়ার করুন:\n"
            f"{WHATSAPP_REFER_LINK}\n\n"
            f"🎁 **Per Refer Bonus: 20 TK**"
        )
        await query.message.reply_text(refer_text, reply_markup=get_main_keyboard())

    elif data == "group":
        group_text = (
            f"👥 **Join Our Official Group:**\n\n"
            f"সব ধরনের আপডেট ও পেমেন্ট প্রুফ পেতে জয়েন করুন:\n"
            f"{TELEGRAM_GROUP_LINK}"
        )
        await query.message.reply_text(group_text, reply_markup=get_main_keyboard())

    elif data == "support":
        support_text = (
            f"💬 **Support & LIVE Chat 🔴:**\n\n"
            f"যেকোনো সমস্যায় এডমিনের সাথে সরাসরি যোগাযোগ করুন:\n"
            f"{TELEGRAM_SUPPORT_LINK}"
        )
        await query.message.reply_text(support_text, reply_markup=get_main_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u_data = get_user(user.id)
    text = update.message.text.strip()

    if text == '/start':
        await start(update, context)
        return

    if text == "💸 Earn":
        u_data['withdraw_step'] = False
        letters = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        numbers = "".join(random.choices("0123456789", k=2))
        captcha_code = letters + numbers
        u_data['current_captcha'] = captcha_code
        save_data(user_data_db)
        
        captcha_text = (
            f"💰 **Earn**\n\n"
            f"🔤 **Type The Captcha Text Here 👇**\n\n"
            f"👉 `{captcha_code}`\n\n"
            f"(এই লেখাটি হুবহু চ্যাটে টাইপ করে পাঠান)"
        )
        await update.message.reply_text(captcha_text, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return

    if text == "💵 Withdraw":
        u_data['current_captcha'] = None
        u_data['withdraw_step'] = True
        save_data(user_data_db)
        await update.message.reply_text("📱 **Type Your Number (Valid Number)** 👇", reply_markup=get_main_keyboard(), parse_mode='Markdown')
        return

    if text == "🆔 Account":
        u_data['current_captcha'] = None
        u_data['withdraw_step'] = False
        save_data(user_data_db)
        account_text = (
            f"🆔 **User Id:** `{user.id}`\n"
            f"📍 **Location:** Bangladesh 🇧🇩\n"
            f"💰 **Balance:** {u_data['balance']} TK\n"
            f"👥 **Referrals:** 0\n"
            f"✅ **Total Complete Captchas:** {u_data['completed_captchas']}\n"
            f"❌ **Total Wrong Captchas:** {u_data['wrong_captchas']}\n\n"
            f"📌 **Status:** {u_data['status']} 🔴\n"
            f"💸 **Pay 1$ = 125 TK For Activation Fee**"
        )
        await update.message.reply_text(account_text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
        return

    if text == "🔗 Refer & Earn":
        refer_text = (
            f"🔗 **Your Refer & Earn:**\n\n"
            f"আপনার বন্ধুদের সাথে শেয়ার করুন:\n"
            f"{WHATSAPP_REFER_LINK}\n\n"
            f"🎁 **Per Refer Bonus: 20 TK**"
        )
        await update.message.reply_text(refer_text, reply_markup=get_main_keyboard())
        return

    if text == "👥 Group":
        group_text = (
            f"👥 **Join Our Official Group:**\n\n"
            f"সব ধরনের আপডেট ও পেমেন্ট প্রুফ পেতে জয়েন করুন:\n"
            f"{TELEGRAM_GROUP_LINK}"
        )
        await update.message.reply_text(group_text, reply_markup=get_main_keyboard())
        return

    if text == "💬 Support & LIVE Chat":
        support_text = (
            f"💬 **Support & LIVE Chat 🔴:**\n\n"
            f"যেকোনো সমস্যায় এডমিনের সাথে সরাসরি যোগাযোগ করুন:\n"
            f"{TELEGRAM_SUPPORT_LINK}"
        )
        await update.message.reply_text(support_text, reply_markup=get_main_keyboard())
        return

    if u_data.get('current_captcha'):
        if text == u_data['current_captcha']:
            u_data['completed_captchas'] += 1
            u_data['balance'] = float(u_data['balance']) + 2.0  
            u_data['current_captcha'] = None
            save_data(user_data_db)  
            
            await update.message.reply_text(
                f"✅ সঠিক হয়েছে! আপনার অ্যাকাউন্টে স্থায়ীভাবে ২ টাকা যোগ করা হয়েছে।\n"
                f"💰 বর্তমান মোট ব্যালেন্স: {u_data['balance']} TK",
                reply_markup=get_main_keyboard()
            )
        else:
            u_data['wrong_captchas'] += 1
            save_data(user_data_db)
            await update.message.reply_text("❌ ভুল ক্যাপচা কোড! আবার সঠিকভাবে চেষ্টা করুন।", reply_markup=get_main_keyboard())
        return

    if u_data.get('withdraw_step'):
        u_data['withdraw_step'] = False
        save_data(user_data_db)
        withdraw_msg = (
            f"❌ Withdraw Failed ❌\n\n"
            f"🚦 **Status:** Inactive 🔴\n"
            f"Account Active First 🟢\n\n"
            f"অ্যাকাউন্টটি একটিভ করতে নিচের নাম্বারে **১২৫ টাকা (১$)** সেন্ড মানি করুন:\n"
            f"নগদ (Personal): `{NAGAD_NUMBER}`\n\n"
            f"টাকা পাঠানোর পর স্ক্রিনশটটি সাপোর্টে প্রদান করুন।"
        )
        await update.message.reply_text(withdraw_msg, parse_mode='Markdown', reply_markup=get_main_keyboard())
        return

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print('Bot is running...')
    application.run_polling()

if __name__ == '__main__':
    main()
