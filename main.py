""" sammy: next steps, create step by step minimal command running game for POC of tkinter
start from deciding bare necessity functions (world init, parser, handler, world updater, etc) """

import os
#import functions
import sys
import json
import pygame
from tkinter import Tk, Text, Entry, Frame, Button, Scrollbar, END
import tkinter as tk
from title import *

# setting global variables
game_output = None
user_input = None
splash_title_label = None
splash_description_text = None
continue_label = None

# handle user commands
def handle_input(event):
    global state
    command = user_input.get()
    #functions.process_command(user_command, player_instance, submarine_instance, game_output)
    user_input.delete(0, tk.END)
    #update_game_state_display(player_instance, submarine_instance)

    if state == "splash":
        update_output("Choose input 1 or 2")
        state = "choose_input"
    elif state == "choose_input":
        if command == "1":
            update_output("Starting a new game...")
            #functions.start_game()
            splash()
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
    main_frame()
    bottom_frame()

    global state
    state = "choose_input"
    update_output("Enter '1' for new game, or '2' to quit")

def main_frame():
    global game_output
    # Create a main frame for game output
    main_frame = Frame(root, bg='black')
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    # Place game_output in the main frame
    game_output = tk.Text(main_frame, wrap=tk.WORD, height=15, width=70, font=("Arial", 20), fg='white', bg='black', bd=0, highlightthickness=0)
    game_output.pack(pady=10, padx=20, fill="both", expand=True)
    game_output.config(state=tk.DISABLED)

def bottom_frame():
    global user_input
    # Create a bottom frame for user input
    bottom_frame = Frame(root, bg='black')
    bottom_frame.pack(pady=10, padx=20, fill="x")
    # Place user_input in the bottom frame
    user_input = tk.Entry(bottom_frame, font=("Arial", 20), fg='black', bg='white', width=50)
    user_input.pack(pady=10, padx=20, fill="x")
    # Place curson in input box
    user_input.focus_set()
    user_input.bind('<Return>', handle_input)

root = tk.Tk() # main window
root.title('600 Feet') # title bar
root.geometry('800x600') # window size
root.configure(bg='black')  # set window background color to black

splash()

# referenced by def handle_input()
state = "splash"

# Return to continue
root.bind('<Return>', splash_clear)
root.mainloop()