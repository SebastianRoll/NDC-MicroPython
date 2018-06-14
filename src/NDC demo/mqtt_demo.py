import time
from umqtt.simple import MQTTClient

# Publish test messages e.g. with:
#mosquitto_pub -h broker.hivemq.com -p 1883 -t "foo_topic" -m "UP"

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

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

#main(Host)
if __name__ == "__main__":
    Host = 'broker.hivemq.com'
    port = 1883
    port_websocket = 8000

    main(Host)