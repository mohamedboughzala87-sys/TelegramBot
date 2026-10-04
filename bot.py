from flask import Flask
from threading import Thread

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
import telebot
import sqlite3
import threading
import time
from telebot import types

TOKEN = "8794366009:AAFRtcM891gvxLkJgc39jwwrq6gSqWC9yFQ"
bot = telebot.TeleBot(TOKEN)

MY_USDT_WALLET = "TULQfGqF2AtB41ybkPbj7pvX8FBQpWfVLw"
ADMIN_ID = 58392019

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

LOCALES['hi'] = {
    'welcome': "✨ **ग्लोबल चैनल ग्रोथ प्लेटफॉर्म** ✨\n\n🚀 वास्तविक सदस्यों के साथ अपने चैनल को बढ़ावा देने का सबसे तेज़ तरीका।",
    'choose': "👇 नीचे दिए गए मेनू से चुनें:",
    'btn_promo': "💎 प्रमोशन पैकेज",
    'btn_guide': "📖 भुगतान गाइड",
    'btn_lang': "🌐 भाषा बदलें / Language",
    'pkg_title': "💎 **ग्रोथ पैकेज** 💎\n\n📌 चालान जेनरेट करने के लिए पैकेज चुनें:",
    'invoice': "┌─── ❖ ⚙️ **स्मार्ट चालान** ❖ ───────┐\n\n🆔 **ऑर्डर आईडी:** `#{order_id}`\n📦 **सेवा:** {name}\n💰 **देय राशि:** `{price}$ USDT` *(TRC-20)*\n\n📥 **क्रिप्टो वॉलेट पता:**\n`{wallet}`\n\n🔄 ट्रांसफर के बाद सक्रिय करने के लिए नीचे दबाएं!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 भुगतान स्वचालित सत्यापित करें",
    'guide': "📖 **गाइड:**\n1️⃣ अपना क्रिप्टो वॉलेट खोलें।\n2️⃣ USDT (TRC-20) भेजें।\n3️⃣ बोट का वॉलेट पता कॉपी करके फंड भेजें।"
}

LOCALES['fa'] = {
    'welcome': "✨ **پلتفرم جهانی رشد کانال** ✨\n\n🚀 سریع‌ترین راه برای افزایش اعضای واقعی کانال شما.",
    'choose': "👇 از منوی زیر انتخاب کنید:",
    'btn_promo': "💎 پکیج‌های ارتقا",
    'btn_guide': "📖 راهنمای پرداخت",
    'btn_lang': "🌐 تغییر زبان / Language",
    'pkg_title': "💎 **پکیج‌های رشد** 💎\n\n📌 پکیج مورد نظر را برای صدور فاکتور انتخاب کنید:",
    'invoice': "┌─── ❖ ⚙️ **فاکتور هوشمند** ❖ ───────┐\n\n🆔 **شماره سفارش:** `#{order_id}`\n📦 **خدمات:** {name}\n💰 **مبلغ:** `{price}$ USDT` *(TRC-20)*\n\n📥 **آدرس ولت:**\n`{wallet}`\n\n🔄 پس از انتقال، برای فعال‌سازی دکمه زیر را فشار دهید!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 تایید خودکار پرداخت",
    'guide': "📖 **راهنما:**\n1️⃣ ولت کریپتو خود را باز کنید.\n2️⃣ ارز USDT (TRC-20) ارسال کنید.\n3️⃣ آدرس ولت بات را کپی کرده و وجه را ارسال کنید."
}

LOCALES['es'] = {
    'welcome': "✨ **Plataforma Global de Crecimiento de Canales** ✨\n\n🚀 Tu forma más rápida de potenciar tu canal con miembros reales.",
    'choose': "👇 Elige del menú de abajo:",
    'btn_promo': "💎 Paquetes de Promoción",
    'btn_guide': "📖 Guía de Pago",
    'btn_lang': "🌐 Cambiar Idioma / Language",
    'pkg_title': "💎 **Paquetes de Crecimiento** 💎\n\n📌 Elige un paquete para generar una factura:",
    'invoice': "┌─── ❖ ⚙️ **FACTURA INTELIGENTE** ❖ ───┐\n\n🆔 **ID de Orden:** `#{order_id}`\n📦 **Servicio:** {name}\n💰 **Monto:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Dirección de Billetera:**\n`{wallet}`\n\n🔄 ¡Presiona abajo después de transferir para activar!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 Verificar Pago Automáticamente",
    'guide': "📖 **Guía:**\n1️⃣ Abre tu billetera cripto.\n2️⃣ Envía USDT (TRC-20).\n3️⃣ Copia la dirección del bot y envía los fondos."
}

LOCALES['pt'] = {
    'welcome': "✨ **Plataforma Global de Crescimento de Canais** ✨\n\n🚀 A sua forma mais rápida de impulsionar o seu canal com membros reais.",
    'choose': "👇 Escolha no menu abaixo:",
    'btn_promo': "💎 Pacotes de Promoção",
    'btn_guide': "📖 Guia de Pagamento",
    'btn_lang': "🌐 Mudar Idioma / Language",
    'pkg_title': "💎 **Pacotes de Crescimento** 💎\n\n📌 Escolha um paquete para gerar uma fatura:",
    'invoice': "┌─── ❖ ⚙️ **FATURA INTELLIGENTE** ❖ ───┐\n\n🆔 **ID do Pedido:** `#{order_id}`\n📦 **Serviço:** {name}\n💰 **Valor:** `{price}$ USDT` *(TRC-20)*\n\n📥 **Endereço da Carteira:**\n`{wallet}`\n\n🔄 Pressione abaixo após transferir para ativar o seu pacote!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 Verificar Pagamento",
    'guide': "📖 **Guia:**\n1️⃣ Abra a sua carteira cripto.\n2️⃣ Envie USDT (TRC-20).\n3️⃣ Copie o endereço do bot e envie os fundos."
}

LOCALES['tr'] = {
    'welcome': "✨ **Küresel Kanal Büyütme Platformu** ✨\n\n🚀 Kanalınızı gerçek üyelerle büyütmenin en hızlı yolu.",
    'choose': "👇 Aşağıdaki menüden seçim yapın:",
    'btn_promo': "💎 Tanıtım Paketleri",
    'btn_guide': "📖 Ödeme Kılavuzu",
    'btn_lang': "🌐 Dili Değiştir / Language",
    'pkg_title': "💎 **Büyüme Paketleri** 💎\n\n📌 Fatura oluşturmak için bir paket seçin:",
    'invoice': "┌─── ❖ ⚙️ **AKILLI FATURA** ❖ ───┐\n\n🆔 **Sipariş NO:** `#{order_id}`\n📦 **Hizmet:** {name}\n💰 **Tutar:** `{price}$ USDT` *(TRC-20)*\n\n\n📥 **Cüzdan Adresi:**\n`{wallet}`\n\n🔄 Aktif etmek için transferden sonra aşağıdaki butona basın!\n└───❖───✦───❖───┘",
    'btn_verify': "🔄 Ödemeyi Doğrula",
    'guide': "📖 **Kılavuz:**\n1️⃣ Kripto cüzdanınızı açın.\n2️⃣ USDT (TRC-20) gönderin.\n3️⃣ Bot cüzdan adresini kopyalayıp gönderin."
}

PACKAGES = {
    '1': {'ar': '🥉 باقة الأفراد (200 مشترك)', 'en': '🥉 Personal Pack (200 subs)', 'fr': '🥉 Pack Perso (200 subs)', 'zh': '🥉 个人礼包 (200 成员)', 'ru': '🥉 Персональный пакет (200 суб)', 'hi': '🥉 पर्सनल पैक (200 सदस्य)', 'fa': '🥉 پکیج شخصی (200 عضو)', 'es': '🥉 Pack Personal (200 subs)', 'pt': '🥉 Pack Pessoal (200 subs)', 'tr': '🥉 Kişisel Paket (200 üye)', 'price': 10.0},
    '2': {'ar': '🏢 باقة الشركات (2000 مشترك)', 'en': '🏢 Business Pack (2000 subs)', 'fr': '🏢 Pack Pro (2000 subs)', 'zh': '🏢 商业礼包 (2000 成员)', 'ru': '🏢 Бизнес-пакет (2000 ...)', 'hi': '🏢 बिजनेस पैक (2000 सदस्य)', 'fa': '🏢 پکیج تجاری (2000 عضو)', 'es': '🏢 Pack Empresa (2000 subs)', 'pt': '🏢 Pack Empresa (2000 subs)', 'tr': '🏢 Kurumsal Paket (2000 üye)', 'price': 80.0}
}

user_clicks = {}

def init_db():
    conn = sqlite3.connect("perfect_global_wealth.db")
    conn.cursor().execute("PRAGMA auto_vacuum = FULL;")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, lang TEXT DEFAULT 'ar')")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, buyer_id INTEGER, package_id TEXT, price REAL, timestamp INTEGER, status TEXT DEFAULT 'pending')")
    conn.commit()
    conn.close()

def get_user_lang(user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'ar'
    except:
        return 'ar'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    init_db()
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    
    # جلب نص الترحيب حسب لغة المستخدم المبرمجة في الكود
    welcome_text = LOCALES.get(lang, LOCALES['ar'])['welcome']
    
    # إنشاء أزرار اختيار اللغة
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_ar = types.KeyboardButton("العربية 🇹🇳")
    btn_en = types.KeyboardButton("English 🇬🇧")
    markup.add(btn_ar, btn
        bot.reply_to(message, welcome_text, reply_markup=markup)

bot.infinity_polling()
