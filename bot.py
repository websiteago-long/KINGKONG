import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

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

# មុខងារពេលអតិថិជនចុច /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "សួស្តី! សូមស្វាគមន៍មកកាន់សេវាកម្មរបស់យើងខ្ញុំ។ សូមជ្រើសរើសសេវាកម្មនៅខាងក្រោម៖", reply_markup=get_main_menu())

# មុខងារពេលអតិថិជនចុចប៊ូតុង "🎮 GAME TOPUP"
@bot.message_handler(func=lambda message: message.text == "🎮 GAME TOPUP")
def handle_game_topup(message):
    bot.send_message(message.chat.id, "សូមជ្រើសរើសហ្គេមដែលអ្នកចង់ Top Up ខាងក្រោម៖", reply_markup=get_game_menu())

# មុខងារពេលអតិថិជនចុចប៊ូតុង "👤 គណនី"
@bot.message_handler(func=lambda message: message.text == "👤 គណនី")
def handle_account(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    username_text = f"@{username}" if username else "មិនមាន"
    balance = 0.00
        
    text = f"**ព័ត៌មានគណនីរបស់អ្នក៖**\n\n🆔 ID: `{user_id}`\n👤 Username: {username_text}\n💰 ទឹកប្រាក់ចំនួន: `${balance}`"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# មុខងារពេលអតិថិជនចុចប៊ូតុង "💵 ដាក់ប្រាក់"
@bot.message_handler(func=lambda message: message.text == "💵 ដាក់ប្រាក់")
def handle_deposit(message):
    # បង្កើតប៊ូតុង បញ្ជាក់ និង បោះបង់ ជាប់ជាមួយរូបភាព
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
    
    # ប្រើប្រាស់ Link រូបភាព QR Code របស់បងដោយផ្ទាល់
    qr_url = "https://img.sanishtech.com/u/a643db727d41e55abb4f8b49920c49e7.jpeg" 
    
    try:
        bot.send_photo(message.chat.id, qr_url, caption=text, parse_mode="Markdown", reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, "⚠️ សូមអភ័យទោស រូបភាព QR មានបញ្ហាក្នុងការទាញយក។\n\n" + text, parse_mode="Markdown", reply_markup=markup)

# មុខងារចាប់យកការចុចប៊ូតុង បញ្ជាក់ ឬ បោះបង់
@bot.callback_query_handler(func=lambda call: call.data in ["confirm_deposit", "cancel_deposit"])
def handle_deposit_action(call):
    bot.answer_callback_query(call.id) # បិទការ loading វិលៗ
    
    if call.data == "confirm_deposit":
        msg = bot.send_message(call.message.chat.id, "✅ សូមផ្ញើរូបភាពវិក្កយបត្រ (Screenshot) ដែលអ្នកបានវេរប្រាក់រួច មកកាន់ទីនេះឥឡូវនេះ។")
        bot.register_next_step_handler(msg, process_receipt)
    elif call.data == "cancel_deposit":
        bot.send_message(call.message.chat.id, "❌ ប្រតិបត្តិការដាក់ប្រាក់ត្រូវបានបោះបង់ដោយជោគជ័យ។")

# មុខងារចាំទទួលយករូបភាពវិក្កយបត្រពីអតិថិជន
def process_receipt(message):
    if message.content_type == 'photo':
        bot.send_message(message.chat.id, "✅ **ជោគជ័យ!**\n\nយើងខ្ញុំបានទទួលវិក្កយបត្ររបស់អ្នកហើយ។ សូមរង់ចាំការត្រួតពិនិត្យពីអ្នកគ្រប់គ្រងបន្តិច ទំហំទឹកប្រាក់នឹងត្រូវបានបញ្ចូលទៅក្នុងគណនីរបស់អ្នកឆាប់ៗនេះ។", parse_mode="Markdown")
    else:
        msg = bot.send_message(message.chat.id, "⚠️ សូមផ្ញើជាទម្រង់ **រូបភាព** (Photo) ប៉ុណ្ណោះ។ សូមផ្ញើវិក្កយបត្រម្ដងទៀត។", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_receipt)

# មុខងារពេលអតិថិជនចុចប៊ូតុង "👨‍💻 អ្នកគ្រប់គ្រង"
@bot.message_handler(func=lambda message: message.text == "👨‍💻 អ្នកគ្រប់គ្រង")
def handle_admin(message):
    bot.send_message(message.chat.id, "ប្រសិនបើអ្នកមានបញ្ហា ឬសំណួរផ្សេងៗ សូមទំនាក់ទំនងអ្នកគ្រប់គ្រងតាមរយៈ៖\n👉 @PiSetHsPP")

# មុខងារពេលអតិថិជនចុចលើឈ្មោះហ្គេមណាមួយ
@bot.message_handler(func=lambda message: message.text in ["Roblox", "Mobile Legends", "Free Fire"])
def handle_topup_selection(message):
    game_name = message.text
    bot.send_message(
        message.chat.id, 
        f"អ្នកបានជ្រើសរើសហ្គេម **{game_name}**។\n\nសូមផ្ញើព័ត៌មាន (ID ហ្គេម ឬ ឈ្មោះ) និងចំនួនដែលអ្នកចង់ Top up មកកាន់យើងខ្ញុំនៅទីនេះ។", 
        parse_mode="Markdown"
    )

# មុខងារពេលអតិថិជនចុចប៊ូតុង "🔙 ត្រឡប់ក្រោយ"
@bot.message_handler(func=lambda message: message.text == "🔙 ត្រឡប់ក្រោយ")
def handle_back(message):
    bot.send_message(message.chat.id, "សូមជ្រើសរើសសេវាកម្មនៅខាងក្រោម៖", reply_markup=get_main_menu())

bot.infinity_polling()
