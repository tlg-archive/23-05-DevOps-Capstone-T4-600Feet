import time

def print_description_slowly(description, delay=0.02):     
    for char in description:         
        print(char, end='', flush=True)         
        time.sleep(delay)
