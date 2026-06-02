import sys
import time
import select
from machine import Pin
import Sound

poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

gelb = Pin(15, Pin.OUT)
gruen = Pin(11, Pin.OUT)
rot = Pin(7, Pin.OUT)
blau = Pin(3, Pin.OUT)

def send(text: str) -> str:
    sys.stdout.write(text + "\n")
    
    start_time = time.time()
    response = ""
    
    while (time.time() - start_time) < 2:
        if poller.poll(100):
            char = sys.stdin.read(1)
            if char == '\n':  
                break
            response += char
    return response

def connect_usb():

    gelb.on()
    gruen.on()
    rot.on()
    blau.on()
    Sound.play_connect()

    while True:
        if send("ping") == "pong": break
        time.sleep(1)
    
    Sound.play_connected()
    gelb.off()
    gruen.off()
    rot.off()
    blau.off()

connect_usb()

while True:
    status = send("status")
    if status == "Normal":
        gelb.on()
        time.sleep(5)
        gelb.off()
        time.sleep(120)
    elif status == "Weiter":
        gruen.on()
        Sound.play_dur()
        time.sleep(60)
    elif status == "Schade":
        rot.on()
        Sound.play_moll()
        time.sleep(60)
    elif status == "Session":
        blau.on()
        Sound.play_session()
        for _ in range(5):
            blau.on()
            time.sleep(0.5)
            blau.off()
            time.sleep(0.5)
    elif status == "Fehler":
        blau.on()
        Sound.play_error()
        for _ in range(25):
            blau.on()
            time.sleep(0.1)
            blau.off()
            time.sleep(0.1)
    elif status == "ping":
        continue
    else:
        connect_usb()
