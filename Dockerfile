FROM node:18

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm i @opentelemetry/sdk-node
RUN npm i @opentelemetry/auto-instrumentations-node
RUN npm i @opentelemetry/context-async-hooks
RUN npm i @opentelemetry/api

COPY . .

RUN npm run build

CMD ["node", "dist/main.js"]
