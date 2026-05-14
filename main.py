"""Aðal skráin sem Lalli keyrir"""

import subprocess
from movement import stop
from manualdrive import manual
from auto import *
from lidar_auto import *


def lalli() -> None:
    """Fallið hans Lalla"""
    
    print("\n=== Hæ, hæ, ég er Lalli Róbóti ===\n")
    """myndavel = subprocess.Popen("python3 Desktop/Robotics-Hopur-9/myndavel.py", shell=True, 
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, 
                                stdin=subprocess.PIPE) # Keyrir myndavél í bakgrunni
    """
    time.sleep(2)
    while True:
        print("Hvað viltu að ég geri?")
        print("1 - Sjálfvirk keyrsla\n2 - Handvirk keyrsla\n3 - Hætta")

        try:
            selection = int(input("Val: "))

            if selection == 1:
                autopilot()
            elif selection == 2:
                manual()
            elif selection == 3:
                raise KeyboardInterrupt
            elif selection == 4:
                autopilot_prufa()
            else:
                print("Ég veit ekki hvað þessi tala gerir.\nVeldu tölu á bilinu 1-3.\n")

        except ValueError:
            print("Úps. Passaðu að slá inn tölustaf á bilinu 1-3.\n")

        except KeyboardInterrupt:
            stop()
            print("\n=== Hætti í keyrslu ===\nSé þig seinna.")
            myndavel.terminate()
            break
    
            

if __name__ == "__main__":
    lalli()
