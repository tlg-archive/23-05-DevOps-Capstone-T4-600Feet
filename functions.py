#All imports needed for game to run
import time
import random
import json
import sys
import os
import random
import pygame.mixer


f = open('./data/gamedata.json')
gen = json.load(f)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def press_enter_to_return():
    print("\nPress Enter to return to the game.")
    while True:
        return_input = input("\n> ").strip().lower()
        if return_input == '':
            clear_screen()
            break
        else:
            print("Invalid input. Press Enter to return to the game.")
##################################
#####Avaiable Action Commands#####
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

def ps(description, delay=0.00):     
    for char in description:         
        print(char, end='', flush=True)         
        time.sleep(delay)

############################
######Start Menu Setup######
############################
def start_menu():
     #updating this to put these options on the same line
    print(f"\n{ '1. New Game' : <25} { '2. Quit' : >25}\n")
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

####################################
######Save and Load Game Code#######
####################################
def save_game(player, submarine):
    save_data = {
        "current_room": player.current_room,
        "inventory": player.inventory,
        "sanity": player.sanity,
        "rooms":{}
    }
    for i in range(1, 7):
        save_data["rooms"]["room"+str(i)] = submarine.get_room_content(i)
    with open("save_game.json", "w") as save_file:
        json.dump(save_data, save_file)
        print("Game saved.")

def load_game(player, submarine):
    #first clear the room
    for room in submarine.rooms:
        submarine.rooms[room]['content'][1].clear()

    try:
        with open("save_game.json", "r") as save_file:
            save_data = json.load(save_file)
            player.current_room = save_data["current_room"]
            player.inventory = save_data["inventory"]
            player.sanity = save_data["sanity"]
            for room in submarine.rooms:
                #get items only NOT NPCs
                submarine.rooms[room]['content'][1] = save_data["rooms"]["room" + str(room)][1]
        print("Game loaded.")
    except FileNotFoundError:
        print("\nNo saved game found.\n")


####################################
####Save Rest and Override##########
####################################
def reset_saved_data():
    try:
        os.remove("save_game.json")
        print("\nSaved data reset to default.\n")
    except FileNotFoundError:
        print("No saved data found.")

#####################################
#########Sound and Volume############
#####################################
def play_sound(filename, volume):
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(volume)
    sound.play()

def display_look(oobject):
    npc = oobject[0]['nameOfNpc']
    items = ' and '.join(oobject[1].keys())

    print(f"You look around and see {npc}.\n")
    if len(oobject[1]) > 0:
        print(f"You also see {items}.\n")

######################################
#######Map and Submarine Code#########
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
    
    def display_map(self, player_current_room):
        map_visual = [
            "         ------>Alan's Quarters[6]<--------------",
            "        |              ^                        |",
            "        |              |                        |",
            "        |              |                        |",
            "        V              V                        V",
            "Connor's Quarters[5]<--->John's Quarters[3]<--->Chad's Quarters[4]",
            "               ^                                       ^",
            "               |                                       |",
            "               |                                       |",
            "               V                                       V",
            "    Supply Room[1](advil)                      Storage Area[2](Key)"
        ]

        # Highlight the player's current room
        for idx, line in enumerate(map_visual):
            if f"[{player_current_room}]" in line:
                map_visual[idx] = line.replace(f"[{player_current_room}]", f"[YOU ARE HERE {player_current_room}]")

        for line in map_visual:
            print(line)

# Example of usage
sub = Submarine()
sub.display_map(3)

############################################
######Commands, Stats and Information#######
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

#########################
######Game Setup#########
#########################
def main():
    submarine = Submarine()
    player = Player()
    pygame.mixer.init()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    sfx_volume = 1
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
        print(f"Your sanity is at {player.sanity}\n")
        print("=-=-=-=-=-=-=-=-=Inventory Data=-=-=-=-=-=-=-=-=")
        print(f"Things in your inventory {player.inventory}\n")
        pair = input("What do you want to do\n>").lower()
        os.system("cls" if os.name == 'nt' else 'clear')
        if pair.lower() == "setsanity1":
            player.sanity = 1
            print("Cheat activated! Sanity set to 1.")
        if pair.lower() == 'help':
            clear_screen()
            print("=-=-Game Commands-=-=")
            print("-type 'm (room #)' to move rooms ")
            print("-type 't (item name)' to pick up an item")
            print("-type 'look' to see descriptions of the rooms ")
            print("-type 'TA (NPC name)' to talk to an NPC")
            print("-type 'quit' at any point to exit the game")
            print("-type 'drop (item)' to drop an item")
            print("-type 'map' to view a map of the submarine")
            #print("=-=-=-=-=-=-=-=-=")
            print("\n=-=-Items-=-=")
            print("-there is a key in this game. find the key and take it")
            print("-there is an advil in this game. use the advil to gain 5 sanity points")
            print("\n=-=-Sound Commands-=-=")
            print("-type music (any number 0-100) to lower or increase the music volume")
            print("-type sfx (any number 0-100) to lower or increase the sfx volume")
            print("\n=-=-Save Your Game-=-=")
            print("1. type 'save' 2. exit the game 3. start a new game 4. type 'load'")
            print("you should see your previous game")
            print("=-=-=-=-=-=-=-=-=")
            #print("\nYou can do the following actions:")
            press_enter_to_return()
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
            if len(pair) < 2:
                print("You need to specify a room number. For example, 'm 3' to move to room 3.\n")
                continue
            room_choice = check_location(pair[1], adjacent_rooms) 
            if room_choice:
                player.move(int(pair[1]))
                play_sound("walk.mp3", sfx_volume)
                if player.sanity == 0:
                    reset_saved_data()
                    print("\n\nAs the weight of unseen horrors and twisted visions press down upon you, you feel your last thread of sanity snap. The depths of the abyss are nothing compared to the chasm that now yawns within your mind. You've lost your grip on reality, and the darkness swallows you whole. You can no longer continue...\n\n")
                    # SAMMY: looping back to game start
                    start_menu()
                    break

            else:
                print("you cannot move there\n")
                continue
        elif action == 'u':
            player.use_item(pair[1].lower())
        elif action == 'mu':
            test_vol = check_wanted_vol(pair[1])
            if type(test_vol) == type(1) and test_vol in range(0,101):
                set = test_vol/100
                pygame.mixer.music.set_volume(0.3 *set)
            else:
                print("that isnt possible")
        elif action == 'fx':
            test_vol = check_wanted_vol(pair[1])
            if type(test_vol) == type(1) and test_vol in range(0,101):
                sfx_volume = test_vol/100
            print("sound effects volume changed")
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

        #else:
            #print("endgame ")
            break
