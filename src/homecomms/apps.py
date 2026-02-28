from django.apps import AppConfig


class HomecommsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homecomms'

    def ready(self):
        from .mqtt import MqttManager

        mqtt_manager = MqttManager()
        mqtt_manager.initialize()
        mqtt_manager.start()
