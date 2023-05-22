import random
from gtts import gTTS
import telebot
from telebot import types
from telebot import TeleBot
from khayyam import JalaliDatetime
import qrcode

bot = TeleBot("YOUR_BOT_TOKEN_HERE")


# پیام خوش‌آمدگویی که در هنگام اجرای دستور /start ارسال می‌شود
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 سلام، به ربات من خوش آمدید آقای/خانم "
        + message.from_user.first_name
        + ". برای استفاده از کد من، /help را ارسال کنید",
    )


# تابع بازی برای حدس عدد
@bot.message_handler(commands=["game"])
def start_game(message):
    msg = bot.send_message(
        message.chat.id,
        "🎮 حدس عدد!\nبرای شروع /NewGame را ارسال کنید و برای خروج /stop را ارسال کنید",
    )
    bot.register_next_step_handler(msg, game)


# تابع محاسبه سن بر اساس تاریخ تولد
@bot.message_handler(commands=["age"])
def send_age(message):
    msg = bot.send_message(
        message.chat.id,
        "🎂 تاریخ تولد خود را مانند این شکل وارد کنید: 1350/5/5 یا /stop برای خروج",
    )
    bot.register_next_step_handler(msg, age)


# تابع تبدیل جمله انگلیسی به پیام صوتی
@bot.message_handler(commands=["voice"])
def send_voice(message):
    msg = bot.send_message(
        message.chat.id, "🔊 یک جمله انگلیسی ارسال کنید یا /stop برای خروج"
    )
    bot.register_next_step_handler(msg, voice)


# تابع برای پیدا کردن بزرگترین عدد در آرایه اعداد صحیح
@bot.message_handler(commands=["max"])
def send_max(message):
    msg = bot.send_message(
        message.chat.id,
        "🔢 اعدادی مانند: 1,2,3,4,5 ارسال کنید تا بزرگترین عدد را پیدا کنید یا /stop برای خروج",
    )
    bot.register_next_step_handler(msg, max_arr)


# تابع برای پیدا کردن اندیس بزرگترین عدد در آرایه اعداد صحیح
@bot.message_handler(commands=["argmax"])
def send_argmax(message):
    msg = bot.send_message(
        message.chat.id,
        "🔢 اعدادی مانند: 1,2,3,4,5 ارسال کنید تا اندیس بزرگترین عدد را پیدا کنید یا /stop برای خروج",
    )
    bot.register_next_step_handler(msg, argmax)


# تابع تولید کد QR برای ورودی داده شده
@bot.message_handler(commands=["qrcode"])
def send_qrcode(message):
    msg = bot.send_message(
        message.chat.id, "📷 یک متنی ارسال کنید تا کد QR آن تولید شود یا /stop برای خروج"
    )
    bot.register_next_step_handler(msg, qr_code)


# پیام راهنما که لیستی از تمام دستورات موجود را نشان می‌دهد
@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(
        message.chat.id,
        """این لیستی از دستوراتی است که من پشتیبانی می‌کنم:
🚀 /start
(به شما سلام می‌کند و با نام شما آشنا می‌شود)
🎮 /game 
(بازی حدس عدد)
🎂 /age
(محاسبه سن شما بر اساس تاریخ تولد)
🔊 /voice
(تبدیل یک جمله انگلیسی به پیام صوتی)
🔢 /max
(پیدا کردن بزرگترین عدد در یک آرایه اعداد صحیح)
🎯 /argmax
(پیدا کردن اندیس بزرگترین عدد در یک آرایه اعداد صحیح)
📷 /qrcode
(تولید کد QR برای ورودی داده شده)
ℹ️ /help
(نمایش این پیام راهنما)""",
    )


# متغیر جهانی برای ذخیره عدد تصادفی در تابع بازی
random_number = random.randint(-20, 20)


# پیاده‌سازی تابع بازی
def game(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn = types.KeyboardButton("/NewGame")
    markup.add(btn)
    if message.text == "/stop":
        bot.send_message(
            message.chat.id,
            "🚫 بازی متوقف شد",
            reply_markup=types.ReplyKeyboardRemove(selective=True),
        )
    else:
        try:
            if message.text == "/NewGame":
                global random_number
                random_number = random.randint(-20, 20)
                bot.send_message(
                    message.chat.id, "🎮 بازی جدید شروع شد. عددی را حدس بزنید!"
                )

            elif int(message.text) == random_number:
                bot.send_message(
                    message.chat.id,
                    "🎉 تبریک می‌گویم، شما برنده شدید!",
                    reply_markup=types.ReplyKeyboardRemove(selective=True),
                )
            elif int(message.text) < random_number:
                bot.send_message(message.chat.id, "⬇️ خیلی کم است، دوباره امتحان کنید")
            elif int(message.text) > random_number:
                bot.send_message(
                    message.chat.id, "⬆️ خیلی زیاد است، دوباره امتحان کنید"
                )

            bot.register_next_step_handler(message, game)

        except ValueError:
            bot.send_message(message.chat.id, "❗️ لطفاً یک عدد وارد کنید")


# پیاده‌سازی تابع محاسبه سن
def age(message):
    if message.text == "/":
        bot.send_message(message.chat.id, "Stopped")
    else:
        try:
            if len(message.text.split("/")) == 3:
                date_difference = JalaliDatetime.now() - JalaliDatetime(
                    message.text.split("/")[0],
                    message.text.split("/")[1],
                    message.text.split("/")[2],
                )
                bot.send_message(
                    message.chat.id, "شما حدودا " + str(date_difference.days // 365)
                )
            else:
                msg = bot.send_message(message.chat.id, "لطفا ورودی درست وارد کنید /")
                bot.register_next_step_handler(msg, age)
        except:
            msg = bot.send_message(message.chat.id, "لطفا ورودی درست وارد کنید /")
            bot.register_next_step_handler(msg, age)


# پیاده‌سازی تابع تولید پیام صوتی
def voice(message):
    try:
        text = message.text
        language = "en"
        myobj = gTTS(text=text, lang=language, slow=False)
        myobj.save("voice_message.mp3")

        with open("voice_message.mp3", "rb") as voice:
            bot.send_voice(message.chat.id, voice, caption="🔊 اینجا پیام صوتی شماست!")
    except Exception as e:
        bot.send_message(message.chat.id, "❗️ اوه! مشکلی پیش آمد...")
        print(e)


# پیاده‌سازی تابع بزرگترین عدد
def max_arr(message):
    try:
        numbers = message.text.split(",")
        max_num = max(list(map(int, numbers)))
        bot.send_message(message.chat.id, f"🔢 بزرگترین عدد {max_num} است")

    except Exception as e:
        bot.send_message(message.chat.id, "❗️ اوه! مشکلی پیش آمد...")
        print(e)


# پیاده‌سازی تابع اندیس بزرگترین عدد
def argmax(message):
    try:
        numbers = message.text.split(",")
        index_max = max(range(len(numbers)), key=lambda i: int(numbers[i]))
        bot.send_message(message.chat.id, f"🎯 اندیس بزرگترین عدد {index_max} است")

    except Exception as e:
        bot.send_message(message.chat.id, "❗️ اوه! مشکلی پیش آمد...")
        print(e)


# پیاده‌سازی تابع تولید کد QR
def qr_code(message):
    try:
        img = qrcode.make(message.text)
        img.save("qrcode.png")

        with open("qrcode.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="📷 اینجا کد QR شماست!")

    except Exception as e:
        bot.send_message(message.chat.id, "❗️ اوه! مشکلی پیش آمد...")
        print(e)


bot.polling()
