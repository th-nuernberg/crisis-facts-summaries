#FLASK and FLASK-Endpoint
import json
import nltk
from pymprog import *
import re
from nltk import ngrams
import time


pathToFile = "/usr/src/app/Datensaetze/prepared/26.relonly.jsonl"

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

# Das gleiche wie die Funktion darüber nur mit n-grammen (also n Wörterbündel)
def ngrame(text,anzahl_worte=2):
    result = []
    for i in range(2,anzahl_worte+1):
        ngrame = []
        n_grams = ngrams(text.split(), i)
        for grams in n_grams:
            hold =""
            for gram in grams:
                hold += gram
                hold +="_"
            hold = hold[:-1]
            ngrame.append(hold)
        result.extend(ngrame)
    return result

# 
def extractSentencesNLTK(rawDicts,numberOfWords):
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
                                        ('bigrams', list(set(ngrame(sentence,numberOfWords))))]))
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

# TODO: TFIDF anschauen
# TF-IDF:
#   - Termn Frequency: Gewichtung der Wörter anhand der Häufigkeit im Text
#   - Document Frequency: Gewichtung der Wörter anhand der Häufigkeit in Seiten (oder größerer Texteinheit -> Wort kam in 3 Texteinheiten vor)
#   - Inverse Document Frequency: Auch Häufigkeit, aber sehr häufig vorkommende Wörter werden weniger gewichtet und sehr selten vorkommende Wörter schwerer gewichtet.
#   - 
# Gewichtung der Bigramme feststellen -> Wie häufig kommt ein Bigramm in dem Text vor
def extractWeightPerBigram(documentsDict):
    bigramDict = {}
    for documentId in documentsDict:
        for bigram in documentsDict[documentId]:
            bigramDict.setdefault(bigram, 0)
            bigramDict[bigram] = bigramDict[bigram] + 1
    return bigramDict

# TODO: Ckitlearn kann das evtl. effizienter -> besseres Format
# TODO: count vectorizer
# TODO: sparseMatrix
def calculateOccurrences(bigramList, sentenceBigramList):
    dim_columns = len(bigramList)
    dim_rows = len(sentenceBigramList)
    occ = [[0 for j in range(dim_columns)] for i in range(dim_rows)]
    for i in range(len(sentenceBigramList)):
        for j in range(len(bigramList)):
            if bigramList[j] in sentenceBigramList[i]:
                occ[i][j] = 1
    return occ


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

# 
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
                if occurrences[maxSentence][j] == 1:
                    for i in range(len(occurrences)):
                        sentenceValue[i] -= occurrences[i][j] * weights[j]
        else:
            continueSearching = False # no new sentence that fit the length was found, end the search

    summary = { "sentences": [],
            "timestamp": []  }

    # TODO: Hier kann potentiell des JSON Format korriegiert werden
    for i in sentenceIndices:
        for s in sentences:
            if(s["sentence_id"] == saetze[i]):
                summary["sentences"].append(s["sentence"])
                summary["timestamp"].append(s["timestamp"])

    return summary


satz1 = "hallo wie geht es"
satz2 = "test satz bla"
satz3 = "test satz 2"

saetze = ["hallo wie geht es",
        "test satz bla",
        "test satz 2"
        ]

# l = list(map(lambda x: len(x), saetze))  # [len(satz1), len(satz2), len(satz3)]  # länge der Sätze
# j = len(saetze)  # anzahl Sätze

w = [1,  # hallo    Gewichte der Konzepte, hier Wörter
    2,  # wie
    3,  # geht
    4,  # es
    5,  # test
    6,  # satz
    2,  # bla
    8,  # 2
    ]
# aktualität = (zeitpunkt_erste_erwähnung - startzeitpunkt) / (endzeitpunkt - startzeitpunkte)
# w = anzahl_dokumente * x + (1-x) * aktualität
Occ = [  # ob ein Konzept in einem Satz enthalten ist
    [1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 1],
]

# print(calculateSummary(saetze, w, Occ, L))
# TODO: einschränkung auf einen gewissen Zeitraum
# TODO: zeitpunkte in Gewichtung mi einbeziehen
# TODO: mit evaluationsmatrix evaluieren -> siehe Mail

def gesamt(ngamms=2,timespan=0,weigth=0,max_length=600,question=""):

    print("Start!")
    start = time.time()
    L = max_length # Anzhal Buchstaben im Summary

    #init()
    data = readInput()
    #print(data[0])
    sentences = extractSentencesNLTK(data,ngamms)
    #print(sentences[0])
    bigramsPerDocument = extractBigramsPerDocument(sentences)
    # print(bigramsPerDocument['7b32de22a8f61f2c6d86e40a5a786cc7'])
    bigramWeights = extractWeightPerBigram(bigramsPerDocument)
    # print(bigramWeights['amid_heavy'])
    occ = calculateOccurrences(list(bigramWeights.keys()), [s['bigrams'] for s in sentences])
    # print(occ[1])
    #print("occurrences ready")
    weights = list(bigramWeights.values())
    saetzeList = [s['sentence_id'] for s in sentences]
    #print(len(weights))
    #print(len(saetzeList))

    # TODO: calculateSummaryGreedy liefert kein gültiges JSON
    summarySenetences = calculateSummaryGreedy(saetzeList, sentences, weights, occ, L)

    #testBigrams = ['hallo', 'wie', 'geht', 'es', 'test', 'satz', 'bla', '2']
    #testSatzBigrams = [s.split() for s in saetze]

    # occ = calculateOccurrences(testBigrams, testSatzBigrams)
    # print(occ)

    # summarySenetences = calculateSummary(saetze, w, occ, L)

    #for s in summarySenetences:
        #print(s)
        #totalLength += len(s)
    #print(totalLength)

    end = time.time()
    print("Fertig!")
    print(end - start)
    print("Sekunden Ausfuehrungszeit")
    #print(summarySenetences)
    return json.dumps(summarySenetences)