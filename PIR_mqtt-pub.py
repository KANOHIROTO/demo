#!/usr/bin/env python

import RPi.GPIO as GPIO
import time, datetime
import paho.mqtt.client as mqtt

###### Edit variables to your MQTT environment #######
broker_address = "test.mosquitto.org"     #MQTT broker_address
Topic = "hoge/hoge"

###### GPIO environment setup #######
PIR_OUT_PIN = 11    # pin11
today = datetime.datetime.fromtimestamp(time.time())			
message="Movement detected!..."+ today.strftime('%Y/%m/%d %H:%M:%S')

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(PIR_OUT_PIN, GPIO.IN)    # Set BtnPin's mode is input



print("creating new instance")
client = mqtt.Client("pub2") #create new instance

print("connecting to broker: %s" % broker_address)
client.connect(broker_address) #connect to broker

def loop():
	while True:
		if GPIO.input(PIR_OUT_PIN) == GPIO.HIGH:
			print (message)
			client.publish(Topic, message)
			GPIO.cleanup()

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()