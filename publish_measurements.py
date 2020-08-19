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
        
        parsed_data = serial_read().split(",")    
        seconds = int(round(time.time()))
        
        data = { 
                "timestamp":("%d" % seconds), 
                "Phase_1_voltage_RMS":float(parsed_data[1]),
                "Phase_2_voltage_RMS":float(parsed_data[2]),
                "Phase_3_voltage_RMS":float(parsed_data[3]),
                "Phase_1_current_RMS":float(parsed_data[4]),
                "Phase_2_current_RMS":float(parsed_data[5]),
                "Phase_3_current_RMS":float(parsed_data[6]),
                "Phase_1_frequency":float(parsed_data[8]),
                "Phase_2_voltage_phase_angle":float(parsed_data[9]),
                "Phase_3_voltage_phase_angle":float(parsed_data[10]),
                "Phase_1_Active_Power":float(parsed_data[17]),
                "Phase_2_Active_Power":float(parsed_data[18]),  
                "Phase_3_Active_Power":float(parsed_data[19]),
                "Phase_1_Reactive_Power":float(parsed_data[20]),
                "Phase_2_Reactive_Power":float(parsed_data[21]),
                "Phase_3_Reactive_Power":float(parsed_data[22])
                }

        print(topic)
        #print(json.dumps(data))
        client.publish(topic=topic, payload=json.dumps(data))


while True:
        try:
                publish()
                ser.flushInput()
                time.sleep(0.94)
                
        except:
                print("parse error")