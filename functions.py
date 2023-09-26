#All imports needed for game to run
import time
import random
import json
import sys
import os
import pygame
import pygame.mixer
import tkinter as tk
from common import clear_screen, press_enter_to_return, update_main_window

# changed to absolute path for unit testing
current_directory = os.path.dirname(os.path.abspath(__file__))
gamedata_path = os.path.join(current_directory, 'data', 'gamedata.json')
f = open(gamedata_path)

gen = json.load(f)

gamedata = gen#json.load(f)

################################################
### ROOM AND FLOOR SET UP WITH NUMERIC VALUE ###
################################################

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

#######################
### SUBMARINE CLASS ###
#######################

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
    
    ## CHAT GPT PROVIDED THIS, NEED TO CORRECT ARGS AND VARIABLES? ##
    def is_item_in_room(self, item_name, room):
        room_content = self.get_room_content(room)
        for content in room_content:
            if isinstance(content, dict) and item_name in content:
                return True
        return False


####################
### PLAYER CLASS ###
####################
           
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
            from main import update_output
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
