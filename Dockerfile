FROM node:14
WORKDIR /usr/app/src
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "."]