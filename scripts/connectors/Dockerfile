FROM python:latest

WORKDIR /scripts/connectors

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN chmod +x influxdb-mqtt-consumer.py

CMD ["python", "influxdb-mqtt-consumer.py"]