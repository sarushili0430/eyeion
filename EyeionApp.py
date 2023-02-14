from RaspiGUI import BatteryGUI
from os.path import exists
from writelog import *
import nfc, time, threading
import datetime
import traceback
import csv

#Specify the USB port of the device
USB_PORTS = ["usb:054c:06c1","usb:054c:06c3"]

"""
Configuration
    Args:
    gui: The main gui application
    student_id: Holds the student number
    clf: NFC-reader Object
"""
gui = BatteryGUI()
student_id = ""
clf = None
card_reader_active = threading.Event()
clf_isclosed = True

#Activating the NFC reader
def activate_reader():
    global clf
    for port in USB_PORTS:
        try:
            print(port)
            print(nfc.ContactlessFrontend(port))
            clf = nfc.ContactlessFrontend(port)
            print("found:", clf)
            print("App successfully launched!")
            break
        except Exception as e:
            print(str(e))
    else:
        gui.print_errmsg("ERROR: Card reader not found")
        card_reader_active.set()


def nfcreader():
    global clf_isclosed
    #Check whether the connection is closed or not
    if clf_isclosed == True:
        activate_reader()
        clf_isclosed = False
    #Check whether the card reader is active or not
    if card_reader_active.is_set():
        return
    try:
        prev = None
        when = time.time()
        while True:
            tag = clf.connect(rdwr = { 'on-connect' : lambda tag: False })
            scs = [nfc.tag.tt3.ServiceCode(648, 0xA20B)]
            bcs = [ nfc.tag.tt3.BlockCode(1),
                    nfc.tag.tt3.BlockCode(2),
                    nfc.tag.tt3.BlockCode(3),
                    nfc.tag.tt3.BlockCode(4)
            ]
            data = tag.read_without_encryption(scs, bcs)
            student_id = data[2:10].decode()
            now  = time.time()
            if now-when > 2 or student_id != prev:
                prev = student_id
                when = now
                status = CheckStatus(sid=student_id)
                gui.print_msg(status=status,sid=student_id)
                WriteLog(status=status,sid=student_id)
                WriteState()
                time.sleep(0.01)
            else:
                when = now
                time.sleep(1)
    except Exception as e:
        gui.reset()
        print(e)
        if str(e) == "invalid service code number or attribute":
            gui.print_errmsg("ERROR: Please touch the card again")
            return
    clf.close()
    clf_isclosed = True
    print(clf)

#Monitors the nfcreader thread (thread1)
def thread_monitor():
    global thread1
    while True:
        #print(thread1.is_alive())
        if card_reader_active.is_set():
            break
        if thread1.is_alive() == False:
            thread1 = threading.Thread(target=nfcreader)
            thread1.start()

thread2 = threading.Thread(target=thread_monitor)
thread1 = threading.Thread(target=nfcreader)
thread1.start()
thread2.start()

gui.root.mainloop()
