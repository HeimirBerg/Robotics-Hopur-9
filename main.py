"""Aðal skráin sem Lalli keyrir"""

import subprocess

from movement import stop
from manualdrive import manual
from auto import *


def lalli() -> None:
    """Fallið hans Lalla"""
    
    print("\n=== Hæ, hæ, ég er Lalli Róbóti ===\n")

    """subprocess.Popen("python3 myndavel.py")""" # Keyrir myndavél í bakgrunni

    while True:
        print("Hvað viltu að ég geri?")
        print("1 - Sjálfvirk keyrsla\n2 - Hanvirk keyrsla\n3 - Hætta")

        try:
            selection = int(input("Val: "))

            if selection == 1:
                autopilot()
            elif selection == 2:
                manual()
            elif selection == 3:
                raise KeyboardInterrupt
            else:
                print("Ég veit ekki hvað þessi tala gerir.\nVeldu tölu á bilinu 1-3.\n")

        except ValueError:
            print("Úps. Passaðu að slá inn tölustaf á bilinu 1-3.\n")

        except KeyboardInterrupt:
            stop()
            print("\n=== Hætti í keyrslu ===\nSé þig seinna.")
            break
            

if __name__ == "__main__":
    lalli()
