import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

# ទាញយក Token ពី Variables នៅក្នុង Railway (សុវត្ថិភាព 100%)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# មុខងារពេលអតិថិជនចុច /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # បង្កើតប៊ូតុងនៅខាងក្រោម Keyboard
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_topup = KeyboardButton("🎮 GAME TOPUP")
    
    # បន្ថែមប៊ូតុងទៅក្នុងផ្ទាំង
    markup.add(btn_topup)

    bot.send_message(message.chat.id, "សួស្តី! សូមស្វាគមន៍មកកាន់សេវាកម្មរបស់យើងខ្ញុំ។ សូមជ្រើសរើសសេវាកម្មនៅខាងក្រោម៖", reply_markup=markup)

# មុខងារពេលអតិថិជនចុចប៊ូតុង "🎮 GAME TOPUP"
@bot.message_handler(func=lambda message: message.text == "🎮 GAME TOPUP")
def handle_game_topup(message):
    # បង្កើតប៊ូតុងជាប់សារ (Inline) សម្រាប់រាយឈ្មោះហ្គេម
    markup = InlineKeyboardMarkup()
    
    btn_roblox = InlineKeyboardButton("Roblox", callback_data="topup_roblox")
    btn_ml = InlineKeyboardButton("Mobile Legends", callback_data="topup_ml")
    btn_ff = InlineKeyboardButton("Free Fire", callback_data="topup_ff")
    
    # តម្រៀបប៊ូតុងទាំង៣បញ្ឈរចូលគ្នា (មួយជួរមួយ)
    markup.add(btn_roblox)
    markup.add(btn_ml)
    markup.add(btn_ff)

    bot.send_message(message.chat.id, "សូមជ្រើសរើសហ្គេមដែលអ្នកចង់ Top Up ខាងក្រោម៖", reply_markup=markup)

# មុខងារសម្រាប់ចាប់យកការចុចលើឈ្មោះហ្គេមនីមួយៗ
@bot.callback_query_handler(func=lambda call: call.data.startswith("topup_"))
def handle_topup_selection(call):
    if call.data == "topup_roblox":
        game_name = "Roblox"
    elif call.data == "topup_ml":
        game_name = "Mobile Legends"
    elif call.data == "topup_ff":
        game_name = "Free Fire"
        
    # ឆ្លើយតបទៅការចុចប៊ូតុងដើម្បីបិទការ loading វិលៗ
    bot.answer_callback_query(call.id)
    
    # ផ្ញើសារប្រាប់អតិថិជនពីហ្គេមដែលគាត់បានរើស
    bot.send_message(
        call.message.chat.id, 
        f"អ្នកបានជ្រើសរើសហ្គេម **{game_name}**។\n\nសូមផ្ញើព័ត៌មាន (ID ហ្គេម ឬ ឈ្មោះ) និងចំនួនដែលអ្នកចង់ Top up មកកាន់យើងខ្ញុំនៅទីនេះ។", 
        parse_mode="Markdown"
    )

bot.infinity_polling()
