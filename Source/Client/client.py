#from curses import window
import socket
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter.ttk as exTk
import tkinter as tk

HOST = '10.0.29.36'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print('connecting to %s port ' + str(server_address))
s.connect(server_address)

def seeAllMembers():
    msg = "op1"
    s.sendall(bytes(msg, "utf8"))

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

root = tk.Tk()
def showMenu():
    root.title("Client")
    root.geometry('250x150+300+300')
    opt1 = Button(root, text = "Show All Members", command = seeAllMembers())
    opt1.grid(column=1, row=0)
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


showMenu()