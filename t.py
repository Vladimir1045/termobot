import pyowm
import telebot
import logging
import traceback
from bot_config import Token, API_Token

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
owm = pyowm.OWM(API_Token)
mgr = owm.weather_manager()
bot = telebot.TeleBot(Token)


@bot.message_handler(content_types=['text'])
def send_echo(message):
    log.debug(f'Погода для {message.text}')
    try:
        weather = mgr.weather_at_place(message.text).weather
        temp = float(weather.temperature('celsius')['temp'])
        log.debug(f'Температура {temp}')
    except Exception as e:
        traceback.print_exc()
        log.error(f'Ошибка {e}')
        bot.send_message(message.chat.id, f'Не могу сказать тк {e}')
        return
    answer = f'В городе {message.text} сейчас {weather.detailed_status}\nТемпература сейчас в районе {temp}\n\n'
    if temp < 10:
        answer += "Сейчас ппц холодно, одевайся как танк!"
    elif temp < 20:
        answer += "сейчас холодно, оденься потеплее."
    elif temp > 20:
        answer += "Температура норм, одевай что угодно,"
    bot.send_message(message.chat.id, answer)

log.info('Начали')
bot.polling(none_stop=True)   # your code goes here# your code goes here
