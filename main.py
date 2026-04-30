# ---------- Main ---------- #
# Þetta er kóðinn sem Lalli mun keyra.
# Hér er kallað á föll úr modules og kóði til að kveikja og slökkva á Raspberry Lalli.

import src.motorcontrol as mc

print("Test")
print(mc.I2C_ADDRESS)


mc.stop()
print(mc.send_speeds(0,0))

print(mc.forward(200))
print(mc.reverse(200))
print(mc.turn_left(200))
print(mc.turn_right(200))