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

    client.connect("10.200.180.7", 1883, 60)
    client.loop_forever()

t1 = Thread(target=run_mqtt).start()

def index(request):
	template_name = 'waterpump/index.html'
	nodes = Node.objects.all()
	contents = {}
	nums = []
	
	for node in nodes:
		if not node.node_id in nums:
			nums.append(node.node_id)
	
	nums.sort()
	
	for num in nums:
		obj = Node.objects.filter(node_id=num).order_by('-id')[0]
		content = {
			str(num):str(obj.moisture),
		}
		
		contents.update(content)
	
	context = {
		'contents':contents,
	}
	
	return render(request, template_name, context)



