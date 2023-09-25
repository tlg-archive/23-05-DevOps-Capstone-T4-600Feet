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

def handle_sound_control(command, sfx_volume):
    from functions import check_wanted_vol
    global pair
    if command.startswith("mu"):
        test_vol = check_wanted_vol(pair[1])
        if type(test_vol) == type(1) and test_vol in range(0,101):
            set = test_vol/100
            pygame.mixer.music.set_volume(0.3 *set)
        else:
            update_output("that isnt possible")

    elif command.startswith("fx"):   # <-- Fixed line
        test_vol = check_wanted_vol(pair[1])
        if type(test_vol) == type(1) and test_vol in range(0,101):
            sfx_volume = test_vol/100
        update_output("sound effects volume changed")
