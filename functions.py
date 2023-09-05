import time

'''def slow_print(sentence):
    for char in sentence:
        print(char, end='')
        time.sleep(.05)'''

def print_description_slowly(description, delay=0.02):     
    for char in description:         
        print(char, end='', flush=True)         
        time.sleep(delay)
