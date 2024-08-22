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

import BME280
from machine import ADC, Pin, SoftI2C
import dht
import LDR
from hcsr04 import HCSR04

#WIFI Setting and IP Address
ssid = 'Area 51.'
password = 'n4VqJm8a'
mqtt_server = '192.168.100.6'

client_id = ubinascii.hexlify(machine.unique_id())

#MQTT Topics
topic_pub_bme_temp = b'esp/bme280/temperature'
topic_pub_bme_hum = b'esp/bme280/humidity'
topic_pub_bme_pre = b'esp/bme280/pressure'
topic_pub_temp_dht = b'esp/dht/temperature'
topic_pub_hum_dht = b'esp/dht/humidity'
topic_pub_ldr = b'esp/ldr/intensity'
topic_pub_distance = b'esp/hcsr04/distance'


last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')

#SENSOR PINS IN ESP32
#sensor = dht.DHT22(Pin(5))
d = dht.DHT11(Pin(19))
ldr = LDR.LDR(35)
i2c = SoftI2C(scl = Pin(22), sda =Pin(21), freq=10000)
us_sensor = HCSR04(trigger_pin=32, echo_pin =33, echo_timeout_us = 10000)

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
        #DHT11
        d.measure()
        dtemp = d.temperature()
        #temp = temp * (9/5) + 32.0  #Fahrenheit
        dhum = d.humidity()
        temp = (b'{0:3.1f},'.format(dtemp))
        hum =  (b'{0:3.1f},'.format(dhum))
        #LDR
        inten = ldr.value()
        #Ultrasonic
        distance = us_sensor.distance_cm()
        #bme280
        bme = BME280.BME280(i2c=i2c)
        bmetemp = bme.temperature
        bmehum = bme.humidity
        bmepre = bme.pressure
        
        
        #MODE-RED Publish
        client.publish(topic_pub_bme_temp,bmetemp)
        client.publish(topic_pub_bme_hum,bmehum)
        client.publish(topic_pub_bme_pre,bmepre)
        client.publish(topic_pub_temp_dht, temp)
        client.publish(topic_pub_hum_dht, hum)
        client.publish(topic_pub_ldr, str(inten))
        client.publish(topic_pub_distance, str(distance))
        last_message = time.time()

  except OSError as e:
    restart_and_reconnect()