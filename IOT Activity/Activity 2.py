#DISTANCE MEASUREMENT USING ULTRASONIC SENSOR HC-SR04 AND I2C LCD DISPLAY WITH ESP32

from machine import Pin, SoftI2C, I2C
from i2c_lcd import I2cLcd
import time
import dht
from hcsr04 import HCSR04

# LCD
i2c = SoftI2C(scl=Pin(22), sda=Pin(21),freq=100000)
lcd = I2cLcd(i2c, 0x27,2,16)
time.sleep(1)
lcd.clear()

sensor = HCSR04(trigger_pin=13, echo_pin=12, echo_timeout_us=10000)

# START
text = 'Ultrasonic'
lcd.putstr(text)
time.sleep(2)

while True:
    try:
        distance = sensor.distance_cm()
