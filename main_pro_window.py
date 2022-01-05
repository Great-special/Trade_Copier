import tkinter as tk
from Slave_copier import *
from tkinter import ttk

# Creating the Copier User InterFace program
_window = tk.Tk()
_window.title('Trade Copier beta - Client')
_window.minsize(450,600)
_window.maxsize(450,600)


upper_frame = tk.Frame(_window, height=200, bg='red')
upper_frame.pack(fill=tk.X, pady=5)
middle_frame = tk.Frame(_window, height=200, bg='blue')
middle_frame.pack(fill=tk.X)
lower_frame = tk.Frame(_window, height=200, bg='green')
lower_frame.pack(fill=tk.X, pady=5)

# Connecting login to interFace
def connect_account():
    startMT5(Account.get(), TradeServer.get(), Password.get())

# Account number or Login
global Account
Account = tk.IntVar()
acc_details_label = tk.Label(upper_frame, text='Account Details', font=('bold', 12), pady=5).grid(row=0, column=1, columnspan=2, pady=10)
account_label = tk.Label(upper_frame, text='Login:', font=('bold', 13), padx=10)
account_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
account_entry = tk.Entry(upper_frame, textvariable=Account, width=30)
account_entry.grid(row=1, column=1,  sticky=tk.W, pady=5)
account_entry.focus()

# Trade Server or Account Server
global TradeServer
TradeServer = tk.StringVar()
tradeserver_label = tk.Label(upper_frame, text='Server:', font=('bold', 13), padx=15)
tradeserver_label.grid(row=2, column=0, sticky=tk.W, padx=10)
tradeserver_entry = tk.Entry(upper_frame, textvariable=TradeServer, width=30)
tradeserver_entry.grid(row=2, column=1, sticky=tk.W)

# Password
global Password
Password = tk.StringVar()
pword_label = tk.Label(upper_frame, text='Password:', font=('bold', 13), padx=10)
pword_label.grid(row=3, column=0, sticky=tk.W, pady=10, padx=10)
pword_entry = tk.Entry(upper_frame, textvariable=Password, width=30)
pword_entry.grid(row=3, column=1, sticky=tk.W, pady=10)

# Connect Button
start_MT5_btn = tk.Button(upper_frame, text='Connect Account', width=20, command=connect_account)
start_MT5_btn.grid(row=4, column=1, pady=5, padx=15, columnspan=2)

#open positions
pos_details_label = tk.Label(middle_frame, text='Position Details', font=('bold', 12), pady=5).grid(row=0, column=1, columnspan=3, pady=5, padx=150)
pos_list = tk.Listbox(middle_frame, height=10, width=70,border=0)
pos_list.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

#General info
gen_info = tk.Label(lower_frame, text='General Info', font=('bold', 12), pady=5).grid(row=0, column=1, columnspan=2, padx=70, pady=10)
conn_server_btn = tk.Button(lower_frame, text='Connect Server', width=15, command=startServer, padx=10)
conn_server_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

# close_pos_btn = tk.Button(lower_frame, text='Close Position', width=13, command=closeOpenPosition, padx=10)
# close_pos_btn.grid(row=1, column=3, sticky=tk.E, padx=10)

info_bar_label = tk.Label(lower_frame, text='Info Bar', font=('bold', 12), pady=5).grid(row=2, column=0, sticky=tk.W, padx=10)
info_bar_box = tk.Listbox(lower_frame, height=3, width=30).grid(row=2, column=1, padx=5, pady=10)

print('[STARTING] Program Window')
_window.mainloop()
