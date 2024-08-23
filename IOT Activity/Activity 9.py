#PHOTODIODE AND LDR SENSOR

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import gc
gc.collect()
esp.osdebug(None)

from machine import ADC, Pin, SoftI2C

#WIFI Setting and IP Address
ssid = 'Area 51.'
password = 'n4VqJm8a'
mqtt_server = '192.168.100.6'

client_id = ubinascii.hexlify(machine.unique_id())

#MQTT Topics
topic_pub_photodiode = b'esp/photodiode'
topic_pub_ldr = b'esp/ldr'

last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')

#SENSOR PINS IN ESP32
photodiode_pin = machine.Pin(34, machine.Pin.IN)
ldr_pin = machine.Pin(35, machine.Pin.IN) 
# Readings
photodiode_value = 0
ldr_value = 0

def connect_mqtt():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    if (time.time() - last_message) > message_interval:
        
        photodiode_value = photodiode_pin.value()
        # Read the LDR value
        ldr_value = ldr_pin.value()
        # Print the sensor values
        print('Photodiode Value:', photodiode_value)
        print('LDR Value:', ldr_value)
        
        client.publish(topic_pub_photodiode,str(photodiode_value))
        client.publish(topic_pub_ldr,str(ldr_value))
        time.sleep_ms(100)  #
        
        last_message = time.time()
  except OSError as e:
    restart_and_reconnect()
