FROM node:21-alpine3.18
WORKDIR /usr/src/app
EXPOSE 3000
COPY docker-start.sh /usr/src/app/docker-start.sh
COPY package.json /usr/src/app/package.json
COPY app.js /usr/src/app/app.js
COPY public/ /usr/src/app/public/
RUN npm install
ENTRYPOINT ["/usr/src/app/docker-start.sh"]
CMD ["--redis", "redis"]