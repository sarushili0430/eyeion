from os.path import exists
import csv
from datetime import datetime

index_nm = 0
df = []

#Writes the rental_log.csv file
def WriteLog(status:str,sid:str):
    date = datetime.now()
    trans_timestamp = datetime.timestamp(date)
    with open("csvfiles/rental_log.csv","a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow([trans_timestamp,sid,status.upper()])

#Writes the total_rental_state_file.csv file
def WriteState():
    global df
    with open("csvfiles/total_rental_state_file.csv","w",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(df)

def CheckStatus(sid:str) -> str:

    global df
    df = []
    date = datetime.now().strftime("%m/%d/%y")

    if exists("csvfiles/rental_log.csv") == False:
        with open("csvfiles/rental_log.csv","w",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp","Student ID","Rent/Return"])

    if exists("csvfiles/total_rental_state_file.csv") == False:
        with open("csvfiles/total_rental_state_file.csv","w",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Student ID","Battery Rental Date","Timestamp"])
            df.append(["Student","Loan Status","Start_Date","End_Date"])
    else:
        with open("csvfiles/total_rental_state_file.csv","r",newline="") as f:
            reader = csv.reader(f,delimiter=",")
            for row in reader:
                df.append(row)
            print(f"df:{df}")
    
    #Search
    #True when on list -> RETURN
    #False -> RENT
    for row in df:
        print(row)
        if sid in row and row[1] == 'On Loan':
            row[1] = "Returned"
            return "RETURN"
        elif sid in row:
            row[1] = "On Loan"
            row[2] = date
            return "RENT"
    df.append([sid,"On Loan",date])
    return "RENT"