# def parse_notes(path='notes.h'):
#     notes = {}
#     with open(path, 'r') as f:
#         for l in f:
#             l = l.split()
#             if len(l) > 0 and l[0] == '#define':
#                 (name, freq) = l[1:3]
#                 notes[name] = freq
#     return notes

def parse_notes(path='notes.csv', filter=None):
    notes = {}
    with open(path, 'r') as f:
        for l in f:
            s = l.strip('\n').split(',')
            if len(s) != 2:
                continue
            (name, freq) = s
            freq = int(freq)
            if filter and name not in filter:
                continue
            notes[name] = freq
    return notes

def play(beeper, tones, melody, rhythm, tempo=5):
    import time
    duty = 64
    rhythm = list(map(lambda x: x * 16, rhythm))
    for tone, length in zip(melody, rhythm):
        #print(tone)
        print(tones[tone])
        if tone is 'MUSIC_END':
            break
        if tones[tone] != 0:
            beeper.freq(tones[tone])
        else:
            beeper.duty(0)
            time.sleep(tempo / length)
            beeper.duty(duty)
            continue
        time.sleep(tempo / length)
    beeper.deinit()


def abc():
    from machine import Pin, PWM
    import time
    tempo = 5
    tones = {
        'c': 262,
        'd': 294,
        'e': 330,
        'f': 349,
        'g': 392,
        'a': 440,
        'b': 494,
        'C': 523,
        ' ': 0,
    }
    beeper = PWM(Pin(19, Pin.OUT), freq=440, duty=64)
    melody = 'cdefgabC'
    rhythm = [8, 8, 8, 8, 8, 8, 8, 8]
    #rhythm = list(map(lambda x: x * 16, rhythm))
    for tone, length in zip(melody, rhythm):
        beeper.freq(tones[tone])
        time.sleep(tempo / length)
    beeper.deinit()