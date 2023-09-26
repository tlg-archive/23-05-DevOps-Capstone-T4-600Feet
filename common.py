import tkinter as tk
from tkinter import END
import pygame
import pygame.mixer

def clear_screen():
    from main import clear_main_frame
    clear_main_frame() # Updated to TKinter function

def press_enter_to_return():
    update_output("\nPress Enter to return to the game.")
    while True:
        return_input = input("\n> ").strip().lower()
        if return_input == '':
            clear_screen()
            break
        else:
            update_output("Invalid input. Press Enter to return to the game.")

# replace every print with function to append text to main window text widget
def update_main_window(message):
    global main_text
    main_text.insert(tk.END, message + "\n")
    main_text.see(tk.END)  # auto-scrolls to the end

#################################
### AVAILABLE ACTION COMMANDS ###
#################################

help = ["help"] #works
move = ["move", "go", "travel", "run", "m"] #works
talk = ["talk", "speak", "chat", "ta", "ask"]
look = ["examine", "look", "focus", "observe", "inspect", "l"] #look works but not syns
take = ["grab", "take", "t", "pickup", "get"] #works
use = ["use", "interact", "u"]
map = ["map"] #works
drop = ['delete', 'drop']
music = ["music"] #works
effects = ["sfx", "fx"] #fx works but not syn
save = ["save"] #works
load = ["load"] #works
quit = ["quit"] #works
setsanity1 = ["setsanity1"]
allpossible = ["setsanity1", "quit", "save", "load", "help", "look", "u", "map", "get", "drop", "delete", "move", "go", "travel", "run", "m", "talk", "speak", "chat", "ta", "ask", "examine", "look", "focus", "observe", "inspect", "l", "grab", "take", "t", "pickup", "use", "interact", "music", 'sfx', 'fx']

################################################
###Action Command Check from Previous List######
################################################

def check_action(given_action):
    if given_action in allpossible:
        if given_action in setsanity1:
            return 'setsanity1'                
        if given_action in save:
            return 'save'
        if given_action in load:
            return 'load'
        if given_action in quit:
            return 'quit'
        if given_action in help:
            return 'help'
        if given_action in music:
            return 'mu'
        elif given_action in talk:
            return 'ta'
        elif given_action in look:
            return 'look'
        elif given_action in take:
            return 't'
        elif given_action in map:
            return 'map'
        elif given_action in drop:
            return 'd'
        elif given_action in effects:
            return 'fx'
        elif given_action in move:
            return 'm'
        else:
            return 'u'
    else:
        return 'invalid'

########################
### SOUND AND VOLUME ###
########################
 
def play_sound(filename, volume):
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(volume)
    sound.play()