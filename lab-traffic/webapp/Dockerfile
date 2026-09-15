FROM node:24-alpine@sha256:50c8e8ca1d27439048670df5883f32d57cf81cff6233222c893fd0d9884cbd81
WORKDIR /usr/src/app
EXPOSE 3000
COPY --chmod=711 docker-start.sh /docker-start.sh
COPY package.json package-lock.json /usr/src/app/
COPY app.js /usr/src/app/app.js
COPY public/ /usr/src/app/public/
RUN npm ci --omit=dev --no-audit --no-fund
ENTRYPOINT ["/docker-start.sh"]
