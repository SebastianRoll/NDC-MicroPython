# https://github.com/peterhinch/micropython-async/blob/master/aledflash.py

from encoder import Encoder
from machine import Pin, PWM
import uasyncio as asyncio

minduty = const(30)
maxduty = const(122)

async def killer(duration):
    await asyncio.sleep(duration)


async def rotary(e, e_click, servo):
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
        elif lastval != val:
            lastval = val
            print(val)
            if val > maxduty or val < minduty:
                break
            servo.duty(val)
        await asyncio.sleep(0.1)


def run(seconds=10):
    servo = PWM(Pin(21), freq=50, duty=77)
    e = Encoder(pin_clk=36, pin_dt=4, clicks=2, min_val=minduty, max_val=maxduty, start_val=77)
    e_click = Pin(34, Pin.IN)

    loop = asyncio.get_event_loop()
    loop.create_task(rotary(e, e_click, servo))
    loop.run_until_complete(killer(seconds))
    servo.duty(77)

run()
