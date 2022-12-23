# Kommentierte Stellen auskommentieren, falls der Container mit Volume laufen soll
FROM python:3

WORKDIR /usr/src/app
#auskommentieren falls nötig
COPY /Data /usr/src/app 

RUN apt-get -y update

#Debugging 
#RUN mkdir switch 
#RUN chmod a+rwx /usr/src/app/switch

RUN pip install flask
RUN pip install flask-cors
RUN pip install pymprog
RUN pip install nltk
RUN pip install -U scikit-learn
RUN pip install -U spacy
RUN python3 -m nltk.downloader popular

#auskommentieren falls nötig
RUN chmod a+rwx /usr/src/app/text_corpus_summarization.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
