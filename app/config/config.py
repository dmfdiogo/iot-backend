import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    INFLUXDB_URL = os.getenv('INFLUXDB_URL')
    INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
    INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
    INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')

    INFLUXDB_DOCKER_URL = os.getenv('INFLUXDB_DOCKER_URL')

    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    INFLUX_MEASUREMENT = os.getenv('INFLUX_MEASUREMENT')

    FRONTEND_URL = os.getenv('FRONTEND_URL')