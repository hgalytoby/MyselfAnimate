FROM python:3.8-alpine
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Taipei
RUN apk add tzdata
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apk update && apk add python3-dev gcc libc-dev libffi-dev libwebp-dev
RUN apk add --no-cache jpeg-dev zlib-dev ffmpeg
RUN apk add --no-cache --virtual .build-deps build-base linux-headers 
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt 
COPY . /usr/src/app