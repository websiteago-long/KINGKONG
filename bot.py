import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_GROUP_ID = "-1003875548933"

# កន្លែងផ្ទុកទឹកប្រាក់អតិថិជន និងការបញ្ជាទិញបណ្ដោះអាសន្ន
user_balances = {}
pending_orders = {}

# តារាងតម្លៃកញ្ចប់ហ្គេមថ្មី
PACKAGES = {
    "Roblox": [
        {"name": "80 Robux", "price": 1.00},
        {"name": "160 Robux", "price": 2.00},
        {"name": "240 Robux", "price": 3.00},
        {"name": "320 Robux", "price": 4.00},
        {"name": "400 Robux", "price": 5.00},
        {"name": "480 Robux", "price": 6.00},
        {"name": "560 Robux", "price": 7.00}
    ]
}

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("👤 គណនី"), KeyboardButton("🎮 GAME TOPUP"),
        KeyboardButton("💵 ដាក់ប្រាក់"), KeyboardButton("👨‍💻 អ្នកគ្រប់គ្រង")
    )
    return markup

def get_game_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("Roblox"), KeyboardButton("Mobile Legends"), KeyboardButton("Free Fire"))
    markup.add(KeyboardButton("🔙 ត្រឡប់ក្រោយ"))
    return markup

@bot.message_handler(commands=['getid'])
def send_id(message):
    bot.send_message(message.chat.id, f"📍 ID របស់ទីតាំងនេះគឺ: `{message.chat.id}`", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "សួស្តី! សូមស្វាគមន៍មកកាន់សេវាកម្មរបស់យើងខ្ញុំ។ សូមជ្រើសរើសសេវាកម្មនៅខាងក្រោម៖", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "👤 គណនី")
def handle_account(message):
    user_id = message.from_user.id
    username = message.from_user.username
    username_text = f"@{username}" if username else "មិនមាន"
    balance = user_balances.get(user_id, 0.0)
    text = f"**ព័ត៌មានគណនីរបស់អ្នក៖**\n\n🆔 ID: `{user_id}`\n👤 Username: {username_text}\n💰 ទឹកប្រាក់ចំនួន: `${balance:.2f}`"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🎮 GAME TOPUP")
def handle_game_topup(message):
    bot.send_message(message.chat.id, "សូមជ្រើសរើសហ្គេមដែលអ្នកចង់ Top Up ខាងក្រោម៖", reply_markup=get_game_menu())

@bot.message_handler(func=lambda message: message.text in ["Roblox", "Mobile Legends", "Free Fire"])
def handle_topup_selection(message):
    user_id = message.from_user.id
    game_name = message.text
    
    if game_name in PACKAGES:
        markup = InlineKeyboardMarkup()
        for i, pkg in enumerate(PACKAGES[game_name]):
            btn = InlineKeyboardButton(f"{pkg['name']} - ${pkg['price']:.2f}", callback_data=f"pkg_{game_name}_{i}")
            markup.add(btn)
        bot.send_message(message.chat.id, f"🎮 សូមជ្រើសរើសកញ្ចប់ **{game_name}** ខាងក្រោម៖", parse_mode="Markdown", reply_markup=markup)
    else:
        pending_orders[user_id] = {"game": game_name}
        msg = bot.send_message(message.chat.id, f"🎮 អ្នកបានជ្រើសរើស: **{game_name}**\n\n💵 តើអ្នកចង់ Top Up អស់ប៉ុន្មានដុល្លារ? (សូមវាយតែលេខ ឧទាហរណ៍: 1.5, 5):", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_topup_amount)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pkg_"))
def handle_package_selection(call):
    bot.answer_callback_query(call.id)
    parts = call.data.split('_')
    game_name = parts[1]
    pkg_index = int(parts[2])
    
    pkg = PACKAGES[game_name][pkg_index]
    amount = pkg["price"]
    pkg_name = pkg["name"]
    user_id = call.from_user.id
    balance = user_balances.get(user_id, 0.0)
    
    if balance < amount:
        bot.send_message(call.message.chat.id, f"❌ ទឹកប្រាក់របស់អ្នកមិនគ្រប់គ្រាន់ទេ!\nអ្នកមាន: `${balance:.2f}` | អ្នកចង់ទិញ: `${amount:.2f}`\n\nសូមធ្វើការ 💵 ដាក់ប្រាក់ បន្ថែម។")
        return
        
    pending_orders[user_id] = {"game": game_name, "amount": amount, "package_name": pkg_name}
    msg = bot.send_message(call.message.chat.id, f"✅ អ្នកបានជ្រើសរើស **{pkg_name}** តម្លៃ **${amount:.2f}**\n\nសូមផ្ញើ **ID ហ្គេម ឬ ឈ្មោះតួអង្គ** របស់អ្នកមកកាន់ទីនេះ៖", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_topup_id)

def process_topup_amount(message):
    user_id = message.from_user.id
    if message.text in ["👤 គណនី", "🎮 GAME TOPUP", "💵 ដាក់ប្រាក់", "👨‍💻 អ្នកគ្រប់គ្រង", "🔙 ត្រឡប់ក្រោយ"]:
        bot.send_message(message.chat.id, "❌ បានបោះបង់ការបញ្ជាទិញ។", reply_markup=get_main_menu())
        return
        
    try:
        amount = float(message.text)
        if amount <= 0: raise ValueError
    except ValueError:
        msg = bot.send_message(message.chat.id, "⚠️ សូមវាយបញ្ចូលជាតួលេខឲ្យបានត្រឹមត្រូវ។ ព្យាយាមម្ដងទៀត៖")
        bot.register_next_step_handler(msg, process_topup_amount)
        return
        
    balance = user_balances.get(user_id, 0.0)
    if balance < amount:
        bot.send_message(message.chat.id, f"❌ ទឹកប្រាក់របស់អ្នកមិនគ្រប់គ្រាន់ទេ!\nអ្នកមាន: `${balance:.2f}` | អ្នកចង់ទិញ: `${amount:.2f}`\n\nសូមធ្វើការដាក់ប្រាក់បន្ថែម។")
        return
        
    pending_orders[user_id]["amount"] = amount
    pending_orders[user_id]["package_name"] = "មិនមានបញ្ជាក់"
    msg = bot.send_message(message.chat.id, "✅ លុយក្នុងគណនីគ្រប់គ្រាន់! សូមផ្ញើ **ID ហ្គេម ឬ ឈ្មោះតួអង្គ** របស់អ្នកមកកាន់ទីនេះ៖")
    bot.register_next_step_handler(msg, process_topup_id)

def process_topup_id(message):
    user_id = message.from_user.id
    if message.text in ["👤 គណនី", "🎮 GAME TOPUP", "💵 ដាក់ប្រាក់", "👨‍💻 អ្នកគ្រប់គ្រង", "🔙 ត្រឡប់ក្រោយ"]:
        bot.send_message(message.chat.id, "❌ បានបោះបង់ការបញ្ជាទិញ។", reply_markup=get_main_menu())
        return
        
    order = pending_orders.get(user_id)
    if not order: return
    
    game_name = order["game"]
    amount = order["amount"]
    pkg_name = order.get("package_name", "")
    game_id = message.text
    username = message.from_user.username
    username_text = f"@{username}" if username else "មិនមាន"
    
    user_balances[user_id] -= amount
    bot.send_message(message.chat.id, f"✅ ការបញ្ជាទិញត្រូវបានបញ្ជូន! (ទឹកប្រាក់ `${amount:.2f}` ត្រូវបានកាត់បណ្ដោះអាសន្ន)\nសូមមេត្ដារងចាំការត្រួតពិនិត្យពីអ្នកគ្រប់គ្រងបន្តិច។", parse_mode="Markdown")
    
    caption = f"🎮 **មានការបញ្ជាទិញ TOPUP ថ្មី**\n\n🕹 ហ្គេម: {game_name}\n📦 កញ្ចប់: {pkg_name}\n💵 តម្លៃកាត់ចេញ: `${amount:.2f}`\n📝 ID ហ្គេម: {game_id}\n\n🆔 ID អតិថិជន: `{user_id}`\n👤 Username: {username_text}"
    
    admin_markup = InlineKeyboardMarkup()
    admin_markup.add(InlineKeyboardButton("✅ បញ្ជាក់ការទិញ", callback_data=f"topapp_{user_id}_{amount}"), InlineKeyboardButton("❌ បដិសេធ", callback_data=f"toprej_{user_id}_{amount}"))
    admin_markup.add(InlineKeyboardButton("💬 ផ្ញើសារទៅអតិថិជន", callback_data=f"sendmsg_{user_id}"))
    
    try: 
        bot.send_message(ADMIN_GROUP_ID, caption, parse_mode="Markdown", reply_markup=admin_markup)
    except Exception as e: 
        bot.send_message(message.chat.id, f"⚠️ ប្រព័ន្ធមានបញ្ហាក្នុងការបញ្ជូនទៅកាន់អ្នកគ្រប់គ្រង។\n\n`Error: {e}`", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "💵 ដាក់ប្រាក់")
def handle_deposit(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ បញ្ជាក់ការបង់ប្រាក់", callback_data="confirm_deposit"), InlineKeyboardButton("❌ បោះបង់", callback_data="cancel_deposit"))
    text = "**សូមស្វាគមន៍មកកាន់ការដាក់ប្រាក់!**\n\n🏦 **ធនាគារ**: ACLEDA Bank\n👤 **ឈ្មោះ**: LY SAEVLONG\n\n👉 សូមធ្វើការស្កេន QR Code ខាងលើដើម្បីវេរប្រាក់។ បន្ទាប់ពីវេរប្រាក់រួច សូមចុចប៊ូតុង **✅ បញ្ជាក់ការបង់ប្រាក់**។"
    qr_url = "https://img.sanishtech.com/u/a643db727d41e55abb4f8b49920c49e7.jpeg" 
    bot.send_photo(message.chat.id, qr_url, caption=text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["confirm_deposit", "cancel_deposit"])
def handle_deposit_action(call):
    bot.answer_callback_query(call.id)
    if call.data == "confirm_deposit":
        msg = bot.send_message(call.message.chat.id, "✅ សូមផ្ញើរូបភាពវិក្កយបត្រ (Screenshot) ដែលអ្នកបានវេរប្រាក់រួច មកកាន់ទីនេះឥឡូវនេះ។")
        bot.register_next_step_handler(msg, process_receipt)
    elif call.data == "cancel_deposit":
        bot.send_message(call.message.chat.id, "❌ ប្រតិបត្តិការដាក់ប្រាក់ត្រូវបានបោះបង់ដោយជោគជ័យ។")

def process_receipt(message):
    if message.text in ["👤 គណនី", "🎮 GAME TOPUP", "💵 ដាក់ប្រាក់", "👨‍💻 អ្នកគ្រប់គ្រង", "🔙 ត្រឡប់ក្រោយ"]:
        bot.send_message(message.chat.id, "❌ បានបោះបង់ការដាក់ប្រាក់។", reply_markup=get_main_menu())
        return
    if message.content_type == 'photo':
        user_id = message.from_user.id
        username = message.from_user.username
        username_text = f"@{username}" if username else "មិនមាន"
        bot.send_message(message.chat.id, "✅ យើងខ្ញុំបានទទួលវិក្កយបត្ររបស់អ្នកហើយ។ សូមមេត្ដារងចាំការត្រួតពិនិត្យពីអ្នកគ្រប់គ្រងបន្តិច។", parse_mode="Markdown")
        photo_id = message.photo[-1].file_id
        caption = f"🔔 **មានការដាក់ប្រាក់ថ្មី**\n\n🆔 ID អតិថិជន: `{user_id}`\n👤 Username: {username_text}"
        
        admin_markup = InlineKeyboardMarkup()
        admin_markup.add(InlineKeyboardButton("✅ ទទួលយក", callback_data=f"depapp_{user_id}"), InlineKeyboardButton("❌ បដិសេធ", callback_data=f"deprej_{user_id}"))
        admin_markup.add(InlineKeyboardButton("💬 ផ្ញើសារទៅអតិថិជន", callback_data=f"sendmsg_{user_id}"))
        
        try:
            bot.send_photo(ADMIN_GROUP_ID, photo_id, caption=caption, parse_mode="Markdown", reply_markup=admin_markup)
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ ប្រព័ន្ធមានបញ្ហាក្នុងការបញ្ជូនទៅកាន់អ្នកគ្រប់គ្រង។\n\n`Error: {e}`", parse_mode="Markdown")
    else:
        msg = bot.send_message(message.chat.id, "⚠️ សូមផ្ញើជាទម្រង់ **រូបភាព** (Photo) ប៉ុណ្ណោះ។ សូមផ្ញើវិក្កយបត្រម្ដងទៀត។", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_receipt)

@bot.callback_query_handler(func=lambda call: call.data.startswith("depapp_") or call.data.startswith("deprej_") or call.data.startswith("topapp_") or call.data.startswith("toprej_") or call.data.startswith("sendmsg_"))
def handle_admin_group_action(call):
    bot.answer_callback_query(call.id)
    data_parts = call.data.split('_')
    action = data_parts[0]
    user_id = int(data_parts[1])
    
    if action == "depapp":
        msg = bot.send_message(call.message.chat.id, f"✅ អ្នកគ្រប់គ្រងសូមវាយ **ចំនួនទឹកប្រាក់** ដែលចង់បញ្ចូលឲ្យអតិថិជន `{user_id}`:", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_deposit_amount, user_id, call.message)
    elif action == "deprej":
        bot.edit_message_caption((call.message.caption or "") + "\n\n❌ **ស្ថានភាព: បានបដិសេធ**", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
        try: bot.send_message(user_id, "❌ **ការដាក់ប្រាក់ត្រូវបានបដិសេធ!**\nសូមពិនិត្យមើលវិក្កយបត្រម្ដងទៀត។")
        except: pass
    elif action == "topapp":
        amount = float(data_parts[2])
        bot.edit_message_text((call.message.text or "") + "\n\n✅ **ស្ថានភាព: បានបញ្ជាក់រួចរាល់**", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
        try: bot.send_message(user_id, f"✅ **ការបញ្ជាទិញ Top Up របស់អ្នកទទួលបានជោគជ័យ!**\n(ទឹកប្រាក់ `${amount:.2f}` ត្រូវបានកាត់ចេញពីគណនីរួចរាល់)")
        except: pass
    elif action == "toprej":
        amount = float(data_parts[2])
        if user_id not in user_balances: user_balances[user_id] = 0.0
        user_balances[user_id] += amount
        bot.edit_message_text((call.message.text or "") + "\n\n❌ **ស្ថានភាព: បានបដិសេធ (ប្រគល់លុយវិញ)**", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
        try: bot.send_message(user_id, f"❌ **ការបញ្ជាទិញត្រូវបានបដិសេធ!**\nទឹកប្រាក់ `${amount:.2f}` ត្រូវបានប្រគល់ចូលគណនីរបស់អ្នកវិញ។")
        except: pass
    elif action == "sendmsg":
        msg = bot.send_message(call.message.chat.id, f"✏️ **សូមវាយសារដែលអ្នកចង់ផ្ញើទៅកាន់អតិថិជន (ID: `{user_id}`):**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_admin_message, user_id)

def process_admin_message(message, user_id):
    try:
        bot.send_message(user_id, f"💬 **សារពីអ្នកគ្រប់គ្រង៖**\n\n{message.text}", parse_mode="Markdown")
        bot.send_message(message.chat.id, "✅ សារត្រូវបានផ្ញើទៅកាន់អតិថិជនដោយជោគជ័យ!")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ មិនអាចផ្ញើសារបានទេ (អតិថិជនប្រហែលជា Block Bot ឬមានបញ្ហាផ្សេងៗ)។")

def process_deposit_amount(message, user_id, original_call_message):
    try:
        amount = float(message.text)
        if user_id not in user_balances: user_balances[user_id] = 0.0
        user_balances[user_id] += amount
        bot.edit_message_caption((original_call_message.caption or "") + f"\n\n✅ **ស្ថានភាព: បានអនុម័ត និងបញ្ចូលលុយ ${amount:.2f}**", chat_id=original_call_message.chat.id, message_id=original_call_message.message_id, parse_mode="Markdown")
        bot.send_message(user_id, f"✅ **ការដាក់ប្រាក់ជោគជ័យ!**\nអ្នកទទួលបានទឹកប្រាក់ចំនួន `${amount:.2f}` ចូលក្នុងគណនី។", parse_mode="Markdown")
        bot.send_message(message.chat.id, f"✅ បានបញ្ចូលលុយ `${amount:.2f}` ឲ្យអតិថិជនរូចរាល់។")
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ លេខមិនត្រឹមត្រូវ។ សូមចុចប៊ូតុង ✅ ទទួលយក ម្ដងទៀតដើម្បីវាយចំនួនប្រាក់។")

@bot.message_handler(func=lambda message: message.text == "👨‍💻 អ្នកគ្រប់គ្រង")
def handle_admin(message):
    bot.send_message(message.chat.id, "ប្រសិនបើអ្នកមានបញ្ហា សូមទំនាក់ទំនង៖ 👉 @PiSetHsPP")

@bot.message_handler(func=lambda message: message.text == "🔙 ត្រឡប់ក្រោយ")
def handle_back(message):
    bot.send_message(message.chat.id, "សូមជ្រើសរើសសេវាកម្មនៅខាងក្រោម៖", reply_markup=get_main_menu())

bot.infinity_polling()
