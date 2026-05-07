# Gerum forrit svo bíllinn ratar eitthvert
import time
from hreyfing import *

def tiusent():
    senda(255, -255) ## 10cm
    time.sleep(0.25)
    stoppa()

def snua():
    senda(255, 255)
    time.sleep(0.4)
    stoppa()

while True:
    x = input("Hvað á að gera? ")
    if x == "1":
        tiusent()
        break
    elif x == "2":
        snua()
        break
