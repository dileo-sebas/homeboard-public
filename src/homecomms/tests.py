from django.test import TestCase
from unittest.mock import MagicMock, patch
from django.utils import timezone
from .models import Sensor, Reading
from .mqtt import TopicInfo, create_reading, MqttManager

class TopicInfoTestCase(TestCase):
    def test_valid_topic(self):
        topic = "sensor1/temperature"
        info = TopicInfo(topic)
        self.assertEqual(info.sensor_name, "sensor1")
        self.assertEqual(info.reading_type, "temperature")

    def test_invalid_topic_format(self):
        with self.assertRaises(ValueError):
            TopicInfo("sensor1-temperature")

    def test_empty_topic(self):
        with self.assertRaises(ValueError):
            TopicInfo("")

class CreateReadingTestCase(TestCase):
    def setUp(self):
        self.sensor = Sensor.objects.create(name="sensor1", model="DHT22")

    def test_create_reading_valid(self):
        mock_msg = MagicMock()
        mock_msg.topic = "sensor1/temperature"
        mock_msg.payload = b"23.5"
        reading = create_reading(mock_msg)
        self.assertIsInstance(reading, Reading)
        self.assertEqual(reading.sensor, self.sensor)
        self.assertEqual(reading.type, "temperature")
        self.assertEqual(reading.value, "23.5")

    def test_create_reading_invalid_sensor(self):
        mock_msg = MagicMock()
        mock_msg.topic = "unknown/temperature"
        mock_msg.payload = b"23.5"
        reading = create_reading(mock_msg)
        self.assertIsNone(reading)

class MqttManagerTestCase(TestCase):
    @patch("homecomms.mqtt.mqtt.Client")
    def test_initialize_and_start(self, mock_client):
        manager = MqttManager()
        manager.initialize()
        self.assertTrue(hasattr(manager, "mqttc"))
        manager.start()
        mock_client.return_value.loop_start.assert_called_once()

class SensorModelTestCase(TestCase):
    def test_str(self):
        sensor = Sensor.objects.create(name="sensor1", model="DHT22")
        self.assertEqual(str(sensor), "sensor1")

class ReadingModelTestCase(TestCase):
    def setUp(self):
        self.sensor = Sensor.objects.create(name="sensor1", model="DHT22")

    def test_str(self):
        reading = Reading.objects.create(instant=timezone.now(), sensor=self.sensor, type="temperature", value="23.5")
        self.assertIn("sensor1/temperature", str(reading))

    def test_toJSON(self):
        reading = Reading.objects.create(instant=timezone.now(), sensor=self.sensor, type="temperature", value="23.5")
        json_str = reading.toJSON()
        self.assertIsInstance(json_str, str)
        self.assertIn("sensor1", json_str)
