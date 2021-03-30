import telebot
import requests

import datetime
import matplotlib.pyplot as plt
from datetime import *

bot = telebot.TeleBot('1712679759:AAEY5DhGT8kzf3IjgjADTTeybF9vf4sefqM')
r = requests.get("https://api.exchangeratesapi.io/latest?base=USD")


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, '''Привет, я бот для конвертации валют
Вот что я умею:
/list Показывает все валюты
/exchange Проведет конвертацю по твоему запросу
/history Отправлю график изменения валют
Если вы не получили ответ от меня, скорее всего
ввели неверный шаблон''')
    elif message.text == '/list':
        rates = r.json().get('rates')
        lst = []
        for key, value in rates.items():
            m = key + ":" + str(round(value, 2))
            lst.append(str(m))
        bot.send_message(message.from_user.id, '\n'.join(lst))
        bot.send_message(message.from_user.id, '''Попробуй и другие функции))
/list Показывает все валюты
/exchange Проведет конвертуцию по твоему запросу
/history Отправлю график изменения валют''')
    elif message.text == '/exchange':
        bot.send_message(message.from_user.id, '''Какие валюты хочешь конвертировать?
Например "10 USD to CAD"
''')
        bot.register_next_step_handler(message, exchange)
    elif message.text == '/history':
        bot.send_message(message.from_user.id, '''График включает в себя поведение
валюты за 7 предыдущих дней.
Введите например "USD and CAD"''')
        bot.register_next_step_handler(message, history)
    else:
        bot.send_message(message.from_user.id, '''Пожалуйста, выбери одну из команд
/list Показывает все валюты
/exchange Проведет конвертуцию по твоему запросу
/history Отправлю график изменения валют''')


def exchange(message):
    currency = message.text.split()
    number = currency[0]
    base = requests.get("https://api.exchangeratesapi.io/latest?base=" + currency[1].upper())
    rates = r.json().get('rates')
    convertible_currency = currency[3].upper()
    result = str(round(float(float(number) * float(rates.get(convertible_currency))), 2))
    bot.send_message(message.from_user.id, result + ' ' + convertible_currency)
    bot.send_message(message.from_user.id, '''
/list Показывает все валюты
/exchange Проведет конвертуцию по твоему запросу
/history Отправлю график изменения валют''')


def history (message):
    currency = message.text.split()
    first_value = currency[0].upper()
    second_value = currency[2].upper()
    tod = datetime.now()
    d = timedelta(days=7)
    a, b = str(tod - d)[:10], str(date.today())
    r = requests.get(
        "https://api.exchangeratesapi.io/history?start_at=" + a + "&end_at=" + b + "&base=" + first_value + "&symbols=" + second_value)
    rates = r.json().get('rates')
    rates.get(second_value)
    index = []
    for i in rates:
        index.append({"qwe": "qwe", "date": datetime.strptime(i, "%Y-%m-%d")})
    dates = []
    index2 = sorted(index, key=lambda x: x['date'])
    x = []
    y = []
    for i in range(len(index2)):
        dates.append(str(index2[i].get("date"))[:10])
        x.append(dates[i])
        y.append(rates.get(dates[i]).get(second_value))
    fig, ax = plt.subplots()
    plt.plot(x, y, marker="o", c="g")
    fig.savefig('1')
    bot.send_message(message.from_user.id, ''' No exchange 7 days rate data is available for the selected currency.
''')
    bot.send_photo(message.chat.id, open('B:/for python/telebot/1.png', 'rb'))
    bot.send_message(message.from_user.id, '''
/list Показывает все валюты
/exchange Проведет конвертуцию по твоему запросу
/history Отправлю график изменения валют''')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        pass
