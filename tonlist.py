# Tónlist
import random

def tonlist(skra):
    return f"mpg123 -a plughw:3,0 --mono \"music/{skra}\""

tonar = ["guiltynigga.mp3", "baciate.mp3", "barbie.mp3", "Adolf Hitler Speech in 1935.mp3"]

def rtonn():
    return random.choice(tonar)