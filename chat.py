import openai

import config

openai.api_key = config.CHAT_GPT_TOKEN


def textTransform(text):
    promt = 'Представь, что ты журналист и пересскажи текст строго до 1000 символов, чтобы это было интересно читать, выдели ключевые слова символами "**" с двух сторон, выдели в тексте несколько частей и раздели их, в начале каждой части поставь эмоджи выражающие эмоцию этой части'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": promt},
            {"role": "user", "content": text.replace('\n\n', ' ').replace('  ', ' ')},
        ]
    )
    return response['choices'][0]['message']['content']


def getKeywords(text):
    promt = 'выбери ключевые слова из текста'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": promt},
            {"role": "user", "content": text},
        ]
    )
    return response['choices'][0]['message']['content'].split(', ')