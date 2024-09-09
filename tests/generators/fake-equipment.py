import paho.mqtt.client as mqtt
import time
from faker import Faker

MQTT_BROKER_URL = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_PUBLISH_TOPIC = "my-measures"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)
client.loop_start()

fake = Faker()
while True:
    value = fake.random_int(min=0, max=30)
    equipment_number = fake.random_int(min=0, max=2000)
    fake_payload = [{"equipmentId": f"EQ-${equipment_number}"},{"value": value}]
    client.publish(MQTT_PUBLISH_TOPIC, fake_payload)
    print(f"Published new measurement: {fake_payload} to topic: {MQTT_PUBLISH_TOPIC}")
    time.sleep(1)


client.loop_stop()