FROM nginx:alpine 

WORKDIR /usr/share/nginx/html
COPY /Data /usr/share/nginx/html

RUN apk add npm

RUN npm install chart.js


