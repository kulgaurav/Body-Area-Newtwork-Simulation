from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import os
import random
from datetime import datetime
import time


with open('/home/ec2-user/environment/endpoint.json') as json_file:  
    data = json.load(json_file)

deviceName = os.path.split(os.getcwd())[1]
publishTopic = "ScalableComputing/IoT"
PUBLISH_MEMORY = []  #Key : Time || Value : msgToSend
current_power = 100 # To enable sleep mode for some sensors after certain low power threshold
threshold_power = 80
low_sleep_power = 60

keyPath = 'private.pem.key'
certPath = 'certificate.pem.crt'
caPath = '/home/ec2-user/environment/root-CA.crt'
clientId = deviceName
host = data['endpointAddress']
port = 8883

 

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(caPath, keyPath, certPath)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
connected = myAWSIoTMQTTClient.connect()

def getDeviceData(fullPower):
    global current_power
    global PUBLISH_MEMORY
    msgToSend = {}
    #msgToSend['device'] =  deviceName
    msgToSend['BP'] = random.randint(80, 120)
    msgToSend['HeartRate'] = random.randint(65, 80)
    msgToSend['DevicePower'] = current_power
    
    if(fullPower):
        msgToSend['Sugar'] = random.randint(70, 140)
        msgToSend['EMG'] = round(random.uniform(0.05,30),2)
        msgToSend['Temperature'] = round(random.uniform(36,38),2)
        
    current_power -= 5    
    
   
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    msgToSend['Time'] = dt_string

    PUBLISH_MEMORY.append(msgToSend)
    return msgToSend
    
    

def startDataSimulation():
    global PUBLISH_MEMORY
    global threshold_power
    global low_sleep_power
    global current_power
    i = 1
    goingToChargeCountDown = 1
    fullPower = True
    while(True):
        if(i % 5 == 0):
            print("Current Memory Size:" , len(PUBLISH_MEMORY))
        if(i % 100 == 0):
            print("Clearing local on device memory")
            PUBLISH_MEMORY = []
        if(current_power < threshold_power):
            print("Low Power, some sensors are down!!")
            fullPower = False
        if(current_power <= low_sleep_power):
            # SEND DATA TO SERVER/S3
            
            while(goingToChargeCountDown < 5):
                time.sleep(1) # wait until resumed
                goingToChargeCountDown += 1
                print("Power critical, all sensors stopped")
            if(goingToChargeCountDown == 5):
                current_power = 100
                fullPower = True
                print("Device charged!! Runnning with full capacity.")
                    
            
        i += 1
        
        
        print("Sending data to AWS IoT Core for ", deviceName)
        dataToSend = getDeviceData(fullPower)
        dataToSend = json.dumps(dataToSend)
        print(dataToSend)
        #print(myAWSIoTMQTTClient)
        myAWSIoTMQTTClient.publish(publishTopic, dataToSend, 1)
        time.sleep(5)
    # Sleep maybe or setTimeOut
    

if(connected):
    print("Connection established with AWS IoT")
    startDataSimulation()