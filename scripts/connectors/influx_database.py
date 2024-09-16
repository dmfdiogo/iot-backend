from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from app.config.config import Config

class InfluxDB:
    def __init__(self):
        self.client = InfluxDBClient(url=Config.INFLUXDB_URL, token=Config.INFLUXDB_TOKEN, org=Config.INFLUXDB_ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.bucket = Config.INFLUXDB_BUCKET

    def write_data(self, data):
        self.write_api.write(bucket=self.bucket, record=data)

    def query_data(self, query):
        return self.query_api.query(query=query)

    def close(self):
        self.client.close()