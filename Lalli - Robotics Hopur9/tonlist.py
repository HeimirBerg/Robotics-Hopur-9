# Tónlist
import random
import subprocess
import time
import os

spilari = None #Hátalarinn

def term(skra): # Notum þetta fall til að skrifa
    return f"mpg123 -a plughw:3,0 --mono \"Desktop/Robotics-Hopur-9/music/{skra}.mp3\""

def spilatonlist(skra):
    global spilari
    stopdamusic()
    try:
        spilari = subprocess.Popen(
            term(skra),shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, 
            stdin=subprocess.PIPE)
    except Exception as e:
        print(f"Error: {e}")

def stopdamusic():
    os.system("pkill -f mpg123")

def rtonn(): # Spilum lag af handahófi
    tonar = ["guiltynigga", "baciate", "barbie"]
    spilatonlist(random.choice(tonar))
