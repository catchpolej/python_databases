# ideas taken from
# docs.python.org/3/library/sqllite3/sqllite3.html
# and pythoncentral.io/introduction-to-sqlite-in-python
import sqlite3
from tkinter import *
import datetime

conn = sqlite3.connect('stock_trader.db')
c = conn.cursor()

def table_exists(table):
    sql = f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{table}'"
    # print(sql)
    tab = c.execute(sql)
    for num in tab:
        if num[0] == 1:
            return True
        else:
            return False

# Test table existences
stock = table_exists("stocks")
people = table_exists("people")
trans = table_exists("trans")

# Create tables and test records (rows of data) as required
if stock==False:
    c.execute('''CREATE TABLE if NOT EXISTS stocks
                 (id INTEGER PRIMARY KEY, company text, qty real, price real)''')
    c.execute("INSERT INTO stocks(company, qty, price) VALUES('Thames',100,3.142)")
    c.execute("INSERT INTO stocks(company, qty, price) VALUES('Roding',100,2.718)")
    c.execute("INSERT INTO stocks(company, qty, price) VALUES('Canterbury',100,4)")
    c.execute("INSERT INTO stocks(company, qty, price) VALUES('Winchester',100,5)")
    c.execute("INSERT INTO stocks(company, qty, price) VALUES('Rochester',100,6)")
if people==False:
    c.execute('''CREATE TABLE if NOT EXISTS people
                 (id INTEGER PRIMARY KEY, name text)''')
    c.execute("INSERT INTO people(name) VALUES('s1')")
    c.execute("INSERT INTO people(name) VALUES('s2')")
    c.execute("INSERT INTO people(name) VALUES('s3')")
if trans==False:
    c.execute('''CREATE TABLE if NOT EXISTS trans
                 (id INTEGER PRIMARY KEY, date text, qty real, price real,
                 stock_id INTEGER FORIEGN KEY REFERENCES stocks(id), people_id INTEGER FORIEGN KEY REFERENCES people(id))''')
    sql = "INSERT INTO trans(date,qty,price,stock_id,people_id) VALUES('12/12/2012',2,3.4,2,1)"
    sql = "INSERT INTO trans(date,qty,price,stock_id,people_id) VALUES('12/12/2012',2,3.4,1,2)"
    c.execute(sql)
    
# save and commit
conn.commit()

# read back the test data to the terminal
c.execute("SELECT id,company,qty,price from stocks")
for row in c:
    print(row)
c.execute("SELECT * from people")
for row in c:
    print(row)
c.execute("SELECT * from trans")
for row in c:
    print(row)
c.execute('''SELECT people.name, stocks.company FROM people
        JOIN trans ON trans.people_id = people.id
        JOIN stocks ON stocks.id = trans.stock_id''')
for row in c:
    print(row)

def get_transactions(name):
    if name=="name" or name=="":
        where_clause = ""
    else:
        where_clause = f"WHERE people.name = '{name}'"
        
    data = "Transactions are:"
    sql = f'''SELECT people.name, trans.qty, trans.price, trans.date, stocks.company FROM people
            JOIN trans ON trans.people_id = people.id
            JOIN stocks ON stocks.id = trans.stock_id {where_clause} '''
    print(sql)
    c.execute(sql)
    for row in c:
        data = data + "\n" + str(row)
    return data

def get_companies():
    sql = "SELECT company,id  FROM stocks"
    companies=[]
    c.execute(sql)
    for row in c:
        companies.append(row[0])
        companies.append(row[1])
    print(companies)
    return dict(companies[i:i+2] for i in range(0, len(companies), 2))

def get_people():
    sql = "SELECT name,id  FROM people"
    people=[]
    c.execute(sql)
    for row in c:
        people.append(row[0])
        people.append(row[1])
    print(people)
    return dict(people[i:i+2] for i in range(0, len(people), 2))

def insert_trans(person_id, stock_id, price, qty):
    today = datetime.datetime.now()
    sql = f"INSERT into trans (date,qty,price,stock_id,people_id) VALUES('{today}',{qty},{price},{stock_id},{person_id})"
    print(sql)
    c.execute(sql)
    conn.commit()
    
# define the gui
class trader_gui:
    def __init__(self, master):
        self.w = Label(master, text="Stock transactions")
        self.w.pack()

        view_frame = Frame(master, bg='lavender')
        view_frame.pack()                                           #fill=BOTH, expand=True
        self.label1 = Label (view_frame, text =("Filter by name:"))
        self.label1.pack(side="left")
        self.name = StringVar()
        self.name.set("name")
        self.e_name = Entry (view_frame, textvariable=self.name)
        self.e_name.pack(side="left")
        self.b_view = Button(view_frame, text = "View transactions", command=lambda:self.unpack_gui())
        self.b_view.pack(side="left")
        
        data_frame = Frame(master, bg='grey')
        data_frame.pack()
        self.t = Text(data_frame)
        self.t.pack()
        self.t.delete(1.0,END)
        self.t.insert(END, get_transactions(self.name.get()))

        trans_frame = Frame(master, bg='green')
        trans_frame.pack(fill=BOTH, expand=True)
        self.b_add = Button(trans_frame, text = "New transaction", command=lambda:self.new_trans())
        self.b_add.pack(side="right")
        # company list
        self.company = StringVar(trans_frame)
        self.company.trace("w",self.company_chosen)
        self.companies = get_companies()
        print(self.companies)
        self.company.set(next(iter(self.companies)))
        self.compMenu = OptionMenu(trans_frame, self.company, *self.companies)
        self.compMenu.pack(side="left")
        # current_stock_price
        self.price = DoubleVar(trans_frame)
        self.pl = Label(trans_frame, textvariable=self.price)
        self.pl.pack(side="left")
        # person list
        self.person = StringVar(trans_frame)
        self.person.trace("w",self.person_chosen)
        self.people = get_people()
        print(self.people)
        self.person.set(next(iter(self.people)))
        self.persMenu = OptionMenu(trans_frame, self.person, *self.people)
        self.persMenu.pack(side="left")
        # get current stock price
        self.company_chosen()

    def unpack_gui(self):
        self.t.delete(1.0,END)
        self.t.insert(END, get_transactions(self.name.get()))

    def new_trans(self):
        # insert_trans(person_id, stock_id)
        insert_trans(self.people[self.person.get()], self.companies[self.company.get()], self.price.get(), 10)

    # Called if company changes - get current stock price
    def company_chosen(self, *args):
        stock_id = self.companies[self.company.get()]
        sql = f"SELECT price from stocks where id = {stock_id}"
        print(sql)
        c.execute(sql)
        self.price.set(c.fetchone()[0])
        
    # Called if person changes - for debug not for functionality
    def person_chosen(self, *args):
        print("Person id is",self.people[self.person.get()])

        
        
# window setup
window1 = Tk()
window1.geometry("500x600")
window1.title("Window for GUI")
# launch the gui
app1 = trader_gui(window1)
window1.mainloop()

# close the connection
input("Press enter to close")
conn.close()
