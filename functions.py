#All imports needed for game to run
import time
import random
import json
import sys
import os
import pygame
import pygame.mixer
import tkinter as tk
from common import clear_screen, press_enter_to_return, update_main_window, handle_sound_control

f = open('./data/gamedata.json')
gen = json.load(f)

##################################
#####Available Action Commands#####
##################################

move = ["move", "go", "travel", "run", "m"]
talk = ["talk", "speak", "chat", "ta", "ask"]
look = ["examine", "look", "focus", "observe", "inspect", "l"]
take = ["grab", "take", "t", "pickup", "get"]
use = ["use", "interact", "u"]
map = ["map"]
drop = ['delete', 'drop']
music = ["music"]
effects = ["sfx", "fx"]
allpossible = ["u", "map", "get", "drop", "delete", "move", "go", "travel", "run", "m", "talk", "speak", "chat", "ta", "ask", "examine", "look", "focus", "observe", "inspect", "l", "grab", "take", "t", "pickup", "use", "interact", "music", 'sfx', 'fx']

gamedata = gen#json.load(f)

################################################
###Action Command Check from Previous List######
################################################

def check_action(given_action):
    if given_action in allpossible:
        if given_action in music:
            return 'mu'
        elif given_action in talk:
            return 'ta'
        elif given_action in look:
            return 'l'
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

####################################################
####Room and Floor set up with numeric values#######
####################################################

def check_location(wanted_room, adjacent_rooms):
    if wanted_room.isnumeric():
        if int(wanted_room) in range(1,7) and int(wanted_room) in adjacent_rooms:
            return True
    else:
        return False

def check_wanted_vol(wanted_vol):
    if wanted_vol.lower() == 'on':
        return 100
    elif wanted_vol.lower() == "off":
        return 1
    elif wanted_vol.isnumeric() and int(wanted_vol) in range (0, 101):
        return int(wanted_vol)
    return False

def check_item(wanted_item, room_items):
    if wanted_item.lower() in room_items:
        return True
    else:
        return False

#####################################
#########Sound and Volume############
#####################################

def play_sound(filename, volume):
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(volume)
    sound.play()

######################################
####### Submarine Class ##############
######################################

class Submarine:
    def __init__(self):
        self.rooms = {}
        for i in range(1, 7):
            self.rooms[i] = {'adjacent': [], 'content': []}
            connections = [(1,3),(2,4),(3,5,4,1),(4,2,3,6),(5,6,3),(6,5,4)]
        for room, *adjacent in connections:
            self.rooms[room]['adjacent'] = adjacent

    def place_content(self, content, chosen_room):
        self.rooms[chosen_room]['content'].append(content)

    def place_item(self, item, room):
        if item == 'advil':
            self.rooms[room]['content'][1].update({"advil": {"heal": 5}})
        elif item == 'key':
            self.rooms[room]['content'][1].update({"a key": {"unlock": "True"}})

    def get_adjacent_rooms(self, room):
        return self.rooms[room]['adjacent']

    def get_room_content(self, room):
        return self.rooms[room]['content']
    
    def rem_room_content(self, content, room):
        self.rooms[room]['content'][1].pop(content)

############################################
###### Player Class ########################
############################################           
class Player:
    def __init__(self):
        self.current_room = 4
        self.sanity = 30 # everymove subtracts 1
        self.has_advil = False
        self.has_key = False
        self.has_bathroom_access = False
        self.inventory = []
    def get_current_room(self):
        return self.current_room
    def found_key(self):
        self.has_key = True
    #def found_advil(self):
    #    self.has_advil = True
    def has_bathroom_access(self):
        self.has_bathroom_access = True
    def use_item(self, item_name):
        if item_name == "advil" and item_name in self.inventory:
            self.sanity += 5
            self.remove_from_inventory('advil')
            print("You used advil and your sanity has increased by 5.\n")
        else:
            print(f"You can't use {item_name} right now.\n")
    def add_to_inventory(self, item):
        self.inventory.append(item)
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
    def move(self, room):
        self.current_room = room
        self.sanity = self.sanity - 1

########################
### tkinter handlers ###
########################

def handle_npc_interaction(player, npc_name, room_content):
    if npc_name.lower() == room_content[0]['nameOfNpc'].lower():
        npc_intros = room_content[0]['intros']
        print(random.choice(npc_intros))
        if pair[1].lower() == room_content[0]['nameOfNpc'].lower():
            npc_intros = room_content[0]['intros']
            print(random.choice(npc_intros))
            for question in room_content[0]["dialogue"]:
                print(room_content[0]["dialogue"].get(question))
            dialogue_choice = input("\nHow do you want to respond?\n> ")
            os.system("cls" if os.name == 'nt' else 'clear')
            while dialogue_choice != '4':
                if room_content[0]["responses"].get(dialogue_choice) == None:
                    print("You must input a value between 1 and 4.\n")
                else:
                    print(room_content[0]["responses"].get(dialogue_choice))
                for question in room_content[0]["dialogue"]:
                    print(room_content[0]["dialogue"].get(question))
                dialogue_choice = input("\nHow do you want to respond?\n> ")
                os.system("cls" if os.name == 'nt' else 'clear')
            print(room_content[0]["responses"].get('4'))
        else:
            print(f"You can't talk to {pair[1]}\n")
            print(f"Did you mean 'talk {room_content[0]['nameOfNpc']}'?\n")

##################################
######Game Setup / Start #########
##################################


# OLD CODE UINCORPORATED FOR CONSOLE LOOP

""" def main():

    while True:
        adjacent_rooms = submarine.get_adjacent_rooms(player.current_room)       
        room_content = submarine.get_room_content(player.current_room)
        print("=-=-=-=-=-=-=-=-=Location Data=-=-=-=-=-=-=-=-=")
        print(f"you are in room {player.current_room}")
        print(f"Adjacent rooms {adjacent_rooms}\n")
        print("=-=-=-=-=-=-=-=-=Player Data=-=-=-=-=-=-=-=-=") 
        print(f"Your sanity is at {player.sanity}\n")
        print("=-=-=-=-=-=-=-=-=Inventory Data=-=-=-=-=-=-=-=-=")
        print(f"Things in your inventory {player.inventory}\n")
        #SAMMY: Tkinter replacement
        #pair = input("What do you want to do\n>").lower()
        pair = command.lower()
        os.system("cls" if os.name == 'nt' else 'clear')
        pair = pair.split()
        action = pair[0] 
        action = check_action(action)
        if action == 'invalid':
            print("That is not a valid action\n")
            print("Valid options are 'move' 'talk' 'take' 'use' and 'look'\n")
            continue
        #action = input("\n> ").lower()
 """