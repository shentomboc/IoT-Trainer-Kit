#SERVO MOTOR CONTROL USING POTENTIOMETER

from machine import Pin, ADC
from machine import Pin, PWM
from time import sleep

sg90 = PWM(Pin(12, mode=Pin.OUT))
sg90.freq(50)
pot = ADC(Pin(13))
pot.atten(ADC.ATTN_11DB)
sg90.duty(0)
while True:
  pot_value = pot.read()
  pot_value =(pot_value/4095)*180
  pot_value = int(pot_value)
  sg90.duty(pot_value)
  print(pot_value)
  sleep(0.1)
