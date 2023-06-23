import pymorphy2
from pprint import pprint

morph = pymorphy2.MorphAnalyzer()


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