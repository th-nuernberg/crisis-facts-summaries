import pandas as pd
from collections import Counter
import re

### BEGIN SOLUTION
with open("d:\\Meine Dateien\\Uni\\TextAnalytics\\token\\Final.txt", encoding="utf-8") as file:
        full_text = file.read()
        tokens =  full_text.split(";")
tokens = re.findall(r"\'\w+\'", full_text)
#tokens[:10]

counter = Counter(tokens)
print(counter.most_common(30))

def txa_plot(records, columns=['Anzahl', 'Worte'], title=None): 

    df = pd.DataFrame.from_records(records, columns=columns).set_index(columns[0])
    ax = df.plot(kind='barh', width=0.8, figsize=(10, 0.2*len(records)))
    ax.invert_yaxis()
    word_counts = counter.most_common(30)
    txa_plot(word_counts)

#txa_plot(counter)