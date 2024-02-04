import pandas as pd
from datetime import datetime, date, timedelta
import time

df = pd.read_csv(r"events.csv",
    delimiter = ",",
    usecols = ["Tytuł", "Pierwszy dzień", "Ostatni dzień", "Ogłoszony początek", "Ogłoszony koniec", "Miejsce"],
    # subject, start_day, end_day, start_time, end_time, location
    dtype = None)

#CHANGE THE FUCKING LIST NAMES YOU TROGLODYTE (reminder to myself)
subject = df["Tytuł"].values.tolist()
start_day = df["Pierwszy dzień"].values.tolist()
end_day = df["Ostatni dzień"].values.tolist()
start_time = df["Ogłoszony początek"].values.tolist()
end_time = df["Ogłoszony koniec"].values.tolist()
location = df["Miejsce"].values.tolist()
start_begin_day_list = []
start_end_day_list = []
start_begin_datetime_list = []
start_end_datetime_list = []
end_begin_datetime_list = []
end_end_datetime_list = []
weeks = []

current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# starting times of classes on start days list
for index in range(len(start_day)):
    x = start_day[index] + " " + start_time[index]
    start_begin_day_list.append(x)

# ending times of classes on start days list
for index in range(len(start_day)): 
    x = start_day[index] + " " + end_time[index]
    start_end_day_list.append(x)

# creating a list of lists of the end_day column
# accounting for when end_day[i] == missing value and end_day[i] == start_day[i]
for i in range(len(end_day)):
    if pd.isna(end_day[i]) or end_day[i] == start_day[i]:
        end_begin_datetime_list.append("N/A")
        end_end_datetime_list.append("N/A")
        weeks.append(0)
    else: # take start_day[i] and end_day[i], count how many weeks are between them
        x = datetime.strptime(end_day[i], "%d.%m.%Y")
        y = datetime.strptime(start_day[i], "%d.%m.%Y")
        week_count = (abs(x - y).days) // 7
        weeks.append(week_count)
        end_begin_datetime_list.append([]) # multidimensional list so that the indices for each list still correspond with the rows
        end_end_datetime_list.append([])
        for number in range(0, (week_count + 1)):
            date = y + timedelta(weeks = number)
            date = datetime.strftime(date, "%d.%m.%Y")
            date_begin = date + " " + start_time[i]
            date_end = date + " " + end_time[i]
            date_begin = datetime.strptime(date_begin, "%d.%m.%Y %H:%M")
            date_end = datetime.strptime(date_end, "%d.%m.%Y %H:%M")
            end_begin_datetime_list[i].append(date_begin)
            end_end_datetime_list[i].append(date_end)

# checking if it matches
""" for i in range(len(end_begin_datetime_list)):
    if end_begin_datetime_list[i] != "N/A":
        print(i)
        print(subject_list[i]) """
# works, correct subject with correct index

# str to datetime for day of class + starting times of the class (only for start days, end days were converted above)
for start in start_begin_day_list:
    start =  datetime.strptime(start, "%d.%m.%Y %H:%M")
    start_begin_datetime_list.append(start)

# str to datetime for day of class + ending times of the class (only for start days, end days were converted above)
for end in start_end_day_list:
    end =  datetime.strptime(end, "%d.%m.%Y %H:%M")
    start_end_datetime_list.append(end)

# now onto combining start and end days
full_begin_datetime_list = []
full_end_datetime_list = []

for i in range(len(start_begin_datetime_list)):
    if end_begin_datetime_list[i] == "N/A":
        full_begin_datetime_list.append([start_begin_datetime_list[i]])
        full_end_datetime_list.append([start_end_datetime_list[i]])
    else:        
        full_begin_datetime_list.append(end_begin_datetime_list[i])
        full_end_datetime_list.append(end_end_datetime_list[i])

# first thing in this loop should be asking what the user wants to know exactly, for example will i be free at 15 on 15.03.2023
# or when will i have my next class, based off current_time etc
# ^ to do later
while True:
    user_given_date = input(f"Give me a date and an hour in the following format:
                            \ndd/mm/yyyy hours:minutes:seconds\nExample: {current_time}\n")
    try: # make this whole thing a function maybe. will be using a lot
        user_given_date = datetime.strptime(user_given_date, "%d/%m/%Y %H:%M:%S")
        print(user_given_date)
    except ValueError:
        print("")
        print("Double check the format you sent it in. It's probably wrong!")
    finally: # just so that the text isnt cluttered and it doesnt post the new input prompt instantly. otherwise it's overwhelming
        print("")
        time.sleep(3)
