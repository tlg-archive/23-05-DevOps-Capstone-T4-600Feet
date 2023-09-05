import os
from functions import *
from read import *

os.system("cls" if os.name == 'nt' else 'clear')
print(gen["name"][0])
print_description_slowly(gen["description"]) 
