from stopWordsFilter import stopWfilter

with open('testBase.txt', 'r', encoding='utf-8') as f:
    texts = f.read().replace('\t', '\n').split('===')

normTexts = list(map(stopWfilter, texts))

print(normTexts)