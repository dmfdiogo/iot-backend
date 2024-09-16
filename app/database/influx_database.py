import time
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from app.config.config import Config

class InfluxDB:
    def __init__(self):
        self.client = InfluxDBClient(url=Config.INFLUXDB_DOCKER_URL, token=Config.INFLUXDB_TOKEN, org=Config.INFLUXDB_ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.bucket = Config.INFLUXDB_BUCKET

    def write_data(self, data, retries=3, delay=1):
        for attempt in range(retries):
            try:
                self.write_api.write(bucket=self.bucket, record=data)
                return
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise

    def query_data(self, query):
        return self.query_api.query(query=query)

    def close(self):
        self.client.close()