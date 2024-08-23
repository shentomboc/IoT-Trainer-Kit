#MQTT- PUBLISH RAINDROPS SENSOR AND SOIL MOISTURE SENSOR READINGS (USING ESP32)

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
topic_pub_soil = b'esp/liquid/soilmoisture'
topic_pub_rain = b'esp/liquid/raindrops'

last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')

#SENSOR PINS IN ESP32
soil = ADC(Pin(34))
rain = ADC(Pin(35))
m1 = 100
m2 = 100

min_moisture=0
max_moisture=4095

soil.atten(ADC.ATTN_11DB)       #Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     #range 0 to 4095

rain.atten(ADC.ATTN_11DB)       #Full range: 3.3v
rain.width(ADC.WIDTH_12BIT)     #range 0 to 4095

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
        soil.read()
        rain.read()
        time.sleep(2)
        m1 = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
        m2 = (max_moisture-rain.read())*100/(max_moisture-min_moisture)
        
        smoisture = '{:.1f}%'.format(m1)
        rmoisture = '{:.1f}%'.format(m2)
        
        print('Soil Moisture:', smoisture)
        print('Rain Drops:', rmoisture)
        #MODE-RED Publish
        client.publish(topic_pub_rain,rmoisture)
        client.publish(topic_pub_soil,smoisture)
        last_message = time.time()

  except OSError as e:
    restart_and_reconnect() 
