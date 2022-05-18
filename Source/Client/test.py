import tkinter as tk
from tkinter import ttk
from PIL import ImageTk as itk
import PIL.Image
import io

s= tk.Tk()
s.title('No *£/**@#* image showing')
s.geometry('400x400')

s.rowconfigure(1, weight = 1)

s.columnconfigure(1,weight=1)

headings=['Image']

p = 'Image001.jpg'
img1 = PIL.Image.open('Image001.jpg')
#img1 = img1.resize((10,10))
img = itk.PhotoImage(img1)

tree = ttk.Treeview(s)
tree.grid(column=1,row=1,sticky='NSEW')
tree['columns']=headings
tree['show']='headings'
for i in headings:
    tree.heading(i,text=i)
    
tree.column(0, width=125,stretch=True)
#tree.column(1, width=125,stretch=True)

tree.insert('','end','0', open =True, image= img)
tree.image = img

s.mainloop()