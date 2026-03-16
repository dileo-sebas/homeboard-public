# homeboard
This is a personal project for real time visualization of sensor data, obtained from a Raspberry Pi Pico microntroller (Or any other microcontroller with support for micropython) via MQTT protocol. The embedded code is located in the pico_client.py file.
The application only supports temperature readings at the moment, but it's intended to become more customizable in order to support different reading types.
Django Channels is used for the WebSocket that make readings available to the web client for visualization.

## Technical Details

The project is based on Python 3.8, Django 4.2, Paho MQTT 2.0 and Bootstrap 5

## Setup

A file called *.env* with the following content has to be created in the root directory with the following contents (the placeholders between angle brackets have to be replaced with the real values):

DJANGO_SECRET_KEY=<secret_key><br>
DJANGO_DEBUG=<True_or_False><br>
DATABASE_URL=<database_url><br>
POSTGRES_DB=<database_name><br>
POSTGRES_USER=<database_user><br>
POSTGRES_PASSWORD=<database_password><br>

## Licencing

This project adheres to the MIT licence. For more details, please read the file present in the root directory.
