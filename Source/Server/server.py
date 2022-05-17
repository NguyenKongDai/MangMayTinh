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
import sys

HOST = '10.0.29.36'  # Standard loopback interface address (localhost)
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
    inforAllMember = []
    for i in data.keys():
        inforAllMember.append((i, data[i]["fullname"]))
    return inforAllMember

def sendMsg(data):
    #conn.sendall(bytes(data, "utf8"))
    conn.sendall(bytes(data), decode='utf8')

def readMsg(str_data, data):
    if str_data == "quit":
        exit
    if str_data == "op1":
        inforAllMember = showAllMember(data)
    
    sendMsg(inforAllMember)
    
    
def runServer(data):
    while True:
        # conn, addr = s.accept()
        try:
            print('Connected by', addr)
            while True:
                data1 = conn.recv(1024)
                str_data = data1.decode("utf8")
                # if str_data == "quit":
                #     break
                # """if not data:
                #     break
                # """
                # if str_data == "op1":
                #     data = readJsonFile(MEMBER_PATH)
                #     for i in data.keys():
                #         msg = i + data[i]['phone']
                #         conn.sendall(bytes(msg, "utf8"))
                
                # print("Client: " + str_data)

                # # Server send input
                # msg = input("Server: ")
                # conn.sendall(bytes(msg, "utf8"))
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
