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

# kết nối đến server theo giao thức TCP
HOST = 'localhost'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print('connecting to %s port ' + str(server_address))
s.connect(server_address)

FM = "utf8"


# nhận dữ liệu tất cả các member từ server bằng cách gửi một đoạn mã "showAllMembers" 
def seeAllMembers():
    s.sendall(str("showAllMembers").encode(FM))

    member = []
    members = []
    while True:
        data = s.recv(1024).decode(FM)
        if data == "end":
            break
        # member : [id, name, size Small, Small Img]

        for i in range(0, 2):
            data = s.recv(1024).decode(FM)
            s.sendall(str("done").encode(FM))
            member.append(data)
        
        size = int(s.recv(1024).decode(FM))
        s.sendall(str("done").encode(FM))

        data = s.recv(round((size/1024) + 0.5)*1024)
    
        str_path = "Image/ImageSmall" + member[0] + ".jpg"
        f = open(str_path, 'wb')
        f.write(data)
        f.close()
        s.sendall(str("done").encode(FM))

        members.append(member)          # lưu thông tin rút gọn của member vào mảng members
        member = []   
    return(members)

# get id mà client nhập và gửi qua server để tìm
def search():
    if len(searchEntry.get())==0:
        messagebox.showinfo('Notice', 'ID Error') 
        return
    id = searchEntry.get()
    s.sendall(str("search").encode(FM))
    s.sendall(str(id).encode(FM))
    member = []
    while True:
        data = s.recv(1024).decode(FM)
        if data == "False":
            s.sendall(str(data).encode(FM))
            return("False")                             # không có member nào thõa id
        if data == "end":   
            break
        # member : [id, name, phone, email, size, small img, size, big img]
        # nhận id, fullname, phone, email
        for i in range(0, 4):
            data = s.recv(1024).decode(FM)
            s.sendall(str("done").encode(FM))
            member.append(data)
        
        # nhận size và dữ liệu hình nhỏ
        sizeSmall = int(s.recv(1024).decode(FM))
        s.sendall(str("done").encode(FM))
        dataSmall = s.recv(round((sizeSmall/1024) + 0.5)*1024) 
        s.sendall(str("Done 1").encode(FM))
        str_path = "Image/ImageSmall" + member[0] + ".jpg"
        f = open(str_path, 'wb')
        f.write(dataSmall)
        f.close()
        # nhận size và dữ liệu hình lớn
        sizeBig = int(s.recv(1024).decode(FM))
        s.sendall(str("done").encode(FM))
        dataBig = s.recv(round((sizeBig/1024) + 0.5)*1024) 
        s.sendall(str("Done 2").encode(FM))
        str_path = "Image/ImageBig" + member[0] + ".jpg"
        f = open(str_path, 'wb')
        f.write(dataBig)
        f.close()
        
    return(member)

# làm sạch frame
def clearFrameShow():
    for widget in show_frame.winfo_children():
        widget.destroy()

# giao diện show all members
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

    # show_frame.tkraise()

# giao diện show thông tin chi tiết 1 member
def showMember():
    member = search()
    clearFrameShow()
    if member == "False":
        messagebox.showinfo('Notice', 'Can\'t find member') 
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
        
    # show_frame.tkraise()

# đóng kết nối với server
def closeConnect():
    window.destroy()
    s.sendall(str("exit").encode(FM))       # gửi lệnh cho server biết
    #s.recv(1024)
    


# giao diện của client
window = tk.Tk()
window.protocol('WM_DELETE_WINDOW', closeConnect)

window.title('Client')
window.geometry('600x500')
window.resizable(width=True, height=True)

main_frame = tk.Frame(master=window, height=200)
show_frame = tk.Frame(master=window, height=500)

searchEntry = tk.Entry(main_frame, width = 20)
searchButton = tk.Button(main_frame, text = "Search by ID", command = showMember)
showAllMembers = tk.Button(main_frame, text = "Show All Members", command = showAllMembers)
exitButton = tk.Button(main_frame, text = "Exit", command = closeConnect)

searchEntry.pack(pady=(10,0)) 
searchButton.pack(pady=(5,0))
showAllMembers.pack(pady = (5, 0))
exitButton.pack(pady = 5)

main_frame.pack()
show_frame.pack()

main_frame.tkraise()
window.mainloop()
