import os
from functions import *
import sys
import json
import read
import pygame.mixer


os.system("cls" if os.name == 'nt' else 'clear')

pygame.mixer.init()
pygame.mixer.music.load('zelda.mp3')
pygame.mixer.music.play()


print(read.gen["name"][0])
ps(gen["titlesplash"]["description"]) 
ps(gen["titlesplash"]["controls"]) # remember to make slow print()
ps("\nRemember that at anytime you can enter 'quit' and you will leave the game\n") # remember to make slow print()
f.close()


start_menu()
