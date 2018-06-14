# https://github.com/dhylands/upy-rtttl

#
# This particular test was coded for the GHI Electronics G30 Development
# Board: https://www.ghielectronics.com/catalog/product/555
#
from machine import Timer, PWM, Pin
from time import sleep_ms
from rtttl import RTTTL
import songs

buz_tim = Timer(-1)
buz_ch = PWM(Pin(19, Pin.OUT), freq=440, duty=64)
pwm = 20 # reduce this to reduce the volume

def play_tone(freq, msec):
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        buz_ch.duty(pwm)
        buz_ch.freq(int(freq))
        sleep_ms(int(msec * 0.9))
    buz_ch.duty(0)
    sleep_ms(int(msec * 0.1))

def play(tune):
    try:
        for freq, msec in tune.notes():
            play_tone(freq, msec)
    except KeyboardInterrupt:
        play_tone(0, 0)

def play_song(search):
    play(RTTTL(songs.find(search)))

# play songs from songs.py
# play_song('Super Mario - Main Theme')
# play_song('Super Mario - Title Music')
play_song('MissionImp')

# play songs directly
# play(RTTTL('Monty Python:d=8,o=5,b=180:d#6,d6,4c6,b,4a#,a,4g#,g,f,g,g#,4g,f,2a#,p,a#,g,p,g,g,f#,g,d#6,p,a#,a#,p,g,g#,p,g#,g#,p,a#,2c6,p,g#,f,p,f,f,e,f,d6,p,c6,c6,p,g#,g,p,g,g,p,g#,2a#,p,a#,g,p,g,g,f#,g,g6,p,d#6,d#6,p,a#,a,p,f6,f6,p,f6,2f6,p,d#6,4d6,f6,f6,e6,f6,4c6,f6,f6,e6,f6,a#,p,a,a#,p,a,2a#'))
buz_ch.deinit()