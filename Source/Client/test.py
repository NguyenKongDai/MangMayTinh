# from tkinter import *

# window = Tk()
# window.title("Welcome to VniTeach app")
# window.geometry('350x200')
# #lbl = Label(window, text="Hello")
# #lbl.grid(column=0, row=0)

# #Thêm một nút nhấn Click Me
# btn = Button(window, text="Click Me", bg="orange", fg="red")

# #Thiết lập vị trí của nút nhấn có màu nền và màu chữ
# btn.grid(column=1, row=0)

# window.mainloop()


import mysql.connector

#establishing the connection
conn = mysql.connector.connect(
   user='root', password='password', host='127.0.0.1', database='mydb'
)

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Dropping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

#Creating table as per requirement
sql ='''CREATE TABLE EMPLOYEE(
   FIRST_NAME CHAR(20) NOT NULL,
   LAST_NAME CHAR(20),
   AGE INT,
   SEX CHAR(1),
   INCOME FLOAT
)'''
cursor.execute(sql)

#Closing the connection
conn.close()