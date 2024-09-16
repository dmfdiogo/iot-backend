import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    INFLUXDB_URL = os.getenv('INFLUXDB_URL')
    INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
    INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
    INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')
    INFLUXDB_MEASUREMENT = os.getenv('INFLUXDB_MEASUREMENT')

    MQTT_BROKER_URL = "localhost"
    MQTT_BROKER_PORT = 1883
    MQTT_PUBLISH_TOPIC = "my-measures"