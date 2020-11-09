import pyowm
import telebot
import logging
import traceback
from bot_config import Token, API_Token

intervals = [
    {'from': None, 'to': 10, 'text': 'Сейчас ппц холодно, одевайся как танк!'},
    {'from': 10, 'to': 20, 'text': 'Сейчас холодно, оденься потеплее.'},
    {'from': 20, 'to': None, 'text': 'Температура норм, надевай что угодно.'},
]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
owm = pyowm.OWM(API_Token)
mgr = owm.weather_manager()
bot = telebot.TeleBot(Token)


def get_advise(temp):
    rc = 'Мне нечего сказать.'
    for x in intervals:
        if (x['from'] is None or temp >= x['from']) and (x['to'] is None or temp < x['to']):
            return x['text']
    return rc


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
    advise = get_advise(temp)
    bot.send_message(message.chat.id, f'В городе {message.text} сейчас {weather.detailed_status}\n'
                                      f'Температура сейчас в районе {temp}\n\n{advise}')


log.info('Начали')
bot.polling(none_stop=True)   # your code goes here# your code goes here
