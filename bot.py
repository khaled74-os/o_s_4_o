import telebot
from telebot.types import Message
from PIL import Image, ImageOps
import requests
from io import BytesIO

# استبدل 'YOUR_BOT_TOKEN' برمز البوت الخاص بك
BOT_TOKEN = '7329718611:AAE190cMx8Jlwae5lpF_lKnQ2siCi4FrPo8'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, "مرحباً! أرسل /photo لبدء معالجة الصور.")

@bot.message_handler(commands=['photo'])
def ask_for_photo(message: Message):
    bot.reply_to(message, "أرسل الصورة التي ترغب في تطبيق الفلتر البنفسجي عليها.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    # تحميل الصورة من التليجرام
    file_info = bot.get_file(message.photo[-1].file_id)
    photo_bytes = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}').content
    image = Image.open(BytesIO(photo_bytes))

    # تطبيق الفلتر البنفسجي
    purple_image = ImageOps.colorize(image.convert("L"),  black="black", white="rgb(181,118,211)")

    bio = BytesIO()
    bio.name = 'filtered_image.jpeg'
    purple_image.save(bio, 'JPEG')
    bio.seek(0)

    bot.send_photo(message.chat.id, bio, caption='إليك صورتك بالفلتر البنفسجي!')

bot.polling()