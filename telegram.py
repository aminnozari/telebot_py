import random
from gtts import gTTS
import telebot
from telebot import types
from telebot import TeleBot
from khayyam import JalaliDatetime
import datetime
import qrcode
bot = TeleBot("5337410070:AAGvUj5gYf00DWJK7Bv3wU6aSSrq707Ev8Q")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, welcome to my bot Mr/Mrs" +
                 message.from_user.first_name +
                 "for use my code sent to me /help")
@bot.message_handler(commands=['game'])
def start_game(message):
    msg = bot.send_message(
        message.chat.id, 'Guess the number!\nSend /NewGame to start \nSend / to Stop')
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


def game(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn = types.KeyboardButton('/NewGame')
    markup.add(btn)
    if message.text == '/':
        bot.send_message(message.chat.id, 'Stopped',
                         reply_markup=types.ReplyKeyboardRemove(selective=True))
    else:
        try:
            if message.text == '/NewGame':
                global random_number
                random_number = random.randint(0, 50)
                bot.send_message(message.chat.id, 'New Game\nGuess the number:',
                                 reply_markup=markup)
                bot.register_next_step_handler_by_chat_id(
                    message.chat.id, game)
            elif int(message.text) < random_number:
                msg = bot.send_message(
                    message.chat.id, 'Go Higher', reply_markup=markup)
                bot.register_next_step_handler(msg, game)
            elif int(message.text) > random_number:
                msg = bot.send_message(
                    message.chat.id, 'Go Lower', reply_markup=markup)
                bot.register_next_step_handler(msg, game)
            else:
                bot.send_message(message.chat.id, 'You Won!',
                                 reply_markup=types.ReplyKeyboardRemove(selective=True))
        except:
            msg = bot.send_message(
                message.chat.id, 'Please send a valid number or Send / to Stop', reply_markup=markup)
            bot.register_next_step_handler(msg, game)


def age(message):
    if message.text == '/':
        bot.send_message(
            message.chat.id, 'Stopped')
    else:
        try:
            if len(message.text.split('/')) == 3:
                date_difference = JalaliDatetime.now(
                ) - JalaliDatetime(message.text.split('/')[0], message.text.split('/')[1], message.text.split('/')[2])
                bot.send_message(message.chat.id, 'You are about ' +
                                 str(date_difference.days // 365))
            else:
                msg = bot.send_message(
                    message.chat.id, 'Please send valid input or send /')
                bot.register_next_step_handler(msg, age)
        except:
            msg = bot.send_message(
                message.chat.id, 'Please send valid input or send /')
            bot.register_next_step_handler(msg, age)


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


def argmax(message):
    if message.text == '/':
        bot.send_message(
            message.chat.id, 'Stopped')
    else:
        try:
            numbers = list(map(int, message.text.split(',')))
            bot.send_message(message.chat.id, 'Maximum number index: ' +
                             str(numbers.index(max(numbers))))
        except:
            msg = bot.send_message(
                message.chat.id, 'Please send valid input or send /')
            bot.register_next_step_handler(msg, argmax)


def qr_code(message):
    if message.text == '/':
        bot.send_message(
            message.chat.id, 'Stopped')
    else:
        try:
            qrcode_img = qrcode.make(message.text)
            qrcode_img.save('QR-Code.png')
            photo = open('QR-Code.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        except:
            msg = bot.send_message(
                message.chat.id, 'Somethong went wrong!\nPlease send valid input or send /')
            bot.register_next_step_handler(msg, qr_code)


bot.infinity_polling()
