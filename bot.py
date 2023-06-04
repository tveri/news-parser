import telebot, requests, datetime, time
from telebot import types

import config, main


bot = telebot.TeleBot(config.API_TOKEN)

url = 'https://ria.ru/society/'
sleepTime = 300


with open('./tmp', 'r+', encoding='utf-8') as f:
    lastPublicationTimestamp = int(f.readlines()[0])
    lastWriting = int(lastPublicationTimestamp)

while True:
    print(format(datetime.datetime.now(), '%H:%M:%S  %D').center(100, '-'), file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
    print('parsing...', file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
    for news in main.parseNews(url, lastPublicationTimestamp):
        lastPublicationTimestamp = news['timestamp'] if news['timestamp'] > lastPublicationTimestamp else lastPublicationTimestamp
        post = f"<b>{news['content']['title']}</b>\n\n{news['content']['article-text']}"
        msg = bot.send_message(chat_id='@testnewsnews', text=post, parse_mode='HTML')
        print(f"Post with title \"{news['content']['title']}\", message id: {msg.id}", file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
    else:
        print('new posts weren\'t find', file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))

    if lastWriting != lastPublicationTimestamp:
        with open('./tmp', 'w', encoding='utf-8') as f:
            print(f'writing tmp with timestamp: {lastPublicationTimestamp}', file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
            f.write(str(lastPublicationTimestamp))
            lastWriting = int(lastPublicationTimestamp)
    print(format(datetime.datetime.now(), '%H:%M:%S  %D').center(100, '-'), file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
    time.sleep(sleepTime)
    print(f'waiting {round(sleepTime/60, 1)} mins...', file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))

# post = f"<b>{news['content']['title']}</b>\n\n{news['content']['article-text']}"