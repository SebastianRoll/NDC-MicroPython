connect()


import time
from umqtt.simple import MQTTClient
from machine import Pin


# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

def main(server="localhost"):
    c = MQTTClient("NDC MicroPython controller", server)
    c.connect()

    def callback(p):
        print("PUSHED")
        c.publish(b"foo_topic", b"UP")
        

    e_click = Pin(27, Pin.IN, Pin.PULL_UP)
    e_click.irq(trigger=Pin.IRQ_FALLING, handler=callback)
    try:
        while True:
            pass
    finally:
        c.disconnect()


if __name__ == "__main__":
    Host = 'broker.hivemq.com'
    port = 1883
    port_websocket = 8000

    main(Host)
