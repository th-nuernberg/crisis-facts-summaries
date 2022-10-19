#FLASK and FLASK-Endpoint
from audioop import maxpp, reverse
import json
from statistics import variance
from sys import maxsize
import nltk
import math
from pymprog import *
import re
from nltk import ngrams
import time
import textacy as tprep
import spacy

nlp = spacy.load('en_core_web_sm')

def init():
    nltk.download('punkt')

#Funktion zum einlesen der Daten
def readInput(pathToFile):
    df = []
    with open(pathToFile, 'r', encoding="utf-8") as jsonFile:
        mytext = jsonFile.read()
        lines = mytext.split("\n")
        for line in lines:
            if len(line) > 0:
                df.append(json.loads(line))
    return df

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
    text = re.sub(r'http.+', ' ', text)
    text = re.sub(r'[\U00010000-\U0010ffff]', ' ', text)
    # sequences of white spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize(text):
    text = tprep.normalize.hyphenated_words(text)
    text = tprep.normalize.quotation_marks(text)
    text = tprep.normalize.unicode(text)
    text = tprep.remove.accents(text)
    return text

# Erzeugt n-gramme aus dem input Text
def ngrame(originalText,testDict,toLower,toLemma):
    stopwords =[]
    with open('/usr/src/app/Datensaetze/stopwords-en.txt', encoding='utf-8') as file:
        stopwords = file.read().splitlines()
    result = []
    text = ""
    originalText = clean(originalText)
    if toLower:
        originalText = originalText.lower()
    #original_text = normalize(original_text)
    
    for w in originalText.split():
        if w not in stopwords:
            text = text + " " + w
    for i in range(1,5):
        if(testDict[str(i)]):
            ngrame = []
            nGrams = ngrams(re.findall(r'[A-Za-z0-9]+', text), i)
            for grams in nGrams:
                hold =""
                for gram in grams:
                    if toLemma:
                        doc = nlp(gram)
                        for t in doc:                    
                            hold += t.lemma_
                    else:
                        hold += gram
                        hold +="___"
                ngrame.append(hold)
            result.extend(ngrame)
    return result
 
def extractSentencesNLTK(rawDicts,testDict,toLower,toLemma):
    sentencesDicts = []
    sentenceId = 0
    for rawDict in rawDicts:

        sentences = nltk.sent_tokenize (rawDict['content'])
        sentences = list(map(lambda x: x.strip(), sentences))
        for sentence in sentences:
            if len(clean(sentence)) >0:
                sentencesDicts.append(dict([("timestamp", rawDict['timestamp']),
                                            ("document_id", rawDict['document_id']),
                                            ("sentence_id", sentenceId),
                                            ("sentence", clean(sentence)),
                                            ('bigrams', list(set(ngrame(sentence,testDict,toLower,toLemma))))]))
            sentenceId += 1
    return sentencesDicts

def filter(sentences, exclude):
    badWords = exclude.lower().split()
    filteredsentences = []
    for sentence in sentences:
        test = True
        for word in badWords:
            for gramm in sentence["bigrams"]:
                if  (word+"___") in gramm:
                    test = False
        if test:
            filteredsentences.append(sentence)
    return filteredsentences

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
def extractWeightPerBigram(documentsDict,sentences,TF,IDF,minDf,maxDf,percentConcepts,question,exclude,preferencefactor =2,schritt1=0):
    bigramDict = {}
    amountDict = {1:0,2:0,3:0,4:0,5:0}
    bigrammList = []

    if TF:    
        # Term Frequency
        for sentence in sentences:
            for bigram in sentence["bigrams"]:
                bigramDict.setdefault(bigram, 0)
                bigramDict[bigram] = bigramDict[bigram] + 1
                bigrammList.append(bigram)
                amountDict[bigram.count('___')+1] = amountDict[bigram.count('___')+1]+1
    else:            
        # Document Frequency
        for documentId in documentsDict:
            for bigram in documentsDict[documentId]:
                bigramDict.setdefault(bigram, 0)
                bigramDict[bigram] = bigramDict[bigram] + 1  
                bigrammList.append(bigram) 
                amountDict[bigram.count('___')+1] = amountDict[bigram.count('___')+1]+1         
    
    #Korrekturfaktor
    amountShortestGramms =0
    for i in range(1,5):
        if amountShortestGramms ==0:
            amountShortestGramms= amountDict[i]

    schritt21 = time.time()
    print("schritt2.1:"+str(schritt21-schritt1))        

    uniqueBigrams = list(set(bigrammList))
    #IDF Fakor und Vorbereitung für minDf und maxDf als Filter auch bei DF und TF
    documentList =[]
    for sentence in sentences:
        documentList.append(sentence['document_id'])
    uniquesentences = list(set(documentList))
    amountSen =len(uniquesentences)    
    testDict = {}

    #for gram in uniqueBigrams:
        #testDict.setdefault(gram,[])
        #for documentId in documentsDict:
            #if gram in documentsDict[documentId]:
                #testDict[gram].append(documentId)
        #testDict[gram] = list(set(testDict[gram]))

    for documentID in documentsDict:
        for gramm in documentsDict[documentID]:
            testDict.setdefault(gramm,[])
            testDict[gramm].append(documentID)
            testDict[gramm] = list(set(testDict[gramm]))
    
    #question Vorbereitung
    goodWords = question.lower().split()
    questionFactor =5
    #exclude Vorbereitung
    badWords = exclude.lower().split()
    excludeFactor= -0.5

    schritt22 = time.time()
    print("schritt2.2:"+str(schritt22-schritt21))
    
    #Wert Berchnung
    if IDF:
        for gramm in uniqueBigrams:
            grammLength =gramm.count('___')+1
            # Gewichtung * Vorzugsfaktor * Korrekturfaktor *log *IDF
            if len(testDict[gramm])/amountSen <= maxDf and len(testDict[gramm]) >= minDf:
                bigramDict[gramm] = bigramDict[gramm] * (grammLength*preferencefactor) * (amountShortestGramms/amountDict[grammLength]) * math.log(amountSen/len(testDict[gramm]))
                for word in goodWords:
                    if (word+ "___") in gramm:
                        bigramDict[gramm] = bigramDict[gramm] *questionFactor
                for word in badWords:
                    if (word+ "___") in gramm:
                        bigramDict[gramm] = bigramDict[gramm] *excludeFactor
            else:
                bigramDict.pop(gramm, None)
    else:
        for gramm in uniqueBigrams:
            grammLength =gramm.count('___')+1
            # Gewichtung * Vorzugsfaktor * Korrekturfaktor 
            if len(testDict[gramm])/amountSen <= maxDf and len(testDict[gramm]) >= minDf:
                bigramDict[gramm] = bigramDict[gramm] * (grammLength*preferencefactor) * (amountShortestGramms/amountDict[grammLength]) 
                for word in goodWords:
                    if (word+ "___") in gramm:
                        bigramDict[gramm] = bigramDict[gramm] *questionFactor
                for word in badWords:
                    if (word+ "___") in gramm:
                        bigramDict[gramm] = bigramDict[gramm] *excludeFactor
            else:
                bigramDict.pop(gramm, None)

    schritt23 = time.time()
    print("schritt2.3:"+str(schritt23-schritt22))
    # Top N Prozent auswählen 
    if percentConcepts != "100":
        amountConcepts = int(len(bigramDict) *(int(percentConcepts)/100))
        bigramDict =dict(sorted(bigramDict.items(), key=lambda item: item[1], reverse = True)[:amountConcepts])
    return bigramDict

# Erstellt eine Matrix mit den Vorkommnissen der Engrammen in den Sätzen
# Anzahl der Spalten ist Anzahl der Ngramme
# Anzahl der Zeilen ist Anzahl der Sätze
def calculateOccurrences(bigramList, sentenceBigramList):
    dimColumns = len(bigramList)
    dimRows = len(sentenceBigramList)
    occ = [[0 for j in range(dimColumns)] for i in range(dimRows)]
    for i in range(len(sentenceBigramList)):
        for j in range(len(bigramList)):
            if bigramList[j] in sentenceBigramList[i]:
                occ[i][j] = 1
    return occ

# TODO: dies ist zu ressourcenintensiv -> doch direkt mit glpk? Kann das optimiert werden?
# TODO: wegen Serverzugriff Mail schreiben 
def calculateSummary(saetze, weights, occurrences, totalLength):
    i = len(weights)  # Anzahl der Konzepte
    l = list(map(lambda x: len(x), saetze))  # [len(satz1), len(satz2), len(satz3)]  # länge der Sätze
    j = len(saetze)
    begin('test konzepte')
    c = var('c', i, kind=bool)  # ist ein konzept im Summary enhalten
    s = var('s', j, kind=bool)  # ist ein Satz im Summary enthalten

    maximize(sum(weights[a] * c[a] for a in range(i)))
    sum(l[b] * s[b] for b in range(j)) <= totalLength
    for a in range(i):
        sum(s[b] * occurrences[b][a] for b in range(j)) >= c[a]
        for b in range(j):
            s[b] * occurrences[b][a] <= c[a]
    solve()
    print("###>Objective value: %f" % vobj())
    sentences = []
    for b in range(j):
        # print(s[b].primal)
        if s[b].primal == 1.0:
            sentences.append(saetze[b]["sentence"])

    summary = { "sentences": [],
            "timestamp": [],
            "timestampsforDiagramm": [],
            "occurrencesforDiagramm": [],
            "timestamp_dict": {} }
    print(sentences)
    summary["sentences"] = sentences
    return summary

def calculateSummaryGreedy(sentenceList, sentences, weights, occurrences, maxTotalLength):
    sentenceIndices = []
    totalLength = 0
    continueSearching = True
    sentenceDict={}
    for s in sentences:
        sentenceDict[s["sentence_id"]]= s["sentence"]

    # calculate total value for all sentences
    sentenceValue = []
    for s in sentenceList:
        sentenceValue.append(0)
    for i in range(len(sentenceList)):
        for j in range(len((weights))):
            sentenceValue[i] += occurrences[i][j] * weights[j]

    sentence =""
    while continueSearching:
        # get maximum value per length
        maxVal = 0
        maxSentence = -1
        for i in range(len(sentenceValue)):
            val = sentenceValue[i] / len(sentenceDict[sentenceList[i]])
            if (maxVal < val) & (totalLength + len(sentenceDict[sentenceList[i]]) < maxTotalLength):
                maxVal = val
                maxSentence = i
                sentence = sentenceDict[sentenceList[i]]

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
            "occurrencesforDiagramm": [],
            "timestamp_dict": {} }

    for i in sentenceIndices:
        for s in sentences:
            if(s["sentence_id"] == sentenceList[i]):
                # timestamp wird auf das passende Format gebracht
                summary["sentences"].append(s["sentence"])
                fastformatiert = s["timestamp"].replace('T', ' ')
                formatiert = fastformatiert.replace('.0Z', '')
                summary["timestamp"].append(formatiert)
                summary["timestamp_dict"][formatiert] = s["sentence"]

    return summary

# TODO: einschränkung auf einen gewissen Zeitraum
# TODO: zeitpunkte in Gewichtung mi einbeziehen
# TODO: mit evaluationsmatrix evaluieren -> siehe Mail

def gesamt(one,two,three,four, dataset,percentConcepts,maxLength,startDate=None,endDate=None,returnorder="",hardexclude=True,TF=True,IDF=True,minDf=3,maxDf=0.8,toLower=True,toLemma=False,question="",exclude=""):
    testDict = {"1":one, "2":two,"3":three,"4":four}
    print("Start!")
    start = time.time()
    pathToFile = "/usr/src/app/Datensaetze/prepared/"+dataset
    data = readInput(pathToFile)

    # Test für grafische Darstellung des Diagramms
    timeDataForDiagramm = sum_appearances(data)

    sentences_all = extractSentencesNLTK(data,testDict,toLower,toLemma)

    sentences= []
    if startDate != "T" and endDate != "T":
        for sentence in sentences_all:
            if sentence["timestamp"] > startDate and sentence["timestamp"] < endDate:
                sentences.append(sentence)
    else:
        sentences = sentences_all

                

    if exclude != "" and hardexclude:
        sentences = filter(sentences,exclude)

    bigramsPerDocument = extractBigramsPerDocument(sentences)
    if hardexclude:
        exclude= ""

    schritt1 = time.time()
    print("Schritt1:"+str(schritt1-start))
    
    bigramWeights = extractWeightPerBigram(bigramsPerDocument,sentences,TF,IDF,minDf,maxDf,percentConcepts,question,exclude,schritt1)
    schritt2 = time.time()
    print("Schritt2:"+str(schritt2-schritt1))
    print(len(sentences))
    print(len(bigramWeights))
    occ = calculateOccurrences(list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).keys()), [s['bigrams'] for s in sentences])
    weights = list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).values())
    sentenceList = [s['sentence_id'] for s in sentences]
    schritt3 = time.time()
    print("Schritt3:"+str(schritt3-schritt2))

    summarySenetencesincomplete = calculateSummaryGreedy(sentenceList, sentences, weights, occ, maxLength)
    #summarySenetences = calculateSummary(sentences, weights, occ, maxLength)#summarySenetencesincomplete
    summarySenetences = add_sum_appearances(summarySenetencesincomplete,timeDataForDiagramm)

    if returnorder == "first_found_first":
        summarySenetences["sentences"] =list(summarySenetences["timestamp_dict"].values())
    if returnorder == "last_found_first":
        summarySenetences["sentences"] =list(sorted(summarySenetences["timestamp_dict"],reverse=True).values())

    schritt4 = time.time()
    print("Schritt4:"+str(schritt4-schritt3))
    #print(summarySenetences)

    end = time.time()
    print("Fertig!")
    print(end - start)
    print("Sekunden Ausfuehrungszeit")
    return json.dumps(summarySenetences) 