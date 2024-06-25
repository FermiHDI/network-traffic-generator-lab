FROM node:21-alpine3.18
WORKDIR /usr/src/app
EXPOSE 3000
COPY --chmod=711 docker-start.sh /docker-start.sh
COPY package.json /usr/src/app/package.json
COPY app.js /usr/src/app/app.js
COPY public/ /usr/src/app/public/
RUN npm install
ENTRYPOINT ["/docker-start.sh"]
