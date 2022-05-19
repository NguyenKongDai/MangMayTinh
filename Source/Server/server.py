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
import threading
from _thread import *

HOST = '172.20.178.31'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
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
          
def sendInforAllMembers(inforAllMembers, conn):
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
    return("False")

def sendInforDetailMember(inforDetailMember, conn):
    if inforDetailMember == "False":
        conn.sendall(str("False").encode('utf8'))
        conn.recv(1024)
    else:
        conn.sendall(str("begin").encode('utf8'))

        conn.sendall(str(inforDetailMember[0]).encode('utf8'))      # id
        conn.sendall(str(inforDetailMember[1]).encode('utf8'))      # fullname
        conn.sendall(str(inforDetailMember[2]).encode('utf8'))      # phone
        conn.sendall(str(inforDetailMember[3]).encode('utf8'))      # email
        conn.sendall(str(inforDetailMember[4]).encode('utf8'))      # size Small Img
        conn.sendall(inforDetailMember[5])                         # Small Img
        conn.recv(1024)                                         # done 1 img
        conn.sendall(str(inforDetailMember[6]).encode('utf8'))      # size Big Img
        conn.sendall(inforDetailMember[7])                          # Big Img
        conn.recv(1024)
        conn.sendall(str("end").encode('utf8'))
    
def readMsg(str_data, data, conn):
    if str_data == "quit":
        exit
    if str_data == "showAllMembers":
        print("showAllMembers")
        inforAllMembers = showAllMember(data)
        sendInforAllMembers(inforAllMembers, conn)
    if str_data == "search":
        print("search")
        id = conn.recv(1024).decode('utf8')
        inforDetail = search(data, id)
        sendInforDetailMember(inforDetail, conn)
    
    
def runServer(conn, addr, data):
    while True:
        try:
            print('Connected by', addr)
            while True:
                data1 = conn.recv(1024)
                str_data = data1.decode("utf8")
                readMsg(str_data, data, conn)

        finally:
            # Clean up the connection
            conn.close()
            # if count == 2: 
            #     break
        
def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    data = readJsonFile(MEMBER_PATH)
    try:
        while True:
            conn, addr = s.accept()
            start_new_thread(runServer, (conn, addr, data))  
    except:
        s.close()
    finally:
        s.close()


if __name__ == '__main__':
    Main()