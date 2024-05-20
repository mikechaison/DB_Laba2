import pyodbc
from tkinter import *
from tkinter import messagebox

class Table:
     
    def __init__(self, table_name, table_cols, root):

        # clear the frame
        for widget in root.winfo_children():
            widget.destroy()

        m=len(table_cols)

        # code for creating table
        for i in range(m):
            self.e = Label(root, text=table_cols[i], width=16, font=('Arial',10,'bold'))
            self.e.grid(row=0, column=i, padx=5, pady=2)

        self.e=Button(root, text="+", command=lambda: build_form(table_name, table_cols, root))
        self.e.grid(row=0, column=m)
        

        try:
            connection = pyodbc.connect('Driver={SQL Server};'+
                                        'Server=DESKTOP-3GC3GOK\\SQLEXPRESS;'+
                                        'Database=television_db;'+
                                        'Trusted_Connection=True')
            cursor = connection.cursor()

            cursor.execute("select * from "+table_name)
            i=1
            for data in cursor:
                for j in range(m):
                    self.e = Label(root, text=data[j], width=16,  font=('Arial', 10))
                    self.e.grid(row=i, column=j, padx=5, pady=2)
                self.e = Button(root, text="Update", command=lambda d=data: build_update_form(table_name, table_cols, d, root))
                self.e.grid(row=i, column=m, padx=5, pady=2)
                self.e = Button(root, text="Delete", command=lambda ID=data[0]: delete_object(table_name, table_cols, ID, root))
                self.e.grid(row=i, column=m+1, padx=5, pady=2)
                i+=1
                
                
        except pyodbc.Error as ex:
            messagebox.showerror('Failure', 'Connection failed: '+ex)

class InsertForm:

    def __init__(self, table_name, table_cols, root):
        self.entries=[]

        # clear the frame
        for widget in root.winfo_children():
            widget.destroy()

        # code for creating form
        self.e = Label(root, text='Create new object', font=('Arial',16,'bold'))
        self.e.grid(row=0, column=0, columnspan=2)
        n = len(table_cols)
        
        for i in range(n):
            self.e = Label(root, text=table_cols[i], width=14, font=('Arial',10,'bold'))
            self.e.grid(row=i+1, column=0, padx=5, pady=5)
            self.e = Entry(root, width=14, font=('Arial',10,'bold'))
            self.e.grid(row=i+1, column=1, padx=5, pady=5)
            self.entries.append(self.e)

        self.e = Button(root, text='Back', command=lambda: build_table(table_name, table_cols, root))
        self.e.grid(row=n+1, column=0, padx=5, pady=5)
        self.e = Button(root, text='Create', command=lambda: insert_object(table_name, table_cols, self.entries, root))
        self.e.grid(row=n+1, column=1, padx=5, pady=5)

class UpdateForm:

    def __init__(self, table_name, table_cols, data, root):
        self.entries=[]

        # clear the frame
        for widget in root.winfo_children():
            widget.destroy()

        # code for creating form
        self.e = Label(root, text='Update object', font=('Arial',16,'bold'))
        self.e.grid(row=0, column=0, columnspan=2)
        n = len(table_cols)
        ID=data[0]

        self.e = Label(root, text=table_cols[0], width=14, font=('Arial',10,'bold'))
        self.e.grid(row=1, column=0, padx=5, pady=5)
        self.e = Label(root, text=ID, width=14, font=('Arial',10,'bold'))
        self.e.grid(row=1, column=1, padx=5, pady=5)
        
        for i in range(1, n):
            self.e = Label(root, text=table_cols[i], width=14, font=('Arial',10,'bold'))
            self.e.grid(row=i+1, column=0, padx=5, pady=5)
            self.e = Entry(root, width=14, font=('Arial',10,'bold'))
            self.e.grid(row=i+1, column=1, padx=5, pady=5)
            self.e.insert(END, data[i])
            self.entries.append(self.e)

        self.e = Button(root, text='Back', command=lambda: build_table(table_name, table_cols, root))
        self.e.grid(row=n+1, column=0, padx=5, pady=5)
        self.e = Button(root, text='Update', command=lambda: update_object(table_name, table_cols, self.entries, ID, root))
        self.e.grid(row=n+1, column=1, padx=5, pady=5)


def build_table(table_name, table_cols, root):
    t=Table(table_name, table_cols, root)

def build_form(table_name, table_cols, root):
    f=InsertForm(table_name, table_cols, root)

def build_update_form(table_name, table_cols, data, root):
    f=UpdateForm(table_name, table_cols, data, root)

def insert_object(table_name, table_cols, entries, root):
    data=[]
    for i in entries:
        data.append(i.get())
    
    try:
        connection = pyodbc.connect('Driver={SQL Server};'+
                                    'Server=DESKTOP-3GC3GOK\\SQLEXPRESS;'+
                                    'Database=television_db;'+
                                    'Trusted_Connection=True')
        connection.autocommit = True
        query=f"INSERT INTO {table_name} VALUES ("
        for a in data:
            query+=f"'{a}', "
        query=query[:-2]
        query+=")"
        connection.execute(query)
    except pyodbc.Error as ex:
        messagebox.showerror('Failure', 'Connection failed: '+ex)

    build_table(table_name, table_cols, root)

def update_object(table_name, table_cols, entries, ID, root):
    data=[]
    for i in entries:
        data.append(i.get())
    
    try:
        connection = pyodbc.connect('Driver={SQL Server};'+
                                        'Server=DESKTOP-3GC3GOK\\SQLEXPRESS;'+
                                        'Database=television_db;'+
                                        'Trusted_Connection=True')
        connection.autocommit = True
        query=f"UPDATE {table_name} SET "
        for i in range(len(data)):
            query+=f"{table_cols[i+1]}='{data[i]}', "
        query=query[:-2]
        query+=f" WHERE {table_cols[0]}='{ID}'"
        connection.execute(query)
    except pyodbc.Error as ex:
        messagebox.showerror('Failure', 'Connection failed: '+ex)

    build_table(table_name, table_cols, root)

def delete_object(table_name, table_cols, ID, root):
    try:
        connection = pyodbc.connect('Driver={SQL Server};'+
                                        'Server=DESKTOP-3GC3GOK\\SQLEXPRESS;'+
                                        'Database=television_db;'+
                                        'Trusted_Connection=True')
        connection.autocommit = True
        query=f"DELETE FROM {table_name} WHERE {table_cols[0]}='{ID}'"
        connection.execute(query)
    except pyodbc.Error as ex:
        messagebox.showerror('Failure', 'Connection failed: '+ex)

    build_table(table_name, table_cols, root)

def show_info():
    messagebox.showinfo('Info', 'Лабораторна робота №2 студента 2 курсу групи К-24 Минька Вадима')

root=Tk()
root.title('TV Management System')
root.geometry('1020x720')

tables=['TVchannel', 'TVshow', 'TVhost', 'TVstudio', 'Transmission',
        'TransmissionChannel', 'HostShow', 'StudioShow']

cols=[['channel_number', 'name', 'category', 'country'],
      ['id', 'name', 'category'],
      ['ssn', 'email', 'phone_number', 'first_name', 'second_name', 'BirthDate'],
      ['id', 'viewers', 'chromakey', 'city', 'building', 'floor', 'room'],
      ['id', 'air_day', 'begin_time', 'end_time', 'show_id'],
      ['transmission_id', 'channel_number'],
      ['show_id', 'host_ssn'],
      ['show_id', 'studio_id']]

frtable=Frame(root)
#tables
for i in range(len(tables)):
    print(tables[i], cols[i])
    Button(root, text=tables[i], command=lambda n=i: build_table(tables[n], cols[n], frtable)).grid(row=0, column=i, padx=5, pady=5)

Button(root, text='SQL Queries').grid(row=0, column=8, padx=5, pady=5)
Button(root, text='Info', command=show_info).grid(row=0, column=9, padx=5, pady=5)

frtable.grid(row=1, column=0, columnspan=10)

root.mainloop()
