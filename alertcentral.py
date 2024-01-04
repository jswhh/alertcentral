#!/usr/bin/env python3
# Version 0.0

from Credentials import *

import paho.mqtt.client as mqtt_client
import json
import smtplib, ssl

client_id = "alertcentral"
topic = "ALARM"

def send_mail(sender_email, receiver_email, subject, text):
    port = 465  # For SSL
    smtp_server = "smtp.ionos.com"
    password = input("Type your password and press enter: ")
    message = """\
    Subject: {subject}

    {text}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    
# Connect to MQTT
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(mqtt_user, mqtt_pwd)
    client.on_connect = on_connect
    client.connect(mqtt_broker)
    return client

# Subscribe
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        #send_mail()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
