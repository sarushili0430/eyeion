from tkinter import messagebox
from writelog import WriteLog,WriteState
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk

RENTMESSAGE = "Would you like to rent a battery?"
RETURNMESSAGE = "Would you like to return a battery?"
ROOT_BGCOLOR = "#CFF5E7"
CLOCK_FONT = ("Helvetica Neue",75,"bold")
DATE_FONT = ("Helvetica Neue",20,"bold")
RETURN_MSG_FONT = ("Helvetica Neue",57,"bold")
RENT_MSG_FONT = ("Helvetica Neue",65,"bold")
SID_FONT = ("Helvetica Neue",45,"bold")

class BatteryGUI():
    
    def __init__(self):
        #Setting the main "root" screen
        self.is_scanned = False
        self.root = tk.Tk()
        self.root.config(bg=ROOT_BGCOLOR)
        self.root.title("Battery Rental Project")
        self.root.geometry("640x400")
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        #Setting the Date,Clock,Message component 
        self.date = tk.Label(self.root,text="22/11/19",font=DATE_FONT,background=ROOT_BGCOLOR,pady=-10)
        self.clock = tk.Label(self.root,text="12:00:00",font=CLOCK_FONT,background=ROOT_BGCOLOR,pady=-10)
        self.date.pack()
        self.clock.pack()
        self.message = tk.Label(self.root,background=ROOT_BGCOLOR)
        self.sid_print = tk.Label(self.root,background=ROOT_BGCOLOR)
        self.update_clock()
    
    def print_msg(self,status:str,sid:str):
        self.is_scanned = True
        self.sid_print.config(text=sid,font=SID_FONT)
        self.sid_print.pack(pady=5)
        if status == "RENT":
            self.message.config(text="Battery Rent",fg="#9AF432",highlightbackground="#9AF432",font=RENT_MSG_FONT)
            self.message.pack(pady=5)
            self.root.after(ms=3000,func=self.reset)
        elif status == "RETURN":
            self.message.config(text="Battery Return",fg="#FCAAA5",highlightbackground="#FCAAA5",font=RETURN_MSG_FONT)
            self.message.pack(pady=5)
            self.root.after(ms=3000,func=self.reset)
        else:
            raise ValueError("Value not valid.")
    
    def reset(self):
        self.message.forget()
        self.sid_print.forget()

    def update_clock(self):
        now = datetime.now()
        current_date = now.strftime("%m/%d/%y")
        current_time = now.strftime("%H:%M:%S")
        self.clock.config(text=current_time)
        self.date.config(text=current_date)
        self.root.after(ms=1000,func=self.update_clock)
        pass
    

