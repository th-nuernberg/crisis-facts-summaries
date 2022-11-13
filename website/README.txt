Wichtig! Da ständiges Builden auf längere Zeit lästig wird habe ich bei mir ein Volume erstellt. Damit kann der Inhalt vom Ordner "Data" geändert werden, ohne, dass das komplette Image neu gebuildet werden muss.
Um das Image auf anderen Rechnern, die kein Volume besitzen, lauffähig zu machen müssen die auskommentierte Stellte in der Dockerfile wieder reaktiviert werden.

- Dockerfile Kommentare clearen
- node_Modules aus Data löschen 


Für Build:
docker build -t <Name> . 

Für den Run:
docker run -v <PathToDocuments>:/usr/src/app/Datensaetze/ -p 5000:5000 <ImageName>




