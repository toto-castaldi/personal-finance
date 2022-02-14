# build stage
FROM node:16.13-alpine3.14 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./src/ ./src/
COPY ./public/ ./public/
COPY vue.config.js ./
COPY babel.config.js ./
COPY package.json ./
COPY package-lock.json ./
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /data/www
COPY nginx.conf /etc/nginx/nginx.conf


EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]