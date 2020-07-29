FROM node:14
LABEL maintainer="KislBall <kislball@yahoo.com>"
WORKDIR /app
COPY package*.json ./
# installing jq for getting data from json file
RUN apt update && apt install jq -y
RUN mkdir -p /root/.cache && mkdir -p /root/.cache/ffmpeg-static-nodejs && npm ci --only=production
RUN mkdir /app/logs
COPY . .
CMD ["npm", "run", "start"]