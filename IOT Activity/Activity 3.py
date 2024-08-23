#MQTT- PUBLISH BH1750 (AMBEINT LIGHT SENSOR) SENSOR READINGS (USING ESP32)

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

from machine import I2C, Pin, SoftI2C
import bh1750
from sensor_pack.bus_service import I2cAdapter

#WIFI Setting and IP Address
ssid = 'Area 51.'
password = 'n4VqJm8a'
mqtt_server = '192.168.100.6'

client_id = ubinascii.hexlify(machine.unique_id())

#MQTT Topics
topic_pub_bh1750_norm = b'esp/bh1750/norm'
topic_pub_bh1750_lux = b'esp/bh1750/lux'
topic_pub_bh1750_max = b'esp/bh1750/max'

last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')

i2c = SoftI2C(scl = Pin(22), sda =Pin(21), freq=10000)
adaptor = I2cAdapter(i2c)
sol = bh1750.Bh1750(adaptor)

sol.power(on=True)     # Sensor Of Lux
sol.set_mode(continuously=True, high_resolution=True)
sol.measurement_accuracy = 1.0      # default value
old_lux = curr_max = 1.0

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
        for lux in sol:
            if lux != old_lux:
                curr_max = max(lux, curr_max)
                lt = time.localtime()
                client.publish(topic_pub_bh1750_norm,f"{100*lux/curr_max}")
                client.publish(topic_pub_bh1750_lux,f"{lux}")
                client.publish(topic_pub_bh1750_max,f"{curr_max}")
                print(f"{lt[3:6]}\tIllumination [lux]: {lux}.\tmax: {curr_max}.\tNormalized [%]: {100*lux/curr_max}.")
            old_lux = lux        
            time.sleep_ms(sol.get_conversion_cycle_time())
        #MODE-RED Publish
  except OSError as e:
    restart_and_reconnect()
