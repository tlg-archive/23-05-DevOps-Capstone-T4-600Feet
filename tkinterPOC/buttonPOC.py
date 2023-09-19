from tkinter import *

root = Tk()

def dots():
    myLabel = Label(root, text="-50 DKP!")
    myLabel.pack()

# creating a button
myButton = Button(root, fg="blue", bg="black", text="MOAR DOTS!", padx=50, command=dots).pack()

# loop for program
root.mainloop()