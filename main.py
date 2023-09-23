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

# function to clear main window
def clear_main_frame():
    main_frame.delete(1.0, tk.END)

# handle user commands
def handle_input(event):
    global state
    command = user_input.get()
    print(f"Enter key pressed. Command entered: {command}") #debugging
    #functions.process_command(user_command, player_instance, submarine_instance, game_output)
    user_input.delete(0, tk.END)
    #update_game_state_display(player_instance, submarine_instance)

    if state == "splash":
        print("In splash state") # for debugging
        update_output("Choose input 1 or 2")
        state = "choose_input"
    elif state == "choose_input":
        print("In choose_input state") # for debugging
        if command == "1":
            start_game()
        elif command == "2":
            update_output("You chose option 2!")
            sys.exit()
        else:
            update_output("Invalid choice. Please choose 1 or 2.")

def update_output(text):
    global game_output
    # set text to modifiable 
    game_output.config(state='normal')
    game_output.insert(END, text + "\n")
    # disable text area to prevent player editing it
    game_output.config(state='disabled')
    game_output.see(END)

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
    create_bottom_frame()

    global state
    state = "choose_input"
    update_output("Enter '1' for new game, or '2' to quit")

def create_main_game_frame():
    global game_output
    # Create a main frame for game output
    main_frame = Frame(root, bg='black')
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    # Please game_output in the main frame
    game_output = Text(main_frame, wrap=tk.WORD, height=15, width=70, font=("Arial", 20), fg='white', bg='black', bd=0, highlightthickness=0)
    game_output.pack(pady=10, padx=20, fill="both", expand=True)
    game_output.config(state=tk.DISABLED)

    """ ???artifact from previous build to have updated game status????
    game_status_text_widget = tk.Text(main_frame, wrap=tk.WORD, height=15, width=70, font=("Arial", 20), fg='white', bg='black', bd=0, highlightthickness=0)
    game_status_text_widget.pack(pady=10, padx=20, fill="both", expand=True)
    game_status_text_widget.config(state=tk.DISABLED)
    """
    return game_output

""" def main_frame():
    global game_output
    # Create a main frame for game output
    main_frame = Frame(root, bg='black')
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    # Place game_output in the main frame
    game_output = tk.Text(main_frame, wrap=tk.WORD, height=15, width=70, font=("Arial", 20), fg='white', bg='black', bd=0, highlightthickness=0)
    game_output.pack(pady=10, padx=20, fill="both", expand=True)
    game_output.config(state=tk.DISABLED) """

def create_bottom_frame():
    global user_input
    # Create a bottom frame for user input
    bottom_frame = Frame(root, bg='black')
    bottom_frame.pack(pady=10, padx=20, fill="x")
    # Place user_input in the bottom frame
    user_input = Entry(bottom_frame, font=("Arial", 20), fg='black', bg='white', width=50)
    user_input.pack(pady=10, padx=20, fill="x")
    # Place curson in input box
    user_input.focus_set()
    user_input.bind('<Return>', handle_input)

""" def bottom_frame():
    global user_input
    # Create a bottom frame for user input
    bottom_frame = Frame(root, bg='black')
    bottom_frame.pack(pady=10, padx=20, fill="x")
    # Place user_input in the bottom frame
    user_input = tk.Entry(bottom_frame, font=("Arial", 20), fg='black', bg='white', width=50)
    user_input.pack(pady=10, padx=20, fill="x")
    # Place curson in input box
    user_input.focus_set()
    user_input.bind('<Return>', handle_input) """

def update_game_state_display(text_widget, player, submarine):
    """Updates the game display with the current state."""
    text_widget.config(state=tk.NORMAL)  # Enable editing
    text_widget.delete("1.0", tk.END)  # Clear current display
    
    adjacent_rooms = submarine.get_adjacent_rooms(player.current_room)
    room_content = submarine.get_room_content(player.current_room)
    
    display_text = "=-=-=-=-=-=-=-=-=Location Data=-=-=-=-=-=-=-=-=\n"
    display_text += f"You are in room {player.current_room}\n"
    display_text += f"Adjacent rooms: {adjacent_rooms}\n\n"
    display_text += "=-=-=-=-=-=-=-=-=Player Data=-=-=-=-=-=-=-=-=\n"
    display_text += f"Your sanity is at {player.sanity}\n\n"
    display_text += "=-=-=-=-=-=-=-=-=Inventory Data=-=-=-=-=-=-=-=-=\n"
    display_text += f"Things in your inventory: {', '.join(player.inventory)}\n"
    
    text_widget.insert(tk.END, display_text)
    text_widget.config(state=tk.DISABLED)  # Disable editing after updating

# def initialize_interface():
    # Create and configure your Tkinter interface elements here, including the main frame and Text widget.

def start_game():
    submarine, player, sfx_volume = initialize_game()
    #initialize_interface()  # Initialize the Tkinter interface elements - needed?
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

# Initialize Tkinter
root = tk.Tk()
root.title('600 Feet') # title bar
root.geometry('800x600') # window size
root.configure(bg='black')  # set window background color to black

## START THE GAME ##
splash()
# referenced by def handle_input()
state = "splash"
# Return to continue
root.bind('<Return>', splash_clear)
root.mainloop()