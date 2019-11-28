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

* Node-Red
* AWS

## Dependencies

* AWSIoT device setup
* MQTT

### Device setup setup in AWS IOT

#### AWS Policy creation
* Step 1: Open your AWS account(we have used the free tier account) and select IOT Core
* Step 2: Go to Secure-> Policies and select Create option on top left for creating new policy
* Step 3: Give some proper name to policy and under:
** Action : iot:*  --> to give access to all possible actions related to IOT(as we don't want to go for specific options).
** Resource ARN : * --> again for using all the resources not specific one
* check the allow checknbox and then go ahead and create the policy
* Step 4: Check the added policy in the Policies it must be added there.

#### Certificate creation for the above policy
* Step 1: Go to Secure -> Certificates and Create new certificates using Create on the top right corner
* Step 2: Download A certificate for this thing(Client cetificate), A private key and A root CA for AWS (A public key is optional).
* Step 3: Click on the Activate to activate these certificates.
* Step 4: Click on the Attach the policy and select the policy with the name created by you in the above section and press Done.
* Step 5: Check in certificate sectiona and activate the created certificate if they show INACTIVE on them.

### Creating Flow in NODE-RED

#### Problem addressed 1
* We have created the three flows to immitate the various aspects of protocol involved in Hostspot Preventing Routing Protocol.
* We have used the blood pressure sensor as a sensor node and publishing data in peer to peer communication scenario this sensor will sends it data to node 2 and if node 2's temprature is less then node one then this will directly send our data to sink but in the other case it will nit act as the linking node nad hence BP sensor has to search next nearest neighbour node to send its data to sink.

### Node Red implementation
* Open node red on your system
* Download HPRflow.json file from the git and import this file in your node red.
* Node red is UI based tools so the implementation is quite straight forward.
* We have used the inject node with a fuction to generate random temorature and senor values for particular sectiona and provided the clear naming convention as well.
* If you want to publish data from the BP sensor just press the inject node for BP sensor and it will check for the temprature logic explained above and publish the data accordingly.
* mytopic 3 is used as sink node where we want to publish our data and mqtt protocol is used to transmit data from the sensor to AWS test instance mytopic 3
* For creating test instance my topic3 goto AWS -> IOT Core -> test
** create Subscription topic - mytopic3 and press Subscribe to topic
* Now when you try to publish data from BP sensor it will be published and can be seen on AWS test instance under mytopic3


#### Problem addressed 2
* We have created a scenario where we are keeping count of the no. of packects that has been forwarded by the node while it is acting like a linking node if this count exceed the MAX_hop count this node will stop sending the packets which will prevent it from heating and can be used to avoid DDOS attack to certain extent.

### Node red Implementation
* Open node red on your system
* Download MaxHopandBackupSink.json file from the git and import this file in your node red.
* Implementation is straight forward three sensor made using inject nodes are trying to send data using sensor4 implemented using function block where the counter is increasing for maxhop.
* In switch node value of maxhop is copared with default value and accordingly action is taken.
* For reset the value of maxhop counter press the inject node Reset:Reset Counter inject node on top of the flow.

#### Problem addressed 3
* We have implemeted a concept of standby sink that is in case if battery of the primary sink is down it will send it data to standby sink which is mytopic4 on AWS test instance and craeted using the same steps as for mytopic3.

### Node red Implementation
* Open node red on your system
* Download MaxHopandBackupSink.json file from the git and import this file in your node red.
* Taking input from my topic three battery value is simulated in function block and if battery value is less then certain limit it is passing on its data to mytopic4(stanby sink) and condition is checked inside switch block.
* For reset the value of battery value press the inject node Reset:Reset Battery inject node on top of the flow.





