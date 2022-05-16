import os

import pprint as pp
import regex as re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

from helper_funct_token_txt import artikel_tokenice


files = os.listdir("D:\\Meine Dateien\\Uni\\IT-Projekt\Arbeit\\it-projekt\\marcus\\data\\tokens")
if len(files) == 0:
    artikel_tokenice()


#test Graph making
with open("D:\\Meine Dateien\\Uni\\IT-Projekt\Arbeit\\it-projekt\\marcus\\data\\tokens\\Final.txt", encoding="utf-8") as file:
        full_text = file.read()
        tokens =  full_text.split(";")
tokens = re.findall(r"\'\w+\'", full_text)
#tokens[:10]

counter = Counter(tokens)
test = counter.most_common(30)

def txa_plot(records, columns=['Anzahl', 'Worte'], title=None): 
    df = pd.DataFrame.from_records(records, columns=columns).set_index(columns[0])
    ax = df.plot(kind='barh', width=0.8, figsize=(10, 0.2*len(records)))
    ax.invert_yaxis()

txa_plot(test)
plt.show()

pp.pprint("Done")