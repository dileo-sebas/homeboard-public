import logging
from time import sleep

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import paho.mqtt.client as mqtt

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# TODO Create Sensor for this to work. Maybe from admin? Add check that verifies the sensor exists.
from .models import Reading, Sensor

class TopicInfo:
    def __init__(self, topic):
        if topic:
            topic_parts = topic.split("/")
            if len(topic_parts) != 2:
                raise ValueError("Wrong format for topic. Expected \"<sensor_name>/<reading_type>\".")

            self.sensor_name = topic_parts[0]
            self.reading_type = topic_parts[1]
        else:
            raise ValueError("Empty topic received.") 

def create_reading(message):
    topic = message.topic

    try:
        topic_info = TopicInfo(topic)

        sensor = Sensor.objects.filter(name=topic_info.sensor_name).get()
        reading_type = topic_info.reading_type
        # TODO With MQTTv5 it's possible to add a property to send the timestamp in the message.
        # Otherwise, it has to either be sent in the payload, or keep on doing it like this, but it's less accurate.
        reading_timestamp = timezone.now()
        try:
            reading_value = message.payload.decode()
        except (UnicodeDecodeError, AttributeError):
            reading_value = str(message.payload)

        reading = Reading(instant=reading_timestamp, sensor=sensor, type=reading_type, value=reading_value)
        reading.save()

        return reading
    except Exception as e:
        logging.error(e)

class MqttManager:
    def __init__(self):
        self.connected = False

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        self.connected = True
        logging.info(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("picotemp/temperature")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        logging.info(f"{msg.topic} {str(msg.payload)}")
        reading = create_reading(msg)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'temperature',
        {
            'type': 'temperature_reading',
            'message': reading
        }
        )

    def initialize(self):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.username_pw_set("admin", "admin")
        self.mqttc._connect_timeout = 60
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        for i in range(3, -1, -1):
            try:
                if not self.connected:
                    self.mqttc.connect("mosquitto", 1883, 60)
                break
            except Exception as e:
                logging.error(e)
                logging.warning("Failed to connect to mqtt server. Retrying...")
                sleep(10)
        else:
            logging.error("Unable to conect to mqtt server.")

    def start(self):
        self.mqttc.loop_start()
