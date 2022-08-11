Wichtig! Da ständiges Builden auf längere Zeit lästig wird habe ich bei mir ein Volume erstellt. Damit kann der Inhalt vom Ordner "Data" geändert werden, ohne, dass das komplette Image neu gebuildet werden muss.
Um das Image auf anderen Rechnern, die kein Volume besitzen, lauffähig zu machen muss die auskommentierte Stellte in der Dockerfile wieder reaktiviert werden.

Für Build:
docker build -t <Name> . 


