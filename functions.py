import time

def print_description_slowly(description, delay=0.02):     
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
        print("this is where game logic would go")
        player_input = input("placeholder to stop infinite loop").lower()
        if player_input == "quit":
            print("Goodbye!")
            exit()

#def play_game(user_start):
#    return 1
