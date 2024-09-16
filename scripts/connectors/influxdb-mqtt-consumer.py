import influxdb_client
import paho.mqtt.client as mqtt
from influxdb_client import Point

from scripts.connectors.config import Config
from scripts.connectors.influx_database import InfluxDB

mqttc = mqtt.Client()
mqttc.connect(host = Config.MQTT_BROKER_URL, port = Config.MQTT_BROKER_PORT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(Config.INFLUXDB_MEASUREMENT)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    payload_data = msg.payload
    point = Point(Config.INFLUXDB_MEASUREMENT).tag("equipmentId", payload_data["equipmentId"]).field("value", payload_data["value"])
    InfluxDB.write_data(point)

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_forever()