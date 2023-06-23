import telebot, requests, datetime, time
from telebot import types

import config, main, chat


bot = telebot.TeleBot(config.API_TOKEN)

url = 'https://ria.ru/spetsialnaya-voennaya-operatsiya-na-ukraine/'
sleepTime = 300


with open('./tmp', 'r+', encoding='utf-8') as f:
    fileTimestamp = int(f.readlines()[0])
    lastPublicationTimestamp = fileTimestamp if int(datetime.datetime.now().timestamp()) - fileTimestamp < 3600 else int(datetime.datetime.now().timestamp())
    lastWriting = int(lastPublicationTimestamp)

while True:
    print(format(datetime.datetime.now(), '%H:%M:%S  %D').center(100, '-'), file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
    print('parsing...', file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
    for news in main.parseNews(url, lastPublicationTimestamp):
        lastPublicationTimestamp = news['timestamp'] if news['timestamp'] > lastPublicationTimestamp else lastPublicationTimestamp
        post = chat.textTransform(f"{news['content']['title']}\n\n{news['content']['article-text']}")
        time.sleep(21)
        keywords = chat.getKeywords(post)
        time.sleep(21)
        
        while len(post) > 1024:
            post = '\n'.join(post.split('\n')[:-1])

        post = main.highlightWords(post.strip(), keywords)
        

        msg = bot.send_photo(chat_id='@testnewsnews', photo=requests.get(news['content']['img']['url']).content, caption=post[:1024], parse_mode='markdown')
        print(f"Post title \"{news['content']['title']}\", message id: {msg.id}", file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
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