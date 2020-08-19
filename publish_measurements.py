#!/usr/bin/env python3

import ssl 
import paho.mqtt.client as mqtt
import serial
import time
import json 

machine_id = open('/etc/machine-id').readline().strip()

client = mqtt.Client(transport="websockets")
client.ws_set_options("/mqtt")
client.tls_set('/etc/ssl/certs/DST_Root_CA_X3.pem', tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set("user", "pass")
client.connect("example.com", 443)

topic = "resolvd/pmc/" + machine_id
        
ser = serial.Serial('/dev/ttyS2',
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_ODD,
                        stopbits=serial.STOPBITS_ONE)


def serial_read():
   
    while True:
            try:
                serial_data = ser.readline().decode('utf-8')  
                return serial_data

            except:
                print("serial error")
                time.sleep(0.1)
                continue

  
def publish():
        
        #data is parsed according to standard
        d = serial_read().split(",")    
        seconds = int(round(time.time()))
        
        data = { 
                "t":("%d" % seconds), 
                "U1":float(d[1]),
                "U2":float(d[2]),
                "U3":float(d[3]),
                "I1":float(d[4]),
                "I2":float(d[5]),
                "I3":float(d[6]),
                "f1":float(d[8]),
                "fi_U2":float(d[9]),
                "fi_U3":float(d[10]),
                "P1":float(d[17]),
                "P2":float(d[18]),  
                "P3":float(d[19]),
                "Q1":float(d[20]),
                "Q2":float(d[21]),
                "Q3":float(d[22])
                }
        #uncomment below to debug
        #print(topic)
        #print(json.dumps(data))
        client.publish(topic=topic, payload=json.dumps(data))


while True:
        try:
                publish()
                ser.flushInput()
                time.sleep(0.94)
                
        except:
                print("parse error")