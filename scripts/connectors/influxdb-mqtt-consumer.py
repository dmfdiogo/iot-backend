import influxdb_client, os, time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from influxdb_client import Point

load_dotenv()

influxdb_token = os.getenv('INFLUXDB_TOKEN')
BUCKET = "dio-bucket"
org = "dio-org"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=influxdb_token, org=org)
write_api = client.write_api()

MQTT_BROKER_URL = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_PUBLISH_TOPIC = "my-measures"

mqttc = mqtt.Client()
mqttc.connect(host = MQTT_BROKER_URL, port = MQTT_BROKER_PORT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(MQTT_PUBLISH_TOPIC)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    payload_data = msg.payload

    point = Point(MQTT_PUBLISH_TOPIC).tag("equipmentId", payload_data["equipmentId"]).field("value", payload_data["value"])
    write_api.write(bucket=BUCKET, record=point)

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_forever()