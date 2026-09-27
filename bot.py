import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# មុខងារសម្រាប់បង្កើតប៊ូតុងទំព័រដើម (មាន៣ប៊ូតុងរៀងគ្នា)
def get_main_menu():
    # row_width=3 មានន័យថាតម្រៀប៣ប៊ូតុងក្នុង១ជួរ
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn_account = KeyboardButton("👤 គណនី")
    btn_topup = KeyboardButton("🎮 GAME TOPUP")
    btn_admin = KeyboardButton("👨‍💻 អ្នកគ្រប់គ្រង")
    
    markup.add(btn_account, btn_topup, btn_admin)
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
    
    # ឆែកមើលថាគាត់មានដាក់ Username ក្នុង Telegram គាត់ឬអត់
    if username:
        username_text = f"@{username}"
    else:
        username_text = "មិនមាន"
        
    text = f"**ព័ត៌មានគណនីរបស់អ្នក៖**\n\n🆔 ID: `{user_id}`\n👤 Username: {username_text}"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

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
