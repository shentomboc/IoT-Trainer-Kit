#MQTT- PUBLISH APDS9960 (RGB, AMBIENT LIGHT, PROXIMITY SENSOR) READINGS USING ESP32

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

from machine import ADC, Pin, I2C
from time import sleep_ms
from uPy_APDS9960.apds9960LITE import APDS9960LITE


#WIFI Setting and IP Address
ssid = 'Area 51.'
password = 'n4VqJm8a'
mqtt_server = '192.168.100.6'

client_id = ubinascii.hexlify(machine.unique_id())

#MQTT Topics
topic_pub_apds_clear = b'esp/apds/clear'
topic_pub_apds_red = b'esp/apds/red'
topic_pub_apds_blue = b'esp/apds/blue'
topic_pub_apds_green = b'esp/apds/green'
topic_pub_apds_prox = b'esp/apds/proximity'
topic_pub_apds_amb = b'esp/apds/ambient'

last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')

#SENSOR PINS IN ESP32
#i2c = SoftI2C(scl = Pin(22), sda =Pin(21), freq=10000)
i2c =  I2C(0,scl=Pin(22), sda=Pin(21))

apds9960=APDS9960LITE(i2c)
apds9960.prox.eLEDCurrent    =0 # LED_DRIVE_100MA    
apds9960.prox.eProximityGain =3 # PGAIN_8X   
apds9960.prox.enableSensor()

apds9960.als.enableSensor()   # Enable Light sensor
apds9960.als.eLightGain=3  

#IRQ Functionalities
apds9960.prox.setInterruptThreshold(high=10,low=0,persistance=7)
apds9960.prox.enableInterrupt()

ProxThPin=Pin(15, Pin.IN ,Pin.PULL_UP)
IrqThPin=machine.Pin(15, machine.Pin.IN ,machine.Pin.PULL_UP)

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
        sleep_ms(50)
        print (IrqThPin.value())
        if(IrqThPin.value()==0):
            print("Ambient light level:", apds9960.als.ambientLightLevel )
            client.publish(topic_pub_apds_amb, str(apds9960.als.ambientLightLevel))    
            
        if(ProxThPin.value()==0):
            print("proximity:", apds9960.prox.proximityLevel )
            client.publish(topic_pub_apds_prox, str(apds9960.prox.proximityLevel))

        #MODE-RED Publish
        client.publish(topic_pub_apds_clear,str(apds9960.als.ambientLightLevel))
        client.publish(topic_pub_apds_red,str(apds9960.als.ambientLightLevel))
        client.publish(topic_pub_apds_blue,str(apds9960.als.greenLightLevel))
        client.publish(topic_pub_apds_green,str(apds9960.als.blueLightLevel))
        
        apds9960.als.clearInterrupt()
        apds9960.prox.clearInterrupt()
        
        last_message = time.time()

  except OSError as e:
    restart_and_reconnect()
 