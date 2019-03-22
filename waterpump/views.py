from django.shortcuts import render
import paho.mqtt.client as mqtt
from .models import *
from threading import Thread

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Node/#")

def on_message(client, userdata, msg):
    node_object = Node.objects.create(node_id=msg.topic[5:], moisture=float(str(msg.payload)[2:len(str(msg.payload))-1]))
    print("NODE ID: " + msg.topic[5:])
    print("MOISTURE: " + str(msg.payload)[2:len(str(msg.payload))-1])
    
def run_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("10.200.180.6", 1883, 60)
    client.loop_forever()

t1 = Thread(target=run_mqtt).start()
