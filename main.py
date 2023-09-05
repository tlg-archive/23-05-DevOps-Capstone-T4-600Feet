import os
from functions import *
from read import *
import sys

os.system("cls" if os.name == 'nt' else 'clear')
print(gen["name"][0])
print_description_slowly(gen["description"]) 

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
	while True:
		player_input = input("Press Enter to start game")
		if player_input == "quit":
			print("Goodbye!")
			exit()

start_menu()
	
