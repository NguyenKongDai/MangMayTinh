from base64 import decode
from ctypes import sizeof
from faulthandler import cancel_dump_traceback_later
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from turtle import width
from PIL import Image, ImageTk

import socket
import json
import os
import threading
from _thread import *

window = tk.Tk()

HOST = 'localhost'  # host để client kết nối
PORT = 12345        # port để client kết nối

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

MEMBER_PATH = 'Database/member.json'
LIVE_CLIENT = []
FM = "utf8"
# Đọc dữ liệu từ file json
def readJsonFile():
    with open(MEMBER_PATH, encoding=FM) as json_file:
        data = json.load(json_file)
    return data

# Lấy thông tin rút gọn của các member
def showAllMember():
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
        conn.sendall(str("begin").encode(FM))
        # member : [id, name, sizeSmallImg, smallImg]
        conn.sendall(str(member[0]).encode(FM))
        conn.recv(1024)
        conn.sendall(str(member[1]).encode(FM))
        conn.recv(1024)
        conn.sendall(str(member[2]).encode(FM))
        conn.recv(1024)
        conn.sendall(member[3])
        conn.recv(1024)

    conn.sendall(str("end").encode(FM))

# Tìm kiếm thông tin member bằng ID
def search(id):
    if len(id) == 0:
        return("False")
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
        conn.sendall(str("False").encode(FM))       # Nếu member đó không tồn tại
        conn.recv(1024)
    else:
        conn.sendall(str("begin").encode(FM))

        conn.sendall(str(inforDetailMember[0]).encode(FM))      # id
        conn.recv(1024)
        conn.sendall(str(inforDetailMember[1]).encode(FM))      # fullname
        conn.recv(1024)
        conn.sendall(str(inforDetailMember[2]).encode(FM))      # phone
        conn.recv(1024)
        conn.sendall(str(inforDetailMember[3]).encode(FM))      # email
        conn.recv(1024)
        conn.sendall(str(inforDetailMember[4]).encode(FM))      # size Small Img
        conn.recv(1024)
        conn.sendall(inforDetailMember[5])                          # Small Img
        conn.recv(1024)                                             # done 1 img
        conn.sendall(str(inforDetailMember[6]).encode(FM))      # size Big Img
        conn.recv(1024)
        conn.sendall(inforDetailMember[7])                          # Big Img
        conn.recv(1024)                                             # done 2 img
        conn.sendall(str("end").encode(FM))

# Update các Client đang hoạt động
def showLiveClient():
    showListBox.delete(0, len(LIVE_CLIENT))
    for i in range(len(LIVE_CLIENT)):
        address = "(\'" + str(LIVE_CLIENT[i][0]) + "\',  " + str(LIVE_CLIENT[i][1]) + ")" 
        showListBox.insert(0, address)

# Nếu Client thoát
def closeConnect(addr, conn):
    conn.close()
    for i in range(0, len(LIVE_CLIENT)):
        if LIVE_CLIENT[i] == addr:
            del LIVE_CLIENT[i]          # Xóa thông tin client
            break
    showLiveClient()                    # update lại list box live client

# kết nối và đọc tin nhắn từ Client
def connect(conn, addr):
    try:
        print('Connected by', addr)
        LIVE_CLIENT.append(addr)                # thêm thông tin client vào list box
        showLiveClient()                        # cập nhập lại list box live client
        while True:                             # đọc các lệnh từ client
            data1 = conn.recv(1024)
            str_data = data1.decode("utf8")
            if str_data == "showAllMembers":
                print("showAllMembers")
                inforAllMembers = showAllMember()
                sendInforAllMembers(inforAllMembers, conn)
            if str_data == "search":
                print("search")
                id = conn.recv(1024).decode(FM)
                inforDetail = search(id)
                sendInforDetailMember(inforDetail, conn)
            # if str_data == "exit":
            if str_data == "exit":
                print("exit")
                closeConnect(addr, conn)
                break
    except:
        closeConnect(addr, conn)
    finally:
        closeConnect(addr, conn)

# Chạy server
def runServer():
    try:
        while True:
            conn, addr = s.accept()                     # chấp nhận kết nối của client
            start_new_thread(connect, (conn, addr))  
    except KeyboardInterrupt:
        print("Error")
        s.close()
    finally:
        print("end")
        s.close()

# lấy đường dẫn ảnh nhỏ
def chooseSmall(smallImgInsertEntry):
        smallImgInsertEntry.delete(0, END)
        ifile = filedialog.askopenfile(mode='rb', title='Choose a image', filetypes=[('image files', ('.png', '.jpg'))])
        pathSmall = ifile.name
        smallImgInsertEntry = smallImgInsertEntry.insert(0, pathSmall)

# lấy đường dẫn ảnh lớn
def chooseBig(bigImgInsertEntry):
        bigImgInsertEntry.delete(0, END)
        ifile = filedialog.askopenfile(mode='rb', title='Choose a image', filetypes=[('image files', ('.png', '.jpg'))])
        pathBig = ifile.name
        bigImgInsertEntry = bigImgInsertEntry.insert(0, pathBig)

# kiểm tra id đã tồn tại chưa
def checkID(id):
    for key in data:
        if id == key:
            return("false")         # đã tồn tại
    return("true")                  # chưa tồn tại

# Lấy thông tin nhập vào server để thêm member
def insertData(idInsertEntry, fullnameInsertEntry, phoneInsertEntry, emailInsertEntry, smallImgInsertEntry, bigImgInsertEntry):
    
    if len(idInsertEntry.get()) ==0 or len(fullnameInsertEntry.get()) == 0 or len(phoneInsertEntry.get()) == 0 or len(emailInsertEntry.get()) == 0 and len(smallImgInsertEntry.get()) == 0 or len(bigImgInsertEntry.get()) == 0:
        messagebox.showinfo('Notice', 'Insert Member: Error data')
        return
    
    id = idInsertEntry.get()
    if checkID(id) == "false":
        messagebox.showinfo('Notice', 'ID already exists')      # không thể có 2 member cùng id
        return

    # tạo đường dẫn để lưu hình nhỏ và lớn khi thêm member
    pathSmallImg = "Image/small" + id + ".jpg"
    pathBigImg = "Image/big" + id + ".jpg"

    # đọc và lưu ảnh nhỏ
    with open(smallImgInsertEntry.get(), "rb") as f:
        dataSmallImg = f.read()
        f.close()
    f = open(pathSmallImg, 'wb')
    f.write(dataSmallImg)
    f.close()
    # đọc và lưu ảnh lớn
    with open(bigImgInsertEntry.get(), "rb") as f:
        dataBigImg = f.read()
        f.close()
    f = open(pathBigImg, 'wb')
    f.write(dataBigImg)
    f.close()
    # thêm member mới vào data
    data[id] = {
        "fullname": fullnameInsertEntry.get(),
        "phone": phoneInsertEntry.get(),
        "email": emailInsertEntry.get(),
        "imageDir_small": pathSmallImg,
        "imageDir_big": pathBigImg
        } 

    messagebox.showinfo('Notice', 'Insert Member: Success')

# làm sạch fram
def clearFuncFrame():
    for widget in func_frame.winfo_children():
        widget.destroy()


# hàm thêm, xuất hiện khi click vào button insert
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
    smallImgInsertEntry.grid(row=4, column=1)
    smallImgInsertButton =  tk.Button(func_frame, text='Browse', command=lambda: chooseSmall(smallImgInsertEntry))
    smallImgInsertButton.grid(row=4, column=2)

    bigImgInsertLabel = tk.Label(func_frame, text = "Path Big Img: ")
    bigImgInsertLabel.grid(row=5, column=0)
    bigImgInsertEntry = tk.Entry(func_frame)
    bigImgInsertEntry.grid(row=5, column=1)
    bigImgInsertButton =  tk.Button(func_frame, text='Browse', command=lambda: chooseBig(bigImgInsertEntry))
    bigImgInsertButton.grid(row=5, column=2)

    doneButton = tk.Button(func_frame, text="Confirm", command=lambda: insertData(idInsertEntry, 
                                                                            fullnameInsertEntry, 
                                                                            phoneInsertEntry, 
                                                                            emailInsertEntry, 
                                                                            smallImgInsertEntry,
                                                                            bigImgInsertEntry))
    doneButton.grid(row = 6, column= 1, pady = 5)
    cancelButton = tk.Button(func_frame, text = "Cancel", command = clearFuncFrame)
    cancelButton.grid(row=6, column=2)

# xóa dữ liệu theo id
def deleteData(idDeleteEntry):
    if len(idDeleteEntry.get()) == 0:
        messagebox.showinfo('Notice', 'Error ID')
        return
    id = idDeleteEntry.get()
    if checkID(id) == "true":
        messagebox.showinfo('Notice', 'ID is not exists')
        return

    pathSmall = data[id]["imageDir_small"]
    pathBig = data[id]["imageDir_big"]

    for key in data:
        if key == id:
            data.pop(key)
            break

    os.remove(pathSmall)
    os.remove(pathBig)

    messagebox.showinfo('Notice', 'Delete Member: Success')

# giao diện của chức năng xóa
def funcDelete():

    clearFuncFrame()

    idDeleteLabel = tk.Label(func_frame, text = "ID to Delete: ")
    idDeleteLabel.grid(row=0, column=0)
    idDeleteEntry = tk.Entry(func_frame, width = 20)
    idDeleteEntry.grid(row=0, column=1)
    doneButton = tk.Button(func_frame, text = 'Confirm', command=lambda: deleteData(idDeleteEntry))
    doneButton.grid(row = 1, column= 1, pady = 5)
    cancelButton = tk.Button(func_frame, text = "Cancel", command = clearFuncFrame)
    cancelButton.grid(row=1, column=2)

# thay đổi thông tin của member
def changeData(id, fullnameChangeEntry, phoneChangeEntry, emailChangeEntry, smallImgChangeEntry, bigImgChangeEntry):
    if len(fullnameChangeEntry.get()) == 0 or len(phoneChangeEntry.get()) == 0 or len(emailChangeEntry.get()) == 0 and len(smallImgChangeEntry.get()) == 0 or len(bigImgChangeEntry.get()) == 0:
        messagebox.showinfo('Notice', 'Change Infor Member: Error data')
        return

    pathSmallImg = "Image/small" + id + ".jpg"
    pathBigImg = "Image/big" + id + ".jpg"

    with open(smallImgChangeEntry.get(), "rb") as f:
        dataSmallImg = f.read()
        f.close()

    f = open(pathSmallImg, 'wb')
    f.write(dataSmallImg)
    f.close()

    with open(bigImgChangeEntry.get(), "rb") as f:
        dataBigImg = f.read()
        f.close()

    f = open(pathBigImg, 'wb')
    f.write(dataBigImg)
    f.close()

    data[id] = {
        "fullname": fullnameChangeEntry.get(),
        "phone": phoneChangeEntry.get(),
        "email": emailChangeEntry.get(),
        "imageDir_small": pathSmallImg,
        "imageDir_big": pathBigImg
        } 

    messagebox.showinfo('Notice', 'Change Infor Member: Success')

# lấy thông tin member theo id, có thể xem và giữ nguyên
def getData(idChangeEntry):
    if (idChangeEntry.get()) == 0:
        messagebox.showinfo('Notice', 'Error ID')
        return
    id = idChangeEntry.get()
    if checkID(id) == "true":
        messagebox.showinfo('Notice', 'ID is not exists')
        return
    idChangeEntry.config(state= "disabled")     # khóa ô nhập id lại
    fullnameChangeLabel = tk.Label(func_frame, text = "Full name: ")
    fullnameChangeLabel.grid(row=2, column=0)
    fullnameChangeEntry = tk.Entry(func_frame, width = 20)
    fullnameChangeEntry.insert(0, data[id]["fullname"])
    fullnameChangeEntry.grid(row=2, column=1)

    phoneChangeLabel = tk.Label(func_frame, text = "Phone: ")
    phoneChangeLabel.grid(row=3, column=0)
    phoneChangeEntry = tk.Entry(func_frame, width = 20)
    phoneChangeEntry.insert(0, data[id]["phone"])
    phoneChangeEntry.grid(row=3, column=1)

    emailChangeLabel = tk.Label(func_frame, text = "Email: ")
    emailChangeLabel.grid(row=4, column=0)
    emailChangeEntry = tk.Entry(func_frame, width = 20)
    emailChangeEntry.insert(0, data[id]["email"])
    emailChangeEntry.grid(row=4, column=1)

    smallImgChangeLabel = tk.Label(func_frame, text = "Path Small Img: ")
    smallImgChangeLabel.grid(row=5, column=0)
    smallImgChangeEntry = tk.Entry(func_frame)
    smallImgChangeEntry.grid(row=5, column=1)
    smallImgChangeButton =  tk.Button(func_frame, text='Browse', command=lambda: chooseSmall(smallImgChangeEntry))
    smallImgChangeEntry.insert(0, data[id]["imageDir_small"])
    smallImgChangeButton.grid(row=5, column=2)

    bigImgChangeLabel = tk.Label(func_frame, text = "Path Big Img: ")
    bigImgChangeLabel.grid(row=6, column=0)
    bigImgChangeEntry = tk.Entry(func_frame)
    bigImgChangeEntry.grid(row=6, column=1)
    bigImgChangeButton =  tk.Button(func_frame, text='Browse', command=lambda: chooseBig(bigImgChangeEntry))
    bigImgChangeEntry.insert(0, data[id]["imageDir_big"])
    bigImgChangeButton.grid(row=6, column=2)

    doneButton = tk.Button(func_frame, text="Confirm", command=lambda: changeData(id, fullnameChangeEntry,
                                                                                phoneChangeEntry, 
                                                                                emailChangeEntry, 
                                                                                smallImgChangeEntry,
                                                                                bigImgChangeEntry))

    doneButton.grid(row = 7, column= 1, pady = 5)
    cancelButton = tk.Button(func_frame, text = "Cancel", command = clearFuncFrame)
    cancelButton.grid(row=7, column=2)

# giao diện tìm kiếm id trước khi thực hiện change
def funcChange():
    clearFuncFrame()
    # tìm kiếm thông tin member theo id
    idChangeLabel = tk.Label(func_frame, text = "ID to Change: ")
    idChangeLabel.grid(row=0, column=0)
    idChangeEntry = tk.Entry(func_frame, width = 20)
    idChangeEntry.grid(row=0, column=1)
    findButton = tk.Button(func_frame, text = 'Find', command=lambda: getData(idChangeEntry))
    findButton.grid(row = 1, column= 0)

# Khi đóng server thì lưu dữ liệu lại file json
def closeServer():
    with open(MEMBER_PATH, 'w', encoding=FM) as outfile:        # gán dữ liệu lại file database
        json.dump(data, outfile, ensure_ascii=False)
    window.destroy()
    s.close()

# code giao diện server
window.protocol('WM_DELETE_WINDOW', closeServer)
window.title('Server')
window.geometry('400x500')
window.resizable(width=True, height=True)

data = readJsonFile()

main_frame = tk.Frame(master=window)
main_frame.pack()
func_frame = tk.Frame(master=window)
func_frame.pack()

# xử lí đa luồng: cho nhiều client kết nối, khởi chạy runServer
thread = threading.Thread(target = runServer)
thread.deamon = True
thread.start()

showLabel = tk.Label(main_frame, text = "Live Client", font=(30))
showListBox = tk.Listbox(main_frame, width=40, height=6, font=(20))
exitButton = tk.Button(main_frame, text = "Exit", command=closeServer)
insertButton = tk.Button(main_frame, text = "Insert Member", command = funcInsert)
deleteButton = tk.Button(main_frame, text = "Delete Member", command = funcDelete)
changeButton = tk.Button(main_frame, text = "Change Member", command = funcChange)

showLabel.pack()
showListBox.pack()
insertButton.pack(pady = (5,0))
deleteButton.pack(pady = (5,0))
changeButton.pack(pady = (5,0))
exitButton.pack(pady = (5,10))
main_frame.tkraise()

window.mainloop()
s.close()