import webbrowser
import telebot
import requests
import datetime
import random
import saper
from pprint import pprint
from telebot import types
from config import open_weather_token
from config import private_bot_token

bot = telebot.TeleBot(private_bot_token)

@bot.message_handler(commands = ['weather']) # реагирует на команду 'weather'
def weather(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton('Погода в любом городе'), types.KeyboardButton('Погода рядом'))
    msg = bot.send_message(message.chat.id, "Выберите кнопку",reply_markup=markup)
    bot.register_next_step_handler(msg, help_func)

def help_func(message):
    if message.text == "Погода в любом городе":
        msg = bot.send_message(message.chat.id, "Введите город")
        bot.register_next_step_handler(msg, get_coord_city)
    else:
        get_coord_user(message)

def get_coord_city(message):
        reductions = {
            "krd": "Krasnodar",
            "nsk": "Novosibirsk",
            "msk": "Moscow",
            "крд": "Krasnodar",
            "нск": "Novosibirsk",
            "мск": "Moscow"
        }

        if message.text.lower() in reductions:
            message.text = reductions[message.text.lower()]

        l = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={message.text},&limit=1&appid={open_weather_token}&units=metric"
        )

        data = l.json()
        lat = data[0]["lat"]  # широта
        lon = data[0]["lon"]  # долгота
        get_weather(message, lat, lon)

def get_coord_user(message):
    markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    markup.add(button_geo)
    bot.send_message(message.chat.id,"У кого чистая советь, тому скрывать нечего. Показывай!", reply_markup=markup)
    @bot.message_handler(content_types=['location'])
    def location (message):
        if message.location is not None:
            get_weather(message,message.location.latitude, message.location.longitude)

def get_weather(message, lat , lon):
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&units=metric&lang=ru"
    )
    data1 = r.json()
    time_zone = (25200 - data1["timezone"])

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U0001F325",
        "Rain": "Дождь \U0001F327",
        "Drizzle": "Дождь \U0001F326",
        "Thunderstorm": "Гроза \U000026C8",
        "Snow": "Снег \U00002744",
        "Mist": "Туман \U0001F32B"
    }

    city = data1["name"]
    humidity = data1["main"]["humidity"] #влажность
    temp = data1["main"]["temp"]
    temp_max = data1["main"]["temp_max"]
    temp_min = data1["main"]["temp_min"]
    feels_like = data1["main"]["feels_like"]
    wind_speed = data1["wind"]["speed"]
    offset = datetime.timedelta(hours=data1["timezone"]/3600)
    tz = datetime.timezone(offset, name='МСК')
    sunrise = datetime.datetime.fromtimestamp(data1["sys"]["sunrise"] - time_zone)
    sunset = datetime.datetime.fromtimestamp(data1["sys"]["sunset"] - time_zone)
    cloudiness = data1["clouds"]["all"]
    len_day = sunset - sunrise
    weather = data1["weather"][0]["main"]

    if weather in code_to_smile:
        wd = code_to_smile[weather]
    else:
        wd = "Посмотри в окно, не ибу что там за параша"

    bot.send_message(message.chat.id,f"****{datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M')}****\n"
                                     f"      \U0001F449{city}\U0001F448\nПогода: {wd}\nОблачность: {cloudiness} %\n"
                                     f"Температура: {temp} °C, ощущается как {feels_like}°C\n"
                                     f"Температура днём / ночью : {temp_max} / {temp_min} °C\n"
                                     f"Влажность: {humidity} %\nСкорость ветра: {wind_speed} м/c\n"
                                     f"Рассвет солнца: {sunrise}\nЗакат солнца: {sunset}\nПродолжительность светового дня: {len_day}\n"
                                     f"Хорошего дня!"
                     )
    menu(message)

@bot.message_handler(commands=['info'])
def info_about_user(message):
    try:
        bot.send_message(message.chat.id, message)
    except:
        bot.send_message(message.chat.id, "Слишком много инфы. Не могу вывести, sorry")
    menu(message)

@bot.message_handler(commands=['top_site'])
def vk (message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти по ссылке virus365", url = "https://www.virustotal.com/gui/home/upload"))
    bot.send_message(message.chat.id, "Переходи сайт имба ваще", reply_markup=markup)
    menu(message)

@bot.message_handler(commands=['sapper'])
def sapper(message):
    field_bot = [[0] * 5 for i in range(5)]
    field_user = [[0] * 5 for i in range(5)]
    count_mines = 0
    for i in range(5):
        if count_mines == 10:
            break
        for j in range(5):
            field_bot[i][j] = random.randint(0,1)
            if field_bot[i][j] == 1:
                count_mines += 1
                if count_mines == 10:
                    break

    for i in range(5):
        for j in range(5):
            if field_bot[i][j] == 1:
                if j + 1 <= 4 and field_user[i][j] < 9 and field_bot[i][j + 1] == 0:
                    field_user[i][j + 1] += 1
                if j - 1 >= 0 and field_user[i][j] < 9 and field_bot[i][j - 1] == 0:
                    field_user[i][j - 1] += 1
                if j + 1 <= 4 and i - 1 >= 0 and field_user[i][j] < 9 and field_bot[i - 1][j + 1] == 0:
                    field_user[i - 1][j + 1] += 1
                if j + 1 <= 4 and i + 1 <= 4 and field_user[i][j] < 9 and field_bot[i + 1][j + 1] == 0:
                    field_user[i + 1][j + 1] += 1
                if i + 1 <= 4 and field_user[i][j] < 9 and field_bot[i + 1][j] == 0:
                    field_user[i + 1][j] += 1
                if i + 1 <= 4 and j - 1 >= 0 and field_user[i][j] < 9 and field_bot[i + 1][j - 1] == 0:
                    field_user[i + 1][j - 1] += 1
                if i - 1 >= 0 and field_user[i][j] < 9 and field_bot[i - 1][j] == 0:
                    field_user[i - 1][j] += 1
                if i - 1 >= 0 and j - 1 >= 0 and field_user[i][j] < 9 and field_bot[i - 1][j - 1] == 0:
                    field_user[i - 1][j - 1] += 1
                field_user[i][j] = 9

    for i in range(5):
        print(field_bot[i])
    print("\n")
    for i in range(5):
            print(field_user[i])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    for i in range(1,26,5):
        markup.add(types.KeyboardButton(str(i)), types.KeyboardButton(str(i + 1)), types.KeyboardButton(str(i + 2)), types.KeyboardButton(str(i + 3)), types.KeyboardButton(str(i + 4)))

    msg = bot.send_message(message.chat.id, "test sapper", reply_markup=markup)
    bot.register_next_step_handler(msg, get_result_sapper_about_mines, field_user)

def get_result_sapper_about_mines(message, field_user):
    i = int(message.text) // 5
    j = (int(message.text) % 5) - 1

@bot.message_handler(content_types=['text'])
def another_commands(message):
    if message.text.lower() == "id":
        bot.send_message(message.chat.id, f"<b><u>Твой ID:</u></b> {message.from_user.id}", parse_mode='html')
    elif message.text.lower() == "link":
        bot.send_message(message.chat.id, f"<b><u>Ссылка на тебя в Telegram:</u></b> https://t.me/{message.from_user.username}", parse_mode='html')
    elif message.text.lower() == "photo" or message.text.lower() == "ava":
        photo = open('Atomic Heart.png', 'rb')
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    weather = types.KeyboardButton('/weather')
    info = types.KeyboardButton('/info')
    vk = types.KeyboardButton('/top_site')
    sapper = types.KeyboardButton('/sapper')
    markup.add(weather,info,vk,sapper)
    bot.send_message(message.chat.id,"Общее меню",reply_markup=markup)

bot.infinity_polling()
