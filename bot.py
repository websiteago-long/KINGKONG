import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# មុខងារសម្រាប់បង្កើតប៊ូតុងទំព័រដើម
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🎮 GAME TOPUP"))
    return markup

# មុខងារសម្រាប់បង្កើតប៊ូតុងបញ្ជីហ្គេម
def get_game_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Roblox"))
    markup.add(KeyboardButton("Mobile Legends"))
    markup.add(KeyboardButton("Free Fire"))
    markup.add(KeyboardButton("🔙 ត្រឡប់ក្រោយ")) # ប៊ូតុងថយក្រោយ
    return markup

# មុខងារពេលអតិថិជនចុច /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "សួស្តី! សូមស្វាគមន៍មកកាន់សេវាកម្មរបស់យើងខ្ញុំ។ សូមជ្រើសរើសសេវាកម្មនៅខាងក្រោម៖", reply_markup=get_main_menu())

# មុខងារពេលអតិថិជនចុចប៊ូតុង "🎮 GAME TOPUP"
@bot.message_handler(func=lambda message: message.text == "🎮 GAME TOPUP")
def handle_game_topup(message):
    bot.send_message(message.chat.id, "សូមជ្រើសរើសហ្គេមដែលអ្នកចង់ Top Up ខាងក្រោម៖", reply_markup=get_game_menu())

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
