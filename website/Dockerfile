FROM nginx:alpine 

WORKDIR /usr/share/nginx/html
COPY /Data /usr/share/nginx/html

RUN apk add npm
RUN npm install chart.js

RUN apk add python3
RUN apk add py3-pip
RUN pip install flask
RUN pip install flask-cors

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000