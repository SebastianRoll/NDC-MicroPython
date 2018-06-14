# Connect to WiFi
connect()

import max7219
import time
from machine import Pin, SPI
from umqtt.simple import MQTTClient


spi = SPI(-1, 10000000, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
display = max7219.Matrix8x8(spi, Pin(17), 4)
display.brightness(15)
display.fill(0)
display.text('....',0,0,1)
display.show()


# Publish test messages e.g. with:
# mosquitto_pub -t foo_topic -m hello
counter = 0
# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    global counter
    print((topic, msg))
    if msg == b'UP':
        counter += 1
    elif msg == b'DOWN':
        counter -= 1
    display.fill(0)
    display.text(str(counter),0,0,1)
    display.show()
    

def main(server="localhost"):
    c = MQTTClient("NDC MicroPython", server)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"foo_topic")
    while True:
        if True:
            # Blocking wait for message
            c.wait_msg()
        else:
            # Non-blocking wait for message
            c.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    c.disconnect()


Host = 'broker.hivemq.com'
port = 1883
port_websocket = 8000

main(Host)
if __name__ == "__main__":
    Host = 'broker.hivemq.com'
    port = 1883
    port_websocket = 8000

    main(Host)