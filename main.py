import os
from functions import *
import sys
import json

os.system("cls" if os.name == 'nt' else 'clear')

f = open(os.path.abspath('gamedata.json'))
gen = json.load(f)

print(gen["titlesplash"]["name"][0])
print(gen["titlesplash"]["description"]) 

print(gen["titlesplash"]["intro"]) # remember to make slow print()
print(gen["titlesplash"]["controls"]) # remember to make slow print()
print("remember that at anytime you can enter 'quit' and you will leave the game") # remember to make slow print()
f.close()


start_menu()
