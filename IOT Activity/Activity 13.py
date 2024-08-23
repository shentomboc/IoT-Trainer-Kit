#START, STOP AND RESET PUSHBUTTON VIA LED

import machine
from time import sleep

# Pin Definitions
led_pin = machine.Pin(27, machine.Pin.OUT)  # Pin 2 is connected to the LED
start_button_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)  # Pin 14 is connected to the Start button
stop_button_pin = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)  # Pin 12 is connected to the Stop button
reset_button_pin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)  # Pin 13 is connected to the Reset button

# LED state
led_state = False

# Button state
start_button_state = False
stop_button_state = False
reset_button_state = False

# Interrupt callback for Start button
def start_button_callback(pin):
    global start_button_state
    start_button_state = True

# Interrupt callback for Stop button
def stop_button_callback(pin):
    global stop_button_state
    stop_button_state = True

# Interrupt callback for Reset button
def reset_button_callback(pin):
    global reset_button_state
    reset_button_state = True

def blinking():
    led_pin.on()
    sleep(0.5)
    led_pin.off()
    sleep(0.5)

# Configure interrupt handlers for buttons
start_button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=start_button_callback)
stop_button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=stop_button_callback)
reset_button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=reset_button_callback)

# Main loop
while True:
    if start_button_state:
        led_state = True
        while stop_button_state == False | reset_button_state == False:
            blinking()
        led_pin.on()
        start_button_state = False
    
    if stop_button_state:
        led_state = False
        led_pin.off()
        stop_button_state = False
    
    if reset_button_state:
        led_state = False
        led_pin.off()
        sleep(2)
        reset_button_state = False
        start_button_state = True
