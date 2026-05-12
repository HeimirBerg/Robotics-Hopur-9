# Tónlist
import random
import os
import subprocess
import time

def tonlist(skra): # Notum þetta fall til að spila tónlist
    lag = subprocess.Popen(f"mpg123 -a plughw:3,0 --mono \"music/{skra}.mp3\"", shell=True)
    return lag

tonar = ["guiltynigga", "baciate", "barbie", "Adolf Hitler Speech in 1935"]

def rtonn():
    tonlist(random.choice(tonar))

x = input("Veldu 1 eða 2 fyrir valið eða handahófskennt")
if x == "1":
    skra = input("Veldu lag: ")
    lag = tonlist(skra)
    time.sleep(5)
    lag.terminate()
elif x == "2":
    rtonn()
else:
    print("Veldu eitthvað annað")
