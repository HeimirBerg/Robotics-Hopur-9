# Tónlist
import random
import os
import subprocess

def tonlist(skra):
    lag = subprocess.Popen(f"mpg123 -a plughw:3,0 --mono \"music/{skra}.mp3\"")
    return lag

tonar = ["guiltynigga", "baciate", "barbie", "Adolf Hitler Speech in 1935"]

def rtonn():
    tonlist(random.choice(tonar))

x = input("Veldu 1 eða 2 fyrir valið eða handahófskennt")
if x == "1":
    lag = input("Veldu lag: ")
    print(tonlist(lag))
elif x == "2":
    print(rtonn())
else:
    print("Veldu eitthvað annað")
