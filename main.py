""" working thru: 
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/tkinter/__init__.py", line 1921, in __call__
    return self.func(*args)
  File "/Users/stamimi/Capstone-T4-600Feet/main.py", line 42, in handle_input
    update_game_state_display(game_status_text_widget, player_instance, submarine_instance)
  File "/Users/stamimi/Capstone-T4-600Feet/main.py", line 189, in update_game_state_display
    adjacent_rooms = submarine.get_adjacent_rooms(player.current_room)
AttributeError: 'NoneType' object has no attribute 'get_adjacent_rooms'
 """

import os
#import functions
import sys
import json
import pygame
import tkinter as tk
from tkinter import Tk, Text, Entry, Frame, Button, Scrollbar, END
from title import *
from functions import Submarine, Player, gamedata
from common import clear_screen, press_enter_to_return, update_main_window, handle_sound_control

# setting global variables
game_output = None
user_input = None
splash_title_label = None
splash_description_text = None
continue_label = None
game_status_text_widget = None
player_instance = None
submarine_instance = None
game_output = None 
sfx_volume = None

# function to clear main window
def clear_main_frame():
    main_frame.delete(1.0, tk.END)

# handle user commands
def handle_input(event):
    # added player_instance, submarine_instance, sfx_volume due to "not defined" errors
    global state, submarine_instance, player_instance, sfx_volume
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
    
    # Process the command and update the GUI text widget
    process_command(command)

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
    action = command_parts[0]

    if action == "help":
        handle_game_help(game_output_widget)
    elif action in ["save", "load"]:
        handle_save_load(action, player, submarine)
    elif action == "quit":
        handle_game_quit()
    elif action == "setsanity1":
        handle_game_cheats(action, player)
    elif action == "map":
        handle_map_display(submarine, player.current_room, game_output_widget)
    elif action == "m":
        if len(command_parts) > 1:
            target_room = int(command_parts[1])
            handle_player_movement(player, target_room, submarine, sfx_volume, game_output_widget)
        else:
            update_output("You need to specify a room number. For example, 'm 3' to move to room 3.", game_output_widget)
    elif action in ["take", "use", "drop"]:
        if len(command_parts) > 1:
            item_choice = command_parts[1]
            handle_item_interaction(player, item_choice, action, submarine, game_output_widget)
        else:
            update_output("You need to specify an item to interact with.", game_output_widget)
    elif action == "ta":
        if len(command_parts) > 1:
            npc_name = command_parts[1]
            handle_npc_interaction(player, npc_name, submarine.get_room_content(player.current_room), game_output_widget)
        else:
            update_output("You need to specify an NPC to talk to.", game_output_widget)
    elif action in ["mu", "fx"]:
        handle_sound_control(command, sfx_volume)
    #SAMMY: remarking to test -game_output to fix bug
    #else:
        #update_output("Invalid command. Type 'help' for a list of available commands.", game_output_widget)
    else:
        update_output("Invalid command. Type 'help' for a list of available commands.")

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

    global state
    state = "choose_input"
    update_output("Enter '1' for new game, or '2' to quit")

def create_main_game_frame():
    global game_output, game_status_text_widget
    # Create a main frame for game output
    main_frame = Frame(root, bg='blue')
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Print game status info
    # SAMMY: LIMITED TO 10 FOR NOW BUT CAN BE ADJUSTED
    game_status_text_widget = tk.Text(main_frame, wrap=tk.WORD, height=10, width=70, font=("Arial", 20), fg='white', bg='black', bd=0, highlightthickness=0)
    game_status_text_widget.pack(pady=10, padx=20, fill="both", expand=True)
    game_status_text_widget.config(state=tk.DISABLED)

    # Place game_output in the main frame
    # SAMMY: LIMITED TO 5 FOR NOW BUT CAN BE ADJUSTED
    game_output = Text(main_frame, wrap=tk.WORD, height=5, width=70, font=("Arial", 20), fg='white', bg='black', bd=0, highlightthickness=0)
    game_output.pack(pady=10, padx=20, fill="both", expand=True)
    game_output.config(state=tk.DISABLED)

    return game_output

def bottom_frame():
    global user_input
    # Create a bottom frame for user input
    bottom_frame = Frame(root, bg='red')
    bottom_frame.pack(pady=10, padx=20, fill="x")
    # Place user_input in the bottom frame
    user_input = tk.Entry(bottom_frame, font=("Arial", 20), fg='black', bg='white', width=50)
    user_input.pack(pady=10, padx=20, fill="x")
    # Place curson in input box
    user_input.focus_set()
    user_input.bind('<Return>', handle_input)

def update_game_state_display(text_widget, player, submarine):
    # Update the output display with the current game state
    global game_status_text_widget
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

def start_game():
    global state, submarine_instance, player_instance, sfx_volume 
    #state = "game_state" 
    state = "game_setup" # adding state for debugging
    submarine, player, sfx_volume, submarine_instance, player_instance, sfx_volume = initialize_game()
    update_game_state_display(game_status_text_widget, player, submarine)  # Display initial game status

def initialize_game():
    """Initializes the game state."""
    submarine = Submarine()
    player = Player()

    # Initialize game audio
    pygame.mixer.init()
    pygame.mixer.music.load('music.mp3')
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
    root.geometry('800x600') # window size
    root.configure(bg='black')  # set window background color to black

## START PROGRAM ##
root = tk.Tk()
initialize_tkinter()
splash()
# referenced by def handle_input()
state = "splash"
# Return to continue
root.bind('<Return>', splash_clear)
root.mainloop()