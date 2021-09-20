FROM node:14 as frontend
WORKDIR /usr/src/app
COPY frontend/package.json .
RUN npm i
COPY . .
RUN npm run build


FROM nginx:1.21.1
WORKDIR /usr/src/app
COPY --from=frontend /usr/src/app/dist ./frontend
RUN apt install -y redis-server && apt-get update -y && apt-get install -y python3.7 && apt-get install -y python3-pip \
 && python3 -m pip install --upgrade pip && apt-get install -y libpq-dev python-dev
COPY backend .
COPY nginx.conf /etc/nginx/conf.d/default.conf
WORKDIR /usr/src/app/backend
RUN pip install -r requirements.txt
# 還沒寫完與測試
CMD ["service", "nginx", "start"]
CMD ["nginx", "-g", "daemon off;"]
