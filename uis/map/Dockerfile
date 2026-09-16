FROM node:24

WORKDIR /app

COPY package.json ./
COPY yarn.lock* ./
RUN yarn install --frozen-lockfile || yarn install
COPY . .
# Cloud images must not bake MapTiler/API secrets; always use HTTPS in PRO builds.
RUN printf "VITE_ENV=PRO\n" > .env

EXPOSE 80

CMD yarn run build && yarn run preview --host 0.0.0.0 --port 80

