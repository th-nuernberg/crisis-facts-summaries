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

# %% Loads addtional features of nltk
def init():
    nltk.download('punkt')

# %% Reads the corpus select through the path variable and returns it
def readInput(pathToFile):
    df = []
    with open(pathToFile, 'r', encoding="utf-8") as jsonFile:
        mytext = jsonFile.read()
        lines = mytext.split("\n")
        for line in lines:
            if len(line) > 0:
                df.append(json.loads(line))
    return df

# %% Counts how many entries were created at a given time to use in the website diagramm.
def sum_appearances(rohdaten):
    listofDates = []
    for satz in rohdaten:
        time = satz["timestamp"]
        listofDates.append(time)

    return listofDates

# %% Counts how many sentences from a given were included in the summary
def add_sum_appearances(summarySenetences,timeDataForDiagramm):
    for s in timeDataForDiagramm:
        summarySenetences["timestampsforDiagramm"].append(s)

    return summarySenetences

# %% Cleans the text of unnessacary tokens
def clean(text):
    # tags like <tab>
    text = re.sub(r'<[^<>]*>', ' ', text)
    # markdown URLs like [Some text](https://....)
    text = re.sub(r'\[([^\[\]]*)\]\([^\(\)]*\)', r'\1', text)
    text = re.sub(r'http.+', ' ', text)
    # text or code in brackets like [0]
    text = re.sub(r'\[[^\[\]]*\]', ' ', text)
    # standalone sequences of specials, matches &# but not #cool
    text = re.sub(r'(?:^|\s)[&#<>{}\[\]+|\\:-]{1,}(?:\s|$)', ' ', text)
    # standalone sequences of hyphens like --- or ==
    text = re.sub(r'(?:^|\s)[\-=\+]{2,}(?:\s|$)', ' ', text)
    # smiley or other emojies
    text = re.sub(r'[\U00010000-\U0010ffff]', ' ', text)
    # sequences of white spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# %% Cleans the text input and then creates Ngramms 
# The Ngramms are then used as concepts
def ngrame(originalText_,testDict,toLower,stopwords):
    stopwords =[]
    with open('/usr/src/app/Datensaetze/stopwords-en.txt', encoding='utf-8') as file:
        stopwords = file.read().splitlines()
    result = []
    text = ""
    originalText = clean(originalText_)
    if toLower:
        originalText = originalText.lower()
    if stopwords:
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
                    hold += gram
                    hold +="___"
                ngrame.append(hold)
            result.extend(ngrame)
    
    return result

# %%  Divides the documents into sentences and creates the finegrained text corpus
def extractSentencesNLTK(rawDicts,testDict,toLower,stopwords):
    sentencesDicts = []
    sentenceId = 0
    for rawDict in rawDicts:
        sentences = nltk.sent_tokenize (rawDict['content'])
        sentences = list(map(lambda x: x.strip(), sentences))
        for sentence in sentences:
            if len(clean(sentence)) >0:
                ngrams = list(set(ngrame(sentence,testDict,toLower,stopwords)))
                if len(ngrams) >0:
                    sentencesDicts.append(dict([("timestamp", rawDict['timestamp']),
                                            ("document_id", rawDict['document_id']),
                                            ("sentence_id", sentenceId),
                                            ("sentence", clean(sentence)),
                                            ('bigrams', ngrams)]))
            sentenceId += 1
    return sentencesDicts

# %% If any words must not be in the summray, sentences containg these are remove form the text corpus
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

# %% Creates a Dict to tell which document contains which concepts 
def extractBigramsPerDocument(sentenceDicts):
    documentDict = {}
    for sentenceDict in sentenceDicts:
        documentId = sentenceDict['document_id']
        documentDict.setdefault(documentId, [])
        documentDict[documentId] = documentDict[documentId] + sentenceDict['bigrams']
    for key in documentDict:
        documentDict[key] = list(set(documentDict[key]))
    return documentDict

# %% Creates a weigth for each concept
#   - Termn Frequency: Weight is the amount of appearnces of the concept
#   - Document Frequency: Weight is the amount of appearnces of the concept calculate for each document
#   - Termn Frequency-Inverse Document Frequency: Weight is the amount of appearnces of the concept with a fokus on Concepts that are in very little documents
def extractWeightPerBigram(documentsDict,sentences,TF,IDF,minDf,maxDf,percentConcepts,question,exclude,questionFactor,excludeFactor,preferencefactor =2):
    bigramDict = {}
    amountDict = {1:0,2:0,3:0,4:0,5:0}
    bigrammList = []

    if TF:    
        # Term Frequency also used by the TF-IDF methode
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
    
    #Correction Factor
    amountShortestGramms =0
    for i in range(1,5):
        if amountShortestGramms ==0:
            amountShortestGramms= amountDict[i]        

    uniqueBigrams = list(set(bigrammList))
    #IDF Factor und prepartion for minDf und maxDf to filter the concepts also for DF und TF
    documentList =[]
    for sentence in sentences:
        documentList.append(sentence['document_id'])
    uniquesentences = list(set(documentList))
    amountSen =len(uniquesentences)    
    testDict = {}

    for documentID in documentsDict:
        for gramm in documentsDict[documentID]:
            testDict.setdefault(gramm,[])
            testDict[gramm].append(documentID)
            testDict[gramm] = list(set(testDict[gramm]))
    
    #question words preparation
    goodWords = question.lower().split()
    #exclude words preparation
    badWords = exclude.lower().split()
    
    reducedBigramDict ={}
    #Calculate the value of each concept
    if IDF:
        for gramm in uniqueBigrams:
            grammLength =gramm.count('___')+1
            # Weigth * Preferrnce Factor * Correction Factor *log(IDF)
            if len(testDict[gramm])/amountSen <= maxDf and len(testDict[gramm]) >= minDf:
                reducedBigramDict [gramm] = bigramDict[gramm] * (grammLength*preferencefactor) * (amountShortestGramms/amountDict[grammLength]) * math.log(amountSen/len(testDict[gramm]))
                for word in goodWords:
                    if (word+ "___") in gramm:
                        reducedBigramDict[gramm] = bigramDict[gramm] *questionFactor
                for word in badWords:
                    if (word+ "___") in gramm:
                        reducedBigramDict[gramm] = bigramDict[gramm] *excludeFactor
    else:
        for gramm in uniqueBigrams:
            grammLength =gramm.count('___')+1
             # Weigth * Preferrnce Factor * Correction Factor
            if len(testDict[gramm])/amountSen <= maxDf and len(testDict[gramm]) >= minDf:
                reducedBigramDict[gramm] = bigramDict[gramm] * (grammLength*preferencefactor) * (amountShortestGramms/amountDict[grammLength]) 
                for word in goodWords:
                    if (word+ "___") in gramm:
                        reducedBigramDict[gramm] = bigramDict[gramm] *questionFactor
                for word in badWords:
                    if (word+ "___") in gramm:
                        reducedBigramDict[gramm] = bigramDict[gramm] *excludeFactor

    # Select top N Percent of the Concepts
    if percentConcepts != "100":
        amountConcepts = int(len(reducedBigramDict) *(int(percentConcepts)/100))
        reducedBigramDict =dict(sorted(reducedBigramDict.items(), key=lambda item: item[1], reverse = True)[:amountConcepts])
    return reducedBigramDict

# %% Checks if a sentence is a promising to be inclueded in the summary and returns a list containing only these sentenceces
def filterSentences(sentences,bigramWeights,sentenceFactor):
    sentencesFiltered =[]
    sentenceFactor = float(sentenceFactor)

    weightAllSentences =0
    for sentence in sentences:
        sentenceWeight =0
        for bigramm in sentence['bigrams']:
            sentenceWeight = sentenceWeight+ bigramWeights.get(bigramm,0)
        sentence["meanSentenceWeight"] = sentenceWeight / len(sentence["bigrams"])
        weightAllSentences = weightAllSentences + (sentenceWeight / len(sentence["bigrams"]))

    for sentence in sentences:
        if sentence["meanSentenceWeight"] > (weightAllSentences/ len(sentences))*sentenceFactor:
            sentencesFiltered.append(sentence)
    
    return sentencesFiltered

# %% Selectes only the sentences in the given timespan
def filterTimespan(sentences_all,startDate,endDate):
    sentences= []
    if startDate != "T" and endDate != "T":
        for sentence in sentences_all:
            if sentence["timestamp"] > startDate and sentence["timestamp"] < endDate:
                sentences.append(sentence)
    else:
        sentences = sentences_all
    return sentences

# %% Creates a Matrix depcting the occurnces of Ngramms in sentneces
# The amount of columns equals the amount of concepts 
# The amount of rows equals the amount of sentences 
def calculateOccurrences(bigramList, sentenceBigramList):
    dimColumns = len(bigramList)
    dimRows = len(sentenceBigramList)
    occ = [[0 for j in range(dimColumns)] for i in range(dimRows)]
    for i in range(len(sentenceBigramList)):
        for j in range(len(bigramList)):
            if bigramList[j] in sentenceBigramList[i]:
                occ[i][j] = 1
    return occ

# %% Calculates a summary using inteager linear programming to find a optimal solution
def calculateSummary(saetze, weights, occurrences, totalLength):
    i = len(weights)  # Amount of concepts
    l = list(map(lambda x: len(x["sentence"]), saetze))    # Amount of sentences
    j = len(saetze)
    begin('test konzepte')
    c = var('c', i, kind=bool)  # is a Concept contained in the summary
    s = var('s', j, kind=bool)  # is a Concept contained in a sentence

    # set the functions to solve
    maximize(sum(weights[a] * c[a] for a in range(i)))
    sum(l[b] * s[b] for b in range(j)) <= totalLength
    for a in range(i):
        sum(s[b] * occurrences[b][a] for b in range(j)) >= c[a]
        for b in range(j):
            s[b] * occurrences[b][a] <= c[a]
    solve()
    summary = { "sentences": [],
            "timestampsforDiagramm": [],
            "timestamp_dict": {} }
    for b in range(j): 
        if s[b].primal == 1.0:
            summary["sentences"].append(saetze[b]["sentence"])
            summary["timestamp_dict"][saetze[b]["timestamp"]] = saetze[b]["sentence"]
   
    return summary

# %% Calculates a Summary using a greedy approach
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
            # no new sentence that fit the length was found, end the search
            continueSearching = False 

    summary = { "sentences": [],
            "timestampsforDiagramm": [],
            "timestamp_dict": {} }
    # Creates a list of sentences using the choosen sentenceId
    for i in sentenceIndices:
        for s in sentences:
            if(s["sentence_id"] == sentenceList[i]):
                summary["sentences"].append(s["sentence"])
                summary["timestamp_dict"][s["timestamp"]] = s["sentence"]
    
    return summary

# %% Excution of the functions as needed with the correct parameters. Returns a summary of the selected text and the data for the diagramm
def gesamt(one,two,three,four, dataset,percentConcepts,maxLength,questionFactor,excludeFactor,calcMethode,sentenceFactor,Timeout,startDate=None,endDate=None,returnorder="",stopwords=True,hardexclude=True,TF=True,IDF=True,minDf=3,maxDf=0.8,toLower=True,question="",exclude=""):
    testDict = {"1":one, "2":two,"3":three,"4":four}
    print("Start!")
    start = time.time()
    pathToFile = "/usr/src/app/Datensaetze/prepared/"+dataset
    data = readInput(pathToFile)
    Timeout = Timeout/1000
    returnValueTimeout = { "sentences": ["Timeout"],"timestampsforDiagramm": [],"timestamp_dict": {},"amountSentences":0,"amountConcepts":0}

    # Test für grafische Darstellung des Diagramms
    timeDataForDiagramm = sum_appearances(data)

    # Creates a finegrained text corpus
    sentences_all = extractSentencesNLTK(data,testDict,toLower,stopwords)

    # Filters the corpus only including the sentences which are in a given timespan
    sentences = filterTimespan(sentences_all,startDate,endDate)

    if exclude != "" and hardexclude:
        sentences = filter(sentences,exclude)

    if hardexclude:
        exclude= ""

    bigramsPerDocument = extractBigramsPerDocument(sentences)

    # Checks if the maximum time for the calculation is up 
    schritt1 = time.time()
    if schritt1-start >Timeout:
        # returns an empty json 
        return returnValueTimeout
    else:
        # prints how long it took for the first step to finish
        print("Schritt1:"+str(schritt1-start))
    
    # Calculates the weigth for each bigramm using the reqeusted represtation form
    bigramWeights = extractWeightPerBigram(bigramsPerDocument,sentences,TF,IDF,minDf,maxDf,percentConcepts,question,exclude,questionFactor,excludeFactor)

    # Checks if the maximum time for the calculation is up
    schritt2 = time.time()
    if schritt2-start >Timeout:
        return returnValueTimeout
    else:
        print("Schritt2:"+str(schritt2-schritt1))

    # Filters the sentences to only include the most promising ones
    sentences = filterSentences(sentences, bigramWeights,sentenceFactor)
  
    occ = calculateOccurrences(list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).keys()), [s['bigrams'] for s in sentences])
    weights = list(dict(sorted(bigramWeights.items(), key=lambda item:item[1], reverse=True)).values())
    sentenceList = [s['sentence_id'] for s in sentences]

    # Checks if the maximum time for the calculation is up
    schritt3 = time.time()
    if schritt3-start >Timeout:
        return returnValueTimeout
    else:
        print("Schritt3:"+str(schritt3-schritt2))

    # Checks if the greedy or the optimal solution is requested
    if calcMethode == "Greedy":
        summarySenetencesIncomplete = calculateSummaryGreedy(sentenceList, sentences, weights, occ, maxLength)
    else:
        summarySenetencesIncomplete = calculateSummary(sentences, weights, occ, maxLength)
    summarySenetences = add_sum_appearances(summarySenetencesIncomplete,timeDataForDiagramm)
    
    # Gets the sentences in the reqeusted order
    if returnorder == "oldest_found_first":
        summarySenetences["sentences"] =[]
        timestamps = sorted(summarySenetences["timestamp_dict"])
        for timestamp in timestamps:
            summarySenetences["sentences"].append(summarySenetences["timestamp_dict"][timestamp])
    if returnorder == "newest_found_first":
        summarySenetences["sentences"] = []
        timestamps = sorted(summarySenetences["timestamp_dict"],reverse=True)
        for timestamp in timestamps:
            summarySenetences["sentences"].append(summarySenetences["timestamp_dict"][timestamp])

    # Checks if the maximum time for the calculation is up
    schritt4 = time.time()
    if schritt4-start >Timeout:
        return returnValueTimeout
    else:
        print("Schritt4:"+str(schritt4-schritt3))

    # Checks  how many concepts and sentences were used 
    summarySenetences["amountSentences"] = str(len(sentences))
    summarySenetences["amountConcepts"] = str(len(bigramWeights))

    # some information for the user
    end = time.time()
    print("Fertig!")
    print(end - start)
    print("Sekunden Ausfuehrungszeit")

    return json.dumps(summarySenetences) 