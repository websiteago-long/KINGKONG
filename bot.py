import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# ដាក់ ID គ្រុបអ្នកគ្រប់គ្រង (Admin Group ID) ដែលបងបានផ្ដល់ឲ្យ
ADMIN_GROUP_ID = "-1003875548933"

# មុខងារសម្រាប់បង្កើតប៊ូតុងទំព័រដើម 
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_account = KeyboardButton("👤 គណនី")
    btn_topup = KeyboardButton("🎮 GAME TOPUP")
    btn_deposit = KeyboardButton("💵 ដាក់ប្រាក់")
    btn_admin = KeyboardButton("👨‍💻 អ្នកគ្រប់គ្រង")
    
    markup.add(btn_account, btn_topup, btn_deposit, btn_admin)
    return markup

# មុខងារសម្រាប់បង្កើតប៊ូតុងបញ្ជីហ្គេម
def get_game_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_roblox = KeyboardButton("Roblox")
    btn_ml = KeyboardButton("Mobile Legends")
    btn_ff = KeyboardButton("Free Fire")
    btn_back = KeyboardButton("🔙 ត្រឡប់ក្រោយ")
    
    markup.add(btn_roblox, btn_ml, btn_ff)
    markup.add(btn_back)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "សួស្តី! សូមស្វាគមន៍មកកាន់សេវាកម្មរបស់យើងខ្ញុំ។ សូមជ្រើសរើសសេវាកម្មនៅខាងក្រោម៖", reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: message.text == "🎮 GAME TOPUP")
def handle_game_topup(message):
    bot.send_message(message.chat.id, "សូមជ្រើសរើសហ្គេមដែលអ្នកចង់ Top Up ខាងក្រោម៖", reply_markup=get_game_menu())

@bot.message_handler(func=lambda message: message.text == "👤 គណនី")
def handle_account(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    username_text = f"@{username}" if username else "មិនមាន"
    balance = 0.00
        
    text = f"**ព័ត៌មានគណនីរបស់អ្នក៖**\n\n🆔 ID: `{user_id}`\n👤 Username: {username_text}\n💰 ទឹកប្រាក់ចំនួន: `${balance}`"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# មុខងារពេលអតិថិជនចុចលើឈ្មោះហ្គេមណាមួយ
@bot.message_handler(func=lambda message: message.text in ["Roblox", "Mobile Legends", "Free Fire"])
def handle_topup_selection(message):
    game_name = message.text
    msg = bot.send_message(
        message.chat.id, 
        f"អ្នកបានជ្រើសរើសហ្គេម **{game_name}**។\n\nសូមផ្ញើព័ត៌មាន (ID ហ្គេម ឬ ឈ្មោះ) និងចំនួនដែលអ្នកចង់ Top up មកកាន់យើងខ្ញុំនៅទីនេះ។", 
        parse_mode="Markdown"
    )
    # ចាំទទួលព័ត៌មាន ID ហ្គេមពីអតិថិជន
    bot.register_next_step_handler(msg, process_topup_order, game_name)

# មុខងារបញ្ជូនការបញ្ជាទិញ Top up ទៅកាន់ Group Admin
def process_topup_order(message, game_name):
    # បើគាត់ចុចប៊ូតុង Menu ផ្សេង គឺបោះបង់ការទិញ
    if message.text in ["👤 គណនី", "🎮 GAME TOPUP", "💵 ដាក់ប្រាក់", "👨‍💻 អ្នកគ្រប់គ្រង", "🔙 ត្រឡប់ក្រោយ"]:
        bot.send_message(message.chat.id, "❌ បានបោះបង់ការបញ្ជាទិញ។", reply_markup=get_main_menu())
        return
        
    user_id = message.from_user.id
    username = message.from_user.username
    username_text = f"@{username}" if username else "មិនមាន"
    order_details = message.text if message.text else "ផ្ញើជាឯកសារ/រូបភាព"
    
    bot.send_message(message.chat.id, "✅ យើងខ្ញុំបានទទួលការបញ្ជាទិញរបស់អ្នកហើយ។ សូមមេត្ដារងចាំការត្រួតពិនិត្យពីអ្នកគ្រប់គ្រងបន្តិច។", parse_mode="Markdown")
    
    caption = f"🎮 **មានការបញ្ជាទិញ TOPUP ថ្មី**\n\n🕹 ហ្គេម: {game_name}\n📝 ព័ត៌មានអតិថិជនផ្ញើមក: {order_details}\n\n🆔 ID អតិថិជន: `{user_id}`\n👤 Username: {username_text}"
    
    admin_markup = InlineKeyboardMarkup()
    btn_approve = InlineKeyboardButton("✅ បញ្ជាក់ការទិញ", callback_data=f"topapp_{user_id}")
    btn_reject = InlineKeyboardButton("❌ បដិសេធ", callback_data=f"toprej_{user_id}")
    admin_markup.add(btn_approve, btn_reject)
    
    try:
        bot.send_message(ADMIN_GROUP_ID, caption, parse_mode="Markdown", reply_markup=admin_markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ សូមអភ័យទោស ប្រព័ន្ធមានបញ្ហាក្នុងការបញ្ជូនទៅកាន់អ្នកគ្រប់គ្រង។ (សូម Admin Add Bot ចូល Group {ADMIN_GROUP_ID} ជាមុនសិន)")

@bot.message_handler(func=lambda message: message.text == "💵 ដាក់ប្រាក់")
def handle_deposit(message):
    markup = InlineKeyboardMarkup()
    btn_confirm = InlineKeyboardButton("✅ បញ្ជាក់ការបង់ប្រាក់", callback_data="confirm_deposit")
    btn_cancel = InlineKeyboardButton("❌ បោះបង់", callback_data="cancel_deposit")
    markup.add(btn_confirm)
    markup.add(btn_cancel)

    text = (
        "**សូមស្វាគមន៍មកកាន់ការដាក់ប្រាក់!**\n\n"
        "🏦 **ធនាគារ**: ACLEDA Bank\n"
        "👤 **ឈ្មោះ**: LY SAEVLONG\n\n"
        "👉 សូមធ្វើការស្កេន QR Code ខាងលើដើម្បីវេរប្រាក់។ បន្ទាប់ពីវេរប្រាក់រួច សូមចុចប៊ូតុង **✅ បញ្ជាក់ការបង់ប្រាក់** ដើម្បីបញ្ជូនវិក្កយបត្រមកកាន់យើងខ្ញុំ។"
    )
    
    qr_url = "https://img.sanishtech.com/u/a643db727d41e55abb4f8b49920c49e7.jpeg" 
    try:
        bot.send_photo(message.chat.id, qr_url, caption=text, parse_mode="Markdown", reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, "⚠️ រូបភាព QR មានបញ្ហាក្នុងការទាញយក។\n\n" + text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["confirm_deposit", "cancel_deposit"])
def handle_deposit_action(call):
    bot.answer_callback_query(call.id)
    if call.data == "confirm_deposit":
        msg = bot.send_message(call.message.chat.id, "✅ សូមផ្ញើរូបភាពវិក្កយបត្រ (Screenshot) ដែលអ្នកបានវេរប្រាក់រួច មកកាន់ទីនេះឥឡូវនេះ។")
        bot.register_next_step_handler(msg, process_receipt)
    elif call.data == "cancel_deposit":
        bot.send_message(call.message.chat.id, "❌ ប្រតិបត្តិការដាក់ប្រាក់ត្រូវបានបោះបង់ដោយជោគជ័យ។")

# មុខងារចាំទទួលយករូបភាពវិក្កយបត្រ និងបញ្ជូនទៅ Group Admin
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
        btn_approve = InlineKeyboardButton("✅ ទទួលយក", callback_data=f"depapp_{user_id}")
        btn_reject = InlineKeyboardButton("❌ បដិសេធ", callback_data=f"deprej_{user_id}")
        admin_markup.add(btn_approve, btn_reject)
        
        try:
            bot.send_photo(ADMIN_GROUP_ID, photo_id, caption=caption, parse_mode="Markdown", reply_markup=admin_markup)
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ សូមអភ័យទោស ប្រព័ន្ធមានបញ្ហាក្នុងការបញ្ជូនទៅកាន់អ្នកគ្រប់គ្រង។ (សូម Admin Add Bot ចូល Group {ADMIN_GROUP_ID} ជាមុនសិន)")
    else:
        msg = bot.send_message(message.chat.id, "⚠️ សូមផ្ញើជាទម្រង់ **រូបភាព** (Photo) ប៉ុណ្ណោះ។ សូមផ្ញើវិក្កយបត្រម្ដងទៀត។", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_receipt)

# មុខងារចាំទទួលការចុចប៊ូតុងរបស់ Admin នៅក្នុង Group
@bot.callback_query_handler(func=lambda call: call.data.startswith("depapp_") or call.data.startswith("deprej_") or call.data.startswith("topapp_") or call.data.startswith("toprej_"))
def handle_admin_group_action(call):
    bot.answer_callback_query(call.id)
    
    data_parts = call.data.split('_')
    action = data_parts[0]
    user_id = data_parts[1]
    
    # ករណី Admin ចុច ទទួលយកការដាក់ប្រាក់
    if action == "depapp":
        new_caption = (call.message.caption or "") + "\n\n✅ **ស្ថានភាព: បានទទួលយក (Approved)**"
        bot.edit_message_caption(new_caption, chat_id=call.message.chat.id, message_id=call.message.message_id)
        try: bot.send_message(user_id, "✅ **ការដាក់ប្រាក់របស់អ្នកទទួលបានជោគជ័យ!**\nទឹកប្រាក់ត្រូវបានបញ្ជាក់ដោយអ្នកគ្រប់គ្រង។", parse_mode="Markdown")
        except: pass
    
    # ករណី Admin ចុច បដិសេធការដាក់ប្រាក់
    elif action == "deprej":
        new_caption = (call.message.caption or "") + "\n\n❌ **ស្ថានភាព: បានបដិសេធ (Rejected)**"
        bot.edit_message_caption(new_caption, chat_id=call.message.chat.id, message_id=call.message.message_id)
        try: bot.send_message(user_id, "❌ **ការដាក់ប្រាក់របស់អ្នកត្រូវបានបដិសេធ!**\nសូមពិនិត្យមើលវិក្កយបត្រម្ដងទៀត ឬទាក់ទងអ្នកគ្រប់គ្រង (@PiSetHsPP)។", parse_mode="Markdown")
        except: pass
        
    # ករណី Admin ចុច បញ្ជាក់ការបញ្ជាទិញ Top Up
    elif action == "topapp":
        new_text = (call.message.text or "") + "\n\n✅ **ស្ថានភាព: បានបញ្ជាក់ (Completed)**"
        bot.edit_message_text(new_text, chat_id=call.message.chat.id, message_id=call.message.message_id)
        try: bot.send_message(user_id, "✅ **ការបញ្ជាទិញ Top Up របស់អ្នកទទួលបានជោគជ័យ!**\nសូមចូលទៅពិនិត្យមើលក្នុងគណនីហ្គេមរបស់អ្នក។", parse_mode="Markdown")
        except: pass
        
    # ករណី Admin ចុច បដិសេធការបញ្ជាទិញ Top Up
    elif action == "toprej":
        new_text = (call.message.text or "") + "\n\n❌ **ស្ថានភាព: បានបដិសេធ (Rejected)**"
        bot.edit_message_text(new_text, chat_id=call.message.chat.id, message_id=call.message.message_id)
        try: bot.send_message(user_id, "❌ **ការបញ្ជាទិញ Top Up របស់អ្នកត្រូវបានបដិសេធ!**\nសូមត្រួតពិនិត្យព័ត៌មានរបស់អ្នកម្ដងទៀត ឬទាក់ទងអ្នកគ្រប់គ្រង។", parse_mode="Markdown")
        except: pass

@bot.message_handler(func=lambda message: message.text == "👨‍💻 អ្នកគ្រប់គ្រង")
def handle_admin(message):
    bot.send_message(message.chat.id, "ប្រសិនបើអ្នកមានបញ្ហា ឬសំណួរផ្សេងៗ សូមទំនាក់ទំនងអ្នកគ្រប់គ្រងតាមរយៈ៖\n👉 @PiSetHsPP")

@bot.message_handler(func=lambda message: message.text == "🔙 ត្រឡប់ក្រោយ")
def handle_back(message):
    bot.send_message(message.chat.id, "សូមជ្រើសរើសសេវាកម្មនៅខាងក្រោម៖", reply_markup=get_main_menu())

bot.infinity_polling()
