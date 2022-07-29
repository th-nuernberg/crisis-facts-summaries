# import pandas as pd
# from collections import Counter
# import re

# ### BEGIN SOLUTION
# with open("d:\\Meine Dateien\\Uni\\TextAnalytics\\token\\Final.txt", encoding="utf-8") as file:
#         full_text = file.read()
#         tokens =  full_text.split(";")
# tokens = re.findall(r"\'\w+\'", full_text)
# #tokens[:10]

# counter = Counter(tokens)
# print(counter.most_common(30))

# def txa_plot(records, columns=['Anzahl', 'Worte'], title=None): 

#     df = pd.DataFrame.from_records(records, columns=columns).set_index(columns[0])
#     ax = df.plot(kind='barh', width=0.8, figsize=(10, 0.2*len(records)))
#     ax.invert_yaxis()
#     word_counts = counter.most_common(30)
#     txa_plot(word_counts)

#txa_plot(counter)

from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
  
example_sent = """This is a sample sentence,
                  showing off the stop words filtration."""
  
stop_words = set(stopwords.words('english'))
  
word_tokens = word_tokenize(example_sent)
  
filtered_sentence = []
  
for w in word_tokens:
    if w.lower() not in stop_words:
        filtered_sentence.append(w)
  
print(word_tokens)
print(filtered_sentence)

def ngrame():
    sentence = 'this is a foo bar sentences and i want to ngramize it'
    results = {}
    for i in range(2,6):
        ngrame = []
        n_grams = ngrams(sentence.split(), i)

        for grams in n_grams:
            hold =""
            for gram in grams:
                hold += gram
                hold +="_"
            hold = hold[:-1]
            ngrame.append(hold)
        print(ngrame)
        results[str(i)] = ngrame