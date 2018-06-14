import max7219
import uasyncio
from machine import Pin, SPI, PWM

spi = SPI(-1, 10000000, miso=Pin(19), mosi=Pin(23), sck=Pin(18))

display = max7219.Matrix8x8(spi, Pin(17), 4)
display.brightness(15)

buz_ch1 = PWM(Pin(19), freq=440, duty=0)
pwm_duty = 100

async def file_to_led():
    while True:
        with open('ledtext.txt', 'r') as f:
            for l in f:
                print(l)
                display.fill(0)
                display.text(l,0,0,1)
                display.show()
                await uasyncio.sleep(0.5)

        display.fill(0)
        display.show()
        await uasyncio.sleep(1)

        
async def temp():
    import dht
    from time import sleep
    
    d = dht.DHT22(Pin(4))
    while True:
        print('measuring..')
        d.measure()
        #await uasyncio.sleep_ms(200)
        t = d.temperature()
        h = d.humidity()
        display.fill(0)
        display.text('{}C'.format(int(t)),0,0,1)
        display.show()
        buz_ch1.duty(0)
        sleep(1)
        await uasyncio.sleep(5)

        
async def play_tone(freq, msec, buz_ch):
    print('{} - freq = {:6.1f} msec = {:6.1f}'.format(buz_ch, freq, msec))
    if freq > 0:
        buz_ch.duty(pwm_duty)
        buz_ch.freq(int(freq))
        await uasyncio.sleep_ms(int(msec * 0.9))
    buz_ch.duty(0)
    await uasyncio.sleep_ms(int(msec * 0.1))


async def play(tune, buz_ch):
    try:
        for freq, msec in tune.notes():
            await play_tone(freq, msec, buz_ch)
    except KeyboardInterrupt:
        await play_tone(0, 0, buz_ch)        
    
    
async def killer():
    print("sleeping {} seconds".format(20))
    await uasyncio.sleep(20)

    
loop = uasyncio.get_event_loop()
loop.create_task(file_to_led())
loop.create_task(temp())

from rtttl import RTTTL
import songs
loop.create_task(play(RTTTL(songs.find('MissionImp')), buz_ch1))

try:
    loop.run_until_complete(killer())
finally:
    buz_ch1.deinit()
    display.fill(0)
    display.show()