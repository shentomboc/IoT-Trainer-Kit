#RELAY AND LED (WED SERVER)

try: 
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'Area 51.'
password = 'n4VqJm8a'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

# ESP32 GPIO 26
relay = Pin(13, Pin.OUT)

# ESP8266 GPIO 5
#relay = Pin(5, Pin.OUT)
