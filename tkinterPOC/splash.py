import tkinter as tk
from back import *

def start_game(event=None):
    splash_title_label.pack_forget()
    splash_description_text.pack_forget()
    setup_game()

def setup_game():
    game_label = tk.Label(root, text='TRANSITION TO MAIN GAME HERE', fg='white', bg='black')
    game_label.pack(expand=True, fill=tk.BOTH)

root = tk.Tk()
root.title('600 Feet') # title bar
root.geometry('800x600') # window size
root.configure(bg='black')  # set window background color to black

# Load the splash text from back.py
game_title = gen["name"] # changed source from tuple due to import error
game_description = gen["description"]

splash_title_label = tk.Label(root, text=game_title, font=("Courier", 14), fg='white', bg='black')
splash_title_label.pack(pady=20)
#Text box settings adjusted so border is "invis"
splash_description_text = tk.Text(root, wrap=tk.WORD, height=30, width=40, font=("Arial", 18), fg='white', bg='black', bd=0, highlightthickness=0)
splash_description_text.insert(tk.END, game_description)
splash_description_text.config(state=tk.DISABLED)  # Make it read-only
splash_description_text.pack(pady=20, padx=(60, 20))

#Return to continue into game
root.bind('<Return>', start_game)
root.mainloop()
