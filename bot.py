from flask import Flask
from threading import Thread
import telebot
import sqlite3
import time
import requests
from telebot import types

app = Flask('')
@app.route('/')
def home(): return "Bot is alive and checking payments!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()
keep_alive()

# إعدادات البوت الأساسية
TOKEN = "8794366009:AAFRtcM891gvxLkJgc39jwwrq6gSqWC9yFQ"
bot = telebot.TeleBot(TOKEN)
MY_USDT_WALLET = "TULQfGqF2AtB41ybkPbj7pvX8FBQpWfVLw"
ADMIN_ID = 58392019

LOCALES = {
    'ar': {
        'welcome': "✨ **منصة دعم القنوات العالمية** ✨\n\n🚀 طريقتك الأسرع لتكبير قناتك بأعضاء حقيقيين وتفاعل تلقائي.",
        'choose': "👇 اختر من القائمة أدناه:",
        'btn_promo': "💎 باقات الترويج السريع",
        'btn_guide': "📖 دليل الدفع المبسط",
        'btn_lang': "🌐 تغيير اللغة / Language",
        'pkg_title': "💎 **باقات النمو والتفاعل** 💎\n\n📌 اختر الباقة لتوليد الفاتورة فوراً:",
        'invoice': "┌─── ❖ ⚙️ **فـاتـورة ذكـيـة** ❖ ───┐\n\n🆔 **الطلب:** `#{order_id}`\n📦 **الخدمة:** {name}\n💰 **المبلغ:** `{price}$ USDT` *(TRC-20)*\n\n📥 **المحفظة:**\n`{wallet}`\n\n🔄 اضغط أدناه بعد التحويل للتفعيل فورا!\n└───❖───✦───❖───┘",
        'btn_verify': "🔄 تأكيد استلام الدفعة آلياً",
        'guide': "📖 **دليل الشراء:**\n1️⃣ افتح محفظتك الرقمية.\n2️⃣ أرسل USDT (TRC-20).\n3️⃣ انسخ عنوان البوت وأرسل المال."
    },
    'en': {
        'welcome': "✨ **Global Channel Growth Platform** ✨\n\n🚀 Your fastest way to boost your channel with real members.",
        'choose': "👇 Choose from the menu below:",
        'btn_promo': "💎 Promotion Packages",
        'btn_guide': "📖 Payment Guide",
        'btn_lang': "🌐 Change Language / اللغة",
        'pkg_title': "💎 **Growth Packages** 💎\n\n📌 Choose a package to generate an invoice:",
        'invoice': "┌─── ❖ ⚙️ **SMART INVOICE** ❖ ───┐\n\n🆔 **Order ID:** `#{order_id}`\n📦 **Service:** {name}\n💰 **Amount:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Wallet Address:**\n`{wallet}`\n\n🔄 Press below after transferring to activate!\n└───❖───✦───❖───┘",
        'btn_verify': "🔄 Verify Payment Automatically",
        'guide': "📖 **Guide:**\n1️⃣ Open your crypto wallet.\n2️⃣ Send USDT (TRC-20).\n3️⃣ Copy bot wallet and transfer."
    }
}

PACKAGES = {
    '1': {'name': "باقة الأفراد (200 مشترك)", 'price': 5.0},
    '2': {'name': "باقة الشركات (2000 مشترك)", 'price': 45.0}
}

def init_db():
    conn = sqlite3.connect("perfect_global.db"); cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, buyer_id INTEGER, package_id TEXT, price REAL, timestamp INTEGER, status TEXT DEFAULT 'pending');")
    conn.commit(); conn.close()

def get_user_lang(user_id):
    try:
        conn = sqlite3.connect("perfect_global.db"); cursor = conn.cursor()
        cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone(); conn.close()
        return result if result else 'ar'
    except: return 'ar'

def set_user_lang(user_id, lang):
    conn = sqlite3.connect("perfect_global.db"); cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang))
    conn.commit(); conn.close()

def create_order(buyer_id, package_id, price):
    conn = sqlite3.connect("perfect_global.db"); cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (buyer_id, package_id, price, timestamp) VALUES (?, ?, ?, ?)", (buyer_id, package_id, price, int(time.time())))
    order_id = cursor.lastrowid
    conn.commit(); conn.close()
    return order_id

def get_order(order_id):
    conn = sqlite3.connect("perfect_global.db"); cursor = conn.cursor()
    cursor.execute("SELECT buyer_id, package_id, price, status FROM orders WHERE order_id = ?", (order_id,))
    result = cursor.fetchone(); conn.close()
    return result

def update_order_status(order_id, status):
    conn = sqlite3.connect("perfect_global.db"); cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id))
    conn.commit(); conn.close()

# 🔍 دالة فحص شبكة البلوكشين تلقائياً للتحقق من وصول الـ USDT
def check_blockchain_payment(wallet, expected_amount):
    try:
        url = f"https://trongrid.io{wallet}/transactions/trc20"
        response = requests.get(url, timeout=10).json()
        if "data" in response:
            for tx in response["data"]:
                # التحقق من أن العملة هي USDT (عقد عملة USDT على شبكة ترون)
                if tx["token_info"]["symbol"] == "USDT":
                    amount = float(tx["value"]) / (10 ** tx["token_info"]["decimals"])
                    tx_time = tx["block_timestamp"] / 1000
                    
                    # إذا وصلت دفعة تطابق السعر المطلوب في آخر 30 دقيقة
                    if abs(amount - expected_amount) < 0.1 and (time.time() - tx_time) < 1800:
                        return True
        return False
    except:
        return False

def get_main_menu(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    texts = LOCALES.get(lang, LOCALES['ar'])
    markup.add(types.KeyboardButton(texts['btn_promo']))
    markup.add(types.KeyboardButton(texts['btn_guide']), types.KeyboardButton(texts['btn_lang']))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    init_db()
    user_id = message.from_user.id; lang = get_user_lang(user_id)
    texts = LOCALES.get(lang, LOCALES['ar'])
    bot.reply_to(message, f"{texts['welcome']}\n\n{texts['choose']}", reply_markup=get_main_menu(lang), parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_id = message.from_user.id; lang = get_user_lang(user_id)
    texts = LOCALES.get(lang, LOCALES['ar'])
    
    if message.text == texts['btn_guide']:
        bot.reply_to(message, texts['guide'], parse_mode="Markdown")
        
    elif message.text == texts['btn_promo']:
        markup = types.InlineKeyboardMarkup()
        for pkg_id, pkg in PACKAGES.items():
            markup.add(types.InlineKeyboardButton(f"{pkg['name']} - {pkg['price']}\$", callback_data=f"buy_{pkg_id}"))
        bot.reply_to(message, texts['pkg_title'], reply_markup=markup, parse_mode="Markdown")
        
    elif message.text == texts['btn_lang']:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(*(types.InlineKeyboardButton(name, callback_data=f"set_lang_{code}") for code, name in [
            ('ar', "العربية 🇹🇳"), ('en', "English 🇬🇧")]))
        bot.reply_to(message, "🌐 Choose your language / اختر لغتك:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def callback_buy(call):
    user_id = call.from_user.id; lang = get_user_lang(user_id); texts = LOCALES.get(lang, LOCALES['ar'])
    pkg_id = call.data.replace('buy_', '')
    pkg = PACKAGES.get(pkg_id)
    
    if pkg:
        order_id = create_order(user_id, pkg_id, pkg['price'])
        invoice_text = texts['invoice'].format(order_id=order_id, name=pkg['name'], price=pkg['price'], wallet=MY_USDT_WALLET)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(texts['btn_verify'], callback_data=f"verify_{order_id}"))
        bot.send_message(call.message.chat.id, invoice_text, reply_markup=markup, parse_mode="Markdown")

# 🔄 معالجة الضغط على زر "تأكيد استلام الدفعة آلياً"
@bot.callback_query_handler(func=lambda call: call.data.startswith('verify_'))
def callback_verify(call):
    order_id = call.data.replace('verify_', '')
    order = get_order(order_id)
    
    if order:
        buyer_id, package_id, price, status = order
        
        if status == 'completed':
            bot.answer_callback_query(call.id, "✅ هذا الطلب مفعل ومكتمل سابقاً!")
            return
            
        bot.answer_callback_query(call.id, "🔍 جاري فحص شبكة البلوكشين... انتظر لحظة")
        
        # استدعاء دالة الفحص الآلي
        is_paid = check_blockchain_payment(MY_USDT_WALLET, price)
        
        if is_paid:
            update_order_status(order_id, 'completed')
            bot.send_message(call.message.chat.id, f"🎉 **تم تأكيد الدفع بنجاح!**\n\nجاري تجهيز طلبك رقم `#{order_id}` تلقائياً وسيتم إرسال المشتركين لقناتك فوراً.")
            # إشعار للمشرف (أنت) بوصول أموال جديدة
            bot.send_message(ADMIN_ID, f"💰 **إشعار دفع آلي جديد:**\nالزبون: `{buyer_id}` قام بدفع `{price}$ USDT` للطلب `#{order_id}`.")
        else:
            bot.send_message(call.message.chat.id, "❌ **لم نكتشف أي تحويل جديد بهذه القيمة حتى الآن.**\n\nتأكد من إرسال المبلغ الصحيح وانتظر دقيقة ثم اضغط على الزر مرة أخرى.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_lang_'))
def callback_language(call):
    user_id = call.from_user.id; new_lang = call.data.replace('set_lang_', '')
    set_user_lang(user_id, new_lang); texts = LOCALES.get(new_lang, LOCALES['ar'])
    bot.answer_callback_query(call.id, "✅")
    bot.send_message(call.message.chat.id, f"✅ {texts['welcome']}\n\n{texts['choose']}", reply_markup=get_main_menu(new_lang), parse_mode="Markdown")

bot.infinity_polling()
