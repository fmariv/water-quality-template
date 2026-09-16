FROM node:24

WORKDIR /app

COPY package.json ./
COPY yarn.lock* ./
RUN if [ -f yarn.lock ]; then yarn install --frozen-lockfile; else yarn install; fi
COPY . .
COPY .env .env

EXPOSE 80

CMD yarn run build && yarn run preview --host 0.0.0.0 --port 80
