# Tónlist
import random
import subprocess
import time

spilari = None #Hátalarinn

def term(skra): # Notum þetta fall til að skrifa
    return f"mpg123 -a plughw:3,0 --mono \"music/{skra}.mp3\""

def spilatonlist(skra):
    global spilari
    stopdamusic()
    try:
        spilari = subprocess.Popen(
            term(skra),shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error: {e}")

def stopdamusic():
    global spilari
    if spilari is not None:
        spilari.terminate()
        spilari = None

def rtonn(): # Spilum lag af handahófi
    tonar = ["guiltynigga", "baciate", "barbie", "Adolf Hitler Speech in 1935"]
    spilatonlist(random.choice(tonar))


x = input("Veldu 1 eða 2 fyrir valið eða handahófskennt")
if x == "1":
    skra = input("Veldu lag: ")
    spilatonlist(skra)
    time.sleep(5)
    stopdamusic()
elif x == "2":
    rtonn()
else:
    print("Veldu eitthvað annað")
