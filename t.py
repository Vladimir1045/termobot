import pyowm
import telebot
from bot_config import Token

owm = pyowm.OWM ('' 'Language'  == "rus" )
bot = telebot.TeleBot(Token)

@bot.message_handler(content_types=['text'])
def send_echo(message):
    observation = owm.weather_at_place( message.text )
    w = observation.get_weather()
    temp = w.get_temperature('celsius')["temp"]

    answer = "В городе" + message.text + " сейчас " + w.get_detailed_status() + "\n"
    answer += "Температура сейчас в районе" + str(temp) + "\n\n"

    if temp < 10:
        answer += "Сейчас ппц холодно, одевайся как танк!"
    elif temp < 20:
        answer += "сейчас холодно, оденься потеплее."
    elif temp > 20:
        answer += "Температура норм, одевай что угодно,"

    bot.send_message( message.chat.id, answer )

bot.polling( none_stop = True )# your code goes here# your code goes here