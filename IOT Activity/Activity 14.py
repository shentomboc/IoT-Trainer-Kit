#BME180, DHT11 AND ULTRASONIC VIA THINGSPEAK PLATFORM

import machine
import urequests 
from machine import Pin, SoftI2C
import network, time
import BME280
import dht
from hcsr04 import HCSR04

d=dht.DHT11(Pin(13))
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)    #initializing the I2C method
h = HCSR04(trigger_pin=33, echo_pin=32, echo_timeout_us=10000)

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = 'SH0U77YYABJNXW7K' 

UPDATE_TIME_INTERVAL = 5000  # in ms 
last_update = time.ticks_ms() 

ssid='Area 51.'
password='n4VqJm8a'

# Configure ESP32 as Station
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)

if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
     pass
print('network config:', sta_if.ifconfig()) 

while True: 
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL: 
        d.measure()
        time.sleep(1)
        dtemp = d.temperature()
        dhumid = d.humidity()
        
        distance = h.distance_cm()
        
        bme = BME280.BME280(i2c=i2c)          #BME280 object created
        btemp = bme.temperature         #reading the value of temperature
        bhumid = bme.humidity               #reading the value of humidity
        bpres = bme.pressure               #reading the value of pressure

        sensor_readings = {'field1':dtemp, 'field2':dhumid, 'field3':distance,'field4':btemp,'field5':bhumid,'field6':bpres} 
        request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = sensor_readings, headers = HTTP_HEADERS )  
        request.close() 
        print(sensor_readings)
