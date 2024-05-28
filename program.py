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

            update_scrollable_region()
            
        except pyodbc.Error as ex:
            messagebox.showerror('Failure', 'Connection failed: '+str(ex))

class QueryTable:
     
    def __init__(self, table_cols, query, root):

        # clear the frame
        for widget in root.winfo_children():
            widget.destroy()

        m=len(table_cols)

        # code for creating table
        for i in range(m):
            self.e = Label(root, text=table_cols[i], width=16, font=('Arial',10,'bold'))
            self.e.grid(row=0, column=i, padx=5, pady=2)

        self.e=Button(root, text="Back", command=lambda: show_queries())
        self.e.grid(row=0, column=m)

        try:
            connection = pyodbc.connect('Driver={SQL Server};'+
                                        'Server=DESKTOP-3GC3GOK\\SQLEXPRESS;'+
                                        'Database=television_db;'+
                                        'Trusted_Connection=True')
            cursor = connection.cursor()
            cursor.execute(query)
            i=1
            for data in cursor:
                for j in range(m):
                    self.e = Label(root, text=data[j], width=16,  font=('Arial', 10))
                    self.e.grid(row=i, column=j, padx=5, pady=2)
                i+=1

        except pyodbc.Error as ex:
            messagebox.showerror('Failure', 'Connection failed: '+str(ex))

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

class QueryForm:

    def __init__(self, root):

        # clear the frame
        for widget in root.winfo_children():
            widget.destroy()

        #Simple queries

        self.e = Label(root, text='Simple queries', font=('Arial',24,'bold'))
        self.e.grid(row=0, column=0, columnspan=5,padx=5,pady=2)

        self.e = Label(root, width=40, text='Find TV channels from the country of', font=('Arial',10,'bold'))
        self.e.grid(row=1, column=0,padx=5,pady=2)
        self.e11 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e11.grid(row=1, column=1,padx=5,pady=2)
        self.e = Button(root, width=10, text='Search',
                        command=lambda n=0, e1=self.e11: search_objects(query_cols[n], queries[n].format(e1.get()), root))
        self.e.grid(row=1, column = 4,padx=5,pady=2)

        self.e = Label(root, width=40, text='Find TV shows which will be on air on', font=('Arial',10,'bold'))
        self.e.grid(row=2, column=0,padx=5,pady=2)
        self.e21 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e21.grid(row=2, column=1,padx=5,pady=2)
        self.e = Button(root, width=10, text='Search',
                        command=lambda n=1, e1=self.e21: search_objects(query_cols[n], queries[n].format(e1.get()), root))
        self.e.grid(row=2, column = 4,padx=5,pady=2)

        self.e = Label(root, width=40, text='Find TV studios used by TV show', font=('Arial',10,'bold'))
        self.e.grid(row=3, column=0,padx=5,pady=2)
        self.e31 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e31.grid(row=3, column=1,padx=5,pady=2)
        self.e = Button(root, width=10, text='Search',
                        command=lambda n=2, e1=self.e31: search_objects(query_cols[n], queries[n].format(e1.get()), root))
        self.e.grid(row=3, column = 4,padx=5,pady=2)

        self.e = Label(root, width=40, text='Find TV shows hosted by', font=('Arial',10,'bold'))
        self.e.grid(row=4, column=0,padx=5,pady=2)
        self.e41 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e41.grid(row=4, column=1,padx=5,pady=2)
        self.e42 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e42.grid(row=4, column=2,padx=5,pady=2)
        self.e = Button(root, width=10, text='Search',
                        command=lambda n=3, e1=self.e41, e2=self.e42: search_objects(query_cols[n], queries[n].format(e1.get(), e2.get()), root))
        self.e.grid(row=4, column = 4,padx=5,pady=2)

        self.e = Label(root, width=40, text='Find TV hosts who host shows of category', font=('Arial',10,'bold'))
        self.e.grid(row=5, column=0,padx=5,pady=2)
        self.e51 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e51.grid(row=5, column=1,padx=5,pady=2)
        self.e = Label(root, width=25, text='and whose phone number is', font=('Arial',10,'bold'))
        self.e.grid(row=5, column=2,padx=5,pady=2)
        self.e52 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e52.grid(row=5, column=3,padx=5,pady=2)
        self.e = Button(root, width=10, text='Search',
                        command=lambda n=4, e1=self.e51, e2=self.e52: search_objects(query_cols[n], queries[n].format(e1.get(), e2.get()), root))
        self.e.grid(row=5, column = 4,padx=5,pady=2)

        #Complex queries

        self.e = Label(root, text='Complex queries', font=('Arial',24,'bold'))
        self.e.grid(row=6, column=0, columnspan=5,padx=5,pady=2)

        self.e = Label(root, width=40, text='Find TV hosts who host shows only of category', font=('Arial',10,'bold'))
        self.e.grid(row=7, column=0,padx=5,pady=2)
        self.e61 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e61.grid(row=7, column=1,padx=5,pady=2)
        self.e = Button(root, width=10, text='Search',
                        command=lambda n=5, e1=self.e61: search_objects(query_cols[n], queries[n].format(e1.get()), root))
        self.e.grid(row=7, column = 4,padx=5,pady=2)

        self.e = Label(root, width=40, text='Find how many TV shows are held by only', font=('Arial',10,'bold'))
        self.e.grid(row=8, column=0,padx=5,pady=2)
        self.e71 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e71.grid(row=8, column=1,padx=5,pady=2)
        self.e72 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e72.grid(row=8, column=2,padx=5,pady=2)
        self.e = Button(root, width=10, text='Search',
                        command=lambda n=6, e1=self.e71, e2=self.e72: search_objects(query_cols[n], queries[n].format(e1.get(), e2.get()), root))
        self.e.grid(row=8, column = 4,padx=5,pady=2)

        self.e = Label(root, width=40, text='Find TV shows who are hosted by all named', font=('Arial',10,'bold'))
        self.e.grid(row=9, column=0,padx=5,pady=2)
        self.e81 = Entry(root, width=20, font=('Arial',10,'bold'))
        self.e81.grid(row=9, column=1,padx=5,pady=2)
        self.e = Label(root, width=15, text='and someone else', font=('Arial',10,'bold'))
        self.e.grid(row=9, column=2,padx=5,pady=2)
        self.e = Button(root, width=10, text='Search',
                        command=lambda n=7, e1=self.e81: search_objects(query_cols[n], queries[n].format(e1.get()), root))
        self.e.grid(row=9, column = 4,padx=5,pady=2)


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
        messagebox.showerror('Failure', 'Connection failed: '+str(ex))

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
        messagebox.showerror('Failure', 'Connection failed: '+str(ex))

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
        messagebox.showerror('Failure', 'Connection failed: '+str(ex))

    build_table(table_name, table_cols, root)

def show_info():
    messagebox.showinfo('Info', 'Лабораторна робота №2 студента 2 курсу групи К-24 Минька Вадима')

def show_queries():
    global frtable
    q=QueryForm(frtable)

def search_objects(table_cols, query, root):
    qt=QueryTable(table_cols, query, root)
    

root=Tk()
root.title('TV Management System')
root.geometry('1024x720')

tables=['TVchannel', 'TVshow', 'TVhost', 'TVstudio', 'Transmission',
        'TransmissionChannel', 'HostShow', 'StudioShow']

cols=[['channel_number', 'name', 'category', 'country'],
      ['id', 'name', 'category'],
      ['ssn', 'email', 'phone_number', 'first_name', 'second_name', 'BirthDate'],
      ['id', 'viewers', 'chromakey', 'city', 'building', 'room'],
      ['id', 'air_day', 'begin_time', 'end_time', 'show_id'],
      ['transmission_id', 'channel_number'],
      ['show_id', 'host_ssn'],
      ['show_id', 'studio_id']]

queries=[
"SELECT * FROM TVchannel WHERE country='{0}'",
"""SELECT TVshow.id, TVshow.name, Transmission.air_day, Transmission.begin_time, Transmission.end_time 
FROM TVshow INNER JOIN Transmission ON TVshow.id=Transmission.show_id WHERE air_day='{0}'""",
"""SELECT * FROM TVstudio INNER JOIN StudioShow ON TVstudio.id=StudioShow.studio_id 
INNER JOIN TVshow on StudioShow.show_id=TVshow.id WHERE TVshow.name='{0}'""",
"""SELECT * FROM TVshow INNER JOIN HostShow ON TVshow.id=HostShow.show_id 
INNER JOIN TVhost ON HostShow.host_ssn=TVhost.ssn
WHERE TVhost.first_name='{0}' AND TVhost.second_name='{1}'""",
"""SELECT * FROM TVhost INNER JOIN HostShow ON TVhost.ssn=HostShow.host_ssn 
INNER JOIN TVshow ON HostShow.show_id=TVshow.id 
WHERE TVshow.category='{0}' AND TVhost.phone_number='{1}'""",
"""SELECT * FROM TVhost WHERE EXISTS
(SELECT * FROM TVshow WHERE TVshow.category='{0}' AND TVshow.id IN
(SELECT HostShow.show_id FROM HostShow WHERE HostShow.host_ssn=TVhost.ssn))
AND NOT EXISTS
(SELECT * FROM TVshow WHERE TVshow.category!='{0}' AND TVshow.id IN
(SELECT HostShow.show_id FROM HostShow WHERE HostShow.host_ssn=TVhost.ssn))""",
"""SELECT COUNT(DISTINCT TVshow.id)
FROM TVshow WHERE EXISTS
(SELECT * FROM HostShow INNER JOIN TVhost ON TVhost.ssn=HostShow.host_ssn
WHERE TVhost.first_name='{0}' AND TVhost.second_name='{1}' AND HostShow.show_id=TVshow.id)
AND NOT EXISTS
(SELECT * FROM HostShow INNER JOIN TVhost ON TVhost.ssn=HostShow.host_ssn
WHERE (TVhost.first_name!='{0}' OR TVhost.second_name!='{1}') AND HostShow.show_id=TVshow.id)""",
"""SELECT * FROM TVshow
WHERE TVshow.id IN (SELECT HostShow.show_id FROM HostShow WHERE HostShow.host_ssn IN
(SELECT TVhost.ssn FROM TVhost WHERE TVhost.first_name='{0}'))
AND EXISTS (SELECT * FROM HostShow WHERE HostShow.show_id=TVshow.id AND HostShow.host_ssn NOT IN
(SELECT TVhost.ssn FROM TVhost WHERE TVhost.first_name='{0}'))"""
]

query_cols=[['channel_number', 'name', 'category', 'country'],
            ['id', 'name', 'air_day', 'begin_time', 'end_time'],
            ['id', 'viewers', 'chromakey', 'city', 'building', 'room'],
            ['id', 'name', 'category'],
            ['ssn', 'email', 'phone_number', 'first_name', 'second_name', 'BirthDate'],
            ['ssn', 'email', 'phone_number', 'first_name', 'second_name', 'BirthDate'],
            ['count'],
            ['id', 'name', 'category']]

frame = Frame(root)

canvas = Canvas(frame)
fr1=Frame(canvas)
scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)

scrollbar.config(command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
canvas_window = canvas.create_window((0, 0), window=fr1, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

def update_scrollable_region(event=None):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    fr1_width = fr1.winfo_reqwidth()
    fr1_height = fr1.winfo_reqheight()

    canvas.configure(scrollregion=(0, 0, max(canvas_width, fr1_width), max(canvas_height, fr1_height)))
    

fr1.bind("<Configure>", update_scrollable_region)

frtable=Frame(fr1)
frbuttons=Frame(fr1)


#tables
for i in range(len(tables)):
    Button(frbuttons, text=tables[i], command=lambda n=i: build_table(tables[n], cols[n], frtable)).grid(row=0, column=i, padx=5, pady=5)

Button(frbuttons, text='SQL Queries', command=lambda: show_queries()).grid(row=0, column=8, padx=5, pady=5)
Button(frbuttons, text='Info', command=show_info).grid(row=0, column=9, padx=5, pady=5)

frbuttons.grid(row=0, column=0, sticky='W')
frtable.grid(row=1, column=0)

frame.pack(fill=BOTH, expand=True)
root.mainloop()
