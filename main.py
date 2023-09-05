import os
from functions import *
from read import *
import sys

os.system("cls" if os.name == 'nt' else 'clear')
print(gen["name"][0])
print(gen["description"]) 

print(gen["intro"]) # remember to make slow print()
print(gen["controls"]) # remember to make slow print()
print("remember that at anytime you can enter 'quit' and you will leave the game") # remember to make slow print()



start_menu()
	
