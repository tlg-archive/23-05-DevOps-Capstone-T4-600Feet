import tkinter as tk

def clear_screen():
    clear_main_frame() # Updated to TKinter function

def press_enter_to_return():
    print("\nPress Enter to return to the game.")
    while True:
        return_input = input("\n> ").strip().lower()
        if return_input == '':
            clear_screen()
            break
        else:
            print("Invalid input. Press Enter to return to the game.")

def update_main_window(message, text_widget):
    print(f"Updating main window with message: {message}") # debugging
    text_widget.insert(tk.END, message + "\n")
    text_widget.see(tk.END)

# replace every print with function to append text to main window text widget
def update_main_window(message):
    main_text.insert(tk.END, message + "\n")
    main_text.see(tk.END)  # auto-scrolls to the end

def handle_sound_control(command, sfx_volume):
    if command.startswith("mu"):
        test_vol = check_wanted_vol(pair[1])
        if type(test_vol) == type(1) and test_vol in range(0,101):
            set = test_vol/100
            pygame.mixer.music.set_volume(0.3 *set)
        else:
            print("that isnt possible")

    elif command.startswith("fx"):
        test_vol = check_wanted_vol(pair[1])
        if type(test_vol) == type(1) and test_vol in range(0,101):
            sfx_volume = test_vol/100
        print("sound effects volume changed")
