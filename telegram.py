import random
from gtts import gTTS
import telebot
from telebot import types
bot = telebot.TeleBot("5337410070:AAGvUj5gYf00DWJK7Bv3wU6aSSrq707Ev8Q")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, welcome to my bot Mr/Mrs" +
                 message.from_user.first_name)
@bot.message_handler(commands=['game'])
def start_game(message):
    msg = bot.send_message(
        message.chat.id, 'Guess the number!\nSend / to Stop')
    bot.register_next_step_handler(msg, game)
@bot.message_handler(commands=['age'])
def send_age(message):
    msg = bot.send_message(
        message.chat.id, 'Send your birthday like: 1350/5/5\nSend / to Stop')
    bot.register_next_step_handler(msg, age)
@bot.message_handler(commands=['voice'])
def send_voice(message):
    msg = bot.send_message(
        message.chat.id, 'Send an English sentence\nSend / to Stop')
    bot.register_next_step_handler(msg, voice)
@bot.message_handler(commands=['max'])
def send_max(message):
    msg = bot.send_message(
        message.chat.id, 'Send numbers like: 1,2,3,4,5 to for maximum\nSend / to Stop')
    bot.register_next_step_handler(msg, max_arr)
@bot.message_handler(commands=['argmax'])
def send_argmax(message):
    msg = bot.send_message(
        message.chat.id, 'Send numbers like: 1,2,3,4,5 to for maximum index\nSend / to Stop')
    bot.register_next_step_handler(msg, argmax)
@bot.message_handler(commands=['qrcode'])
def send_qrcode(message):
    msg = bot.send_message(
        message.chat.id, 'Send something to find its QR-Code\nSend / to Stop')
    bot.register_next_step_handler(msg, qr_code)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id,
                     """All works that I can are :
/start
 (To say hello with your name account)
/game 
 (Game that you should guess my number to win)
/age
 (If you want to undrestand how old are you from your brithday date)
/voice
 (To pronounce your English context as voice message)
/max
 (Find maximum in integers array)
/argmax
 (To find max index of integer array)
/qrcode
 (To do qrcode on your context)
/help
        """)
random_number = random.randint(-20, 20)
def voice(message):
    if message.text == '/':
        bot.send_message(
            message.chat.id, 'Stopped')
    else:
        try:
            content = gTTS(text=message.text, slow=False)
            content.save('voice.ogg')
            content = open('voice.ogg', 'rb')
            bot.send_voice(message.chat.id, content)
        except:
            msg = bot.send_message(
                message.chat.id, 'Please send valid input or send /')
            bot.register_next_step_handler(msg, voice)

def max_arr(message):
    if message.text == '/':
        bot.send_message(
            message.chat.id, 'Stopped')
    else:
        try:
            numbers = list(map(int, message.text.split(',')))
            bot.send_message(
                message.chat.id, 'Maximum number : ' + str(max(numbers)))
        except:
            msg = bot.send_message(
                message.chat.id, 'Please send valid input or send /')
            bot.register_next_step_handler(msg, max_arr)

def qrcode(message):
    if message.text == "/":
        bot.send_message(
            message.chat.id , 'stopped'
        )
    else:
        try:
            qrcode_img = qrcode.make(message.text)
            qrcode_img.save('QR-Code.png')
            photo = open('QR-Code.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        except:
            msg = bot.send_message(
                message.chat.id, 'Somethong went wrong!\nPlease send valid input or send /')
            bot.register_next_step_handler(msg, qrcode)
            
bot.infinity_polling()