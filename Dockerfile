FROM node:14-alpine as frontend
WORKDIR /usr/src/app
COPY ./frontend/package.json .
RUN npm i && npm install --save @popperjs/core
COPY ./frontend .
RUN npm run build

FROM nginx:1.20.1-alpine
WORKDIR /usr/src/app
COPY --from=frontend /usr/src/app/dist ./dist
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 48763
CMD nginx -g 'daemon off;'
