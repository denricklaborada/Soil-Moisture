from django.shortcuts import render
import paho.mqtt.client as mqtt
from .models import *
import datetime
from django.utils import timezone
from threading import Thread


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Node/#")


def on_message(client, userdata, msg):
    Node.objects.create(node_id=msg.topic[5:],
                        moisture=float(str(msg.payload)[2:len(str(msg.payload)) - 1]))
    print("NODE ID: " + msg.topic[5:])
    print("MOISTURE: " + str(msg.payload)[2:len(str(msg.payload)) - 1])


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
    maxData = 0

    for node in nodes:
        if not node.node_id in nums:
            nums.append(node.node_id)

    nums.sort()

    for num in nums:
        obj = Node.objects.filter(node_id=num).order_by('-id')[0]
        content = {
            str(num): [str(obj.moisture), obj.timestamp],
        }

        contents.update(content)
        objCount = Node.objects.count()
        if maxData < objCount:
            maxData = objCount

    context = {
        'contents': contents,
        'nums': nums,
        'nodes': nodes,
        'maxData': range(maxData),
        'date': timezone.now(),
    }

    return render(request, template_name, context)


def nodePage(request, node_id, node_day):
    template_name = 'waterpump/node.html'
    obj = Node.objects.filter(node_id=node_id,
                              timestamp__date=datetime.date(int(node_day[:4]), int(node_day[6:7]), int(node_day[8:10])))

    context = {
        'node': obj,
        'node_id': node_id,
        'node_day': node_day,
    }

    return render(request, template_name, context)


def contentPage(request, node_id):
    template_name = 'waterpump/content.html'
    obj = Node.objects.filter(node_id=node_id).order_by('-id')

    dates = []

    for n in obj:
        if str(timezone.localtime(n.timestamp))[:10] not in dates:
            dates.append(str(timezone.localtime(n.timestamp))[:10])

    context = {
        'values': dates,
        'node_id': node_id,
    }

    return render(request, template_name, context)

