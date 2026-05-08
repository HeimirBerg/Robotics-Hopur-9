# Gerum forrit svo bíllinn ratar eitthvert
import time
from movement import *

def tiusent():
    send_speeds(255, -255) ## 10cm
    time.sleep(0.25)
    stop()

def snua(): # 90 gradur
    send_speeds(255, 255)
    time.sleep(0.405)
    stop()

while True:
    x = input("Hvað á að gera? ")
    if x == "1":
        tiusent()
        break
    elif x == "2":
        snua()
        break
