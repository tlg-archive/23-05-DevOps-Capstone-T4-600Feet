import time
import random

move = ["move", "go", "travel", "run", "m"]
talk = ["talk", "speak", "chat", "ta", "ask"]
look = ["examine", "look", "focus", "observe", "inspect", "l"]
take = ["grab", "take", "t", "pickup"]
use = ["use", "interact"]

allpossible = ["move", "go", "travel", "run", "m", "talk", "speak", "chat", "ta", "ask", "examine", "look", "focus", "observe", "inspect", "l", "grab", "take", "t", "pickup", "use", "interact"]

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
        
def help_message():
    return "this print help screen"


def ps(description, delay=0.02):     
    for char in description:         
        print(char, end='', flush=True)         
        time.sleep(delay)


def start_menu():
    print("1.New Game")
    print("2.Quit")
    player_choice = input("Enter your choice '1 or 2'> ")
    if player_choice == "1":
        start_game()
    elif player_choice == "2":
        print("Goodbye!")
        exit()
    else:
        print("invalid answer, try again")
        start_menu()
def start_game():
    player_input = ''
    while player_input != 'quit':
        # This is where game logic would go
        ps("what do you want to do?")
        #player_input = input("placeholder to stop infinite loop\n >").lower()
        main()
        if player_input == "quit":
            print("Goodbye!")
            exit()

#def play_game(user_start):
#    return 1
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

    def get_adjacent_rooms(self, room):
        return self.rooms[room]['adjacent']

    def get_room_content(self, room):
        return self.rooms[room]['content']

class Player:
    def __init__(self):
        self.current_room = 1
        self.sanity = 30 # everymove subtracts 1
        self.has_advil = False
        self.has_key = False
        self.has_bathroom_access = False
    def found_key():
        self.has_key = True
    def found_advil():
        self.has_advil = True
    def has_bathroom_access():
        self.has_bathroom_access = True
    def move(self, room):
        self.current_room = room
        self.sanity = self.sanity - 1

def main():
    submarine = Submarine()
    player = Player()

    while True:
        adjacent_rooms = submarine.get_adjacent_rooms(player.current_room)       
        room_content = "some random function"
        print(f"you are in room {player.current_room}")
        print(f"Adjacent rooms {adjacent_rooms}")
        pair = input("\n>")
        if pair.lower() == 'help':
            print("you can do the following actions Move (M) Take (T) Look (L) Talk (TA)")
            continue
        pair = pair.split()
        action = pair[0] 
        action = check_action(action)
        if action == 'invalid':
            print("That is not a valid action")
            print("Valid options are 'move' 'talk' 'take' 'use' and 'look'")
            continue
        #action = input("\n> ").lower()
        if action == "m":
            room_choice = check_location(pair[1], adjacent_rooms) 
            if room_choice:
                player.move(int(pair[1]))
            else:
                print("you cannot move there\n")
                continue
        else:
            print(submarine)
            break
