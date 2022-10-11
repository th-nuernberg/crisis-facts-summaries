# Kommentierte Stellen einkommentieren, falls der Container ohne Volume laufen soll
FROM python:3

WORKDIR /usr/src/app
#COPY /Data /usr/src/app

RUN apt-get -y update

RUN apt-get -y install npm
RUN npm install chart.js
RUN npm install date-fns chartjs-adapter-date-fns --save
RUN npm install chartjs-plugin-zoom

RUN pip install flask
RUN pip install flask-cors
RUN pip install pymprog
RUN pip install nltk
RUN pip install textacy
RUN pip install pandas
RUN pip install -U scikit-learn
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN python3 -m nltk.downloader popular

#RUN mv /usr/src/app/node_modules/ /usr/src/app/static/
#RUN chmod a+rwx /usr/src/app/glpk_test.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
