import json

from pymprog import *
import json
import re

pathToFile = "../prepared/28.relonly.jsonl"


def readInput():
    df = []
    with open(pathToFile, 'r', encoding="utf-8") as json_file:
        mytext = json_file.read()
        lines = mytext.split("\n")
        for line in lines:
            if len(line) > 0:
                df.append(json.loads(line))
    return df


def bigramme(text):
    words = re.findall(r'[A-Za-z0-9]+', text)
    result = []
    for i in range(0, len(words)):
        if (i < (len(words) - 1)):
            result.append(words[i] + "_" + words[i + 1])
    return result


# TODO: split ist zu allgemein und trennt z. B. auch bei "B. Fischer" -> verbessern
def extractSentences(rawDicts):
    sentencesDicts = []
    sentenceId = 0
    for rawDict in rawDicts:
        sentences = re.split("\.\s", rawDict['content'])
        sentences = list(map(lambda x: x.strip() + ".", sentences))
        for sentence in sentences:
            sentencesDicts.append(dict([("timestamp", rawDict['timestamp']),
                                        ("document_id", rawDict['document_id']),
                                        ("sentence_id", sentenceId),
                                        ("sentence", sentence),
                                        ('bigrams', bigramme(sentence))]))
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


def extractWeightPerBigram(documentsDict):
    bigramDict = {}
    for documentId in documentsDict:
        for bigram in documentsDict[documentId]:
            bigramDict.setdefault(bigram, 0)
            bigramDict[bigram] = bigramDict[bigram] + 1
    return bigramDict


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
    summary = []
    for b in range(j):
        # print(s[b].primal)
        if s[b].primal == 1.0:
            print(b)
            summary.append(saetze[b])
    return summary


# TODO: this can go (slightly) above the max size
def calculateSummaryGreedy(saetze, weights, occurrences, maxTotalLength):
    sentenceIndices = []
    totalLength = 0
    ngramValuable = [1 for a in weights]
    while totalLength < maxTotalLength:
        print(totalLength)
        # calculate total value for all sentences
        sentenceValue = [0 for a in saetze]
        for i in range(len(saetze)):
            for j in range(len((weights))):
                sentenceValue[i] += occurrences[i][j] * weights[j] * ngramValuable[j]
            if i % 1000 == 0:
                print(i)
        # get maximum value per length
        maxVal = 0
        maxSentence = -1
        for i in range(len(sentenceValue)):
            val = sentenceValue[i] / len(saetze[i])
            if maxVal < val:
                maxVal = val
                maxSentence = i

        # add senetence index to the used sentences and remove the used ngrams from the valuable list
        sentenceIndices.append(maxSentence)
        totalLength += len(saetze[maxSentence])
        for i in range(len(occurrences[maxSentence])):
            if ngramValuable[i] == 1 & occurrences[maxSentence][i] == 1:
                ngramValuable[i] = 0
        print("Sentence selected:")
        print(saetze[maxSentence])

    summary = []
    for i in sentenceIndices:
        summary.append(saetze[i])

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

L = 300  # Anzhal Buchstaben im Summary

# print(calculateSummary(saetze, w, Occ, L))

data = readInput()
print(data[0])
sentences = extractSentences(data)
print(sentences[0])
bigramsPerDocument = extractBigramsPerDocument(sentences)
# print(bigramsPerDocument['7b32de22a8f61f2c6d86e40a5a786cc7'])
bigramWeights = extractWeightPerBigram(bigramsPerDocument)
# print(bigramWeights['amid_heavy'])
occ = calculateOccurrences(list(bigramWeights.keys()), [s['bigrams'] for s in sentences])
# print(occ[1])
print("occurrences ready")
weights = list(bigramWeights.values())
saetzeList = [s['sentence'] for s in sentences]
print(len(weights))
print(len(saetzeList))
summarySenetences = calculateSummaryGreedy(saetzeList, weights, occ, L)

testBigrams = ['hallo', 'wie', 'geht', 'es', 'test', 'satz', 'bla', '2']
testSatzBigrams = [s.split() for s in saetze]

# occ = calculateOccurrences(testBigrams, testSatzBigrams)
# print(occ)

# summarySenetences = calculateSummary(saetze, w, occ, L)


totalLength = 0
for s in summarySenetences:
    print(s)
    totalLength += len(s)
print(totalLength)
