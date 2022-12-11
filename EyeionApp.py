from guiforbattery3 import BatteryGUI
from os.path import exists
from writelog import *
import nfc, time, threading
import datetime
import traceback
import csv

#Specify the USB port of the device
USB_PORT = "usb:001:002"

"""
Configuration
    Args:
    gui: The main gui application
    student_id: Holds the student number
    clf: NFC-reader Object
"""
gui = BatteryGUI()
student_id = ""
clf = nfc.ContactlessFrontend(USB_PORT)
print("found:", clf)

def nfcreader():
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
    except Exception:
        e = traceback.format_exc()
        print(e)
    clf.close()

thread1 = threading.Thread(target=nfcreader)
thread1.start()

gui.root.mainloop()