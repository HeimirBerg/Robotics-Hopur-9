# Tónlist
import random
import subprocess
import time
import os

spilari = None #Hátalarinn

def term(skra): # Notum þetta fall til að skrifa
    return f"mpg123 --mono \"music/{skra}.mp3\""

def spilatonlist(skra):
    global spilari
    stopdamusic()
    try:
        spilari = subprocess.Popen(
            term(skra),
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

"""while True:
    x = input("Veldu 1 eða 2 fyrir valið eða handahófskennt")
    if x == "1":
        skra = input("Veldu lag: ")
        spilatonlist(skra)
    elif x == "2":
        rtonn()
    elif x == "3":
        stopdamusic()
        break
    else:
        print("Veldu eitthvað annað")"""
