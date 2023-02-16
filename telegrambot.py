import requests
from bs4 import BeautifulSoup as b
import random
import telebot
API_KEY = '6025975946:AAEWgIrDUILp7vmhfELZYAtIYQkvSw5Lf1I'
bot = telebot.TeleBot(API_KEY)
URL_ = ''#сайт парсера


def pasers(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    a = soup.find_all('', class_='') #tegs
    random.shuffle(a)
    return a


rekc = pasers(URL_)
random.shuffle(rekc)


@bot.message_handler(commands=['start'])
def rekom(message):
    bot.send_message(message.chat.id, 'Здравствуйте,посмотрите на наши лучшие блюда! , введите любую цифру от 1 до 9 и мы вам предложим один из вариантов')


@bot.message_handler(content_types=['text'])
def pars(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, rekc[0])
        del rekc[0]
    else:
        bot.send_message(message.chat.id, 'По-моему вы вели не цифру,попробуйте снова " введите цифру от 1 до 9 " ')


bot.polling()
