from stopWordsFilter import stopWfilter

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

with open('testBase.txt', 'r', encoding='utf-8') as f:
    texts = f.read().replace('\t', '\n\n').split('===')

# normTexts = list(map(lambda x: stopWfilter(x).split(), texts))

normTexts = list(map(stopWfilter, texts))

# tfidf_vectorizer = TfidfVectorizer()
# values = tfidf_vectorizer.fit_transform(normTexts[0])
#
# # Show the Model as a pandas DataFrame
# feature_names = tfidf_vectorizer.get_feature_names()
# pdf = pd.DataFrame(values.toarray(), columns = feature_names)
# print(pdf)

from rake_nltk import Rake
r = Rake()
r.language = "russian"
# Extraction given the text.
for te in texts:
    r.extract_keywords_from_text(te)
    ranked = r.get_ranked_phrases_with_scores()
    print( ranked[:5])
# # To get keyword phrases ranked highest to lowest.
# r.get_ranked_phrases()
#
# # To get keyword phrases ranked highest to lowest with scores.
# r.get_ranked_phrases_with_scores()

