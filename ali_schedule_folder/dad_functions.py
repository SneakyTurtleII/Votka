import pandas as pd
from datetime import datetime, date, timedelta
from csv import writer

def str_to_date_list(str_list, date_list):
    for string in str_list:
        date_list.append(datetime.strptime(string, "%d/%m/%Y"))

def str_to_datetime_list(str_list, datetime_list):
    for string in str_list:
        datetime_list.append(datetime.strptime(string, "%d/%m/%Y %H:%M:%S"))

def time_to_datetime_list(date_list, time_list):
    date_time_list = []
    for i in range( len(date_list) ):
        date_time_list.append(date_list[i] + " " + time_list[i])
    return date_time_list

def sort_subject_list(s_subject_list, f_start_datetime_list, s_f_start_datetime_list, num_entries):
    for i in range(num_entries):
        for j in range (num_entries):
            if (f_start_datetime_list[j] == s_f_start_datetime_list[i]):
                s_subject_list.append(subject_list[j])
    return s_subject_list

def datetime_to_str(datetime_object, option):
    if (option == "date"):
        return datetime_object.strftime("%d/%m/%Y")
    elif (option == "time"):
        return datetime_object.strftime("%H:%M")
    else:
        return datetime_object.strftime("%d/%m/%Y %H:%M")
    
def str_to_datetime(str_input, option):
    if (option == "date"):
        return datetime.strptime(str_input, "%d/%m/%Y")
    elif (option == "time"):
        return datetime.strptime(str_input, "%H:%M")
    else:
        return datetime.strptime(str_input, "%d/%m/%Y %H:%M")
    
def datediff_to_h_min(end_date, start_date):
    h_min = end_date - start_date
    h_min = str(h_min).replace(":", " ")
    if ("00 00") in h_min:
        h_min = h_min.replace(" 00 00", "h")
    else:
        h_min = h_min.replace(" 00", "")
        h_min = h_min.replace(" ", "h ") + "min"
    return h_min
    
def compare_strings_case_insensitive(string1, string2, option = "equals"):

    if (option == "greater"):
        if (string1.lower() > string2.lower()):
            return True
        else:
            return False
        
    if (option == "lesser"):
        if (string1.lower() < string2.lower()):
            return True
        else:
            return False

    if (string1.lower() == string2.lower()):
        return True
    else:
        return False
    
def compare_datetime(datetime1, datetime2, option = "equals"):
    
    if (option == "greater"):
        if (datetime1 > datetime2):
            return True
        else:
            return False
        
    if (option == "greater or equal"):
        if (datetime1 >= datetime2):
            return True
        else:
            return False
        
    if (option == "lesser"):
        if (datetime1 < datetime2):
            return True
        else:
            return False
        
    if (option == "lesser or equal"):
        if (datetime1 <= datetime2):
            return True
        else:
            return False

    if (datetime1 == datetime2):
        return True
    else:
        return False

def compare_dates_only(datetime1, datetime2, option = "equals"):
    
    if (option == "greater"):
        if (datetime1.date() > datetime2.date()):
            return True
        else:
            return False
        
    if (option == "greater or equal"):
        if (datetime1.date() >= datetime2.date()):
            return True
        else:
            return False
        
    if (option == "lesser"):
        if (datetime1.date() < datetime2.date()):
            return True
        else:
            return False
        
    if (option == "lesser or equal"):
        if (datetime1.date() <= datetime2.date()):
            return True
        else:
            return False

    if (datetime1.date() == datetime2.date()):
        return True
    else:
        return False
    
def is_time_between(datetimeToCompare, datetime1, datetime2):
    if (datetimeToCompare < datetime1) and (datetimeToCompare > datetime2):
        return True
    elif (datetimeToCompare > datetime1) and (datetimeToCompare < datetime2):
        return True
    else:
        return False

df = pd.read_csv(r"dadclasses_copy.csv",
    delimiter = ",",
    usecols = ["Subject", "Date", "Start Time", "End Time"],
    dtype = None)

subject_list =  df["Subject"].values.tolist() # 'COM S 227', 'COM S 227', 'COM S 227', 'COM S 227'
s_subject_list = []
nd_subject_list = [*set(subject_list)]

# list of dates where I have classes
date_list = df["Date"].values.tolist() # '19/1/2023', '26/1/2023', '31/1/2023', '2/2/2023', '7/2/2023'
f_date_list = []
str_to_date_list(date_list, f_date_list)
s_f_date_list = sorted(f_date_list)

# start time of classes
start_time_list = df["Start Time"].values.tolist() # '08:50:00', '08:50:00', '08:50:00', '08:50:00', '08:50:00'
start_datetime_list = time_to_datetime_list(date_list, start_time_list)
f_start_datetime_list = []
str_to_datetime_list(start_datetime_list, f_start_datetime_list)
s_f_start_datetime_list = sorted(f_start_datetime_list)

# end time of classes 
end_time_list = df["End Time"].values.tolist() # '09:40:00', '09:40:00', '09:40:00', '09:40:00', '09:40:00', '09:40:00'
end_datetime_list = time_to_datetime_list(date_list, end_time_list)
f_end_datetime_list = []
str_to_datetime_list(end_datetime_list, f_end_datetime_list)
s_f_end_datetime_list = sorted(f_end_datetime_list)

# useful when iterating over lists, length of most lists unless they are nd or otherwise
num_entries = len(subject_list)

# sorting subject list
for i in range(num_entries):
    for j in range (num_entries):
        if (f_start_datetime_list[j] == s_f_start_datetime_list[i]):
            s_subject_list.append(subject_list[j])

current_datetime = datetime.now()
example_datetime = datetime_to_str(current_datetime, "datetime")
example_date = datetime_to_str(current_datetime, "date")