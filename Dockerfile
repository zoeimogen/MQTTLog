FROM python:3-alpine
LABEL maintainer="zoe@complicity.co.uk"
RUN apk add build-base python3-dev
RUN pip install paho-mqtt
COPY mqttlog.py /app/
WORKDIR /app
CMD python3 ./mqttlog.py
