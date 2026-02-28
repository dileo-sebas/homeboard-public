import json
from django.db import models

class Sensor(models.Model):
    class Meta:
        ordering = ("name", "model",)

    name = models.CharField(max_length=60, unique=True)
    model = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.name


class Reading(models.Model):
    class Meta:
        ordering = ("instant", "type",)

    instant = models.DateTimeField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="readings")
    type = models.CharField(max_length=30)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"[{self.sensor.name}/{self.type}] {self.instant}: {self.value}"

    def toJSON(self):
        return json.dumps(
            self,
            default=str,
            sort_keys=True,
            indent=4)
