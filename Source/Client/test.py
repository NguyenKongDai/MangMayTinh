# import tkinter as tk
# from tkinter import ttk
# from tkinter.messagebox import showinfo

# root = tk.Tk()
# root.title('Treeview demo')
# root.geometry('620x200')

# # define columns
# columns = ('first_name', 'last_name', 'email')

# tree = ttk.Treeview(root, columns=columns, show='headings')

# # define headings
# tree.heading('first_name', text='First Name')
# tree.heading('last_name', text='Last Name')
# tree.heading('email', text='Email')

# # generate sample data
# contacts = []
# for n in range(1, 100):
#     contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

# # add data to the treeview
# for contact in contacts:
#     tree.insert('', tk.END, values=contact)


# # def item_selected(event):
# #     for selected_item in tree.selection():
# #         item = tree.item(selected_item)
# #         record = item['values']
# #         # show a message
# #         showinfo(title='Information', message=','.join(record))


# # tree.bind('<<TreeviewSelect>>', item_selected)

# tree.grid(row=0, column=0, sticky='nsew')

# # add a scrollbar
# scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
# tree.configure(yscroll=scrollbar.set)
# scrollbar.grid(row=0, column=1, sticky='ns')

# # run the app
# root.mainloop()



import tkinter as tk
fields = 'Version', 'Database Name', 'CSV File'

def fetch(entries):
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        print('%s: "%s"' % (field, text))

def callback():
    path = tk.filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, path)

def initUI(root, fields):
    entries = []
    for field in fields:
        if field == 'CSV File':
            frame = tk.Frame(root)
            frame.pack(fill=tk.X)

            lbl = tk.Label(frame, text=field, width=20, anchor='w')
            lbl.pack(side=tk.LEFT, padx=5, pady=5)           

            entry = tk.Entry(frame)
            entry.pack(fill=tk.X, padx=5)

            btn = tk.Button(root, text="Browse", command=callback)
            btn.pack(side=tk.RIGHT,padx=5, pady=5)

            entries.append((field, entry))
        else:
            frame = tk.Frame(root)
            frame.pack(fill=tk.X)

            lbl = tk.Label(frame, text=field, width=20, anchor='w')
            lbl.pack(side=tk.LEFT, padx=5, pady=5)           

            entry = tk.Entry(frame)
            entry.pack(fill=tk.X, padx=5, expand=True)

            entries.append((field, entry))
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Helper")
    entries = initUI(root,fields)
    root.bind('<Return>', (lambda event, e=entries: fetch(e))) 
    frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
    frame.pack(fill=tk.BOTH, expand=True)

    closeButton = tk.Button(root, text="Close", command=root.quit)
    closeButton.pack(side=tk.RIGHT, padx=5, pady=5)
    okButton = tk.Button(root, text="OK", command=(lambda e=entries: fetch(e)))
    okButton.pack(side=tk.RIGHT)
    root.mainloop()  