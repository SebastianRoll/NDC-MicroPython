connect()


import time
from umqtt.simple import MQTTClient
from machine import Pin, ADC


# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

def main(server="localhost"):
    c = MQTTClient("NDC MicroPython controller", server)
    c.connect()

    sw = Pin(27, Pin.IN, Pin.PULL_UP)
    adcl = ADC(Pin(32))
    adcl.atten(ADC.ATTN_11DB)
    adcr = ADC(Pin(39))
    adcr.atten(ADC.ATTN_11DB)
    
    try:
        while True:
            if sw.value() == 0:
                break
            x = (max(3, min(124, int(adcl.read()/32))))
            y = max(3, min(124, int(adcr.read()/32)))
            c.publish(b"foo_topic", b"UP")
            sleep(1)
    finally:
        c.disconnect()


if __name__ == "__main__":
    Host = 'broker.hivemq.com'
    port = 1883
    port_websocket = 8000

    main(Host)
