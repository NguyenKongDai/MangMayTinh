from base64 import decode
from ctypes import sizeof
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

import socket
import numpy as np
import json
import os
import threading
from _thread import *

window = tk.Tk()

HOST = '172.20.178.31'  # host để client kết nối
PORT = 12345        # port để client kết nối

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

MEMBER_PATH = 'member.json'
LIVE_CLIENT = []

# Đọc dữ liệu từ file json
def readJsonFile(path):
    with open(path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

# Lấy thông tin rút gọn của các member
def showAllMember(data):
    inforAllMembers = []
    for i in data.keys():

        with open(data[i]["imageDir_small"], "rb") as f:
            image = f.read()
            size = len(image)
            f.close()

        inforAllMembers.append((i, data[i]["fullname"], str(size), image))
    return inforAllMembers

# Gửi dữ liệu của từng member qua client 
def sendInforAllMembers(inforAllMembers, conn):
    for member in inforAllMembers:
        conn.sendall(str("begin").encode('utf8'))

        conn.sendall(str(member[0]).encode('utf8'))
        conn.recv(1024)
        conn.sendall(str(member[1]).encode('utf8'))
        conn.recv(1024)
        conn.sendall(str(member[2]).encode('utf8'))
        conn.recv(1024)
        conn.sendall(member[3])
        conn.recv(1024)

    conn.sendall(str("end").encode('utf8'))

# Tìm kiếm thông tin member bằng ID
def search(data, id):
    inforDetail = []
    for key in data:
        if key == id:
            # infor : [id, fullname, phone, email, sizeSmallImg, SmallImg, sizeBigImg, BigImg]

            inforDetail.append(id)
            inforDetail.append(data[key]['fullname'])
            inforDetail.append(data[key]['phone'])
            inforDetail.append(data[key]['email'])

            with open(data[key]["imageDir_small"], "rb") as f:
                image = f.read()
                size = len(image)
                f.close()

            inforDetail.append(str(size))
            inforDetail.append(image)

            with open(data[key]["imageDir_big"], "rb") as f:
                image = f.read()
                size = len(image)
                f.close()

            inforDetail.append(str(size))
            inforDetail.append(image)

            return inforDetail
    return("False") # Nếu không tìm thấy member

# Gửi thông tin chi tiết của 1 member
def sendInforDetailMember(inforDetailMember, conn):
    if inforDetailMember == "False":
        conn.sendall(str("False").encode('utf8'))       # Nếu member đó không tồn tại
        conn.recv(1024)
    else:
        conn.sendall(str("begin").encode('utf8'))

        conn.sendall(str(inforDetailMember[0]).encode('utf8'))      # id
        conn.recv(1024)
        conn.sendall(str(inforDetailMember[1]).encode('utf8'))      # fullname
        conn.recv(1024)
        conn.sendall(str(inforDetailMember[2]).encode('utf8'))      # phone
        conn.recv(1024)
        conn.sendall(str(inforDetailMember[3]).encode('utf8'))      # email
        conn.recv(1024)
        conn.sendall(str(inforDetailMember[4]).encode('utf8'))      # size Small Img
        conn.recv(1024)
        conn.sendall(inforDetailMember[5])                         # Small Img
        conn.recv(1024)                                         # done 1 img
        conn.sendall(str(inforDetailMember[6]).encode('utf8'))      # size Big Img
        conn.recv(1024)
        conn.sendall(inforDetailMember[7])                          # Big Img
        conn.recv(1024)
        conn.sendall(str("end").encode('utf8'))

# Update các Client đang hoạt động
def showLiveClient():
    showListBox.delete(0, len(LIVE_CLIENT))
    for i in range(len(LIVE_CLIENT)):
        showListBox.insert(0, LIVE_CLIENT[i])

# Nếu Client thoát
def closeConnect(addr, conn):
    for i in range(0, len(LIVE_CLIENT)):
        if LIVE_CLIENT[i] == addr:
            del LIVE_CLIENT[i]
            break
    showLiveClient()

# Xử lí tin nhắn yêu cầu từ client
def readMsg(str_data, data, addr, conn):
    if str_data == "showAllMembers":
        print("showAllMembers")
        inforAllMembers = showAllMember(data)
        sendInforAllMembers(inforAllMembers, conn)
    if str_data == "search":
        print("search")
        id = conn.recv(1024).decode('utf8')
        inforDetail = search(data, id)
        sendInforDetailMember(inforDetail, conn)
    if str_data == "exit":
        print("exit")
        closeConnect(addr, conn)

# kết nối và đọc tin nhắn từ Client
def connect(conn, addr, data):
    try:
        print('Connected by', addr)
        LIVE_CLIENT.append(addr)
        showLiveClient()
        while True:
            data1 = conn.recv(1024)
            str_data = data1.decode("utf8")
            readMsg(str_data, data, addr, conn)

    finally:
        conn.close()

# Chạy server
def runServer():
    try:
        while True:
            conn, addr = s.accept()
            start_new_thread(connect, (conn, addr, data))  
    except KeyboardInterrupt:
        print("Error")
        s.close()
    finally:
        print("end")
        s.close()


def chooseSmall(smallImgInsertEntry):
        ifile = filedialog.askopenfile(mode='rb', title='Choose a file')
        pathSmall = ifile.name
        smallImgInsertEntry = smallImgInsertEntry.insert(0, pathSmall)


def chooseBig(bigImgInsertEntry):
        ifile = filedialog.askopenfile(mode='rb', title='Choose a file')
        pathBig = ifile.name
        bigImgInsertEntry = bigImgInsertEntry.insert(0, pathBig)

def checkID(id):
    for key in data:
        if id == key:
            return("false")
    return("true")

def getInfor(idInsertEntry, fullnameInsertEntry, phoneInsertEntry, emailInsertEntry, smallImgInsertEntry, bigImgInsertEntry):
    id = idInsertEntry.get()
    if checkID(id) == "false":
        messagebox.showinfo('Insert Member', 'ID already exists')
        return

    pathSmallImg = "Image/small" + id + ".jpg"
    pathBigImg = "Image/big" + id + ".jpg"

    with open(smallImgInsertEntry.get(), "rb") as f:
        dataSmallImg = f.read()
        f.close()

    f = open(pathSmallImg, 'wb')
    f.write(dataSmallImg)
    f.close()

    with open(bigImgInsertEntry.get(), "rb") as f:
        dataBigImg = f.read()
        f.close()

    f = open(pathBigImg, 'wb')
    f.write(dataBigImg)
    f.close()

    data[id] = {
        "fullname": fullnameInsertEntry.get(),
        "phone": phoneInsertEntry.get(),
        "email": emailInsertEntry.get(),
        "imageDir_small": pathSmallImg,
        "imageDir_big": pathBigImg
        } 

    messagebox.showinfo('Insert Member', 'Success')

def clearFuncFrame():
    for widget in func_frame.winfo_children():
        widget.destroy()

def funcInsert():

    clearFuncFrame()

    idInsertLabel = tk.Label(func_frame, text = "ID: ")
    idInsertLabel.grid(row=0, column=0)
    idInsertEntry = tk.Entry(func_frame, width = 20)
    idInsertEntry.grid(row=0, column=1)
    
    fullnameInsertLabel = tk.Label(func_frame, text = "Full name: ")
    fullnameInsertLabel.grid(row=1, column=0)
    fullnameInsertEntry = tk.Entry(func_frame, width = 20)
    fullnameInsertEntry.grid(row=1, column=1)

    phoneInsertLabel = tk.Label(func_frame, text = "Phone: ")
    phoneInsertLabel.grid(row=2, column=0)
    phoneInsertEntry = tk.Entry(func_frame, width = 20)
    phoneInsertEntry.grid(row=2, column=1)

    emailInsertLabel = tk.Label(func_frame, text = "Email: ")
    emailInsertLabel.grid(row=3, column=0)
    emailInsertEntry = tk.Entry(func_frame, width = 20)
    emailInsertEntry.grid(row=3, column=1)

    smallImgInsertLabel = tk.Label(func_frame, text = "Path Small Img: ")
    smallImgInsertLabel.grid(row=4, column=0)
    smallImgInsertEntry = tk.Entry(func_frame)
    smallImgInsertEntry.grid(row=4, column=2)
    smallImgInsertButton =  tk.Button(func_frame, text='Browse', command=lambda: chooseSmall(smallImgInsertEntry))
    smallImgInsertButton.grid(row=4, column=1)

    bigImgInsertLabel = tk.Label(func_frame, text = "Path Big Img: ")
    bigImgInsertLabel.grid(row=5, column=0)
    bigImgInsertEntry = tk.Entry(func_frame)
    bigImgInsertEntry.grid(row=5, column=2)
    bigImgInsertButton =  tk.Button(func_frame, text='Browse', command=lambda: chooseBig(bigImgInsertEntry))
    bigImgInsertButton.grid(row=5, column=1)

    doneButton = tk.Button(func_frame, text="Confirm", command=lambda: getInfor(idInsertEntry, 
                                                                            fullnameInsertEntry, 
                                                                            phoneInsertEntry, 
                                                                            emailInsertEntry, 
                                                                            smallImgInsertEntry,
                                                                            bigImgInsertEntry))
    doneButton.grid(row = 6, column= 0)

def closeServer():
    with open(MEMBER_PATH, 'w') as outfile:
        json.dump(data, outfile)
    window.destroy()

window.title('Server')
window.geometry('800x500')
window.resizable(width=True, height=True)

data = readJsonFile(MEMBER_PATH)

main_frame = tk.Frame(master=window)
main_frame.pack()
func_frame = tk.Frame(master=window)
func_frame.pack()

thread = threading.Thread(target = runServer)
thread.deamon = True
thread.start()

showListBox = tk.Listbox(main_frame, width=60, height=10, font=(20))
exitButton = tk.Button(main_frame, text = "Exit", command=closeServer)
insertButton = tk.Button(main_frame, text = "Insert Member", command = funcInsert)


showListBox.pack()
insertButton.pack(pady = 10)
exitButton.pack(pady = 10)
main_frame.tkraise()
window.mainloop()

# def Main():
#     # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # s.bind((HOST, PORT))
#     # s.listen(5)
#     data = readJsonFile(MEMBER_PATH)
#     try:
#         while True:
#             conn, addr = s.accept()
#             print(1)
#             start_new_thread(runServer, (conn, addr, data, liveListBox))  
#     except:
#         s.close()
#     finally:
#         s.close()

    


# if __name__ == '__main__':
#     window = tk.Tk()
#     window.title('Server')
#     window.geometry('800x500')
#     window.resizable(width=True, height=True)
#     liveListBox = Listbox(window,width=60,height=10)
#     liveListBox.pack()
#     Main()
#     window.mainloop()