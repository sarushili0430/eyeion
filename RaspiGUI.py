from tkinter import messagebox
from writelog import CheckRentalTime
from datetime import datetime
from subprocess import call
import tkinter as tk
import tkinter.ttk as ttk

RENTMESSAGE = "Would you like to rent a battery?"
RETURNMESSAGE = "Would you like to return a battery?"
ROOT_BGCOLOR = "#CFF5E7"
CLOCK_FONT = ("Helvetica Neue",75,"bold")
DATE_FONT = ("Helvetica Neue",20,"bold")
RETURN_MSG_FONT = ("Helvetica Neue",57,"bold")
RENT_MSG_FONT = ("Helvetica Neue",65,"bold")
RETURN_COLOR = "#03C988"
RENT_COLOR = "#FF0032"
SID_FONT = ("Helvetica Neue",45,"bold")

class BatteryGUI():
    
    def __init__(self):
        #Setting the main "root" screen
        self.is_scanned = False
        self.root = tk.Tk()
        self.root.config(bg=ROOT_BGCOLOR)
        self.root.title("Battery Rental Project")
        self.root.attributes('-fullscreen', True)
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.shutdown_img = tk.PhotoImage(file="img/power-off.png")
        self.reboot_img = tk.PhotoImage(file="img/power-restart.png")
        self.msg_event = None #Checks whether the tk.after method is triggered
        #Setting the Date,Clock,Message component 
        self.date = tk.Label(self.root,text="22/11/19",font=DATE_FONT,background=ROOT_BGCOLOR,pady=-10)
        self.clock = tk.Label(self.root,text="12:00:00",font=CLOCK_FONT,background=ROOT_BGCOLOR,pady=-10)
        self.shutdown_button = tk.Button(self.root,image=self.shutdown_img,bg=ROOT_BGCOLOR,width=64,height=64,highlightbackground=ROOT_BGCOLOR,highlightcolor=ROOT_BGCOLOR,
                                activebackground=ROOT_BGCOLOR,bd=0,command=self.system_shutdown)
        self.reboot_button = tk.Button(self.root,image=self.reboot_img,bg=ROOT_BGCOLOR,width=64,height=64,highlightbackground=ROOT_BGCOLOR,highlightcolor=ROOT_BGCOLOR,
                                activebackground=ROOT_BGCOLOR,bd=0,command=self.system_reboot)
        self.date.pack()
        self.clock.pack()
        self.shutdown_button.place(x=5,y=5)
        self.reboot_button.place(x=5,y=80)
        self.status_print = tk.Label(self.root,background=ROOT_BGCOLOR)
        self.rentaltime_print = tk.Label(self.root,background=ROOT_BGCOLOR)
        self.sid_print = tk.Label(self.root,background=ROOT_BGCOLOR)
        self.update_clock()
    
    def print_msg(self,status:str,sid:str):
        self.is_scanned = True
        self.sid_print.config(text=sid,font=SID_FONT)
        self.sid_print.pack(pady=5)
        if status == "RENT":
            self.status_print.config(text="Battery Rent",fg=RENT_COLOR,highlightbackground=RENT_COLOR,font=RENT_MSG_FONT)
            self.status_print.pack(pady=5)
            print(self.msg_event)
            if self.msg_event:
                self.root.after_cancel(self.msg_event)
            self.msg_event = self.root.after(ms=3000,func=self.reset)
        elif status == "RETURN":
            self.status_print.config(text="Battery Return",fg=RETURN_COLOR,highlightbackground=RETURN_COLOR,font=RETURN_MSG_FONT)
            self.status_print.pack(pady=5)
            self.print_rentaltime(sid=sid)
            print(self.msg_event)
            if self.msg_event:
                self.root.after_cancel(self.msg_event)
            self.msg_event = self.root.after(ms=3000,func=self.reset)
        else:
            raise ValueError("Value not valid.")
    
    def print_rentaltime(self,sid:str):
        #Change the color of the font depending on the rental period
        rental_hour,rental_min = CheckRentalTime(sid=sid)
        self.rentaltime_print.config(text=f"Rental time: {rental_hour}:{rental_min}",highlightbackground=RENT_COLOR,font=RETURN_MSG_FONT)
        self.rentaltime_print.pack(pady=5)

    def reset(self):
        self.status_print.forget()
        self.sid_print.forget()
        self.rentaltime_print.forget()
        self.msg_event = None
    
    def system_shutdown(self):
        confirm_shutdown = tk.messagebox.askyesno("Shutdown Confimation","Are you sure to shutdown?")
        if confirm_shutdown:
            call("sudo shutdown -h now", shell = True)
    
    def system_reboot(self):
        confirm_reboot = tk.messagebox.askyesno("Reboot Confirmation", "Are you sure to reboot?")
        if confirm_reboot:
            call("sudo shutdown -r now", shell = True)

    def update_clock(self):
        now = datetime.now()
        current_date = now.strftime("%Y/%m/%d") #Making the time in ISO format
        current_time = now.strftime("%H:%M:%S")
        self.clock.config(text=current_time)
        self.date.config(text=current_date)
        self.root.after(ms=1000,func=self.update_clock)
    
    def print_errmsg(self,text):
        self.status_print.config(text=text,fg=RENT_COLOR,highlightbackground=RENT_COLOR,font=RENT_MSG_FONT)
        self.status_print.pack(pady=5)
    

