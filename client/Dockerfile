FROM node:16-buster-slim

RUN mkdir -p /app
WORKDIR /app

COPY package.json yarn.lock ./

ADD . /app

RUN yarn install

EXPOSE 3000

CMD yarn start
