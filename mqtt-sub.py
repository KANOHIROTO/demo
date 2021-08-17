#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import redis
import requests

###########################################################
#####  Set constant values for MQTT broker   ##############

#Brokorg"    # Cloud MQTT
MqttTopic = "hoge/hoge"              # Local MQTT
BrokerAddress = "test.mosquitto.org"

###########################################################
#####  Set constant values for Radis  #####################

RedisKey = "hoge"

##########################
### For Local Redis
### RedisHost = "127.0.0.1"
### RedisPort = "6379"
### RedisPwd = ""
##########################

##########################
### For using RadisLabs
### You need to change RedisHost,RedisPort and RedisPwd below

RedisHost = "redis-XXXX.XXXX.us-east-X-X.ec2.cloud.redislabs.com"
RedisPort = "XXXXX"
RedisPwd = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
##########################

###########################################################
#####  Define functions   #################################

def check_db():
    ### Check Redis connection
    r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
    print("Connected Radis...: " + RedisHost)
    ### Check Redis Key
    ret = r.get(RedisKey)
    print (ret)                             ### for debug
    if ret is None:                         # if no exist RedisKey
        print("Failed Key: " + RedisKey)
        return ret                          # Return Value
    msg = str(ret.decode("utf-8"))
    print("RedisKey:" + RedisKey + " KeyValue:" + msg)
    return ret

def set_db(msg):                            ### set data to Redis
    r = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPwd, db=0)
    r.set(RedisKey ,msg)
    print("Updated Radis db=0")

def on_message(client, userdata, message):  ### callback when get message from MQTT broker
    msg = str(message.payload.decode("utf-8"))
    url = "https://notify-api.line.me/api/notify"
    token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    headers = {"Authorization" : "Bearer "+ token}
    print("Message received:" + msg)
    set_db(msg)                             ### call Function set_db(msg)
    payload = {"message" :  msg}
    r = requests.post(url ,headers = headers ,params=payload)
    exit(1)
    ### for debug
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)





###########################################################
#####  Main                     ###########################

### Check Radis connection
ret = check_db()
if ret is None:                             # for debug
    print("***** Failed check Radis *****")
    exit(1)

### Connect MQTT broker
print("Connecting to MQTT broker:" + BrokerAddress)
client = mqtt.Client()               # Create new instance with Any clientID
client.on_message=on_message         # Attach function to callback
try:
    client.connect(BrokerAddress)    #connect to broker
except:
    print("***** Broker connection failed *****")
    exit(1)

### Subscribe ###
print("Subscribe topic:", MqttTopic)
client.subscribe(MqttTopic)          # Subscribe MQTT

### loop forever to wait a message ###
print("Waiting message...")
client.loop_forever()                # Loop forever
