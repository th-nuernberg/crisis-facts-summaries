#FLASK and FLASK-Endpoint
import json
import nltk
from pymprog import *
import re
from nltk import ngrams
import time
import textacy as tprep
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

pathToFile = "/usr/src/app/Datensaetze/prepared/26.relonly.jsonl" #Datensatz_1.json

def init():
    nltk.download('punkt')

#Funktion zum einlesen der neuen Daten in Felix/download.py
def readInput():
    df = []
    with open(pathToFile, 'r', encoding="utf-8") as json_file:
        mytext = json_file.read()
        lines = mytext.split("\n")
        for line in lines:
            if len(line) > 0:
                df.append(json.loads(line))
    return df

# Gibt eine Liste mit allen Bigrammen (Bigramm -> "wortA wortB wortC wortD" = "wortA wortB" "wortB wortC" "wortC wortD") aus einem mitgegebenen Text zurück
def bigramme(text):
    words = re.findall(r'[A-Za-z0-9]+', text)
    result = []
    for i in range(0, len(words)):
        if (i < (len(words) - 1)):
            result.append(words[i] + "_" + words[i + 1])
    return result

# Es wird gezählt, wie viele Ereignisse zu einem bestimmten Zeitpunkt erfasst wurden. Diese Daten werden grafisch auf der Webseite angezeigt
def sum_appearances(rohdaten):
    listofDates = {}
    for satz in rohdaten:
        time = satz["timestamp"]
        if time in listofDates.keys():
            listofDates[time] = listofDates[time] + 1
        else:
            listofDates[time] = 1

    #print("Alle Zeitpunkte:")
    #print(listofDates)
    return listofDates

def add_sum_appearances(summarySenetences,timeDataForDiagramm):
    keys = timeDataForDiagramm.keys()
    for s in keys:
        fastformatiert = s.replace('T', ' ')
        formatiert = fastformatiert.replace('.0Z', '')
        summarySenetences["timestampsforDiagramm"].append(formatiert)
        summarySenetences["occurrencesforDiagramm"].append(timeDataForDiagramm[s])
    return summarySenetences

def clean(text):
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

def normalize(text):
    text = tprep.normalize.hyphenated_words(text)
    text = tprep.normalize.quotation_marks(text)
    text = tprep.normalize.unicode(text)
    text = tprep.remove.accents(text)
    return text

# Das gleiche wie die Funktion darüber nur mit n-grammen (also n Wörterbündel)
def ngrame(original_text,test_dict):
    stopwords =[]
    with open('/usr/src/app/Datensaetze/stopwords-en.txt', encoding='utf-8') as file:
        stopwords = file.read().splitlines()
    result = []
    text = ""
    original_text = clean(original_text)
    #original_text = normalize(original_text)
    
    for w in original_text.split():
        if w not in stopwords:
            text = text + " " + w
    for i in range(1,5):
        if(test_dict[str(i)]):
            ngrame = []
            n_grams = ngrams(re.findall(r'[A-Za-z0-9]+', text), i)
            for grams in n_grams:
                hold =""
                for gram in grams:
                    hold += gram
                    hold +="___"
                ngrame.append(hold)
            result.extend(ngrame)
    return result
 
def extractSentencesNLTK(rawDicts,test_dict):
    sentencesDicts = []
    sentenceId = 0
    for rawDict in rawDicts:

        sentences = nltk.sent_tokenize (rawDict['content'])
        sentences = list(map(lambda x: x.strip(), sentences))
        for sentence in sentences:
            sentencesDicts.append(dict([("timestamp", rawDict['timestamp']),
                                        ("document_id", rawDict['document_id']),
                                        ("sentence_id", sentenceId),
                                        ("sentence", sentence),
                                        ('bigrams', list(set(ngrame(sentence,test_dict))))]))
            sentenceId += 1
    return sentencesDicts

def extractBigramsPerDocument(sentenceDicts):
    documentDict = {}
    for sentenceDict in sentenceDicts:
        documentId = sentenceDict['document_id']
        documentDict.setdefault(documentId, [])
        documentDict[documentId] = documentDict[documentId] + sentenceDict['bigrams']
    for key in documentDict:
        documentDict[key] = list(set(documentDict[key]))
    return documentDict

# TF-IDF:
#   - Termn Frequency: Gewichtung der Wörter anhand der Häufigkeit im Text
#   - momentan Document Frequency: Gewichtung der Wörter anhand der Häufigkeit in Seiten (oder größerer Texteinheit -> Wort kam in 3 Texteinheiten vor)
#   - Inverse Document Frequency: Auch Häufigkeit, aber sehr häufig vorkommende Wörter werden weniger gewichtet und sehr selten vorkommende Wörter schwerer gewichtet.
#   - 
# Gewichtung der Bigramme feststellen -> Wie häufig kommt ein Bigramm in dem Text vor
def extractWeightPerBigram(documentsDict,sentences,Vorzugsfaktor =2):
    bigramDict = {}
    anzahl_dict = {1:0,2:0,3:0,4:0,5:0}
    for documentId in documentsDict:
        for bigram in documentsDict[documentId]:
            bigramDict.setdefault(bigram, 0)
            bigramDict[bigram] = bigramDict[bigram] + 1
    bigrammList = []
    for sentence in sentences:
        for bigram in sentence["bigrams"]:
            bigrammList.append(bigram)
    for  gramm in bigrammList:
        anzahl_dict[gramm.count('___')+1] = anzahl_dict[gramm.count('___')+1]+1
    uniqueBigrams = list(set(bigrammList))
    for gramm in uniqueBigrams:
        grammLength =gramm.count('___')+1
        # Gewichtung * Korrekturfaktor * Vorzugsfaktor
        bigramDict[gramm] = bigramDict[gramm]  * (anzahl_dict[1]/anzahl_dict[grammLength]) * (grammLength*Vorzugsfaktor)
    return bigramDict

# TODO: Ckitlearn kann das evtl. effizienter -> besseres Format
# TODO: count vectorizer
# TODO: sparseMatrix

# Erstellt eine Matrix mit den Vorkommnissen der Engrammen in den Sätzen
# Anzahl der Spalten ist Anzahl der Ngramme
# Anzahl der Zeilen ist Anzahl der Sätze
def calculateOccurrences(bigramList, sentenceBigramList):
    dim_columns = len(bigramList)
    dim_rows = len(sentenceBigramList)
    occ = [[0 for j in range(dim_columns)] for i in range(dim_rows)]
    for i in range(len(sentenceBigramList)):
        for j in range(len(bigramList)):
            if bigramList[j] in sentenceBigramList[i]:
                occ[i][j] = 1
    return occ

def TfIdfBerechnen(sentences,ngrams=2):
    df = pd.DataFrame(sentences)
    df = df[:5000]
    df.drop(['document_id','timestamp','bigrams'], axis = 1)
    count_vect = CountVectorizer(lowercase=False, min_df=5, max_df=0.8, ngram_range=(1,ngrams))    
    X_tf = count_vect.fit_transform(df['sentence'])   
    return [X_tf,len(count_vect.get_feature_names())]

# TODO: dies ist zu ressourcenintensiv -> doch direkt mit glpk? Kann das optimiert werden?
# TODO: wegen Serverzugriff Mail schreiben 
# def calculateSummary(saetze, weights, occurrences, totalLength):
#     i = len(weights)  # Anzahl der Konzepte
#     l = list(map(lambda x: len(x), saetze))  # [len(satz1), len(satz2), len(satz3)]  # länge der Sätze
#     j = len(saetze)
#     begin('test konzepte')
#     c = var('c', i, kind=bool)  # ist ein konzept im Summary enhalten
#     s = var('s', j, kind=bool)  # ist ein Satz im Summary enthalten
#     maximize(sum(weights[a] * c[a] for a in range(i)))
#     sum(l[b] * s[b] for b in range(j)) <= totalLength
#     for a in range(i):
#         sum(s[b] * occurrences[b][a] for b in range(j)) >= c[a]
#         for b in range(j):
#             s[b] * occurrences[b][a] <= c[a]
#     solve()
#     print("###>Objective value: %f" % vobj())
#     summary = []
#     for b in range(j):
#         # print(s[b].primal)
#         if s[b].primal == 1.0:
#             print(b)
#             summary.append(saetze[b])
#     return summary

def calculateSummaryGreedy(saetze, sentences, weights, occurrences, maxTotalLength):
    sentenceIndices = []
    totalLength = 0
    continueSearching = True
    satzDict={}
    zeitDict={}
    for s in sentences:
        satzDict[s["sentence_id"]]= s["sentence"]
    for s in sentences:
        zeitDict[s["sentence_id"]]= s["timestamp"]

    # calculate total value for all sentences
    sentenceValue = []
    for s in saetze:
        sentenceValue.append(0)
    for i in range(len(saetze)):
        for j in range(len((weights))):
            sentenceValue[i] += occurrences[i][j] * weights[j]
        #if i % 1000 == 0:
        #    print(i)
    sentence =""
    while continueSearching:
        # get maximum value per length
        maxVal = 0
        maxSentence = -1
        for i in range(len(sentenceValue)):
            val = sentenceValue[i] / len(satzDict[saetze[i]])
            if (maxVal < val) & (totalLength + len(satzDict[saetze[i]]) < maxTotalLength):
                maxVal = val
                maxSentence = i
                sentence = satzDict[saetze[i]]

        # if a new sentence has been found, adjust the values
        if maxSentence != -1:
            sentenceIndices.append(maxSentence)
            totalLength += len(sentence)
            for j in range(len(occurrences[maxSentence])):
                if occurrences[maxSentence][j] > 0:
                    for i in range(len(occurrences)):
                        sentenceValue[i] -= occurrences[i][j] * weights[j]
        else:
            continueSearching = False # no new sentence that fit the length was found, end the search

    summary = { "sentences": [],
            "timestamp": [],
            "timestampsforDiagramm": [],
            "occurrencesforDiagramm": [] }

    for i in sentenceIndices:
        for s in sentences:
            if(s["sentence_id"] == saetze[i]):
                # timestamp wird auf das passende Format gebracht
                summary["sentences"].append(s["sentence"])
                fastformatiert = s["timestamp"].replace('T', ' ')
                formatiert = fastformatiert.replace('.0Z', '')
                summary["timestamp"].append(formatiert)

    return summary

# TODO: einschränkung auf einen gewissen Zeitraum
# TODO: zeitpunkte in Gewichtung mi einbeziehen
# TODO: mit evaluationsmatrix evaluieren -> siehe Mail

def gesamt(eins,zwei,drei,vier,timespan=0,weigth=0,max_length=600,question=""):
    Anzahl_gramme = 5000
    test_dict = {"1":eins, "2":zwei,"3":drei,"4":vier}
    print("Start!")
    start = time.time()
    L = max_length # Anzhal Buchstaben im Summary
    data = readInput()

    # Test für grafische Darstellung des Diagramms
    timeDataForDiagramm = sum_appearances(data)

    sentences = extractSentencesNLTK(data,test_dict)
    bigramsPerDocument = extractBigramsPerDocument(sentences)
    bigramWeights = extractWeightPerBigram(bigramsPerDocument,sentences)

    # True setzen falls der Arbeitsspeicher voll läuft
    if False:
        occ = calculateOccurrences(list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).keys())[:Anzahl_gramme], [s['bigrams'] for s in sentences])
        weights = list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).values())[:Anzahl_gramme]
    else:
        #occ = calculateOccurrences(list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).keys()), [s['bigrams'] for s in sentences])
        #occ = TfIdfBerechnen(sentences)
        occ = calculateOccurrences(list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).keys()), [s['bigrams'] for s in sentences])
        weights = list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).values())
    saetzeList = [s['sentence_id'] for s in sentences]

    summarySenetencesincomplete = calculateSummaryGreedy(saetzeList, sentences, weights, occ, L)
    summarySenetences = add_sum_appearances(summarySenetencesincomplete,timeDataForDiagramm)
    print(summarySenetences)

    end = time.time()
    print("Fertig!")
    print(end - start)
    print("Sekunden Ausfuehrungszeit")
    return json.dumps(summarySenetences) # wieder auf summarySenetences ändern