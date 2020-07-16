FROM node:14
WORKDIR /usr/app/src
COPY package*.json ./
RUN mkdir /root/.cache && mkdir /root/.cache/ffmpeg-static-nodejs && npm install
COPY . .
RUN npm run bundle
CMD ["node", "./dist/bundle.js"]