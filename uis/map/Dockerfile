FROM node:24

WORKDIR /app

COPY package.json ./
COPY yarn.lock* ./
RUN yarn install --frozen-lockfile || yarn install
COPY . .
COPY .env .env

EXPOSE 80

CMD yarn run build && yarn run preview --host 0.0.0.0 --port 80

