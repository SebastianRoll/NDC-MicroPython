import songs
import notes
from machine import Pin, PWM
mel, rhythm = songs.split_tone_melody(songs.fur_elise)
tones = notes.parse_notes(filter=mel)
beeper = PWM(Pin(19, Pin.OUT), freq=440, duty=64)
notes.play(beeper, tones, mel, rhythm, tempo=30)
beeper.deinit()