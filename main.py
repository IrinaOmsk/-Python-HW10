import telebot
import requests

bot_params = {"fail_requests": 0}


def get_currency_rate(curr):
    """Функция принемает валюту и возвращает кортеж из её названия, номинала и курса в рублях"""
    resp = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    return resp['Valute'][curr]['Name'], resp['Valute'][curr]['Nominal'], resp['Valute'][curr]['Value']


def get_all_currency_code():
    "Функция возвращает строку со всеми возможными валютами"
    resp = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    curr_lst = [key for key in resp['Valute']]
    return ', '.join(curr_lst)


def get_bot_token(file_name):
    """Функция возвращает токен, прочитанный из файла"""
    with open(file_name, "r") as file:
        return file.read().strip()


bot = telebot.TeleBot(get_bot_token("token"))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет!, я умею выводить курс валюты\n" + 
        "Напиши /currency код валюты\n" + 
        "Например /currency USD\n" + 
        "Для вывода списка всех кодов введи /all"
        )

@bot.message_handler(commands=['all'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f"Список кодов доступных валют: {get_all_currency_code()}"
        )


@bot.message_handler(commands=['all'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        f"Список кодов доступных валют: {get_all_currency_code()}"
        )

@bot.message_handler(commands=['currency'])
def send_currency(message):
    currency = message.text.strip().split()[-1]
    try:
        name, nominal, value = get_currency_rate(currency)
        bot.send_message(
            message.chat.id, 
            f"{name}: {round(value / nominal, 3)}р."
            )
    except:
        bot.send_message(
            message.chat.id,
            "Неккоректный код валюты."
            )
        if bot_params["fail_requests"] >= 3:
            bot.send_message(
                message.chat.id, 
                f"Допустимые коды: {get_all_currency_code()}"
                )
            bot_params["fail_requests"] = 0
        else:
            bot_params["fail_requests"] += 1

bot.infinity_polling()