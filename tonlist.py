# Tónlist
import random

def tonlist(skra):
    return f"mpg123 -a plughw:3,0 --mono \"music/{skra}\""

tonar = ["guiltynigga.mp3", "baciate.mp3", "barbie.mp3", "Adolf Hitler Speech in 1935.mp3"]

def rtonn():
    tonlist(random.choice(tonar))

x = input("Veldu 1 eða 2 fyrir valið eða handahófskennt")
if x == "1":
    lag = input("Veldu lag")
    print(tonlist(lag))
elif x == "2":
    print(rtonn())
else:
    print("Veldu eitthvað annað")
