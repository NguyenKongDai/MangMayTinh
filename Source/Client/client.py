#from curses import window
import socket
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter.ttk as exTk
import tkinter as tk
from tkinter import messagebox

HOST = '10.0.29.36'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print('connecting to %s port ' + str(server_address))
s.connect(server_address)

def seeAllMembers():
    #msg = "showAllMembers"
    s.sendall(str("showAllMembers").encode('utf8'))

    member = []
    members = []
    while True:
        data = s.recv(1024).decode('utf8')
        #print(data)
        if data == "end":
            break
        # member : [id, name]
        for i in range(0, 2):
            data = s.recv(1024).decode('utf8')
            member.append(data)

        members.append(member)
        member = []

    n = len(members)
    for i in range(0, n):
        print(members[i])

def search():
    id = searchEntry.get()
    #msg = "searchID"
    s.sendall(str("search").encode('utf8'))
    print(id)
    #msg = id
    s.sendall(str(id).encode('utf8'))

    while True:
        data = s.recv(1024).decode('utf8')
        if data == "False":
            print("Don't find member")
            break
        if data == "end":   
            break
        # member : [id, name, phone, email, small img, big img]
        member = []
        for i in range(0, 6):
            data = s.recv(1024).decode('utf8')
            member.append(data)
    
    print(member)


root = tk.Tk()
#def showMenu():
root.title("Client")
root.geometry('500x300')

searchEntry = Entry(root, width = 20)
searchEntry.grid(column=1, row=0)
searchEntry.focus()

searchButton = Button(root, text = "Search by ID", command=lambda: search())
searchButton.grid(column=2, row=0)

showAllMembers = Button(root, text = "Show All Members", command = seeAllMembers)
showAllMembers.grid(column=1, row=1)
root.mainloop()





# try:
#     while True:
#         msg = input('Client: ')
#         s.sendall(bytes(msg, "utf8"))

#         if msg == "quit":
#             break

#         data = s.recv(1024)
#         print('Server: ', data.decode("utf8"))
# finally:
#     print('closing socket')
#     s.close()

