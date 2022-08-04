FROM python:3

WORKDIR /usr/src/app
COPY /Data /usr/src/app

RUN apt-get -y update

RUN apt-get -y install npm
RUN npm install chart.js

RUN pip install flask
RUN pip install flask-cors

RUN mv /usr/src/app/node_modules/ /usr/src/app/static/

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
