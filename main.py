import telebot
from telebot import types
import wikipedia
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
bot = telebot.TeleBot('5416382243:AAGqNUELS1KgUAJbeJqJw5La82fJEWkxmFs')




class TextInfo:
    def __init__(self, arg):
        self.arg = arg

    def printUK(self,arg):
        wikipedia.set_lang('uk')
        try:
            page = wikipedia.page(arg)
            return page.summary
        except wikipedia.exceptions.PageError:
            err = 'Не вдалося знайти інформацію по даному запиту! Спробуйте ще!'
            return err
        except wikipedia.exceptions.DisambiguationError:
            err = 'Не вдалося знайти інформацію по даному запиту! Спробуйте ще!'
            return err
    def printENG(self,arg):
        try:
            wikipedia.set_lang('en')
            page = wikipedia.page(arg)
            return page.summary
        except wikipedia.exceptions.PageError:
            err = 'Could not find information on this request! Try again!'
            return err
        except wikipedia.exceptions.DisambiguationError:
            err = 'Could not find information on this request! Try again!'
            return err




class Video:

    def giveVideo(self,arg):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_SHIM', None)
            browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
            driver = webdriver.Chrome()
            video_href = "https://www.youtube.com/results?search_query=" + arg
            driver.get(video_href)
            sleep(2)
            videos = driver.find_elements(By.ID, "video-title")
            lst = []
            for i in range(len(videos)):
                if i == 0:
                    continue
                else:
                    item = videos[i].get_attribute("href")
                    lst.append(item)
                    if i == 3:
                        break
            return lst
        except Exception:
            err = 'Video could not be found, please try again'
            return err


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Wiki', 'Video')
    msg = bot.send_message(message.chat.id,'Choose what you need!',reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)

def process_step(message):
    chat_id = message.chat.id
    if message.text=='Wiki':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Eng','Ukr')
        msg = bot.send_message(message.chat.id, 'Choose Wiki language!', reply_markup=markup)
        bot.register_next_step_handler(msg, language)
    elif message.text=='Video':
        msg = bot.send_message(message.chat.id, 'Enter what find')
        bot.register_next_step_handler(msg, videoFind)
    else:
        msg = bot.send_message(message.chat.id, 'The command was entered incorrectly! Restart bot - /start ')


def language(message):
    if message.text =='Eng':
        msg = bot.send_message(message.chat.id, 'Enter what find')
        bot.register_next_step_handler(msg,findEng)
    elif message.text == 'Ukr':
        msg = bot.send_message(message.chat.id, 'Введіть, що потрібно знайти')
        bot.register_next_step_handler(msg,findUkr)
    elif message.text == '/start':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Wiki', 'Video')
        msg = bot.send_message(message.chat.id, 'Choose what you need!', reply_markup=markup)
        bot.register_next_step_handler(msg, process_step)
    else:
        msg = bot.send_message(message.chat.id, 'The command was entered incorrectly! Restart bot - /start ')


def findEng(message):
    message_to_save = message.text
    obj1 = TextInfo(message_to_save)
    text = obj1.printENG(message_to_save)
    msg = f'{text}'
    try:
        bot.send_message(message.chat.id, msg, parse_mode='html')
        msg1 = bot.send_message(message.chat.id, 'Restart bot - /start')

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Eng', 'Ukr')
        msg3 = bot.send_message(message.chat.id, 'Choose Wiki language!', reply_markup=markup)
        bot.register_next_step_handler(msg3, language)



    except Exception:
        bot.send_message(message.chat.id, 'Could not find information on this request! Try again!')
        msg1 = bot.send_message(message.chat.id, 'Could not find information on this request! Try again!')

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Eng', 'Ukr')
        msg3 = bot.send_message(message.chat.id, 'Choose Wiki language!', reply_markup=markup)
        bot.register_next_step_handler(msg3, language)



def findUkr(message):
    message_to_save_txt = message.text
    obj = TextInfo(message_to_save_txt)
    text = obj.printUK(message_to_save_txt)
    msg = f'{text}'

    try:
        bot.send_message(message.chat.id, msg, parse_mode='html')
        msg1 = bot.send_message(message.chat.id, 'Перезапустити бота - /start')


        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Eng', 'Ukr')
        msg3 = bot.send_message(message.chat.id, 'Choose Wiki language!', reply_markup=markup)
        bot.register_next_step_handler(msg3, language)

    except Exception:
        bot.send_message(message.chat.id, 'Не вдалося знайти запит! Попробуйте ще раз!')
        msg1 = bot.send_message(message.chat.id, 'Перезапустити бота - /start')

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Eng', 'Ukr')
        msg3 = bot.send_message(message.chat.id, 'Choose Wiki language!', reply_markup=markup)
        bot.register_next_step_handler(msg3, language)



def videoFind(message):
    message_to_save_txt = message.text
    bot.send_message(message.chat.id, "Finding...Please wait")
    a = Video()

    im = a.giveVideo(message_to_save_txt)
    counter = 0
    for i in im:
        counter+=1
        bot.send_message(message.chat.id, i)
        if counter > 3:
            break

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Wiki', 'Video')
    msg = bot.send_message(message.chat.id, 'Choose what you need!', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)





bot.polling(none_stop=True)