from os.path import exists
import csv
import datetime

index_nm = 0
df = []

#Writes the rental_log.csv file
def WriteLog(status:str,sid:str):
    date = datetime.datetime.now()
    trans_timestamp = datetime.datetime.timestamp(date)
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
    date = datetime.datetime.now().strftime("%Y%m%d")
    return_date = datetime.datetime.today() + datetime.timedelta(days=2)
    timestamp = datetime.datetime.now().timestamp()

    if exists("csvfiles/rental_log.csv") == False:
        with open("csvfiles/rental_log.csv","w",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp","Student ID","Rent/Return"])

    if exists("csvfiles/total_rental_state_file.csv") == False:
        with open("csvfiles/total_rental_state_file.csv","w",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Student","Loan Status","Start_Date","End_Date","Days_Remaining","Timestamp"])
            df.append(["Student","Loan Status","Start_Date","End_Date","Days_Remaining","Timestamp"])
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
            row[4] = "NA"
            row[5] = timestamp
            return "RETURN"
        elif sid in row:
            row[1] = "On Loan"
            row[2] = date
            row[3] = return_date.strftime("%Y%m%d")
            row[4] = "NA"
            row[5] = timestamp
            return "RENT"
    df.append([sid,"On Loan",date,return_date,"tbd",timestamp])
    return "RENT"

def CheckRentalTime(sid,*args):
    now = datetime.datetime.now().timestamp()
    #Check whether the file exists or not
    if exists("csvfiles/total_rental_state_file.csv") == False:
        raise FileNotFoundError("File not found")
    with open("csvfiles/total_rental_state_file.csv","r") as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            if row[0] == sid:
                rental_time = now - float(row[5]) #Time duration in seconds
                rental_hour = int(rental_time // 3600)
                rental_min = int((rental_time % 3600)/60)
                if rental_min < 10: rental_min = "0" + str(rental_min)
                if rental_hour < 10: rental_hour = "0" + str(rental_hour)
                return rental_hour,rental_min
                
        

    

    

