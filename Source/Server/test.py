# Python program to create a close button
# using destroy Non-Class method
from tkinter import *
  
# Creating the tkinter window
root = Tk()
root.geometry("200x100")
  
# Function for closing window
  
  
def Close():
    root.destroy()
  
  
# Button for closing
exit_button = Button(root, text="Exit", command=Close)
exit_button.pack(pady=20)
  
root.mainloop()