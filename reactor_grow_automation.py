import requests
import Adafruit_DHT
import math
import Adafruit_ADS1x15
import time
import json
import RPi.GPIO as GPIO
import w1thermsensor
from servosix import ServoSix
from datetime import datetime

API_ENDPOINT = "https://nc-greenhouse-project.herokuapp.com/greenhouse"

ss = ServoSix()
adc = Adafruit_ADS1x15 .ADS1115()
sensor1 = Adafruit_DHT.DHT22

GAIN = 1 # for pump switch
PIN=35 #for pump switch
 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.HIGH)
 
temp_inside_max = 28
sensor = w1thermsensor.W1ThermSensor()
values = [0]*100

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(0.1)

 
try:
    while True:
	setup()
	for i in range(100):
            values[i] = adc.read_adc(0, gain=GAIN)
        #print(max(values))
	soil_moist = max(values)
        if (max(values))>20000:            
	    GPIO.output(PIN, GPIO.LOW)
	    water = "true"
            #print(" Pump ON")
            time.sleep(4)            
            GPIO.output(PIN, GPIO.HIGH)
            #print(" Pump OFF")
            time.sleep(0.1)            
        else:            
            GPIO.output(PIN, GPIO.HIGH)
            water = "false"
            #print(" Pump OFF")
            time.sleep(0.1)
            
        humidity, temp_inside = Adafruit_DHT.read_retry(sensor1, 26)
        temp_outside = sensor.get_temperature()
        time_now = datetime.now()        
        
        if temp_inside > temp_inside_max:
            ss.set_servo(6, 60)
            window = "true"
            #print("doors open")     
        else:
            ss.set_servo(6, 103)
            window = "false"
            #print("doors closed")
            
        data = { "temp_out": math.floor(temp_outside*100)/100,
                 "temp_inside":math.floor(temp_inside*100)/100,
                 "soil_moist": soil_moist,
                 "humidity":math.floor(humidity*100)/100,
                 "window":window,
                 "water":water ,
                 "created_at": str(time_now)
                 }
        #r = requests.post(url = API_ENDPOINT, data = json.dumps(data))
        #print(r.text)
        time_stampp = data["created_at"]
        temperature_outside = data["temp_out"]
        temperature_inside = data["temp_inside"]
        humidity_inside = data["humidity"]
        plant_soil_moisture = data["soil_moist"]
        
        print"************************************"
        print"Date and time of reading: ", time_stampp        
        print"Temperature outside: ", temperature_outside
        print"Temperature inside: ", temperature_inside
        print"Humidity inside: ", humidity_inside
        print"Plant1 soil moisture: ", plant_soil_moisture
        print("------------------------------------")
        print"Window status: ", window
        print"Water pump status: ", water
        print("------------- E N D ------------")
        #print(data)
            
        time.sleep(5)
 
except KeyboardInterrupt:
    GPIO.output(PIN, GPIO.HIGH)
    print('END')
    GPIO.cleanup()
