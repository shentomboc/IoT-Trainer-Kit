from machine import Pin, I2C, SoftI2C
from i2c_lcd import I2cLcd
import time
import dht

#LCD
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=11500)
lcd = I2cLcd(i2c, 0x27,2,16)
time.sleep(1)
lcd.clear()

#DHT11
d=dht.DHT11(Pin(19))
t=0
h=0

#START
lcd.move_to(5,0)
lcd.putstr("DHT11")

while True:
    try:
        d.measure()
        time.sleep(1)
        temp = "Temp: {:.0f} C".format(d.temperature())
        humid = "Humidity: {:.0f} %".format(d.humidity())
        print(d.temperature(), d.humidity())
        lcd.clear()
        lcd.putstr(temp)
        lcd.move_to(0,1)
        lcd.putstr(humid)
        time.sleep(1)
    except:
        pass
        
