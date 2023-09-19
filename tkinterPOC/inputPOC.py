from tkinter import *

root = Tk()

e = Entry(root, width=50, bg="blue", fg="white", borderwidth="5")
e.pack()
e.get()
e.insert(0, "What is your pet's name?")

def click():
        response = "You need to give a treat to " + e.get() +"!"
        myLabel = Label(root, text=response)
        myLabel.pack()

myButton = Button(root, text="submit", command=click)
myButton.pack()

root.mainloop()
