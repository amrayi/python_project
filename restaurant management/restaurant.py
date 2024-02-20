from tkinter import *
from tkinter.font import *
import os
import sqlite3
from subprocess import call

#region کلاس دیتابیس  
class dataBase:
    def __init__(self, db):
        self.__db_name = db
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS [table_menu] (
                            [ID]	INT PRIMARY KEY NOT NULL UNIQUE,
                            [Name]	NVARCHAR(50) NOT NULL UNIQUE,
                            [price]	INT NOT NULL,
                            [is_food] BULL NOT NULL) WITHOUT ROWID;
                            ''')
        
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS [table_receipts](
                            [receipt_id] INT NOT NULL,
                            [menu_id] INT NOT NULL REFERENCES[table_menu]([ID]),
                            [count] INT,
                            [price] INT);
                            ''')

        self.cursor.execute("""
                            CREATE VIEW IF NOT EXISTS view_menu_receipts AS 
                            SELECT table_receipts.receipt_id, table_menu.Name, table_receipts.count,
                            table_receipts.price, (table_receipts.price * table_receipts.count) AS sum 
                            FROM table_menu
                            INNER JOIN table_receipts ON table_menu.ID == table_receipts.menu_id
                            """)
        # self.connection.rollback()  نادیده گرفتن متن نوشته شده
        self.connection.commit()
        self.connection.close()

    def insert(self, id, name, price, is_food):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("INSERT INTO table_menu VALUES (?, ?, ?, ?)" , (id, name, price, is_food))
        self.connection.commit()
        self.connection.close()

    def get_menu_items(self, is_food):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM table_menu WHERE is_food = ?", (is_food,))
        result = self.cursor.fetchall()
        return result
    
    def get_max_receipt(self):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT MAX(receipt_id) FROM table_receipts")
        result = self.cursor.fetchall()
        return result
    
    def get_menu_item_by_name(self, menu_item_name):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM table_menu WHERE name = ? ", (menu_item_name,))
        result = self.cursor.fetchall()
        return result
    
    def insert_into_receipt(self, receipt_id, menu_id, count, price):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("INSERT INTO table_receipts VALUES(?, ?, ?, ?)" , (receipt_id, menu_id, count, price))
        self.connection.commit()
        self.connection.close()

    def get_receipt_by_receipID_menuID(self, receipt_id, menu_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM table_receipts WHERE receipt_id = ? AND menu_id = ? ", (receipt_id, menu_id))
        result = self.cursor.fetchall()
        return result
    
    def increase_count(self, receipt_id, menu_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("UPDATE table_receipts SET count = count +1 WHERE receipt_id = ? AND menu_id = ?",
                            (receipt_id, menu_id))
        self.connection.commit()
        self.connection.close()

    def decrease_count(self, receipt_id, menu_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("UPDATE table_receipts SET count = count -1 WHERE receipt_id = ? AND menu_id = ? AND count > 0",
                            (receipt_id, menu_id))
        self.cursor.execute("DELETE FROM table_receipts WHERE receipt_id = ? AND menu_id = ? AND count = 0" , (receipt_id, menu_id))
        self.connection.commit()
        self.connection.close()

    def get_receipts_by_receiptid(self, receipt_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM view_menu_receipts WHERE receipt_id = ? ", (receipt_id,))
        result = self.cursor.fetchall()
        return result
    
    def delete_receipt(self, receipt_id, menu_id):
        self.connection = sqlite3.connect(self.__db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("DELETE FROM table_receipts WHERE receipt_id = ? AND menu_id = ?" , (receipt_id, menu_id))
        self.connection.commit()
        self.connection.close()
        
#endregion 

#region عمومی
db = None

if os.path.isfile('restaurant.db') == False:
    db = dataBase('restaurant.db')
    db.insert(1, 'چلو مرغ', 22000, True)
    db.insert(2, 'زرشک پلو ساده', 17000, True)
    db.insert(3, 'باقالی پلو با گوشت', 67000, True)
    db.insert(4, 'نوشابه قوطی', 3000, False)
    db.insert(5, 'نوشابه خانواده', 5000, False)
    db.insert(6, 'دوغ بطری', 4000, False)
else:
    db = dataBase('restaurant.db')

window = Tk()

height = window.winfo_screenheight()
width = window.winfo_screenwidth()
window.geometry('%dx%d' %(width,height))

window.grid_columnconfigure(0, weight=2)
window.grid_columnconfigure(1, weight=3)

pad_x =5
pad_y =5

window.grid_rowconfigure(0, weight= 1)

window.state('zoomed')

window.title('نرم افزار مدیریت رستوران')

vazir_font = Font(family= 'Vazir', size= 16)
#endregion

#region فریم صورتحساب

def load_receipts(receipt_id):
    list_box.delete(0, 'end')
    receipts = db.get_receipts_by_receiptid(receipt_id)
    for receipt in receipts:
        list_box.insert(0, "%s-%s %s %s" %(receipt[1], receipt[2], receipt[3], receipt[4]))

receipt_frame = LabelFrame(window, text= 'صورتحساب', font= vazir_font, padx= pad_x, pady= pad_y)
receipt_frame.grid(row=0, column=0, sticky= 'nsew', padx= pad_x, pady= pad_y)

receipt_frame.grid_columnconfigure(0, weight=1)
receipt_frame.grid_rowconfigure(1, weight=1)

entry_order_number = Entry(receipt_frame, font= vazir_font, width=10, justify= 'center')
entry_order_number.grid(row=0, column=0)

def entry_key_release(key):
    try:
        receipt_id = int(entry_order_number.get())
        load_receipts(receipt_id)
    except:
        pass

entry_order_number.bind('<KeyRelease>', entry_key_release)

max_receipt_number = db.get_max_receipt()
if max_receipt_number[0][0] == None:
    max_receipt_number = 0
else:
    max_receipt_number = int(max_receipt_number[0][0])

max_receipt_number += 1

entry_order_number.insert(0, max_receipt_number)

list_box = Listbox(receipt_frame, font= vazir_font)
list_box.grid(row=1, column=0, sticky='nsew', padx= pad_x, pady= pad_y)
list_box.configure(justify= RIGHT)

# ******* فریم دکمه های لیست باکس

ListBox_button_frame = Frame(receipt_frame)
ListBox_button_frame.grid(row=2, column=0, sticky='nsew', padx= pad_x, pady= pad_y)

ListBox_button_frame.grid_columnconfigure(0, weight=1)
ListBox_button_frame.grid_columnconfigure(1, weight=1)
ListBox_button_frame.grid_columnconfigure(2, weight=1)
ListBox_button_frame.grid_columnconfigure(3, weight=1)


def delete_receipt_item():
    try:
        receipt_id = int(entry_order_number.get())
        menu_item = list_box.get(ACTIVE)
        menu_item_name = menu_item.split('-')[0]
        result = db.get_menu_item_by_name(menu_item_name)
        menu_item_id = int(result[0][0])
        db.delete_receipt(receipt_id, menu_item_id)
        load_receipts(receipt_id)
    except:
        pass
button_delete = Button(ListBox_button_frame,text= 'حذف سطر', font= vazir_font, command= delete_receipt_item)
button_delete.grid(row=0, column=0, sticky='nsew')

def new_receipt():
    list_box.delete(0, 'end')
    max_receipt_number = db.get_max_receipt()

    if max_receipt_number[0][0] == 0:
        max_receipt_number =0
    else:
        max_receipt_number = int(max_receipt_number[0][0])

    max_receipt_number += 1
    entry_order_number.delete(0, 'end')
    entry_order_number.insert(0, max_receipt_number)
    
button_new = Button(ListBox_button_frame,text= 'فاکتور جدید', font= vazir_font, command= new_receipt)
button_new.grid(row=0, column=1, sticky='nsew')

def increase_item():
    menu_item_name = list_box.get(ACTIVE)
    result = db.get_menu_item_by_name(menu_item_name.split('-')[0])
    menu_item_id = result[0][0]
    receipt_id = int(entry_order_number.get())
    db.increase_count(receipt_id, menu_item_id)
    load_receipts(receipt_id)

button_increase = Button(ListBox_button_frame,text= '+', font= vazir_font, command= increase_item)
button_increase.grid(row=0, column=2, sticky='nsew')

def decrease_item():
    menu_item_name = list_box.get(ACTIVE)
    result = db.get_menu_item_by_name(menu_item_name.split('-')[0])
    menu_item_id = result[0][0]
    receipt_id = int(entry_order_number.get())
    db.decrease_count(receipt_id, menu_item_id)
    load_receipts(receipt_id)

button_decrease = Button(ListBox_button_frame,text= '-', font= vazir_font, command= decrease_item)
button_decrease.grid(row=0, column=3, sticky='nsew')
#endregion

#region فریم منو

menu_frame = LabelFrame(window, text= 'منو نوشیدنی و غذا', font= vazir_font)
menu_frame.grid(row=0, column=1, sticky= 'nsew', padx= pad_x, pady= pad_y)

menu_frame.grid_columnconfigure(0, weight=1)
menu_frame.grid_columnconfigure(1, weight=1)

menu_frame.grid_rowconfigure(0,weight=1)

# ******* فریم نوشیدنی

drink_frame =LabelFrame(menu_frame, text= 'نوشیدنی ها', padx= pad_x, pady= pad_y)
drink_frame.grid(row=0, column=0, sticky='nsew', padx= pad_x, pady= pad_y)
drink_frame.grid_columnconfigure(0, weight=1)
drink_frame.grid_rowconfigure(0, weight=1)

listbox_drinks = Listbox(drink_frame, font= vazir_font, exportselection= False)
listbox_drinks.grid(sticky= 'nsew')
listbox_drinks.configure(justify= RIGHT)

drinks = db.get_menu_items(False)

for drink in drinks:
    listbox_drinks.insert("end", drink[1])

def add_drink(event):
    drink_item = db.get_menu_item_by_name(listbox_drinks.get(ACTIVE))
    menu_id = drink_item[0][0]
    price = drink_item[0][2]
    receipt_id = int(entry_order_number.get())

    result = db.get_receipt_by_receipID_menuID(receipt_id, menu_id)

    if len(result) == 0:
        db.insert_into_receipt(receipt_id, menu_id,1, price)
    else:
        db.increase_count(receipt_id, menu_id)

    load_receipts(receipt_id)

listbox_drinks.bind("<Double-Button>", add_drink)

# ******* فریم غذا

food_frame = LabelFrame(menu_frame, text= 'غذاها', padx= pad_x, pady= pad_y)
food_frame.grid(row= 0, column= 1, sticky='nsew', padx= pad_x, pady= pad_y)
food_frame.grid_columnconfigure(0, weight=1)
food_frame.grid_rowconfigure(0, weight=1)

listbox_foods = Listbox(food_frame, font= vazir_font, exportselection= False)
listbox_foods.grid(sticky= 'nsew')
listbox_foods.configure(justify= RIGHT)

foods = db.get_menu_items(True)

for food in foods:
    listbox_foods.insert("end", food[1])

def add_food(event):
    food_item = db.get_menu_item_by_name(listbox_foods.get(ACTIVE))
    menu_id = food_item[0][0]
    price = food_item[0][2]
    receipt_id = int(entry_order_number.get())

    result = db.get_receipt_by_receipID_menuID(receipt_id, menu_id)

    if len(result) == 0:
        db.insert_into_receipt(receipt_id, menu_id,1, price)
    else:
        db.increase_count(receipt_id, menu_id)

    load_receipts(receipt_id)

listbox_foods.bind("<Double-Button>", add_food)

#endregion

#region فریم دکمه ها

buttons_frame = LabelFrame(window, font= vazir_font, padx= pad_x, pady= pad_y)
buttons_frame.grid(row=1, column=1, padx= pad_x, pady= pad_y)

from tkinter import messagebox
import tkinter as tk

def exit_program():
    message_box = tk.messagebox.askquestion('خروج','آیا برای خروج مطمین هستید؟', icon = 'warning')
    if message_box == 'yes':
        window.destroy()

window.protocol("WM_DELETE_WINDOW", exit_program)

button_exit = Button(buttons_frame, text= 'خروج', font= vazir_font, command= exit_program)
button_exit.grid(row=0, column=0)

def open_calculator():
    call(['calc.exe'])

button_calculator = Button(buttons_frame, text= 'ماشین حساب', font= vazir_font, command= open_calculator)

button_calculator.grid(row=0, column=1)

def open_website():
    import webbrowser
    webbrowser.open('https://code-academy.net')
button_open_website = Button(buttons_frame, text='وبسایت ما', font= vazir_font, command= open_website)
button_open_website.grid(row= 0, column= 2)
#endregion

window.mainloop()
