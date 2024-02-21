from tkinter import *
from tkinter.font import *
import requests
from tkinter import messagebox
import threading

window = Tk()
window.resizable(0,0)
window.title('Calender')


def get_data():
    my_thread = threading.Thread(target= get_data_from_server)
    my_thread.start()

def get_data_from_server():
    button['state'] = DISABLED
    entry['state'] = DISABLED

    date = entry.get()
    list_box.delete(0,'end')
    r = requests.get('https://pholiday.herokuapp.com/date/' + date)

    data = r.json()

    if r.status_code == 200:
        for item in data['events']:
            event = item['event']
            is_hodilay = item['isHoliday']
            
            if is_hodilay == True:
                list_box.insert(END,'%s (تعطیل)' %(event))
                list_box.itemconfig(END, {'fg':'green'})
            else:
                list_box.insert(END,'%s' %(event))
    else:
        messagebox.showerror('خطا','خطای %d' %(r.status_code))
    
    button['state'] = NORMAL
    entry['state'] = NORMAL

my_font = Font(family='Vazir' , size=18)

pad_x = 10
pad_y = 10

label = Label(window, text=':لطفا تاریخ را وارد کنید', font = my_font)
label.grid(row=0 ,sticky=E,padx = pad_x)


entry = Entry(window , font = my_font,fg='brown')
entry.grid(row=1 ,sticky=E ,padx = pad_x,pady=pad_y)

list_box = Listbox(window,font = my_font,height=7,width=50)
list_box.grid(row=2, padx = pad_x , pady = pad_y,sticky = W+E )
list_box.configure(justify=RIGHT)


button = Button(window, text='دریافت اطلاعات', font = my_font,command=get_data)
button.grid(row=3 , sticky = W+E ,padx = pad_x,pady=pad_y)


def center_window():
    window.update_idletasks()
    w = window.winfo_width()
    h = window.winfo_height()

    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window.geometry('%dx%d+%d+%d' %(w , h , x , y))

center_window()


window.mainloop()
