import machine
import network
import socket
from time import sleep
from picozero import pico_temp_sensor
from umqtt.simple import MQTTClient

class WlanConnection:   
    def __init__(self, ssid, password):
        self._ssid = ssid
        self._password = password

    def connect(self, timeout=120):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self._ssid, self._password)

        while not wlan.isconnected() and timeout > 0:
            print("Connecting...")
            timeout = timeout - 1
            sleep(1)

        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            print(f"Connected to WiFi on IP {ip}")
            return ip
        else:
            raise Exception("Connection timed out")

class MqttConnection:
    def __init__(self, mqtt_server, client_id, user, password):
        self._mqtt_server = mqtt_server
        self._client_id = client_id

    def connect(self, port=None):
        if port is not None:
            self._client = MQTTClient(self._client_id, self._mqtt_server, port=port, keepalive=7200, user=user, password=password)
        else:
            self._client = MQTTClient(self._client_id, self._mqtt_server, keepalive=7200, user=user, password=password)

        self._client.connect()
        print('Connected to {self._mqtt_server} MQTT Broker')
        return self._client
    
    def reconnect(self):
         print('Failed to connect to the MQTT Broker. Reconnecting...')
         sleep(5)
         machine.reset()
    
    def publish(self, topic, message):
        if self._client is not None:
            self._client.publish(topic, message)
        else:
            print("Client not initialized. Connect and try again.")


HOSTNAME = ""
USERNAME = ""
PASSWORD = ""
TOPIC = b"picotemp/temperature"

mqtt_connection = MqttConnection(HOSTNAME, "PicoClient", USERNAME, PASSWORD)
try:
    ssid=""
    password=""

    wlan = WlanConnection(ssid, password)
    ip = wlan.connect()

    client = mqtt_connection.connect(port=1883)

    while True:
        temp = str(pico_temp_sensor.temp)
        print(temp)
        mqtt_connection.publish(TOPIC, bytes(temp, 'utf8'))
        sleep(3)
    
except KeyboardInterrupt:
    machine.reset()
except OSError as e:
    print(e)
    mqtt_connection.reconnect()

