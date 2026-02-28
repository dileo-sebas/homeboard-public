import logging

from django.shortcuts import render
from .models import Reading

def home(request):
    last_reading = Reading.objects.\
        filter(sensor__name="picotemp", type="temperature").order_by("-instant").first()
    logging.info(last_reading)

    context = {"last_temperature": last_reading}
    return render(request, "homecomms/home.html", context=context)
