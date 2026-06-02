from machine import Pin, PWM
import time

tune = 442
pin = 16

n = {
"ces": 1975.53,
"c": 2093.00,
"cis": 2217.46,
"des": 2217.46,
"d": 2349.32,
"dis": 2489.02,
"es": 2489.02,
"e": 2637.02,
"fes": 2637.02,
"f": 2793.83,
"eis": 2793.83,
"fis": 2959.96,
"ges": 2959.96,
"g": 3135.96,
"gis": 3322.44,
"as": 3322.44,
"a": 3520.00,
"ais": 3729.31,
"b": 3729.31,
"h": 3951.07
}

def isnumeric(string):
    try: 
        float(string)
    except ValueError:
        return False
    return True

def frequency(note_name: str):
    if isnumeric(note_name[-1]):
        octave = int(note_name[-1])
        name = note_name[:-1]
    else:
        octave = 0
        name = note_name
    if name.islower():
        freq = n.get(name.lower()) * (2 ** (octave - 4))
        return round(freq)
    else:
        freq = n.get(name.lower()) * (2 ** (-octave - 5))
        return round(freq)

def play_melody(bpm, m):
    buzzer = PWM(Pin(pin))

    try:
        for f, t in m:
            buzzer.duty_u16(30000)
            buzzer.freq(frequency(f)*tune//440)
            time.sleep(0.9*t*60/bpm)
            buzzer.duty_u16(100)
            time.sleep(0.1*t*60/bpm)
    finally:
        buzzer.deinit()

def play_dur():
    play_melody(120, [
    ("d1", 1.5), ("fis1", 0.5), ("a1", 1), ("d2", 1),
    ("h1", 1), ("d2", 0.5), ("h1", 0.5), ("a1", 2),

    ("g1", 1.5), ("a1", 0.5), ("fis1", 1), ("d1", 1),
    ("e1", 2), ("d1", 2),

    ("a1", 1), ("a1", 1), ("g1", 1), ("g1", 1),
    ("fis1", 1), ("a1", 0.5), ("fis1", 0.5), ("e1", 2),

    ("a1", 1), ("a1", 1), ("g1", 1), ("g1", 1),
    ("fis1", 1), ("a1", 0.5), ("fis1", 0.5), ("e1", 2),

    ("d1", 1.5), ("fis1", 0.5), ("a1", 1), ("d2", 1),
    ("h1", 1), ("d2", 0.5), ("h1", 0.5), ("a1", 2),

    ("g1", 1.5), ("a1", 0.5), ("fis1", 1), ("d1", 1),
    ("e1", 2), ("d1", 2),
    ])

def play_moll():
    play_melody(120, [
    ("d1", 1.5), ("f1", 0.5), ("a1", 1), ("d2", 1),
    ("b1", 1), ("d2", 0.5), ("b1", 0.5), ("a1", 2),

    ("g1", 1.5), ("a1", 0.5), ("f1", 1), ("d1", 1),
    ("e1", 2), ("d1", 2),

    ("a1", 1), ("a1", 1), ("g1", 1), ("g1", 1),
    ("f1", 1), ("a1", 0.5), ("f1", 0.5), ("e1", 2),

    ("a1", 1), ("a1", 1), ("g1", 1), ("g1", 1),
    ("f1", 1), ("a1", 0.5), ("f1", 0.5), ("e1", 2),

    ("d1", 1.5), ("f1", 0.5), ("a1", 1), ("d2", 1),
    ("b1", 1), ("d2", 0.5), ("b1", 0.5), ("a1", 2),

    ("g1", 1.5), ("a1", 0.5), ("f1", 1), ("d1", 1),
    ("e1", 2), ("d1", 2),
    ])

def play_error():
    play_melody(120, [("B", 0.5), ("B", 0.5)])

def play_session():
    play_melody(150, [("e2", 0.5), ("d2", 0.5), ("c2", 0.5), ("d2", 0.5), ("e2", 1)])

def play_connect():
    play_melody(130, [("a2", 0.25), ("a2", 0.25)])

def play_connected():
    play_melody(120, [("d1", 0.25), ("fis1", 0.25), ("a1", 0.25), ("d2", 0.75)])

if __name__ == "__main__":
    play_connected()
