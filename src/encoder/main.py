# https://github.com/SpotlightKid/micropython-stm-lib/tree/master/encoder

from time import sleep_ms
from encoder import Encoder


from machine import Pin, PWM
servo = PWM(Pin(21), freq=50, duty=77)
maxduty = const(122)
minduty = const(30)


e = Encoder(pin_clk=36, pin_dt=4, clicks=4, min_val=minduty, max_val=maxduty, start_val=77)
e_click = Pin(34, Pin.IN)

lastval = e.value

while True:
    val = e.value
    if e_click.value() is 0:
        e.reset()
        val = e.value
        lastval = val
        print(val)
        if val > maxduty or val < minduty:
            break
        servo.duty(val)
        sleep_ms(100)
    elif lastval != val:
        lastval = val
        print(val)
        if val > maxduty or val < minduty:
            break
        servo.duty(val)
        sleep_ms(100)