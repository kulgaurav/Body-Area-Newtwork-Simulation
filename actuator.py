import paho.mqtt.client as mqtt


MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "ScalableComputing/IoT"
MQTT_MSG = "Dummy Message" #Get from source


def on_connect(mosq, obj, rc):
    mqttc.subscribe(MQTT_TOPIC, 0)

def on_message(mosq, obj, msg):
	print "Topic: " + str(msg.topic)
	print "Payload for the message: " + str(msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + 
    
    

mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

mqttc.loop_forever()