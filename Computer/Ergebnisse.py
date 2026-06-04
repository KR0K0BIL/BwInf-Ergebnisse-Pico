import subprocess
import serial
import time
import requests
import os
from bs4 import BeautifulSoup

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "de-DE,de;q=0.9,en-DE;q=0.8,en;q=0.7,it-IT;q=0.6,it;q=0.5,en-US;q=0.4",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "referer": "https://login.bwinf.de/app/PMS",
}

BAUD_RATE = 115200

def connect_usb() -> str:
    print("Connect USB...", end="\r")
    while True:
        try:
            cp = subprocess.run(
                "ls /dev/cu.usbmodem*",
                capture_output=True,
                shell=True,
                check=True,
                text=True,
            )
            print("Connected     ")
            return cp.stdout.strip()
        except subprocess.CalledProcessError as cpe:
            time.sleep(1)

url = ""

TOKEN_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".token.txt")

def request_login():
    global url
    url = input("Bitte logge dich auf https://login.bwinf.de ein und gib die URL hier ein:\n")
    split = url.split("/")
    split[-1] = f"1.0.0.27.5.0"
    url = "/".join(split)
    with open(TOKEN_FILE, "w") as file:
        file.write(url)

def load_token():
    global url
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            url = file.read().strip()
    else:
        request_login()

load_token()

while True:
    try:
        SERIAL_PORT = connect_usb()
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

        def send(text: str):
            ser.write((text+"\n").encode('utf-8'))

        time.sleep(1)

        while True:
            if ser.in_waiting > 0:
                request = ser.readline().decode('utf-8').strip()
                response = None
                print(">>", request)
                if request == "ping":
                    response = "pong"
                if request == "status":
                    try:
                        post_response = requests.post(url, headers=headers, cookies={}, timeout=2)

                        soup = BeautifulSoup(post_response.text, 'html.parser')

                        if "Session Timeout" in soup.text:
                            response = "Session"
                        else:
                            response = "Fehler"
                            for label in soup.select("span[class*=label]"):
                                text = label.text
                                if text.startswith("Runde 2"):
                                    if text == "Runde 2 nicht mehr geöffnet, aber noch nicht bewertet":
                                        response = "Normal"
                                    elif "nicht" in text:
                                        response = "Schade"
                                    else:
                                        response = "Weiter"
                            if response == "Fehler":
                                print(soup.text)

                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        response = "Fehler"

                print("<<", response)
                if response is not None:
                    send(response)
                
                if response == "Session":
                    request_login()

    except (serial.SerialException, OSError, FileNotFoundError) as f:
        continue
    except KeyboardInterrupt:
        break
