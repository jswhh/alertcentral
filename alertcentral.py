#!/usr/bin/env python3
# Version 0.1

from Credentials import *

import paho.mqtt.client as mqtt_client
import json
import smtplib, ssl

client_id = "alertcentral"
topic = "ALERT"

def send_mail(receiver_email, subject, text):
    message = f"""Subject: {subject}

        
    {text}"""   # Warning: do not reformat!!!
    context = ssl.create_default_context()
    print(f"Sending mail to {receiver_email})" # as {message}")
    
    with smtplib.SMTP_SSL(mail_smtp_server, mail_smtp_port, context=context) as server:
        server.login(mail_sender, mail_pwd)
        server.sendmail(mail_sender, receiver_email, message) 
    
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
        data = json.loads(msg.payload.decode())
        # print(data["severity"], data["device"], data["message"])
        send_mail("jszw@jszw.de", data["severity"]+" from "+data["device"], data["message"])

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
    ##send_mail("jszw@jszw.de", "Test Subject", "Test Message")
