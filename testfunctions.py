# functions.py

# Define a dictionary to store room descriptions
room_descriptions = {
    "room1": "You are in a dark room with a single door.",
    "room2": "You find yourself in a well-lit library with rows of books.",
    # Add more room descriptions here
}

# Define a dictionary to store item descriptions
item_descriptions = {
    "item1": "A dusty old book lies on a table.",
    "item2": "There's a shiny key on the floor.",
    "item3": "You notice a small vial of mysterious liquid.",
    # Add more item descriptions here
}

# Define a function to look at an item
def look_item(item_name):
    if item_name in item_descriptions:
        return item_descriptions[item_name]
    else:
        return "You don't see that item here."
