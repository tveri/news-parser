from bs4 import BeautifulSoup
import requests, datetime, pymorphy2

import config

morph = pymorphy2.MorphAnalyzer()

def parseNews(url, lastPublicationTimestamp):
    req = requests.get(url)
    print(f'news has got, status code: {req.status_code}', file=open(config.LOG_FILE_PATH, 'a', encoding='utf-8'))
    soup = BeautifulSoup(req.text, 'html.parser')

    newsList = []

    titles = list(soup.find_all(class_='list')[0].find_all('div', class_='list-item'))
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
                'url': content.a.picture.img['src'],
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


def highlightWords(text, keywords):
    text = text.split(' ')
    normalizedText = [morph.parse(word.strip(' ,.-'))[0].normal_form for word in text]
    normalizedKeywords = [' '.join([morph.parse(word)[0].normal_form for word in keyword.split(' ')]) for keyword in keywords]
    keywordsLens = set(len(word.split(' ')) for word in keywords)
    for l in keywordsLens:
        # print(f'\nwords-{l}-lenght\n')
        for i, (word, normalizedWord) in enumerate(zip(text, normalizedText)):
            if '*' in word or '_' in word: continue
            words = text[i:i+l]
            normalizedWords = normalizedText[i:i+l]
            # print('\t', ' '.join(words), '\t|||\t', ' '.join(normalizedWords))
            text[i:i+l] = [word.replace(stripedWord := word.strip(' ,.-\n'), f"*{stripedWord}*" if l != 3 else f"_{stripedWord}_") for word in words] if ' '.join(normalizedWords) in normalizedKeywords else text[i:i+l]
    return ' '.join(text)