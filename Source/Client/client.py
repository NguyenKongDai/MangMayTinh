#from curses import window
import socket
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter.ttk as exTk
import tkinter as tk
from tkinter import messagebox
from turtle import width

HOST = '10.0.29.36'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print('connecting to %s port ' + str(server_address))
s.connect(server_address)

def seeAllMembers():
    s.sendall(str("showAllMembers").encode('utf8'))

    member = []
    members = []
    while True:
        data = s.recv(1024).decode('utf8')
        if data == "end":
            break
        # member : [id, name]
        for i in range(0, 2):
            data = s.recv(1024).decode('utf8')
            member.append(data)

        members.append(member)
        member = []
    return(members)

def search():
    id = searchEntry.get()
    s.sendall(str("search").encode('utf8'))
    s.sendall(str(id).encode('utf8'))

    while True:
        data = s.recv(1024).decode('utf8')
        if data == "False":
            return("False")
            break
        if data == "end":   
            break
        # member : [id, name, phone, email, small img, big img]
        member = []
        for i in range(0, 6):
            data = s.recv(1024).decode('utf8')
            member.append(data)
    return(member)

def showAllMembers():

    tree = ttk.Treeview(show_frame, column = ( 'ID', 'Name'), show='headings',height=15)
    # tree.heading('Small Img', text = 'Avatar')
    # tree.column('Small Img', width=100)
    tree.heading('ID', text = 'ID')
    tree.column('ID', width=50)
    tree.heading('Name', text = 'Full Name')

    contacts = []
    members = seeAllMembers()
    n = len(members)
    for i in range(0, n):
        contacts.append(members[i])
    for contact in contacts:
        tree.insert('', tk.END, values=contact)

    scrollbar = ttk.Scrollbar(show_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky='ns')

    show_frame.tkraise()

def showMember():
    tree = ttk.Treeview(show_frame, column = ( 'ID', 'Name', 'Phone', 'Email', 'Avatar', 'Cover'), show='headings',height=5)
    # tree.heading('Small Img', text = 'Avatar')
    # tree.column('Small Img', width=100)
    tree.heading('ID', text = 'ID')
    tree.column('ID', width=50)
    tree.heading('Name', text = 'Full Name')
    tree.heading('Phone', text = 'Phone')
    tree.heading('Email', text = 'Email')
    tree.heading('Avatar', text = 'Avatar')
    tree.heading('Cover', text = 'Cover')

    contacts = []
    member = search()
    if member == "False":
        fail = tk.Label(show_frame, text="Can't find member")
    else:
        for n in range(0, 1):
            contacts.append(member)
        for contact in contacts:
            tree.insert('', tk.END, values=contact)

        tree.grid(row=0, column=0)

    show_frame.tkraise()




window = tk.Tk()

window.title('Client')
window.geometry('500x500')
window.resizable(width=False, height=True)

main_frame = tk.Frame(master=window, height=200)
show_frame = tk.Frame(master=window, height=500)

searchEntry = tk.Entry(main_frame, width = 20)
searchButton = tk.Button(main_frame, text = "Search by ID", command = showMember)
showAllMembers = tk.Button(main_frame, text = "Show All Members", command = showAllMembers)

searchEntry.pack(pady=(10,0)) 
searchButton.pack(pady=(3,5))
showAllMembers.pack(pady = 10)

main_frame.pack()
show_frame.pack()

main_frame.tkraise()
#show_frame.tkraise()

# searchEntry = tk.Entry(window)
# searchButton = tk.Button(window, text = "Search by ID")

# showAllMembers = tk.Button(window, text = "Show All Members")

# searchEntry.pack()
# searchButton.pack()
# showAllMembers.pack()

window.mainloop()

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

