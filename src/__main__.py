import telebot
import pyowm
from src import cfg
from telebot import types

bot = telebot.TeleBot(cfg.TOKEN)
cities = ['Лондон', 'Париж', 'Москва', 'Санкт-Петербург', 'Дубай', "Другой город"]


@bot.message_handler(commands=['weather'])
def weather_command(message):
    markup = types.ReplyKeyboardMarkup()
    item0 = types.KeyboardButton(cities[0])
    item1 = types.KeyboardButton(cities[1])
    item2 = types.KeyboardButton(cities[2])
    item3 = types.KeyboardButton(cities[3])
    item4 = types.KeyboardButton(cities[4])
    item5 = types.KeyboardButton(cities[5])
    markup.row(item0, item1, item2, item3, item4, item5)
    city = bot.send_message(message.chat.id, "Выберите город:", reply_markup=markup)
    bot.register_next_step_handler(city, city_name)


def city_name(message):
    if message.text == cities[5]:
        city = bot.send_message(message.chat.id, "Введите название города:")
        bot.register_next_step_handler(city, weather_now)
    else:
        weather_now(message)


def weather_now(message):
    try:
        owm = pyowm.OWM(cfg.API_KEY, language="ru")
        city = message.text
        weather = owm.weather_at_place(city)
        w = weather.get_weather()
        temperature = w.get_temperature("celsius")["temp"]
        wind = w.get_wind()["speed"]
        hum = w.get_humidity()
        desc = w.get_detailed_status()
        bot.send_message(message.chat.id, "Сейчас в городе " + str(city) + " " + str(desc) + ", температура - " + str(
            temperature) + "°C, влажность - " + str(hum) + "%, скорость ветра - " + str(wind) + "м/с.")
    except Exception as e:
        print(repr(e))
        msg = bot.send_message(message.chat.id, "Неверное название города. Попробуйте еще раз:")
        bot.register_next_step_handler(msg, weather_now)


bot.polling(none_stop=True)