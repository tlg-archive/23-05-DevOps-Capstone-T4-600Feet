import time
import random
import json
import sys
import os
import random


f = open('./data/gamedata.json')
gen = json.load(f)


move = ["move", "go", "travel", "run", "m"]
talk = ["talk", "speak", "chat", "ta", "ask"]
look = ["examine", "look", "focus", "observe", "inspect", "l"]
take = ["grab", "take", "t", "pickup", "get"]
use = ["use", "interact"]
map = ["map"]
drop = ['delete', 'drop']

allpossible = ["map", "get", "drop", "delete", "move", "go", "travel", "run", "m", "talk", "speak", "chat", "ta", "ask", "examine", "look", "focus", "observe", "inspect", "l", "grab", "take", "t", "pickup", "use", "interact"]

#f = open('gamedata.json')
gamedata = gen#json.load(f)

def check_action(given_action):
    if given_action in allpossible:
        if given_action in move:
            return 'm'
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
        else:
            return 'u'
    else:
        return 'invalid'

def check_location(wanted_room, adjacent_rooms):
    if wanted_room.isnumeric():
        if int(wanted_room) in range(1,7) and int(wanted_room) in adjacent_rooms:
            return True
    else:
        return False
    
def check_item(wanted_item, room_items):
    if wanted_item.lower() in room_items:
        return True
    else:
        return False
        
def help_message():
    "This is a help message"

def ps(description, delay=0.005):     
    for char in description:         
        print(char, end='', flush=True)         
        time.sleep(delay)

def start_menu():
    print("1.New Game")
    print("2.Quit")
    player_choice = input("Enter your choice '1 or 2'> ")
    if player_choice == "1":
        os.system("cls" if os.name == 'nt' else 'clear')
        start_game()
    elif player_choice == "2":
        ps("Goodbye!")
        sys.exit()
    else:
        print("Invalid answer, try again")
        start_menu()
def start_game():

    ps(gen["titlesplash"]["intro"] + '\n') # remember to make slow print()
    main()

def save_game(player, submarine):
        save_data = {
            "current_room": player.current_room,
            "inventory": player.inventory,
            "sanity": player.sanity
        
    }
        with open("save_game.json", "w") as save_file:
            json.dump(save_data, save_file)
        print("Game saved.")

def load_game(player, submarine):
        try:
            with open("save_game.json", "r") as save_file:
                save_data = json.load(save_file)
                player.current_room = save_data["current_room"]
                player.inventory = save_data["inventory"]
                player.sanity = save_data["sanity"]
            print("Game loaded.")
        except FileNotFoundError:
            print("No saved game found.")


def display_look(oobject):
    npc = oobject[0]['nameOfNpc']
    items = ' and '.join(oobject[1].keys())

    print(f"You look around and see {npc}.\n")
    if len(oobject[1]) > 0:
        print(f"You also see {items}.\n")

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
    
    def display_map(self, player_current_room):
        mapstring = ""
        for room_num, room_data in self.rooms.items():
            mapstring += f"Room {room_num}: "
            if room_num == player_current_room:
                mapstring+="[you  r here]"
            else:
                mapstring += " " *13
            for adj_room in room_data["adjacent"]:
                mapstring += f"-> room {adj_room} "
        print("++++++++++++++++++++++++++++++++++++")
        print(mapstring)
            
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
    def found_advil(self):
        self.has_advil = True
    def has_bathroom_access(self):
        self.has_bathroom_access = True
    def add_to_inventory(self, item):
        self.inventory.append(item)
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
    def move(self, room):
        self.current_room = room
        self.sanity = self.sanity - 1

def main():
    submarine = Submarine()
    player = Player()
    for i in range(len(gamedata['rooms'])):
        stuffinroom = gamedata['rooms'][i]['content'].keys()
        npc_data = gamedata['rooms'][i]['content']['npc']
        item_data = gamedata['rooms'][i]['content']['items']
        submarine.place_content(npc_data, i+1)
        submarine.place_content(item_data, i+1)

    while True:
        adjacent_rooms = submarine.get_adjacent_rooms(player.current_room)       
        room_content = submarine.get_room_content(player.current_room)
        print("=-=-=-=-=-=-=-=-=Location Data=-=-=-=-=-=-=-=-=")
        print(f"you are in room {player.current_room}")
        print(f"Adjacent rooms {adjacent_rooms}\n")
        print("=-=-=-=-=-=-=-=-=Player Data=-=-=-=-=-=-=-=-=") 
        print(f"Your sanity is at {player.sanity}")
        print("=-=-=-=-=-=-=-=-=Inventory Data=-=-=-=-=-=-=-=-=")
        print(f"Things in your inventory {player.inventory}")
        pair = input("What do you want to do\n>").lower()
        os.system("cls" if os.name == 'nt' else 'clear')
        if pair.lower() == 'help':
            print("You can do the following actions: Move (M) Take (T) Look (L) Talk (TA)\nAt any point, you can type in 'quit' to exit the game.\n")
            continue
        if pair.lower() == 'quit':
            ps("Goodbye...\n")
            sys.exit()
        elif pair.lower() == 'save':
            save_game(player, submarine)
            continue
        elif pair.lower() == 'load':
            load_game(player, submarine)
            continue
        pair = pair.split()
        action = pair[0] 
        action = check_action(action)
        if action == 'invalid':
            print("That is not a valid action\n")
            print("Valid options are 'move' 'talk' 'take' 'use' and 'look'\n")
            continue
        #action = input("\n> ").lower()
        if action == "m":
            room_choice = check_location(pair[1], adjacent_rooms) 
            if room_choice:
                player.move(int(pair[1]))
                if player.sanity == 0:
                    print("GAME OVER")
                    break
            else:
                print("you cannot move there\n")
                continue
        elif action == 'l':
            display_look(room_content)
        elif action == 't':
            if pair[1].lower() == 'key':
                item_choice = check_item('a key', room_content[1].keys())
                if item_choice == True:
                    player.add_to_inventory(pair[1].lower())
                    submarine.rem_room_content('a key', player.current_room)
                    print("You picked up a key\n")
                else:
                    print(f"There is no {pair[1]} to pick up.\n")
            else:
                item_choice = check_item(pair[1].lower(), room_content[1].keys())
                if item_choice == True:
                    player.add_to_inventory(pair[1].lower())
                    submarine.rem_room_content(pair[1].lower(), player.current_room)
                    print(f"You picked up {pair[1]}\n")
                else:
                    print(f"You cannot pick up {pair[1]}\n")
        elif action == "map":
            submarine.display_map(player.current_room)
            continue
        elif action == 'd':
            item_choice = check_item(pair[1], player.inventory)
            if item_choice:
                player.remove_from_inventory(pair[1].lower())
                submarine.place_item(pair[1].lower(), player.current_room)
                ps(f"You dropped {pair[1]} in the room.\n\n")
        elif action == "ta":
            if pair[1].lower() == room_content[0]['nameOfNpc'].lower():
                npc_intros = room_content[0]['intros']
                print(random.choice(npc_intros))
            else:
                print(f"You can't talk to {pair[1]}\n")
                print(f"Did you mean 'talk {room_content[0]['nameOfNpc']}'?\n")
        else:
            print("endgame ")
            break
