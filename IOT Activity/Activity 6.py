#PIR SENSOR VIA BUZZER

from machine import Pin
import time

pir_pin = Pin(4, Pin.IN)
buzzer_pin = Pin(5, Pin.OUT)

while True:
    if pir_pin.value():
        print("Motion detected!")

        buzzer_pin.on()
        time.sleep(1) 
        buzzer_pin.off()
    time.sleep(0.1)
