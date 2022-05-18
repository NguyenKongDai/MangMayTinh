from base64 import decode
from ctypes import sizeof
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

import socket
import numpy as np
import json
import os


HOST = '172.20.127.238'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
# count = 0

MEMBER_PATH = 'member.json'

def readJsonFile(path):
    with open(path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def showAllMember(data):
    inforAllMembers = []
    for i in data.keys():

        with open(data[i]["imageDir_small"], "rb") as f:
            image = f.read()
            size = len(image)
            f.close()

        inforAllMembers.append((i, data[i]["fullname"], str(size), image))
    return inforAllMembers
          
def sendInforAllMembers(inforAllMembers):
    for member in inforAllMembers:
        conn.sendall(str("begin").encode('utf8'))

        conn.sendall(str(member[0]).encode('utf8'))
        conn.sendall(str(member[1]).encode('utf8'))
        conn.sendall(str(member[2]).encode('utf8'))
        conn.sendall(member[3])

        conn.recv(1024)

    conn.sendall(str("end").encode('utf8'))

def search(data, id):
    inforDetail = []
    for key in data:
        if key == id:
            inforDetail.append(id)
            inforDetail.append(data[key]['fullname'])
            inforDetail.append(data[key]['phone'])
            inforDetail.append(data[key]['email'])
            inforDetail.append(data[key]['imageDir_small'])
            inforDetail.append(data[key]['imageDir_big'])
            return inforDetail
    return("False")

def sendInforDetailMember(inforDetailMember):
    if inforDetailMember == "False":
        conn.sendall(str("False").encode('utf8'))
    else:
        conn.sendall(str("begin").encode('utf8'))
        for data in inforDetailMember:
            conn.sendall(str(data).encode('utf8'))
        conn.sendall(str("end").encode('utf8'))

def readMsg(str_data, data):
    if str_data == "quit":
        exit
    if str_data == "showAllMembers":
        print("showAllMembers")
        inforAllMembers = showAllMember(data)
        sendInforAllMembers(inforAllMembers)
    if str_data == "search":
        print("search")
        id = conn.recv(1024).decode('utf8')
        inforDetail = search(data, id)
        sendInforDetailMember(inforDetail)
    
    
def runServer(data):
    while True:
        # conn, addr = s.accept()
        try:
            print('Connected by', addr)
            while True:
                data1 = conn.recv(1024)
                str_data = data1.decode("utf8")
                readMsg(str_data, data)

        finally:
            # Clean up the connection
            conn.close()
            # if count == 2: 
            #     break
        s.close() 



# def runServer():
#     while True:
#         conn, addr = s.accept()
#         # count += 1
#         try:
#             print('Connected by', addr)
#             while True:
#                 data = conn.recv(1024)
#                 str_data = data.decode("utf8")
#                 if str_data == "quit":
#                     break
#                 """if not data:
#                     break
#                 """
#                 if str_data == "op1":
#                     data = readJsonFile(MEMBER_PATH)
#                     for i in data.keys():
#                         msg = i + data[i]['phone']
#                         conn.sendall(bytes(msg, "utf8"))
                
#                 print("Client: " + str_data)

#                 # Server send input
#                 msg = input("Server: ")
#                 conn.sendall(bytes(msg, "utf8"))
#         finally:
#             # Clean up the connection
#             conn.close()
#             # if count == 2: 
#             #     break
#         s.close() 




conn, addr = s.accept()
data = readJsonFile(MEMBER_PATH)
runServer(data)
