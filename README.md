# Simulating IoT device in Body Area Network and connecting with AWS IoT Core

## Requirements 
* Python
* AWS 

## Dependencies
* AWSIoTPythonSDK
* Boto3
* Paho.MQTT

### The codes can be deployed on a local machine or AWS Cloud9

### Note:

* It is advised to create new IAM User with custom policies for the deployment as it will be easier to clear the resources. 
  
* Create an IoT Core Instance on AWS and register a new device. Get certificate and encryption keys.

* deviceSendingData.py can be used to run the simulation after attaching endpoint, certificate, and private key.

* The chosen _publishTopic_ will be used at IoT Core to publish to the subscribing message. 

* Sensors simulating are:

| Sensors       |
| ------------- |
| Blood Pressure      | 
| Device Power    | 
| Heart Rate | 
| Body Temperature     | 
| EMG Reading | 
| Sugar Level | 


* Data that is below or above the normal range is only published. 

* In-memory caching of data for the period until the device is out of power. 

* Once the power is critical, data is backed up to dynamoDB.


# NODE-RED Implementation:

## Requirements:

Node-Red
AWS

## Dependencies

AWSIoT device setup
MQTT


