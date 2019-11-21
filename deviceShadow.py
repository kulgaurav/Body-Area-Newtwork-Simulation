from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json
import os
import random
from datetime import datetime
import time


with open('/home/ec2-user/environment/endpoint.json') as json_file:  
    data = json.load(json_file)

deviceName = os.path.split(os.getcwd())[1]

initialClientToken = ""

initialState = {
    'state': { 
        'reported': { 
            'powerSaver': False
        }, 
        'desired': None 
    }
};


keyPath = 'private.pem.key'
certPath = 'certificate.pem.crt'
caPath = '/home/ec2-user/environment/root-CA.crt'
clientId = deviceName
host = data['endpointAddress']
port = 8883

myShadowClient = AWSIoTMQTTShadowClient(deviceName)
myShadowClient.configureEndpoint(host, 8883)
myShadowClient.configureCredentials(caPath, keyPath, certPath)
myShadowClient.configureConnectDisconnectTimeout(10)  
myShadowClient.configureMQTTOperationTimeout(5) # IN sec


myShadowClient.connect()

deviceShadowHandler = myShadowClient.createShadowHandlerWithName(deviceName, True)

def shadowCallback_Delta(payload, responseStatus, token):
    print(responseStatus)
    payloadDict = json.loads(payload)
    print("++++++++DELTA++++++++++")
    print("property: " + str(payloadDict["state"]["property"]))
    print("version: " + str(payloadDict["version"]))
    print("+++++++++++++++++++++++\n\n")



# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallback_Delta)

while True:
    time.sleep(1)

