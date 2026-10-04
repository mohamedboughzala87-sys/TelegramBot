from flask import Flask
from threading import Thread
import telebot
import sqlite3
import threading
import time
from telebot import types

# 1. إعداد Flask لإبقاء البوت حياً على منصة Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# 2. إعدادات البوت والبيانات الأساسية
TOKEN = "8794366009:AAFRtcM891gvxLkJgc39jwwrq6gSqWC9yFQ"
bot = telebot.TeleBot(TOKEN)

MY_USDT_WALLET = "TULQfGqF2AtB41ybkPbj7pvX8FBQpWfVLw"
ADMIN_ID = 58392019

# 3. قاموس اللغات الكامل المترجم
LOCALES = {}

LOCALES['ar'] = {
    'welcome': "✨ **منصة دعم القنوات العالمية** ✨\n\n🚀 طريقتك الأسرع لتكبير قناتك بأعضاء حقيقيين وتفاعل تلقائي.",
    'choose': "👇 اختر من القائمة أدناه:",
    'btn_promo': "💎 باقات الترويج السريع",
    'btn_guide': "📖 دليل الدفع المبسط",
    'btn_lang': "🌐 تغيير اللغة / Language",
    'pkg_title': "💎 **باقات النمو والتفاعل** 💎\n\n📌 اختر الباقة لتوليد الفاتورة فوراً:",
    'invoice': "┌─── ❖ ⚙️ **فـاتـورة ذكـيـة** ❖ ───┐\n\n🆔 **الطلب:** `#{order_id}`\n📦 **الخدمة:** {name}\n💰 **المبلغ:** `{price}$ USDT` *(TRC-20)*\n\n📥 **المحفظة:**\n`{wallet}`\n\n🔄 اضغط أدناه بعد التحويل للتفعيل فورا!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 تأكيد استلام الدفعة آلياً",
    'guide': "📖 **دليل الشراء:**\n1️⃣ افتح محفظتك الرقمية.\n2️⃣ أرسل USDT (TRC-20).\n3️⃣ انسخ عنوان البوت وأرسل المال."
}

LOCALES['en'] = {
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

LOCALES['fr'] = {
    'welcome': "✨ **Plateforme de Croissance Globale** ✨\n\n🚀 Boostez votre canal avec des membres réels.",
    'choose': "👇 Choisissez dans le menu:",
    'btn_promo': "💎 Packs de Promotion",
    'btn_guide': "📖 Guide de Paiement",
    'btn_lang': "🌐 Changer de Langue / اللغة",
    'pkg_title': "💎 **Packs de Croissance** 💎\n\n📌 Choisissez un pack pour générer une facture:",
    'invoice': "┌─── ❖ ⚙️ **FACTURE INTELLIGENTE** ❖ ───┐\n\n🆔 **ID Commande:** `#{order_id}`\n📦 **Service:** {name}\n💰 **Montant:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Adresse du Portefeuille:**\n`{wallet}`\n\n🔄 Appuyez ci-dessous après transfert pour activer!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 Vérifier Automatiquement",
    'guide': "📖 **Guide:**\n1️⃣ Ouvrez votre portefeuille crypto.\n2️⃣ Envoyez USDT (TRC-20).\n3️⃣ Copiez l'adresse du bot et transférez."
}

LOCALES['zh'] = {
    'welcome': "✨ **全球频道增长平台** ✨\n\n🚀 快速且安全地提升您的频道成员与互动。",
    'choose': "👇 从下方菜单选择：",
    'btn_promo': "💎 快速推广礼包",
    'btn_guide': "📖 简易支付指南",
    'btn_lang': "🌐 更改语言 / Language",
    'pkg_title': "💎 **增长礼包** 💎\n\n📌 选择礼包生成账单：",
    'invoice': "┌─── ❖ ⚙️ **智能账单** ❖ ───┐\n\n🆔 **订单号:** `#{order_id}`\n📦 **服务:** {name}\n💰 **金额:** `{price}$ USDT` *(TRC-20)*\n\n📥 **钱包地址:**\n`{wallet}`\n\n🔄 转账后点击下方按钮立即激活！\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 自动验证付款",
    'guide': "📖 **指南：**\n1️⃣ 打开去中心化钱包。\n2️⃣ 发送 USDT (TRC-20)。\n3️⃣ 复制机器人钱包地址并转账。"
}

LOCALES['ru'] = {
    'welcome': "✨ **Глобальная Платформа Роста Каналов** ✨\n\n🚀 Самый быстрый способ продвижения вашего канала с реальными участниками.",
    'choose': "👇 Выберите из меню ниже:",
    'btn_promo': "💎 Пакеты Продвижения",
    'btn_guide': "📖 Руководство по Оплате",
    'btn_lang': "🌐 Изменить язык / Language",
    'pkg_title': "💎 **Пакеты Роста** 💎\n\n📌 Выберите пакет для автосчета:",
    'invoice': "┌─── ❖ ⚙️ **УМНЫЙ СЧЕТ** ❖ ───┐\n\n🆔 **ID Заказа:** `#{order_id}`\n📦 **Услуга:** {name}\n💰 **К оплате:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Адрес кошелька:**\n`{wallet}`\n\n🔄 Нажмите кнопку ниже после перевода для активации!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 Проверить оплату",
    'guide': "📖 **Инструкция:**\n1️⃣ Откройте криптокошелек.\n2️⃣ Отправьте USDT (TRC-20).\n3️⃣ Скопируйте адрес кошелька бота."
}

LOCALES['tr'] = {
    'welcome': "✨ **Küresel Kanal Büyütme Platformu** ✨\n\n🚀 Kanalınızı gerçek üyelerle büyütmenin en hızlı yolu.",
    'choose': "👇 Aşağıdaki menüden seçim yapın:",
    'btn_promo': "💎 Paket Tanıtımları",
    'btn_guide': "📖 Basit Ödeme Kılavuzu",
    'btn_lang': "🌐 Dili Değiştir / Language",
    'pkg_title': "💎 **Büyüme Paketleri** 💎\n\n📌 Fatura oluşturmak için bir paket seçin:",
    'invoice': "┌─── ❖ ⚙️ **AKILLI FATURA** ❖ ───┐\n\n🆔 **Sipariş No:** `#{order_id}`\n📦 **Hizmet:** {name}\n💰 **Tutar:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Cüzdan Adresi:**\n`{wallet}`\n\n🔄 Etkinleştirmek için transferden sonra aşağıya basın!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 Ödemeyi Otomatik Doğrula",
    'guide': "📖 **Kılavuz:**\n1️⃣ Kripto cüzdanınızı açın.\n2️⃣ USDT (TRC-20) gönderin.\n3️⃣ Bot cüzdan adresini kopyalayıp gönderin."
}

# 4. إعدادات قاعدة البيانات
def init_db():
    conn = sqlite3.connect("perfect_global.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA auto_vacuum = FULL;")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, buyer_id INTEGER, package_id TEXT, price REAL, timestamp INTEGER, status TEXT DEFAULT 'pending');")
    conn.commit()
    conn.close()

def get_user_lang(user_id):
    try:
        conn = sqlite3.connect("perfect_global.db")
        cursor = conn.cursor()
        cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'ar'
    except:
        return 'ar'

def set_user_lang(user_id, lang):
    conn = sqlite3.connect("perfect_global.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang))
    conn.commit()
    conn.close()

# 5. دالة بناء القائمة الرئيسية حسب لغة المستخدم
def get_main_menu(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    texts = LOCALES.get(lang, LOCALES['ar'])
    markup.add(types.KeyboardButton(texts['btn_promo']))
    markup.add(types.KeyboardButton(texts['btn_guide']), types.KeyboardButton(texts['btn_lang']))
    return markup

# 6. معالجة أمر البداية /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    init_db()
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    
    texts = LOCALES.get(lang, LOCALES['ar'])
    bot.reply_to(message, f"{texts['welcome']}\n\n{texts['choose']}", reply_markup=get_main_menu(lang), parse_mode="Markdown")

# 7. استقبال النصوص وضغطات الأزرار العادية
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    texts = LOCALES.get(lang, LOCALES['ar'])
    
    # إذا ضغط المستخدم على زر الدليل المبسط
    if message.text == texts['btn_guide']:
        bot.reply_to(message, texts['guide'], parse_mode="Markdown")
        
    # إذا ضغط المستخدم على زر تغيير اللغة
    elif message.text == texts['btn_lang']:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("العربية 🇹🇳", callback_data="set_lang_ar"),
            types.InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"),
            types.InlineKeyboardButton("Français 🇫🇷", callback_data="set_lang_fr"),
            types.InlineKeyboardButton("中文 🇨🇳", callback_data="set_lang_zh"),
            types.InlineKeyboardButton("Русский 🇷🇺", callback_data="set_lang_ru"),
            types.InlineKeyboardButton("Türkçe 🇹🇷", callback_data="set_lang_tr")
        )
        bot.reply_to(message, "🌐 Choose your preferred language / اختر لغتك المفضلة:", reply_markup=markup)

# 8. استقبال خيارات الأزرار المضمنة (Inline Buttons) لتغيير اللغة
@bot.callback_query_handler(func=lambda call: call.data.startswith('set_lang_'))
def callback_language(call):
    user_id = call.from_user.id
    new_lang = call.data.replace('set_lang_', '')
    
    set_user_lang(user_id, new_lang)
    
    # تحديث النص للمستخدم بعد تغيير اللغة بنجاح
    texts = LOCALES.get(new_lang, LOCALES['ar'])
    bot.answer_callback_query(call.id, "✅ Done / تم التحديث")
    bot.send_message(call.message.chat.id, f"✅ {texts['welcome']}\n\n{texts['choose']}", reply_markup=get_main_menu(new_lang), parse_mode="Markdown")

# 9. تشغيل البوت بشكل لانهائي ومستمر
bot.infinity_polling()
