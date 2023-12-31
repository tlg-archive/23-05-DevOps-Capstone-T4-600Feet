import os
import sys
import json
import pygame
import random
import tkinter as tk
from tkinter import Tk, Text, Entry, Frame, Button, Scrollbar, END, Toplevel, Label
from title import *
from functions import Submarine, Player, gamedata
from common import clear_screen, press_enter_to_return, update_main_window, play_sound, check_action

# setting global variables
game_output = None
user_input = None
splash_title_label = None
splash_description_text = None
continue_label = None
game_status_text_widget = None
player_instance = None
submarine_instance = None
sfx_volume = .9   # out of 1.0

# function to clear main window
def clear_main_frame():
    main_frame.delete(1.0, tk.END)

# handle user commands
def handle_input(event):
    # added player_instance, submarine_instance, sfx_volume due to "not defined" errors
    global state, game_output, player_instance, submarine_instance, sfx_volume

    command = user_input.get()
    print(f"Enter key pressed. Command entered: {command}") #debugging
    
    # clear user input field
    user_input.delete(0, tk.END)
    
    # Process the command
    process_command(command, player_instance, submarine_instance, game_output, sfx_volume)
    
    # Update game state display
    update_game_state_display(game_status_text_widget, player_instance, submarine_instance)

    if state == "splash":
        print("In splash state") # for debugging
        update_output("Choose input 1 or 2")
        state = "choose_input"
    elif state == "choose_input":
        print("In choose_input state") # for debugging
        if command == "1":
            start_game()
            state = "game_state" # maybe move up a line?
            print("In game state") # for debugging
        elif command == "2":
            update_output("You chose option 2!")
            sys.exit()
        else:
            update_output("Invalid choice. Please choose 1 or 2.")
            # Bug: nothing stopping user from entering anything and

# updates output area #
def update_output(text): 
    global game_output
    # set text to modifiable 
    game_output.config(state='normal')
    game_output.insert(END, text + "\n")
    # disable text area to prevent player editing it
    game_output.config(state='disabled')
    game_output.see(END)

def process_command(command, player, submarine, game_output_widget, sfx_volume):
    # Split the command into action and arguments
    command_parts = command.lower().split()
    action = check_action(command_parts[0])

    if action == 'invalid':
        update_output("Type 'help' for a list of available commands.")
        # was: update_output("That is not a valid action. Type 'help' for a list of available commands.", game_output_widget)
        return

    if action == "help":
        handle_help(game_output_widget)
    elif action in ["save", "load"]:
        handle_save_load(action, player, submarine)
    elif action == "quit":
        handle_quit()
    elif action == "setsanity1":
        handle_cheat(action, player)
    # Not sure about this
    elif action == "look":
        handle_look(command, player, submarine)
    elif action == "map":
        handle_map(submarine, player.current_room, game_output_widget)
    elif action == "m":
        if len(command_parts) > 1:
            target_room = int(command_parts[1])
            handle_move(player, target_room, submarine, sfx_volume, game_output_widget)
        else:
            update_output("You need to specify a room number. For example, 'm 3' to move to room 3.")
    elif action in ["t", "u", "d"]:
        if len(command_parts) > 1:
            item_choice = command_parts[1]
            handle_item_interaction(player, item_choice, action, submarine)
        else:
            update_output("You need to specify an item to interact with.")
    elif action == "ta":
        if len(command_parts) > 1:
            npc_name = command_parts[1]
            handle_npc_interaction(player, npc_name, submarine.get_room_content(player.current_room), game_output_widget)
        else:
            update_output("You need to specify an NPC to talk to.", game_output_widget)
    elif action in ["mu", "fx"]:
        handle_sound_control(command, sfx_volume, game_output_widget)
    else:
        update_output("else: update_output: Invalid command. Type 'help' for a list of available commands.")

def splash():
    global splash_title_label, splash_description_text, continue_label
    # Load the splash text from title.py
    game_title = gen["name"] # changed source from tuple due to import error
    game_description = gen["description"]

    # Label widget for ASCII art
    splash_title_label = tk.Label(root, text=game_title, font=("Courier", 18), fg='white', bg='black')
    splash_title_label.pack(pady=5)

    # Text box settings, adjusted so border is "invis"
    splash_description_text = tk.Text(root, wrap=tk.WORD, height=30, width=50, font=("Arial", 20), fg='white', bg='black', bd=0, highlightthickness=0)
    splash_description_text.insert(tk.END, game_description) # insert description
    splash_description_text.config(state=tk.DISABLED)  # Make it read-only
    splash_description_text.pack(pady=10, padx=(80, 20)) # padding for better aesthetics

    # Press Enter to Continue, positioned absolutely at bottom mid
    continue_label = tk.Label(root, text="Press Enter to Continue", font=("Arial", 14, "italic"), fg='white', bg='black')
    continue_label.place(x=400, y=570, anchor="center")

def splash_clear(event=None):
    # hide splashscreen's title lable and text box
    splash_title_label.pack_forget()
    splash_description_text.pack_forget()
    continue_label.pack_forget()

    # unbind Return so it doesn't call splash_clear() again
    root.unbind('<Return>')

    # create frames
    create_main_game_frame()
    bottom_frame()

    global state, submarine_instance, player_instance, sfx_volume
    submarine_instance, player_instance, sfx_volume = initialize_game()

    state = "choose_input"
    update_output("Enter '1' for new game, or '2' to quit")

def create_main_game_frame():
    global game_output, game_status_text_widget
    # Create a main frame for game output
    main_frame = Frame(root, bg='black')
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Print game status info
    game_status_text_widget = tk.Text(main_frame, wrap=tk.WORD, height=10, width=70, font=("Courier New", 20), fg='white', bg='black', bd=5, relief='solid', highlightbackground='#006400', highlightcolor='#006400', highlightthickness=2)
    game_status_text_widget.pack(pady=10, padx=20, fill="both", expand=True)
    game_status_text_widget.config(state=tk.DISABLED)

    # Place game_output in the main frame
    game_output = Text(main_frame, wrap=tk.WORD, height=10, width=70, font=("Courier New", 20), fg='white', bg='black', bd=5, relief='solid', highlightbackground='#006400', highlightcolor='#006400', highlightthickness=2)
    game_output.pack(pady=10, padx=20, fill="both", expand=True)
    game_output.config(state=tk.DISABLED)

    return game_output

def bottom_frame():
    global user_input
    # Create a bottom frame for user input
    bottom_frame = Frame(root, bg='black')
    bottom_frame.pack(pady=5, padx=20, fill="x")
    # Place user_input in the bottom frame
    user_input = tk.Entry(bottom_frame, font=("Courier New", 20), fg='black', bg='white', width=50, bd=0, highlightthickness=0)
    user_input.pack(pady=5, padx=20, fill="x")
    # Place curson in input box
    user_input.focus_set()
    user_input.bind('<Return>', handle_input)

def update_game_state_display(text_widget, player, submarine):
    # Update the output display with the current game state
    global game_status_text_widget

    ## seeing if it resolves none type error for debugging
    if not submarine:
        print("Error: submarine object is not initialized.")
        return
    if not player:
        print("Error: player object is not initialized.")
        return
    
    text_widget.config(state=tk.NORMAL)  # Enable editing
    text_widget.delete("1.0", tk.END)  # Clear current display
    
    print(f"value of submarine is {submarine}") # debug tracking
    adjacent_rooms = submarine.get_adjacent_rooms(player.current_room)
    room_content = submarine.get_room_content(player.current_room)
    
    display_text = "=-=-=-=-=-=-=-=-=Location Data=-=-=-=-=-=-=-=-=\n"
    display_text += f"You are in room {player.current_room}\n"
    display_text += f"Adjacent rooms: {adjacent_rooms}\n\n"
    display_text += "=-=-=-=-=-=-=-=-=Player Data=-=-=-=-=-=-=-=-=\n"
    display_text += f"Your sanity is at {player.sanity}\n\n"
    display_text += "=-=-=-=-=-=-=-=-=Inventory Data=-=-=-=-=-=-=-=-=\n"
    display_text += f"Things in your inventory: {', '.join(player.inventory)}\n"
    
    game_status_text_widget.insert(tk.END, display_text)
    game_status_text_widget.config(state=tk.DISABLED)  # Disable editing after updating

def open_npc_dialogue_window(npc_data):
    dialogue_window = Toplevel(root)
    dialogue_window.grab_set()  # Restrict interaction with the main window
    dialogue_window.title("Talking to Crewmate")
    dialogue_window.configure(bg='black')
    custom_font = ("Courier New", 20)

    prompt_label = Label(dialogue_window, text="(Click a Button to Ask a Question)", 
                         font=("Courier New", 14, "italic"), bg="black", fg="white")
    prompt_label.pack(pady=10)

    # Border attributes
    border_attrs = {
        'bd': 5, 
        'relief': 'solid', 
        'highlightbackground': '#006400', 
        'highlightcolor': '#006400', 
        'highlightthickness': 2
    }

    # Create a single bordered frame for all the questions
    questions_frame = Frame(dialogue_window, bg='black', **border_attrs)
    questions_frame.pack(pady=10, padx=20, fill="both", expand=True)

    for idx, (question_key, question_value) in enumerate(npc_data["dialogue"].items()):
        # Get the related NPC response
        npc_response = npc_data["responses"].get(question_key)
        
        # Print out the data for diagnostic purposes
        print(f"Question Key: {question_key}, NPC Response: {npc_response}")

        question_frame = Frame(questions_frame, bg='black')
        question_frame.pack(pady=5, fill="x")

        button = Button(question_frame, text=f"{idx+1}", 
                        command=lambda resp=npc_response: display_response(resp), width=5)
        button['font'] = custom_font
        button['bg'] = 'white'  # set button bg color
        button['fg'] = 'black'  # set button text color
        button.pack(side="left", padx=(0, 10))

        question_label = Label(question_frame, text=question_value, bg='black', fg='white')  # Set label bg and text color
        question_label['font'] = custom_font
        question_label.pack(side="left", fill="x")

    response_frame = Frame(dialogue_window, bg='black')
    response_frame.pack(pady=20, fill="x", expand=True)

    response_label = Label(response_frame, bg='black', fg='white')  # Set label bg and text color
    response_label['font'] = custom_font
    response_label.pack(pady=10)

    def display_response(response):
        print(f"Displaying Response: {response}")  # Printing the response for diagnostics
        response_label.config(text=response)

    close_button = Button(dialogue_window, text="Close", command=dialogue_window.destroy, bg='white', fg='black')  # Set button bg and text color
    close_button['font'] = custom_font
    close_button.pack(pady=10, side="bottom")

def start_game():
    global state, submarine_instance, player_instance, sfx_volume 
    state = "game_setup" # adding state for debugging
    print("in game_setup state")
    
    submarine_instance, player_instance, sfx_volume = initialize_game()
    update_game_state_display(game_status_text_widget, player_instance, submarine_instance)

def initialize_game():
    """Initializes the game state."""
    submarine = Submarine()
    player = Player()

    # Initialize game audio
    pygame.mixer.init()
    # updated below for unit tests
    current_directory = os.path.dirname(os.path.abspath(__file__))
    music_path = os.path.join(current_directory, 'music.mp3')
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    sfx_volume = 1

    # Populate submarine's rooms with content
    for i in range(len(gamedata['rooms'])):
        npc_data = gamedata['rooms'][i]['content']['npc']
        item_data = gamedata['rooms'][i]['content']['items']
        submarine.place_content(npc_data, i+1)
        submarine.place_content(item_data, i+1)

    return submarine, player, sfx_volume

def initialize_tkinter(): # Initialize Tkinter
    root.title('600 Feet') # title bar
    root.geometry('800x800') # window size
    root.configure(bg='black')  # set window background color to black

############
### HELP ###
############

def show_help():
    help_win = tk.Toplevel(root) # new toplevel window
    help_win.title("HELP")

    help_win.configure(bg="black")

    help_text = """
=-=-Game Commands-=-=
-type 'drop (item)' to drop an item
-type 'look' for descriptions of the rooms
-type 'map' to view a map of the submarine
-type 'move (room #)' to move rooms 
-type 'quit' to exit the game
-type 'take (item name)' to pick up an item
-type 'talk (NPC name)' to talk to an NPC
-type 'use (item name)' to use an item

=-=-Items-=-=
-KEY: Find and take it!
-ADVIL: Use it to regain 5 sanity points!

=-=-Sound Commands-=-=
-type 'music (any number 0-100)' to change the music volume
-type 'fx (any number 0-100)' to change the fx volume

=-=-Save Your Game-=-=
-type 'save'. 
-type 'load' to restore your save 
-NOTE: saves do not carry across sessions
"""

    
    text_widget = tk.Text(
        help_win, 
        wrap=tk.WORD, 
        bg="black", 
        fg="white",  # Text color
        font=("Courier New", 20),
        padx=10,  # Padding to the left/right
        pady=10   # Padding to the top/bottom
    )
    text_widget.insert(tk.END, help_text)
    text_widget.config(state=tk.DISABLED) # read-only
    text_widget.pack(padx=10, pady=10)

    # close bttn
    close_btn = tk.Button(
        help_win, 
        text="Close", 
        command=help_win.destroy, 
        bg="white", 
        fg="black", 
        font=("Courier New", 20)
    )
    close_btn.pack(pady=10)

#####################################
### SAVE, LOAD, & RESET SAVE CODE ###
#####################################

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
        update_output("Your game is saved, but your soul is still lost...")

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
        update_output("Game loaded.")
    except FileNotFoundError:
        update_output("\nNo saved game found.\n")

# SAMMY: need to test and see why they implemented it. does save not overwrite?
def reset_saved_data():
    try:
        os.remove("save_game.json")
        update_output("\nSaved data reset to default.\n")
    except FileNotFoundError:
        update_output("No saved data found.")

################
### MAP CODE ###
################

def display_map(player_current_room):
    map_visual = [
        "                ------>Alan's Quarters[6]<--------------",
        "               |              ^                        |",
        "               |              |                        |",
        "               |              |                        |",
        "               V              V                        V",
        "Connor's Quarters[5]<--->John's Quarters[3]<--->Chad's Quarters[4]",
        "                              |                        ^",
        "                              |                        |",
        "                              |                        |",
        "                              V                        V",
        "                    Supply Room[1](Advil)      Storage Area[2](Key)"
    ]

    # Highlight the player's current room
    for idx, line in enumerate(map_visual):
        if f"[{player_current_room}]" in line:
            map_visual[idx] = line.replace(f"[{player_current_room}]", f"[*YOU* {player_current_room}]")

    for line in map_visual:
        update_output(line)

#################
### LOOK CODE ### 
#################

def display_look(oobject):
    npc = oobject[0]['nameOfNpc']
    items = ' and '.join(oobject[1].keys())

    update_output(f"You look around and see {npc}.\n")
    if len(oobject[1]) > 0:
        update_output(f"You also see {items}.\n")

################
### COMMANDS ###
################

def handle_cheat(command, player):
    if command == "setsanity1":
        player.sanity = 1
        update_output("\n!! CHEAT ACTIVATED !! Sanity set to 1.")

def handle_help(game_output_widget):
    show_help()

""" def handle_help(game_output_widget):
    #clear_screen() -- command broken at moment, not needed since user can scroll up?
    update_output("\n=-=-Game Commands-=-=")
    update_output("-type 'm (room #)' to move rooms ")
    update_output("-type 't (item name)' to pick up an item")
    update_output("-type 'look' to see descriptions of the rooms ")
    update_output("-type 'TA (NPC name)' to talk to an NPC")
    update_output("-type 'quit' at any point to exit the game")
    update_output("-type 'drop (item)' to drop an item")
    update_output("-type 'map' to view a map of the submarine")
    update_output("\n=-=-Items-=-=")
    update_output("-there is a key in this game. find the key and take it")
    update_output("-there is an advil in this game. use the advil to gain 5 sanity points")
    update_output("\n=-=-Sound Commands-=-=")
    update_output("-type music (any number 0-100) to lower or increase the music volume")
    update_output("-type fx (any number 0-100) to lower or increase the fx volume")
    update_output("\n=-=-Save Your Game-=-=")
    update_output("1. type 'save' 2. at any point type 'load' to restore your save 3. NOTE: saves do not currently carry across sessions")
    update_output("you should see your previous game")
    update_output("\n=-=-=-=-=-=-=-=-=\n")
    #press_enter_to_return() -- not needed in GUI """

def handle_item_interaction(player, item_choice, action, submarine):
    if action == "t":
        if submarine.is_item_in_room(item_choice, player.current_room):
            player.add_to_inventory(item_choice)
            submarine.rem_room_content(item_choice, player.current_room)
            update_output(f"You picked up {item_choice}")
        else:
            update_output(f"There is no {item_choice} to pick up.")
    elif action == "u":
        player.use_item(item_choice)
    elif action == "d":
        if item_choice in player.inventory:
            player.remove_from_inventory(item_choice)
            submarine.place_item(item_choice, player.current_room)
            update_output(f"You dropped {item_choice} in the room.")
        else:
            update_output(f"You don't have a {item_choice} to drop.")

def handle_look(command, player, submarine):
    if command == "look":
        room_content = submarine.get_room_content(player.current_room)
        display_look(room_content)

def handle_map(submarine, player_current_room, game_output_widget):
    display_map(player_current_room)

def handle_move(player, target_room, submarine, sfx_volume, game_output_widget):
    adjacent_rooms = submarine.get_adjacent_rooms(player.current_room)
    
    if not target_room:
        update_output("You need to specify a room number. For example, 'm 3' to move to room 3.\n")
        return
    
    if target_room not in adjacent_rooms:
        update_output("You cannot move there.\n")
        return
    
    player.move(target_room)
    # updated below for unit tests
    current_directory = os.path.dirname(os.path.abspath(__file__))
    walk_sound_path = os.path.join(current_directory, 'walk.mp3')
    play_sound(walk_sound_path, sfx_volume)

    if player.sanity == 0:
        reset_saved_data() # why did OG team implement?
        update_output("\n\nAs the weight of unseen horrors and twisted visions press down upon you, you feel your last thread of sanity snap. The depths of the abyss are nothing compared to the chasm that now yawns within your mind. You've lost your grip on reality, and the darkness swallows you whole. You can no longer continue...\n\n")
        ### SAMMY: SET UP FUNCTION OR TRANSITION BACK TO GAME? ###
        update_output("Dread stains your soul as you realize you are caught in a dreadful loop. The cycle of suffering begins anew...")
        start_game()

def handle_npc_interaction(player, npc_name, room_content, game_output_widget):
    npc_data = room_content[0]
    
    if npc_name.lower() == npc_data['nameOfNpc'].lower():
        open_npc_dialogue_window(npc_data)
        
    else:
        update_output(f"You can't talk to {npc_name}")
        update_output(f"Did you mean 'talk {npc_data['nameOfNpc']}'?")

def handle_quit():
    #Add delay?
    update_output("Goodbye...\n")
    sys.exit()

def handle_save_load(command, player, submarine):
    if command == "save":
        save_game(player, submarine)
    elif command == "load":
        load_game(player, submarine)

def handle_sound_control(command, sfx_volume, game_output_widget):
    from functions import check_wanted_vol

    # Split the command into action and arguments
    command_parts = command.lower().split()

    if len(command_parts) < 2:
        update_output("You need to specify a volume level.")
        return

    # Check the desired volume level
    test_vol = check_wanted_vol(command_parts[1])

    if type(test_vol) == type(1) and 0 <= test_vol <= 100:
        set_volume = test_vol / 100

        if command.startswith("mu"):
            pygame.mixer.music.set_volume(0.3 * set_volume)
            update_output("Music volume changed.")
        elif command.startswith("fx"):
            sfx_volume = set_volume
            update_output("Sound effects volume changed.")
    else:
        update_output("That isn't possible.")

#####################
### START PROGRAM ###
#####################
if __name__ == '__main__':
    root = tk.Tk()
    initialize_tkinter()
    splash()
    # referenced by def handle_input()
    state = "splash"
    # Return to continue
    root.bind('<Return>', splash_clear)
    root.mainloop()

