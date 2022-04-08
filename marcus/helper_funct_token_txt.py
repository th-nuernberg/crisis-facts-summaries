import os

import re
import html
import textacy.preprocessing as tprep
import pandas as pd
import json
#import sqlite3 
import spacy
import pprint as pp

nlp = spacy.load('en_core_web_sm')

def lemmata(doc, include_pos = None): 
    return [t.lemma_ for t in doc if include_pos is None or t.pos_ in include_pos]

#lemmas = lemmta(doc)#, include_pos=['ADJ', 'NOUN'])
#print(*lemmas, sep='|')

def normalize(text):
    text = tprep.normalize.hyphenated_words(text)
    text = tprep.normalize.quotation_marks(text)
    text = tprep.normalize.unicode(text)
    text = tprep.remove.accents(text)
    return text

def clean(text):
    # convert html escapes like &amp; to characters.
    text = html.unescape(text) 
    # tags like <tab>
    text = re.sub(r'<[^<>]*>', ' ', text)
    # markdown URLs like [Some text](https://....)
    text = re.sub(r'\[([^\[\]]*)\]\([^\(\)]*\)', r'\1', text)
    # text or code in brackets like [0]
    text = re.sub(r'\[[^\[\]]*\]', ' ', text)
    # standalone sequences of specials, matches &# but not #cool
    text = re.sub(r'(?:^|\s)[&#<>{}\[\]+|\\:-]{1,}(?:\s|$)', ' ', text)
    # standalone sequences of hyphens like --- or ==
    text = re.sub(r'(?:^|\s)[\-=\+]{2,}(?:\s|$)', ' ', text)
    # sequences of white spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


#copied from felix because of import difficulties
#creates 409 files, better solution? -> put everthing in one file?
def artikel_tokenice(): 
    #name der eingabe datei
    file_path = r"marcus\data\sentences.txt"
    
    with open(file_path, encoding="utf-8") as file:
        full_text = file.read()
        file.close()
    
    tokens = full_text.split("\n\n")
    
    for token in tokens:
        full_text = token.casefold()
        new_tokens = re.findall(r'\w+', full_text)

        with open('Felix\\stopwords-en.txt', encoding='utf-8') as file:
            stopwords = file.read().splitlines()
            stopwords = set(stopwords)

    only_tokens = [t for t in new_tokens if t not in stopwords]
    clean_tokens = [clean(t) for t in only_tokens]
    lemma_tokens = [lemmata(nlp(t)) for t in clean_tokens]

    with open("marcus\\data\\tokens\\Final.txt", "a", encoding="utf-8") as file:    
        for l in lemma_tokens:
            hold = str(l).removeprefix("[")
            hold = hold.removesuffix("]")            
            file.write(hold)
        file.write(";\n")
        file.close()