import boto3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import os
import random
from datetime import datetime
import time

client = boto3.client('iot')

with open('../../endpoint.json') as json_file:  
    data = json.load(json_file)

deviceName = os.path.split(os.getcwd())[1]
publishTopic = "ScalableComputing/IoT"
PUBLISH_MEMORY = []  #Key : Time || Value : msgToSend
CURRENT_POWER = 100 # To enable sleep mode for some sensors after certain low power threshold
LOW_POWER_THRESHOLD = 80
SLEEP_POWER_THRESHOLD = 60

keyPath = '../private.pem.key'
certPath = '../certificate.pem.crt'
caPath = '../../root-CA.crt'
clientId = deviceName
host = data['endpointAddress']
port = 8883

 

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(caPath, keyPath, certPath)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
print("Going to connect")
connected = myAWSIoTMQTTClient.connect()
print("Connected")

def getDeviceData(fullPower):
    global CURRENT_POWER
    global PUBLISH_MEMORY
    currentSensorData = {}
    msgToSend = {}      # Only data which is out of normal is sent/published.
    #currentSensorData['device'] =  deviceName
    currentSensorData['BP'] = random.randint(75, 125)   # 90 - 110
    currentSensorData['HeartRate'] = random.randint(65, 90)  # 70 - 80
    currentSensorData['DevicePower'] = CURRENT_POWER
    
    if(currentSensorData['BP'] >= 110 or currentSensorData['BP'] <= 90):
        msgToSend['BP'] = currentSensorData['BP']
    if(currentSensorData['HeartRate'] >= 80 or currentSensorData['HeartRate'] <= 70):
        msgToSend['HeartRate'] = currentSensorData['HeartRate']

    
    if(fullPower):
        currentSensorData['Sugar'] = random.randint(70, 150) # 100 - 140
        currentSensorData['EMG'] = round(random.uniform(0.05,30),2) # < 20
        currentSensorData['Temperature'] = round(random.uniform(36,38),2) #36.5 - 37.5
        
        if(currentSensorData['Sugar'] >= 140 or currentSensorData['Sugar'] <= 100):
            msgToSend['Sugar'] = currentSensorData['Sugar']
        if(currentSensorData['EMG'] > 20):
            msgToSend['EMG'] = currentSensorData['EMG']
        if(currentSensorData['Temperature'] >= 37.5 or currentSensorData['Temperature'] <= 36.5):
            msgToSend['Temperature'] = currentSensorData['Temperature']
        
    CURRENT_POWER -= 5    
    
   
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    msgToSend['Time'] = dt_string
    PUBLISH_MEMORY.append(msgToSend)
    
    if(len(msgToSend) < 2):
        return None
    
    return msgToSend
    
    

def startDataSimulation():
    global PUBLISH_MEMORY
    global LOW_POWER_THRESHOLD
    global SLEEP_POWER_THRESHOLD
    global CURRENT_POWER
    i = 1
    goingToChargeCountDown = 1
    fullPower = True
    print("==>>Sending data to AWS IoT Core for ", deviceName)
    while(True):
        if(i % 5 == 0):
            print("===============>>Current Memory Size:" , len(PUBLISH_MEMORY))
        if(i % 100 == 0):
            print("================>>>>>>>>Clearing local on device memory")
            PUBLISH_MEMORY = []
        if(CURRENT_POWER < LOW_POWER_THRESHOLD):
            print("===========================>>>>>>>>Low Power, some sensors are down!!<<<<<<<<===============================")
            fullPower = False
        if(CURRENT_POWER <= SLEEP_POWER_THRESHOLD):
            # SEND DATA TO SERVER/S3
            
            while(goingToChargeCountDown < 5):
                time.sleep(1) # wait until resumed
                goingToChargeCountDown += 1
                print("=========================>>>>>Power critical, all sensors stopped.<<<<<<<<<<================================")
            if(goingToChargeCountDown == 5):
                CURRENT_POWER = 100
                fullPower = True
                print("===================>>>>>Device charged!! Runnning with full capacity.<<<<<<<<=============================")
                    
            
        i += 1
        
        dataToSend = getDeviceData(fullPower)
        if(dataToSend == None):
            continue
            
        dataToSend = json.dumps(dataToSend)
        print(dataToSend)
        #print(myAWSIoTMQTTClient)
        myAWSIoTMQTTClient.publish(publishTopic, dataToSend, 1)
        time.sleep(5)
    # Sleep maybe or setTimeOut
    

if(connected):
    print("=====================>>>>>>>>>>>>>>>>Connection established with AWS IoT core<<<<<<<<<<<=============================")
    startDataSimulation()