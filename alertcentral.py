#!/usr/bin/env python3
# Version 0.2.2

from Credentials import *

import paho.mqtt.client as mqtt_client
import json
import smtplib, ssl
import email.message
import socket

client_id = "alertcentral"
topic = "ALERT"

def send_mail(receiver_email, subject, text):
    message = email.message.Message()
    message["Subject"] = subject
    message.set_payload(text)
    context = ssl.create_default_context()
    print(f"Sending mail to {receiver_email}") # as {message}")

    try:
        with smtplib.SMTP_SSL(mail_smtp_server, mail_smtp_port, context=context) as server:
            server.login(mail_sender, mail_pwd)
            server.sendmail(mail_sender, receiver_email, message.as_string().encode("utf-8")) 
    except (socket.gaierror):
        print('Error trying to send Email!')
        
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
        try:
            data = json.loads(msg.payload.decode())
            # print(data["severity"], data["device"], data["message"])
            send_mail("jszw@jszw.de", data["severity"]+" in "+alert_location, "Device: "+data["device"]+"\n"+"Message: "+data["message"])
        except (json.decoder.JSONDecodeError, KeyError):  
            print('Error: Decoding JSON has failed')

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

