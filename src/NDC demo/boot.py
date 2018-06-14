# This file is executed on every boot (including wake-boot from deepsleep)

#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

def connect(ssid='NDC 2018', pwd=''):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def disconnect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.disconnect()
    
def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)