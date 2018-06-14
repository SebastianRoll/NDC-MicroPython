import uasyncio as asyncio

from machine import Timer, PWM, Pin
from rtttl import RTTTL
import songs

buz_ch1 = PWM(Pin(19), freq=440, duty=0)
buz_ch2 = PWM(Pin(4), freq=440, duty=0)

async def play_annoy():
    while True:
        buz_ch1.freq(300)
        await asyncio.sleep_ms(200)
        buz_ch1.freq(500)
        await asyncio.sleep_ms(200)

async def play_annoy2():
    while True:
        buz_ch2.freq(300)
        await asyncio.sleep_ms(200)
        buz_ch2.freq(500)
        await asyncio.sleep_ms(200)

async def play_tone(freq, msec, buz_ch):
    print('{} - freq = {:6.1f} msec = {:6.1f}'.format(buz_ch, freq, msec))
    if freq > 0:
        buz_ch2.duty(pwm)
        buz_ch2.freq(int(freq))
        await asyncio.sleep_ms(int(msec * 0.9))
    buz_ch2.duty(0)
    await asyncio.sleep_ms(int(msec * 0.1))


async def play(tune, buz_ch):
    try:
        for freq, msec in tune.notes():
            await play_tone(freq, msec, buz_ch)
    except KeyboardInterrupt:
        await play_tone(0, 0, buz_ch)


# async def play_song(tune, buz_ch):
#     await play(tune), buz_ch)

# play songs from songs.py
# play_song('Super Mario - Main Theme')
# play_song('Super Mario - Title Music')
# play_song('MissionImp')

# play songs directly
# play(RTTTL('Monty Python:d=8,o=5,b=180:d#6,d6,4c6,b,4a#,a,4g#,g,f,g,g#,4g,f,2a#,p,a#,g,p,g,g,f#,g,d#6,p,a#,a#,p,g,g#,p,g#,g#,p,a#,2c6,p,g#,f,p,f,f,e,f,d6,p,c6,c6,p,g#,g,p,g,g,p,g#,2a#,p,a#,g,p,g,g,f#,g,g6,p,d#6,d#6,p,a#,a,p,f6,f6,p,f6,2f6,p,d#6,4d6,f6,f6,e6,f6,4c6,f6,f6,e6,f6,a#,p,a,a#,p,a,2a#'))

async def bar():
    count = 0
    while True:
        count += 1
        print(count)
        await asyncio.sleep(1)  # Pause 1s


async def killer():
    print("sleeping {} seconds".format(10))
    await asyncio.sleep(10)

pwm = 5 # reduce this to reduce the volume

loop = asyncio.get_event_loop()
loop.create_task(bar())
# loop.create_task(play_song('Super Mario - Title Music', buz_ch1))
# loop.create_task(play(RTTTL(songs.find('MissionImp')), buz_ch1))
loop.create_task(play_annoy())
loop.create_task(play_annoy2())
# loop.create_task(play(RTTTL(songs.find('Super Mario - Title Music')), buz_ch2))

try:
    loop.run_until_complete(killer())
finally:
    buz_ch1.deinit()
    buz_ch2.deinit()

# FreeRTOS