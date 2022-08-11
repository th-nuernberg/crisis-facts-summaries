# Kommentierte Stellen einkommentieren, falls der Container ohne Volume laufen soll
FROM python:3

WORKDIR /usr/src/app
#COPY /Data /usr/src/app

RUN apt-get -y update

RUN apt-get -y install npm
RUN npm install chart.js

RUN pip install flask
RUN pip install flask-cors
RUN pip install pymprog
RUN pip install nltk
RUN python3 -m nltk.downloader popular

#RUN mv /usr/src/app/node_modules/ /usr/src/app/static/
#RUN chmod a+rwx /usr/src/app/glpk_test.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
