from pymprog import *

satz1 = "hallo wie geht es"
satz2 = "test satz bla"
satz3 = "test satz 2"

saetze = ["hallo wie geht es",
          "test satz bla",
          "test satz 2"
          ]

l = list(map( lambda x: len(x), saetze)) #[len(satz1), len(satz2), len(satz3)]  # länge der Sätze
j = len(saetze)  # anzahl Sätze

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
i = len(w)  # Anzahl der Konzepte

L = 30  # Anzhal Buchstaben im Summary

begin('test konzepte')
c = var('c', i, kind=bool)  # ist ein konzept im Summary enhalten
s = var('s', j, kind=bool)  # ist ein Satz im Summary enthalten
maximize(sum(w[a] * c[a] for a in range(i)))
sum(l[b] * s[b] for b in range(j)) <= L
for a in range(i):
    sum(s[b] * Occ[b][a] for b in range(j)) >= c[a]
    for b in range(j):
        s[b] * Occ[b][a] <= c[a]
solve()
print("###>Objective value: %f" % vobj())
for b in range(j):
    #print(s[b].primal)
    if s[b].primal == 1.0:
        print(saetze[b])
