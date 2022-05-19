#from curses import window
import socket
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter.ttk as exTk
import tkinter as tk
from tkinter import messagebox
from turtle import width
import PIL
from PIL import Image, ImageTk
from matplotlib import image

HOST = '172.20.178.31'  # The server's hostname or IP address
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
        # member : [id, name, Small Img]

        for i in range(0, 2):
            data = s.recv(1024).decode('utf8')
            member.append(data)
        
        size = int(s.recv(1024).decode('utf8'))
        data = s.recv(round((size/1024) + 0.5)*1024)
        str_path = "Image/ImageSmall" + member[0] + ".jpg"
        f = open(str_path, 'wb')
        f.write(data)
        f.close()

        s.sendall(str("Done").encode('utf8'))

        
        members.append(member)
        member = []
    return(members)

def search():
    id = searchEntry.get()
    s.sendall(str("search").encode('utf8'))
    s.sendall(str(id).encode('utf8'))
    member = []
    while True:
        data = s.recv(1024).decode('utf8')
        if data == "False":
            s.sendall(str(data).encode('utf8'))
            return("False")
        if data == "end":   
            break
        # member : [id, name, phone, email, size, small img, size, big img]
        for i in range(0, 4):
            data = s.recv(1024).decode('utf8')
            member.append(data)
        
        sizeSmall = int(s.recv(1024).decode('utf8'))
        dataSmall = s.recv(round((sizeSmall/1024) + 0.5)*1024) 

        str_path = "Image/ImageSmall" + member[0] + ".jpg"
        f = open(str_path, 'wb')
        f.write(dataSmall)
        f.close()

        s.sendall(str("Done 1").encode('utf8'))

        sizeBig = int(s.recv(1024).decode('utf8'))
        dataBig = s.recv(round((sizeBig/1024) + 0.5)*1024) 

        str_path = "Image/ImageBig" + member[0] + ".jpg"
        f = open(str_path, 'wb')
        f.write(dataBig)
        f.close()
        
        s.sendall(str("Done 2").encode('utf8'))

    return(member)

def clearFrameShow():
    for widget in show_frame.winfo_children():
        widget.destroy()

def showAllMembers():
    clearFrameShow()
    # set height row

    s = ttk.Style()
    s.configure('Treeview', rowheight=60)

    tree = ttk.Treeview(show_frame, column = ('ID', 'Name'), selectmode='none', height=5)
    tree.grid(row=0, column=0, sticky='nsew')

    tree.heading('#0', text = 'Avatar', anchor='center')
    tree.heading('#1', text = 'ID', anchor='center')
    tree.heading('#2', text = 'Full Name', anchor='center')

    tree.column('#0', anchor='center', width=100)
    tree.column('ID', anchor='center', width=100)
    tree.column('Name', anchor='center', width=200)

    members = seeAllMembers()
    n = len(members)
    images = []

    for i in range(0, n):
        path = 'Image/ImageSmall' + members[i][0] + '.jpg'
        img = Image.open(path) #change to your file path
        resized = img.resize((50, 50), Image.ANTIALIAS)
        imgTk = ImageTk.PhotoImage(resized)
        images.append(imgTk)

    for i in range(0, n):
        tree.insert('', 'end', image = images[i],
                            value=(members[i][0], members[i][1]))
        tree.image = images

    scrollbar = ttk.Scrollbar(show_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky='ns')

    show_frame.tkraise()

def showMember():
    member = search()
    clearFrameShow()
    if member == "False":
        fail = tk.Label(show_frame, text="Can't find member")
        fail.grid(row=0, column=0)
    else:
        s = ttk.Style()
        s.configure('Treeview', rowheight=60)

        tree = ttk.Treeview(show_frame, column = ( 'ID', 'Name', 'Phone', 'Email'), selectmode = 'none',height = 1)
        tree.grid(row=0, column=0, sticky='nsew')

        tree.heading('#0', text = 'Avatar', anchor='center')
        tree.heading('#1', text = 'ID', anchor='center')
        tree.heading('#2', text = 'Full Name', anchor='center')
        tree.heading('#3', text = 'Phone', anchor='center')
        tree.heading('#4', text = 'Email', anchor='center')
        
        tree.column('#0', anchor='center', width=100)
        tree.column('ID', anchor='center', width=50)
        tree.column('Name', anchor='center', width=150)
        tree.column('Phone', anchor='center', width=100)
        tree.column('Email', anchor='center', width=150)

        pathSmall = 'Image/ImageSmall' + member[0] + '.jpg'
        imgSmall = Image.open(pathSmall) #change to your file path
        resizedSmall = imgSmall.resize((50, 50), Image.ANTIALIAS)
        imgTkSmall = ImageTk.PhotoImage(resizedSmall)

        pathBig = 'Image/ImageBig' + member[0] + '.jpg'
        imgBig = Image.open(pathBig) 
        resizedBig = imgBig.resize((200, 150), Image.ANTIALIAS)
        imgTkBig = ImageTk.PhotoImage(resizedBig)
        
        bigImgLabel = tk.Label(show_frame, image = imgTkBig)
        bigImgLabel.image = imgTkBig
        bigImgLabel.grid(row=0, column=0)

        tree.insert('', 'end', image = imgTkSmall,
                            value=(member[0], member[1], member[2], member[3]))
        tree.image = imgTkSmall

        
        tree.grid(row=1, column=0)
        
    show_frame.tkraise()

window = tk.Tk()

window.title('Client')
window.geometry('800x500')
window.resizable(width=True, height=True)

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

