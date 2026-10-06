from flask import Flask
from threading import Thread
from database import init_db

app = Flask('')

@app.route('/')
def home(): 
    return "Bot is alive and checking payments!"

def run(): 
    app.run(host='0.0.0.0', port=8080)

def keep_alive(): 
    Thread(target=run).start()

if __name__ == "__main__":
    init_db()  # تهيئة قاعدة البيانات عند الإقلاع
    keep_alive()
    
    # تشغيل نواة البوت
    from bot_core import bot
    print("Bot is starting...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
import sqlite3

DB_NAME = 'bot_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, pkg_id TEXT, amount REAL, status TEXT)')
    conn.commit()
    conn.close()

def get_lang(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT lang FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 'en'

def set_lang(user_id, lang):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (user_id, lang) VALUES (?, ?)', (user_id, lang))
    conn.commit()
    conn.close()

def create_order(user_id, pkg_id, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (user_id, pkg_id, amount, status) VALUES (?, ?, ?, ?)', (user_id, pkg_id, amount, 'pending'))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def get_order(order_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, amount, status FROM orders WHERE order_id = ?', (order_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def mark_order_paid(order_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET status = ? WHERE order_id = ?', ('paid', order_id))
    conn.commit()
    conn.close()
TOKEN = "8794366009:AAFRtcM891gvxLkJgc39jwwrq6gSqWC9yFQ"
MY_USDT_WALLET = "TULQfGqF2AtB41ybkPbj7pvX8FBQpWfVLw"
ADMIN_ID = 58392019

PACKAGES = [
    {"id": "pkg_1", "name": "Basic Promotion (1000 members)", "price": 10},
    {"id": "pkg_2", "name": "Silver Growth (2500 members)", "price": 20},
    {"id": "pkg_3", "name": "Gold VIP (5000 members)", "price": 35}
]

LOCALES = {
    'ar': {'welcome': "✨ **منصة دعم القنوات العالمية** ✨\n\n🚀 طريقتك الأسرع لتكبير قناتك بأعضاء حقيقيين وتفاعل تلقائي.", 'choose': "👇 اختر من القائمة أدناه:", 'btn_promo': "💎 باقات الترويج السريع", 'btn_guide': "📖 دليل الدفع المبسط", 'btn_lang': "🌐 تغيير اللغة / Language", 'pkg_title': "💎 **باقات النمو والتفاعل** 💎\n\n📌 اختر الباقة لتوليد الفاتورة فوراً:", 'invoice': "┌─── ❖ ⚙️ **فـاتـورة ذكـيـة** ❖ ───┐\n\n🆔 **الطلب:** `#{order_id}`\n📦 **الخدمة:** {name}\n💰 **المبلغ:** `{price}$ USDT` *(TRC-20)*\n\n📥 **المحفظة:**\n`{wallet}`\n\n🔄 اضغط أدناه بعد التحويل للتفعيل فورا!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 تأكيد استلام الدفعة آلياً", 'guide': "📖 **دليل الشراء:**\n1️⃣ افتح محفظتك الرقمية.\n2️⃣ أرسل USDT (TRC-20).\n3️⃣ انسخ عنوان البوت وأرسل المال."},
    'en': {'welcome': "✨ **Global Channel Growth Platform** ✨\n\n🚀 Your fastest way to boost your channel with real members.", 'choose': "👇 Choose from the menu below:", 'btn_promo': "💎 Promotion Packages", 'btn_guide': "📖 Payment Guide", 'btn_lang': "🌐 Change Language / Language", 'pkg_title': "💎 **Growth Packages** 💎\n\n📌 Choose a package to generate an invoice:", 'invoice': "┌─── ❖ ⚙️ **SMART INVOICE** ❖ ───┐\n\n🆔 **Order ID:** `#{order_id}`\n📦 **Service:** {name}\n💰 **Amount:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Wallet Address:**\n`{wallet}`\n\n🔄 Press below after transferring to activate!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Verify Payment Automatically", 'guide': "📖 **Guide:**\n1️⃣ Open your crypto wallet.\n2️⃣ Send USDT (TRC-20).\n3️⃣ Copy bot wallet and transfer."},
    'fr': {'welcome': "✨ **Plateforme de Croissance Globale** ✨\n\n🚀 Boostez votre canal avec des membres réels.", 'choose': "👇 Choisissez dans le menu:", 'btn_promo': "💎 Packs de Promotion", 'btn_guide': "📖 Guide de Paiement", 'btn_lang': "🌐 Changer de Langue / Ligue", 'pkg_title': "💎 **Packs de Croissance** 💎\n\n📌 Choisissez un pack pour générer uma facture:", 'invoice': "┌─── ❖ ⚙️ **FACTURE INTELLIGENTE** ❖ ───┐\n\n🆔 **ID Commande:** `#{order_id}`\n📦 **Service:** {name}\n💰 **Montant:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Adresse du Portefeuille:**\n`{wallet}`\n\n🔄 Appuyez ci-dessous après transfert pour activer!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Vérifier Automatiquement", 'guide': "📖 **Guide:**\n1️⃣ Ouvrez votre portefeuille crypto.\n2️⃣ Envoyez USDT (TRC-20).\n3️⃣ Copiez l'adresse du bot et transférez."},
    'zh': {'welcome': "✨ **全球频道增长平台** ✨\n\n🚀 快速且安全地提升您的频道成员与互动。", 'choose': "👇 从下方菜单选择：", 'btn_promo': "💎 快速推广礼包", 'btn_guide': "📖 简易支付指南", 'btn_lang': "🌐 更改语言 / Language", 'pkg_title': "💎 **增长礼包** 💎\n\n📌 选择礼包生成账单：", 'invoice': "┌─── ❖ ⚙️ **智能账单** ❖ ───┐\n\n🆔 **订单号:** `#{order_id}`\n📦 **服务:** {name}\n💰 **金额:** `{price}$ USDT` *(TRC-20)*\n\n📥 **钱包地址:**\n`{wallet}`\n\n🔄 转账后点击下方按钮立即激活！\n└───❖───✦───❖───┘", 'btn_verify': "🔄 自动验证付款", 'guide': "📖 **指南：**\n1️⃣ 打开去中心化钱包。\n2️⃣ 发送 USDT (TRC-20)。\n3️⃣ 复制机器人钱包地址并转账。"},
    'ru': {'welcome': "✨ **Глобальная Платформа Роста Каналов** ✨\n\n🚀 Самый быстрый способ продвижения вашего канала с реальными участниками.", 'choose': "👇 Выберите из меню ниже:", 'btn_promo': "💎 Пакеты Продвижения", 'btn_guide': "📖 Руководство по Оплате", 'btn_lang': "🌐 Изменить язык / Language", 'pkg_title': "💎 **Пакеты Роста** 💎\n\n📌 Выберите пакет для автосчета:", 'invoice': "┌─── ❖ ⚙️ **УМНЫЙ СЧЕТ** ❖ ───┐\n\n🆔 **ID Заказа:** `#{order_id}`\n📦 **Услуга:** {name}\n💰 **К оплате:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Адрес кошелька:**\n`{wallet}`\n\n🔄 Нажмите кнопку ниже после перевода для активации!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Проверить оплату", 'guide': "📖 **Инструкция:**\n1️⃣ Откройте криптокошелек.\n2️⃣ Отправьте USDT (TRC-20).\n3️⃣ Скопируйте адрес кошелька бота."},
    'hi': {'welcome': "✨ **ग्लोबल चैनल Growth प्लेटफॉर्म** ✨\n\n🚀 वास्तविक सदस्यों के साथ अपने चैनल को बढ़ावा देने का सबसे तेज़ तरीका।", 'choose': "👇 नीचे दिए गए मेनू से चुनें:", 'btn_promo': "💎 प्रमोशन पैकेज", 'btn_guide': "📖 भुगतान गाइड", 'btn_lang': "🌐 भाषा बदलें / Language", 'pkg_title': "💎 **ग्रोथ पैकेज** 💎\n\n📌 चालान जेनरेट करने के लिए पैकेज चुनें:", 'invoice': "┌─── ❖ ⚙️ **स्मार्ट चालान** ❖ ───────┐\n\n🆔 **ऑर्डर आईडी:** `#{order_id}`\n📦 **सेवा:** {name}\n💰 **देय राशि:** `{price}$ USDT` *(TRC-20)*\n\n📥 **क्रिप्टο वॉलेट पता:**\n`{wallet}`\n\n🔄 ट्रांसफर के बाद सक्रिय करने के लिए नीचे दबाएं!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 भुगतान स्वचालित सत्यापित करें", 'guide': "📖 **गाイド:**\n1️⃣ अपना क्रिप्टो वॉलेट खोलें।\n2️⃣ USDT (TRC-20) भेजें।\n3️⃣ बॉट का वॉलेट पता कॉपी करके फंड भेजें।"},
    'fa': {'welcome': "✨ **پلتفرم جهانی رشد کانال** ✨\n\n🚀 سريع‌ترین راه برای افزایش اعضای واقعی کانال شما.", 'choose': "👇 از منوی زیر انتخاب کنید:", 'btn_promo': "💎 پکیج‌های ارتقا", 'btn_guide': "📖 راهنمای پرداخت", 'btn_lang': "🌐 تغییر زبان / Language", 'pkg_title': "💎 **پکیج‌های رشد** 💎\n\n📌 پکیج مورد نظر را برای صدور فاکتور انتخاب کنید:", 'invoice': "┌─── ❖ ⚙️ **فاکتور هوشمند** ❖ ───────┐\n\n🆔 **شماره سفارش:** `#{order_id}`\n📦 **خدمات:** {name}\n💰 **مبلغ:** `{price}$ USDT` *(TRC-20)*\n\n📥 **آدرس ولت:**\n`{wallet}`\n\n🔄 پس از انتقال، برای فعال‌سازی دکمه زیر را فشار دهید!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 تایید خودکار پرداخت", 'guide': "📖 **راهنما:**\n1️⃣ ولت کریپتو خود را باز کنید.\n2️⃣ ارز USDT (TRC-20) ارسال کنید.\n3️⃣ آدرس ولت بات را کپی کرده و وجه را ارسال کنید."},
    'es': {'welcome': "✨ **Plataforma Global de Crecimiento de Canales** ✨\n\n🚀 Tu forma más rápida de potenciar tu canal مع أعضاء حقيقيين.", 'choose': "👇 Elige del menú de abajo:", 'btn_promo': "💎 Paquetes de Promoción", 'btn_guide': "📖 Guide de Pago", 'btn_lang': "🌐 Cambiar Idioma / Language", 'pkg_title': "💎 **Paquetes de Crecimiento** 💎\n\n📌 Elige un paquete para generar una factura:", 'invoice': "┌─── ❖ ⚙️ **FACTURA INTELIGENTE** ❖ ───┐\n\n🆔 **ID de Orden:** `#{order_id}`\n📦 **Servicio:** {name}\n💰 **Monto:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Dirección de Billetera:**\n`{wallet}`\n\n🔄 ¡Presiona abajo después de transferir para activar!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Verificar Pago Automáticamente", 'guide': "📖 **Guía:**\n1️⃣ Abre tu billetera cripto.\n2️⃣ Envía USDT (TRC-20).\n3️⃣ Copia la dirección del bot y envía los funds."},
    'pt': {'welcome': "✨ **Plataforma Global de Crescimento de Canais** ✨\n\n🚀 A sua forma mais rápida de impulsionar o seu canal com membros reais.", 'choose': "👇 Escolha no menu abaixo:", 'btn_promo': "💎 Pacotes de Promoção", 'btn_guide': "📖 Guia de Pagamento", 'btn_lang': "🌐 Mudar Idioma / Language", 'pkg_title': "💎 **Pacotes de Crescimento** 💎\n\n📌 Escolha um pacote para gerar uma fatura:", 'invoice': "┌─── ❖ ⚙️ **FATURA INTELLIGENTE** ❖ ───┐\n\n🆔 **ID do Pedido:** `#{order_id}`\n📦 **Serviço:** {name}\n💰 **Valor:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Endereço da Carteira:**\n`{wallet}`\n\n🔄 Pressione abaixo após transferir para activar o seu pacote!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Verificar Pagamento", 'guide': "📖 **Guide:**\n1️⃣ Abra a sua carteira cripto.\n2️⃣ Envie USDT (TRC-20).\n3️⃣ Copie o endereço do bot."},
    'tr': {'welcome': "✨ **Küresel Kanal Büyütme Platformu** ✨\n\n🚀 Kanalınızı gerçek üyelerle büyütmenin en hızlı yolu.", 'choose': "👇 Aşağıdaki menüden seçim yapın:", 'btn_promo': "💎 Paket Tanıtımları", 'btn_guide': "📖 Basit Ödeme Kılavuzu", 'btn_lang': "🌐 Dili Değiştir / Language", 'pkg_title': "💎 **Büyüme Paketleri** 💎\n\n📌 Fatura oluşturmak için bir paket seçin:", 'invoice': "┌─── ❖ ⚙️ **AKILLI FATURA** ❖ ───┐\n\n🆔 **Sipariş ID:** `#{order_id}`\n📦 **Hizmet:** {name}\n💰 **Miktar:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Cüzdan Adresi:**\n`{wallet}`\n\n🔄 Etkinleştirmek için transferden sonra aşağıya basın!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Ödemeyi Otomatik Doğrula", 'guide': "📖 **Kılavuz:**\n1️⃣ Kripto cüzdanınızı açın.\n2️⃣ USDT (TRC-20) gönderin.\n3️⃣ Bot cüzdanını kopyalayın ve transfer edin."}
}
import telebot
import requests
from telebot import types
import database as db
import locales as lc

bot = telebot.TeleBot(lc.TOKEN)

def main_menu(user_id):
    lang = db.get_lang(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton(lc.LOCALES[lang]['btn_promo']), types.KeyboardButton(lc.LOCALES[lang]['btn_guide']))
    markup.add(types.KeyboardButton(lc.LOCALES[lang]['btn_lang']))
    return markup

def lang_menu():
    markup = types.InlineKeyboardMarkup(row_width=3)
    btns = [types.InlineKeyboardButton(text=l.upper(), callback_data=f"setlang_{l}") for l in lc.LOCALES.keys()]
    markup.add(*btns)
    return markup

def packages_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for pkg in lc.PACKAGES:
        markup.add(types.InlineKeyboardButton(text=f"{pkg['name']} - {pkg['price']}\$", callback_data=f"buy_{pkg['id']}"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "🌐 Choose your language / اختر لغتك الأساسية:", reply_markup=lang_menu())

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    text = message.text

    if text == lc.LOCALES[lang]['btn_promo']:
        bot.send_message(user_id, lc.LOCALES[lang]['pkg_title'], reply_markup=packages_menu())
    elif text == lc.LOCALES[lang]['btn_guide']:
        bot.send_message(user_id, lc.LOCALES[lang]['guide'], parse_mode="Markdown")
    elif text == lc.LOCALES[lang]['btn_lang']:
        bot.send_message(user_id, "🌐 Select Language:", reply_markup=lang_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    data = call.data

    if data.startswith("setlang_"):
        lang = data.split("_")[1]
        db.set_lang(user_id, lang)
        bot.answer_callback_query(call.id, "Language updated!")
        bot.send_message(user_id, f"{lc.LOCALES[lang]['welcome']}\n\n{lc.LOCALES[lang]['choose']}", reply_markup=main_menu(user_id), parse_mode="Markdown")

    elif data.startswith("buy_"):
        pkg_id = data.split("_")[1]
        pkg = next((p for p in lc.PACKAGES if p['id'] == pkg_id), None)
        if pkg:
            order_id = db.create_order(user_id, pkg_id, pkg['price'])
            lang = db.get_lang(user_id)
            inv_text = lc.LOCALES[lang]['invoice'].format(order_id=order_id, name=pkg['name'], price=pkg['price'], wallet=lc.MY_USDT_WALLET)
            
            verify_markup = types.InlineKeyboardMarkup()
            verify_markup.add(types.InlineKeyboardButton(text=lc.LOCALES[lang]['btn_verify'], callback_data=f"verify_{order_id}"))
            bot.send_message(user_id, inv_text, reply_markup=verify_markup, parse_mode="Markdown")

    elif data.startswith("verify_"):
        order_id = int(data.split("_")[1])
        order = db.get_order(order_id)
        
        if not order or order[2] == 'paid':
            bot.answer_callback_query(call.id, "Processed or not found.")
            return

        user_id, amount, status = order
        lang = db.get_lang(user_id)

        try:
            url = f"https://trongrid.io{lc.MY_USDT_WALLET}/transactions/trc20"
            res = requests.get(url, params={"only_confirmed": "true", "limit": 10}).json()
            is_paid = False
            for tx in res.get('data', []):
                if tx.get('token_info', {}).get('symbol') == 'USDT':
                    tx_amount = float(tx.get('value')) / 1_000_000
                    if abs(tx_amount - amount) < 0.01:
                        is_paid = True
                        break

            if is_paid:
                db.mark_order_paid(order_id)
                bot.send_message(user_id, "✅ **🎉 تم تأكيد الدفع بنجاح!**", parse_mode="Markdown")
                bot.send_message(lc.ADMIN_ID, f"🔔 دفع جديد: `{amount}$` من `{user_id}`")
            else:
                bot.send_message(user_id, "❌ **لم يتم العثور على دفعة مطابقة بعد.**", parse_mode="Markdown")
        except:
            bot.send_message(user_id, "⚠️ خطأ في فحص الشبكة، أعد المحاولة لاحقاً.")
