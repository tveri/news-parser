from bs4 import BeautifulSoup
import requests, datetime

import config


def parseNews(url, lastPublicationTimestamp):
    req = requests.get(url)
    print(f'news has got, status code: {req.status_code}', file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
    soup = BeautifulSoup(req.text, 'html.parser')

    newsList = []

    titles = list(soup.find_all(class_='list list-tags')[0].find_all('div', class_='list-item'))
    for _, content, info, tags in titles:
        news = {}
        
        date = content.a['href'].split('/')[3]
        time = info.find('div', class_='list-item__date').text
        
        news['timestamp'] = int(datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8]) - (1 if 'Вчера' in time else 0), int(time.strip('Вчера, ').split(':')[0]), int(time.strip('Вчера, ').split(':')[1])).timestamp())
        news['full-post-url'] = content.a['href']

        if news['timestamp'] <= lastPublicationTimestamp:
            continue
        if news['full-post-url'].split('/')[2] != 'ria.ru':
            continue
        
        req = requests.get(news['full-post-url'])
        print(f'full news have got, status code: {req.status_code}', file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
        soup = BeautifulSoup(req.text, 'html.parser')

        articleTextBlocks = soup.find('div', class_='article__body').find_all('div', class_='article__text')
        fullText = []
        for textBlock in articleTextBlocks:
            text = ''.join([str(l) for l in textBlock.contents])
            fullText.append(text)

        news['content'] = {
            'title': content.find('a', class_='list-item__title').text,
            'article-text': '\n\n'.join(fullText).replace(' – РИА Новости', '').replace(' РИА Новости', ''),
            'img': {
                'alt': content.a.picture.img['alt'],
                'url': content.a.picture.source['srcset'],
            },
        }
        
        news['info'] = {
            'views': info.find('div', class_='list-item__views-text').text,
        }
        
        news['tags'] = []
        for tag in tags.find_all('a', class_='list-tag'):
            news['tags'].append({
                'name': tag.span.text,
                'url': tag['href'],
            })

        newsList.append(news)
    return newsList