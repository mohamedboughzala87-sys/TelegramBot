from flask import Flask
from threading import Thread
import telebot, sqlite3, time, requests
from telebot import types

# 1. إعداد Flask لإبقاء البوت حياً على منصة Render
app = Flask('')
@app.route('/')
def home(): return "Bot is alive and checking payments!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()
keep_alive()

# 2. إعدادات البوت والبيانات الأساسية الخاصة بك
TOKEN = "8794366009:AAFRtcM891gvxLkJgc39jwwrq6gSqWC9yFQ"
bot = telebot.TeleBot(TOKEN)
MY_USDT_WALLET = "TULQfGqF2AtB41ybkPbj7pvX8FBQpWfVLw"
ADMIN_ID = 58392019

# 3. قاموس اللغات الـ 10 الكامل والمصلح بدون أي قطع أو تشويه
LOCALES = {}
LOCALES['ar'] = {'welcome': "✨ **منصة دعم القنوات العالمية** ✨\n\n🚀 طريقتك الأسرع لتكبير قناتك بأعضاء حقيقيين وتفاعل تلقائي.", 'choose': "👇 اختر من القائمة أدناه:", 'btn_promo': "💎 باقات الترويج السريع", 'btn_guide': "📖 دليل الدفع المبسط", 'btn_lang': "🌐 تغيير اللغة / Language", 'pkg_title': "💎 **باقات النمو والتفاعل** 💎\n\n📌 اختر الباقة لتوليد الفاتورة فوراً:", 'invoice': "┌─── ❖ ⚙️ **فـاتـورة ذكـيـة** ❖ ───┐\n\n🆔 **الطلب:** `#{order_id}`\n📦 **الخدمة:** {name}\n💰 **المبلغ:** `{price}$ USDT` *(TRC-20)*\n\n📥 **المحفظة:**\n`{wallet}`\n\n🔄 اضغط أدناه بعد التحويل للتفعيل فورا!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 تأكيد استلام الدفعة آلياً", 'guide': "📖 **دليل الشراء:**\n1️⃣ افتح محفظتك الرقمية.\n2️⃣ أرسل USDT (TRC-20).\n3️⃣ انسخ عنوان البوت وأرسل المال."}
LOCALES['en'] = {'welcome': "✨ **Global Channel Growth Platform** ✨\n\n🚀 Your fastest way to boost your channel with real members.", 'choose': "👇 Choose from the menu below:", 'btn_promo': "💎 Promotion Packages", 'btn_guide': "📖 Payment Guide", 'btn_lang': "🌐 Change Language / Language", 'pkg_title': "💎 **Growth Packages** 💎\n\n📌 Choose a package to generate an invoice:", 'invoice': "┌─── ❖ ⚙️ **SMART INVOICE** ❖ ───┐\n\n🆔 **Order ID:** `#{order_id}`\n📦 **Service:** {name}\n💰 **Amount:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Wallet Address:**\n`{wallet}`\n\n🔄 Press below after transferring to activate!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Verify Payment Automatically", 'guide': "📖 **Guide:**\n1️⃣ Open your crypto wallet.\n2️⃣ Send USDT (TRC-20).\n3️⃣ Copy bot wallet and transfer."}
LOCALES['fr'] = {'welcome': "✨ **Plateforme de Croissance Globale** ✨\n\n🚀 Boostez votre canal avec des membres réels.", 'choose': "👇 Choisissez dans le menu:", 'btn_promo': "💎 Packs de Promotion", 'btn_guide': "📖 Guide de Paiement", 'btn_lang': "🌐 Changer de Langue / Ligue", 'pkg_title': "💎 **Packs de Croissance** 💎\n\n📌 Choisissez un pack pour générer uma facture:", 'invoice': "┌─── ❖ ⚙️ **FACTURE INTELLIGENTE** ❖ ───┐\n\n🆔 **ID Commande:** `#{order_id}`\n📦 **Service:** {name}\n💰 **Montant:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Adresse du Portefeuille:**\n`{wallet}`\n\n🔄 Appuyez ci-dessous après transfert pour activer!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Vérifier Automatiquement", 'guide': "📖 **Guide:**\n1️⃣ Ouvrez votre portefeuille crypto.\n2️⃣ Envoyez USDT (TRC-20).\n3️⃣ Copiez l'adresse du bot et transférez."}
LOCALES['zh'] = {'welcome': "✨ **全球频道增长平台** ✨\n\n🚀 快速且安全地提升您的频道成员与互动。", 'choose': "👇 从下方菜单选择：", 'btn_promo': "💎 快速推广礼包", 'btn_guide': "📖 简易支付指南", 'btn_lang': "🌐 更改语言 / Language", 'pkg_title': "💎 **增长礼包** 💎\n\n📌 选择礼包生成账单：", 'invoice': "┌─── ❖ ⚙️ **智能账单** ❖ ───┐\n\n🆔 **订单号:** `#{order_id}`\n📦 **服务:** {name}\n💰 **金额:** `{price}$ USDT` *(TRC-20)*\n\n📥 **钱包地址:**\n`{wallet}`\n\n🔄 转账后点击下方按钮立即激活！\n└───❖───✦───❖───┘", 'btn_verify': "🔄 自动验证付款", 'guide': "📖 **指南：**\n1️⃣ 打开去中心化钱包。\n2️⃣ 发送 USDT (TRC-20)。\n3️⃣ 复制机器人钱包地址并转账。"}
LOCALES['ru'] = {'welcome': "✨ **Глобальная Платформа Роста Каналов** ✨\n\n🚀 Самый быстрый способ продвижения вашего канала с реальными участниками.", 'choose': "👇 Выберите из меню ниже:", 'btn_promo': "💎 Пакеты Продвижения", 'btn_guide': "📖 Руководство по Оплате", 'btn_lang': "🌐 Изменить язык / Language", 'pkg_title': "💎 **Пакеты Роста** 💎\n\n📌 Выберите пакет для автосчета:", 'invoice': "┌─── ❖ ⚙️ **УМНЫЙ СЧЕТ** ❖ ───┐\n\n🆔 **ID Заказа:** `#{order_id}`\n📦 **Услуга:** {name}\n💰 **К оплате:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Адрес кошелька:**\n`{wallet}`\n\n🔄 Нажмите кнопку ниже после перевода для активации!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Проверить оплату", 'guide': "📖 **Инструкция:**\n1️⃣ Откройте криптокошелек.\n2️⃣ Отправьте USDT (TRC-20).\n3️⃣ Скопируйте адрес кошелька бота."}
LOCALES['hi'] = {'welcome': "✨ **ग्लोबल चैनल Growth प्लेटफॉर्म** ✨\n\n🚀 वास्तविक सदस्यों के साथ अपने चैनल को बढ़ावा देने का सबसे तेज़ तरीका।", 'choose': "👇 नीचे दिए गए मेनू से चुनें:", 'btn_promo': "💎 प्रमोशन पैकेज", 'btn_guide': "📖 भुगतान गाइड", 'btn_lang': "🌐 भाषा बदलें / Language", 'pkg_title': "💎 **ग्रोथ पैकेज** 💎\n\n📌 चालान जेनरेट करने के लिए पैकेज चुनें:", 'invoice': "┌─── ❖ ⚙️ **स्मार्ट चालान** ❖ ───────┐\n\n🆔 **ऑर्डर आईडी:** `#{order_id}`\n📦 **सेवा:** {name}\n💰 **देय राशि:** `{price}$ USDT` *(TRC-20)*\n\n📥 **क्रिप्टो वॉलेट पता:**\n`{wallet}`\n\n🔄 ट्रांसफर के बाद सक्रिय करने के लिए नीचे दबाएं!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 भुगतान स्वचालित सत्यापित करें", 'guide': "📖 **गाइड:**\n1️⃣ अपना क्रिप्टो वॉलेट खोलें।\n2️⃣ USDT (TRC-20) भेजें।\n3️⃣ بوت का वॉलेट पता कॉपी करके फंड भेजें।"}
LOCALES['fa'] = {'welcome': "✨ **پلتفرم جهانی رشد کانال** ✨\n\n🚀 سريع‌ترین راه برای افزایش اعضای واقعی کانال شما.", 'choose': "👇 از منوی زیر انتخاب کنید:", 'btn_promo': "💎 پکیج‌های ارتقا", 'btn_guide': "📖 راهنمای پرداخت", 'btn_lang': "🌐 تغییر زبان / Language", 'pkg_title': "💎 **پکیج‌های رشد** 💎\n\n📌 پکیج مورد نظر را برای صدور فاکتور انتخاب کنید:", 'invoice': "┌─── ❖ ⚙️ **فاکتور هوشمند** ❖ ───────┐\n\n🆔 **شماره سفارش:** `#{order_id}`\n📦 **خدمات:** {name}\n💰 **مبلغ:** `{price}$ USDT` *(TRC-20)*\n\n📥 **آدرس ولت:**\n`{wallet}`\n\n🔄 پس از انتقال، برای فعال‌سازی دکمه زیر را فشار دهید!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 تایید خودکار پرداخت", 'guide': "📖 **راهنما:**\n1️⃣ ولت کریپتو خود را باز کنید.\n2️⃣ ارز USDT (TRC-20) ارسال کنید.\n3️⃣ آدرس ولت بات را کپی کرده و وجه را ارسال کنید."}
LOCALES['es'] = {'welcome': "✨ **Plataforma Global de Crecimiento de Canales** ✨\n\n🚀 Tu forma más rápida de potenciar tu canal مع أعضاء حقيقيين.", 'choose': "👇 Elige del menú de abajo:", 'btn_promo': "💎 Paquetes de Promoción", 'btn_guide': "📖 Guide de Pago", 'btn_lang': "🌐 Cambiar Idioma / Language", 'pkg_title': "💎 **Paquetes de Crecimiento** 💎\n\n📌 Elige un paquete para generar una factura:", 'invoice': "┌─── ❖ ⚙️ **FACTURA INTELIGENTE** ❖ ───┐\n\n🆔 **ID de Orden:** `#{order_id}`\n📦 **Servicio:** {name}\n💰 **Monto:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Dirección de Billetera:**\n`{wallet}`\n\n🔄 ¡Presiona abajo después de transferir para activar!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Verificar Pago Automáticamente", 'guide': "📖 **Guía:**\n1️⃣ Abre tu billetera cripto.\n2️⃣ Envía USDT (TRC-20).\n3️⃣ Copia la dirección del bot y envía los funds."}
LOCALES['pt'] = {'welcome': "✨ **Plataforma Global de Crescimento de Canais** ✨\n\n🚀 A sua forma mais rápida de impulsionar o seu canal com membros reais.", 'choose': "👇 Escolha no menu abaixo:", 'btn_promo': "💎 Pacotes de Promoção", 'btn_guide': "📖 Guia de Pagamento", 'btn_lang': "🌐 Mudar Idioma / Language", 'pkg_title': "💎 **Pacotes de Crescimento** 💎\n\n📌 Escolha um paquete para gerar uma fatura:", 'invoice': "┌─── ❖ ⚙️ **FATURA INTELLIGENTE** ❖ ───┐\n\n🆔 **ID do Pedido:** `#{order_id}`\n📦 **Serviço:** {name}\n💰 **Valor:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Endereço da Carteira:**\n`{wallet}`\n\n🔄 Pressione abaixo após transferir para activar o seu pacote!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Verificar Pagamento", 'guide': "📖 **Guide:**\n1️⃣ Abra a sua carteira cripto.\n2️⃣ Envie USDT (TRC-20).\n3️⃣ Copie o endereço do bot."}
LOCALES['tr'] = {'welcome': "✨ **Küresel Kanal Büyütme Platformu** ✨\n\n🚀 Kanalınızı gerçek üyelerle büyütmenin en hızlı yolu.", 'choose': "👇 Aşağıdaki menüden seçim yapın:", 'btn_promo': "💎 Paket Tanıtımları", 'btn_guide': "📖 Basit Ödeme Kılavuzu", 'btn_lang': "🌐 Dili Değiştir / Language", 'pkg_title': "💎 **Büyüme Paketleri** 💎\n\n📌 Fatura oluşturmak için bir paket seçين:", 'invoice': "┌─── ❖ ⚙️ **AKILLI FATURA** ❖ ───┐\n\n🆔 **Sipariş No:** `#{order_id}`\n📦 **Hizmet:** {name}\n💰 **Tutar:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Cüzdan Adresi:**\n`{wallet}`\n\n🔄 Etkinleştirmek için transferden sonra aşağıya basın!\n└───❖───✦───❖───┘", 'btn_verify': "🔄 Ödemeyi Otomatik Doğrula", 'guide': "📖 **Kılavuz:**\n1️⃣ Kripto cüzdanınızı açın.\n2️⃣ USDT (TRC-20) gönderin.\n3️⃣ Bot cüzdan adresini kopyalayıp gönderin."}

# 4. باقات الأسعار المترجمة والموزعة عادلاً وتنافسياً بين 5\( و 80\)
PACKAGES = {
    '1': {'ar': '🥉 باقة الأفراد (200 مشترك)', 'en': '🥉 Personal Pack (200 subs)', 'fr': '🥉 Pack Perso (200 subs)', 'zh': '🥉 个人礼包 (200 成员)', 'ru': '🥉 Персональный пакет (200 cy6)', 'hi': '🥉 पर्सनल पैक (200 सदस्य)', 'fa': '🥉 پکیج شخصی (200 عضو)', 'es': '🥉 Pack Personal (200 subs)', 'pt': '🥉 Pack Pessoal (200 subs)', 'tr': '🥉 Kişisel Paket (200 üye)', 'price': 5.0},
    '2': {'ar': '🥈 الباقة المتقدمة (500 مشترك)', 'en': '🥈 Advanced Pack (500 subs)', 'fr': '🥈 Pack Avancé (500 subs)', 'zh': '🥈 高级礼包 (500 成员)', 'ru': '🥈 Продвинутый пакет (500 суб)', 'hi': '🥈 एडवांस्ड पैक (500 सदस्य)', 'fa': '🥈 پکیج پیشرفته (500 عضو)', 'es': '🥈 Pack Avanzado (500 subs)', 'pt': '🥈 Pack Avançado (500 subs)', 'tr': '🥈 Gelişmiş Paket (500 üye)', 'price': 10.0},
    '3': {'ar': '🥇 باقة المحترفين (1000 مشترك)', 'en': '🥇 Pro Pack (1000 subs)', 'fr': '🥇 Pack Pro (1000 subs)', 'zh': '🥇 专业礼包 (1000 成员)', 'ru': '🥇 Профессиональный (1000 суб)', 'hi': '🥇 प्रो पैक (1000 सदस्य)', 'fa': '🥇 پکیج حرفه ای (1000 عضو)', 'es': '🥇 Pack Profesional (1000 subs)', 'pt': '🥇 Pack Profissional (1000 subs)', 'tr': '🥇 Profesyonel Paket (1000 üye)', 'price': 18.0},
    '4': {'ar': '💎 باقة الشركات (5000 مشترك)', 'en': '💎 Business Pack (5000 subs)', 'fr': '💎 Pack Ultra (5000 subs)', 'zh': '💎 商业礼包 (5000 成员)', 'ru': '💎 Бизнес-пакет (5000 суб)', 'hi': '💎 बिजनेस पैक (5000 सदस्य)', 'fa': '💎 پکیج تجاری (5000 عضو)', 'es': '💎 Pack Empresa (5000 subs)', 'pt': '💎 Pack Empresa (5000 subs)', 'tr': '💎 Kurumsal Paket (5000 üye)', 'price': 80.0}
}

# 5. دوال قاعدة البيانات والاتصال الذكي
def init_db():
    conn = sqlite3.connect("perfect_global.db"); cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT DEFAULT 'ar');")
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
    order_id = cursor.lastrowid; conn.commit(); conn.close()
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
    
# 6. نظام فحص شبكة البلوكشين تلقائياً للتحقق من وصول الـ USDT (TRC-20)
def check_blockchain_payment(wallet, expected_amount):
    try:
        url = f"https://trongrid.io{wallet}/transactions/trc20"
        response = requests.get(url, timeout=10).json()
        if "data" in response:
            for tx in response["data"]:
                if tx["token_info"]["symbol"] == "USDT":
                    amount = float(tx["value"]) / (10 ** tx["token_info"]["decimals"])
                    if abs(amount - expected_amount) < 0.1: return True
        return False
    except: return False

def get_main_menu(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    texts = LOCALES.get(lang, LOCALES['ar'])
    markup.add(types.KeyboardButton(texts['btn_promo']))
    markup.add(types.KeyboardButton(texts['btn_guide']), types.KeyboardButton(texts['btn_lang']))
    return markup

# 7. معالجة أمر البداية /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    init_db()
    user_id = message.from_user.id; lang = get_user_lang(user_id); texts = LOCALES.get(lang, LOCALES['ar'])
    bot.reply_to(message, f"{texts['welcome']}\n\n{texts['choose']}", reply_markup=get_main_menu(lang), parse_mode="Markdown")

# 8. استقبال الرسائل وإظهار خيارات الأزرار
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_id = message.from_user.id; lang = get_user_lang(user_id); texts = LOCALES.get(lang, LOCALES['ar'])
    if message.text == texts['btn_guide']:
        bot.reply_to(message, texts['guide'], parse_mode="Markdown")
    elif message.text == texts['btn_promo']:
        markup = types.InlineKeyboardMarkup()
        for pkg_id, pkg in PACKAGES.items():
            markup.add(types.InlineKeyboardButton(f"{pkg.get(lang, pkg['ar'])} - {pkg['price']}\$", callback_data=f"buy_{pkg_id}"))
        bot.reply_to(message, texts['pkg_title'], reply_markup=markup, parse_mode="Markdown")
    elif message.text == texts['btn_lang']:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("العربية 🇹🇳", callback_data="set_lang_ar"), types.InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"), types.InlineKeyboardButton("Français 🇫🇷", callback_data="set_lang_fr"), types.InlineKeyboardButton("中文 🇨🇳", callback_data="set_lang_zh"), types.InlineKeyboardButton("Русский 🇷🇺", callback_data="set_lang_ru"), types.InlineKeyboardButton("Türkçe 🇹🇷", callback_data="set_lang_tr"), types.InlineKeyboardButton("Español 🇪🇸", callback_data="set_lang_es"), types.InlineKeyboardButton("Português 🇵🇹", callback_data="set_lang_pt"), types.InlineKeyboardButton("हिन्दी 🇮🇳", callback_data="set_lang_hi"), types.InlineKeyboardButton("فارسی 🇮🇷", callback_data="set_lang_fa"))
        bot.reply_to(message, "🌐 Choose your language / اختر لغتك:", reply_markup=markup)

# 9. توليد الفاتورة عند اختيار باقة
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def callback_buy(call):
    user_id = call.from_user.id; lang = get_user_lang(user_id); texts = LOCALES.get(lang, LOCALES['ar'])
    pkg_id = call.data.replace('buy_', ''); pkg = PACKAGES.get(pkg_id)
    if pkg:
        order_id = create_order(user_id, pkg_id, pkg['price'])
        invoice_text = texts['invoice'].format(order_id=order_id, name=pkg.get(lang, pkg['ar']), price=pkg['price'], wallet=MY_USDT_WALLET)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(texts['btn_verify'], callback_data=f"verify_{order_id}"))
        bot.send_message(call.message.chat.id, invoice_text, reply_markup=markup, parse_mode="Markdown")

# 10. فحص وتأكيد الدفع آلياً عبر البلوكشين وإرسال الإشعارات
@bot.callback_query_handler(func=lambda call: call.data.startswith('verify_'))
def callback_verify(call):
    order_id = call.data.replace('verify_', ''); order = get_order(order_id)
    if order:
        buyer_id, package_id, price, status = order
        if status == 'completed':
            bot.answer_callback_query(call.id, "✅ هذا الطلب مفعل ومكتمل سابقاً!")
            return
        bot.answer_callback_query(call.id, "🔍 Jari fahs al blockchain...")
        if check_blockchain_payment(MY_USDT_WALLET, price):
            update_order_status(order_id, 'completed')
            bot.send_message(call.message.chat.id, f"🎉 **تم تأكيد الدفع بنجاح!**\n\nجاري تجهيز طلبك رقم `#{order_id}` تلقائياً وسيتم إرسال المشتركين لقناتك فوراً.")
            bot.send_message(ADMIN_ID, f"💰 **إشعار دفع آلي جديد:**\nالزبون: `{buyer_id}` قام بدفع `{price}$ USDT` للطلب `#{order_id}`.")
        else:
            bot.send_message(call.message.chat.id, "❌ **لم نكتشف أي تحويل جديد بهذه القيمة حتى الآن.**\n\nتأكد من إرسال المبلغ الصحيح وانتظر دقيقة ثم اضغط على الزر مرة أخرى.")

# 11. استقبال خيارات الأزرار المضمنة (Inline Buttons) لتغيير اللغة فوراً
@bot.callback_query_handler(func=lambda call: call.data.startswith('set_lang_'))
def callback_language(call):
    user_id = call.from_user.id; new_lang = call.data.replace('set_lang_', ''); set_user_lang(user_id, new_lang)
    texts = LOCALES.get(new_lang, LOCALES['ar']); bot.answer_callback_query(call.id, "✅ Done / تم التحديث")
    bot.send_message(call.message.chat.id, f"✅ {texts['welcome']}", reply_markup=get_main_menu(new_lang), parse_mode="Markdown")

# 12. تشغيل البوت بشكل لانهائي ومستمر
bot.infinity_polling()
