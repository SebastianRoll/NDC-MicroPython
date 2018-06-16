connect('kubernetes lifeline', 'workwork')


from machine import Pin, PWM
to_left = PWM(Pin(12, Pin.OUT), freq=50, duty=0)
to_right = PWM(Pin(14, Pin.OUT), freq=50, duty=0)

TOLEFT_DUTY = 100
TORIGHT_DUTY = 100
TICK = 50
MIN_DUTY = 0
MAX_DUTY = 900

html = """<!DOCTYPE html>
<html>
    <head> <title>Drive my breadboard!</title> </head>
    <body> <h1>Drive</h1>
        <form>
        <div>
        <h2>LEFT</h2> %s
            <button name="left" value="DOWN" type="submit">Left -</button>
            <button name="left" value="UP" type="submit">Left +</button>
        </div>
        <div>
        <h2>RIGHT</h2> %s
            <button name="right" value="DOWN" type="submit">Right -</button>
            <button name="right" value="UP" type="submit">Right +</button>
        </div>
        </form>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

import network
sta_if = network.WLAN(network.STA_IF)
print('network config:', sta_if.ifconfig())
print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    print('Content %s' % request)

    left_u = request.find('/?left=UP')
    left_d = request.find('/?left=DOWN')
    right_u = request.find('/?right=UP')
    right_d = request.find('/?right=DOWN')

    if left_u == 6:
        TOLEFT_DUTY += TICK
    if left_d == 6:
        TOLEFT_DUTY -= TICK
    if right_u == 6:
        TORIGHT_DUTY += TICK
    if right_d == 6:
        TORIGHT_DUTY -= TICK

    TOLEFT_DUTY = max(MIN_DUTY, min(TOLEFT_DUTY, MAX_DUTY))
    TORIGHT_DUTY = max(MIN_DUTY, min(TORIGHT_DUTY, MAX_DUTY))
    to_left.duty(TOLEFT_DUTY)
    to_right.duty(TORIGHT_DUTY)
    response = html % (str(TOLEFT_DUTY), str(TORIGHT_DUTY))
    cl.send(response)
    cl.close()