## Iot-backend (for radix challenge)

## Features

* developed with FastApi
* user management
* equipment management
* equipment data (todo)
* csv upload
* swagger documentation

## Auxiliary scripts

* /scripts/connectors/influxdb-mqtt-consumer.py handles the communication from mqtt broker to influxdb 
* /tests/generators/fake-equipment handles fake data generation for emulating an equipment

## Installation

1. Make sure you have Python 3.x installed.
2. Clone this repository: `git clone https://github.com/dmfdiogo/Iot-backend.git`
3. Navigate to the project directory: `cd my-awesome-project`
4. Install dependencies: `pip install -r requirements.txt`
5. run docker commands:
    5.1 docker build --no-cache -t my-api-img .
    5.2 docker-compose up -d