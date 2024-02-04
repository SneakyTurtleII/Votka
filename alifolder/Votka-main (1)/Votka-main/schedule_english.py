import pandas as pd
from datetime import datetime, date, timedelta
import time

def append_hour(date_list, hour_list, ending_list):
    for i in range(len(date_list)):
        list_object = date_list[i] + " " + hour_list[i]
        ending_list.append(list_object)

def datetime_list_conversion(beginning_list, ending_list):
    for list_object in beginning_list:
        list_object =  datetime.strptime(list_object, "%d.%m.%Y %H:%M")
        ending_list.append(list_object)

def datediff_to_h_min(end_date, start_date):
    h_min = end_date - start_date
    h_min = str(h_min).replace(":", " ")
    if ("00 00") in h_min:
        h_min = h_min.replace(" 00 00", "h")
    else:
        h_min = h_min.replace(" 00", "")
        h_min = h_min.replace(" ", "h ") + "min"
    return h_min

def list_to_set_specified(list_from_set: list, new_set: set, specified_list: list, specified_variable):
    for i in range(len(specified_list)):
        if specified_list[i] == specified_variable:
            new_set.add(list_from_set[i])

df = pd.read_csv(r"events.csv",
    delimiter = ",",
    usecols = ["Typ", "Tytuł", "Pierwszy dzień", "Ostatni dzień", "Ogłoszony początek", "Ogłoszony koniec", "Miejsce"],
    dtype = None)

class_type_list = df["Typ"].values.tolist()
subject_list = df["Tytuł"].values.tolist()
start_day = df["Pierwszy dzień"].values.tolist()
end_day = df["Ostatni dzień"].values.tolist()
start_time = df["Ogłoszony początek"].values.tolist()
end_time = df["Ogłoszony koniec"].values.tolist()
location = df["Miejsce"].values.tolist()

# class date in the "first day" column + start/end time
start_time_start_day = []
end_time_start_day = []
# same thing but converting to datetime
start_time_start_day_datetime = [] 
end_time_start_day_datetime = []
# class date in the "last day" column + start/end time
start_time_end_day_datetime = []
end_time_end_day_datetime = []
# used later to find class dates from start_day to end_day
weeks = []

current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M")
current_time = datetime.now()

# class start and end times added to start_day
append_hour(start_day, start_time, start_time_start_day)
append_hour(start_day, end_time, end_time_start_day)

# creating a list of lists of the end_day column
# accounting for when end_day[i] == missing value and end_day[i] == start_day[i]
for i in range(len(end_day)):
    if pd.isna(end_day[i]) or end_day[i] == start_day[i]:
        start_time_end_day_datetime.append("N/A")
        end_time_end_day_datetime.append("N/A")
        weeks.append(0)
    # take start_day[i] and end_day[i], count how many weeks are between them (start_day will be in there, no need to do insert() later)
    # has to be in datetime
    else:
        x = datetime.strptime(end_day[i], "%d.%m.%Y")
        y = datetime.strptime(start_day[i], "%d.%m.%Y")
        week_count = (abs(x - y).days) // 7
        weeks.append(week_count)

        # multidimensional list so that the indices for each list still correspond with the rows
        start_time_end_day_datetime.append([])
        end_time_end_day_datetime.append([])
        
        for number in range(0, (week_count + 1)):
            date = y + timedelta(weeks = number)
            date = datetime.strftime(date, "%d.%m.%Y")
            date_begin = date + " " + start_time[i]
            date_end = date + " " + end_time[i]
            date_begin = datetime.strptime(date_begin, "%d.%m.%Y %H:%M")
            date_end = datetime.strptime(date_end, "%d.%m.%Y %H:%M")
            start_time_end_day_datetime[i].append(date_begin)
            end_time_end_day_datetime[i].append(date_end)

# str to datetime for class start_day + class start, end times
datetime_list_conversion(start_time_start_day, start_time_start_day_datetime)
datetime_list_conversion(end_time_start_day, end_time_start_day_datetime)

# combining start and end days into two multidimensional lists, one with start times and the other with end times
full_start_time_datetime = []
full_end_time_datetime = []

for i in range(len(start_time_start_day_datetime)):
    if start_time_end_day_datetime[i] == "N/A":
        full_start_time_datetime.append([start_time_start_day_datetime[i]])
        full_end_time_datetime.append([end_time_start_day_datetime[i]])
    else:        
        full_start_time_datetime.append(start_time_end_day_datetime[i])
        full_end_time_datetime.append(end_time_end_day_datetime[i])

# main part
print("Select one of the following options:\n1 - shows what classes you have on a given day at a given time\
       \nif you don't have class then, it tells you when you have your next class on the same day\
       \n2 - shows when you have the next class for a given subject (based on the current date or a specified one)\
       \n3 - shows your schedule for the day\
       \nhelp - to see a list of options\n")

while True:
    busy = 0 # inicjalizacja zmiennej, która określa czy osoba jest zajęta
    user_choice = input()

    try:
        if user_choice == "1":
            user_given_date = input(f"\nGive me a date and an hour in the following format:\ndd/mm/yyyy hours:minutes\nExample: {current_time_str}\
                                    \nOr type \"now\" if you're interested in the current date.\n\n")
            
            # if the user wants to base on the current date and time
            if user_given_date == "now":
                user_given_date = current_time_str
            user_given_date += ":00"
            
            user_given_date = datetime.strptime(user_given_date, "%d/%m/%Y %H:%M:%S")

            # checking whether there are classes during the given date and time
            for i in range(len(start_day)):
                for index in range(len(full_start_time_datetime[i])):
                    if (user_given_date <= full_end_time_datetime[i][index]) and (user_given_date >= full_start_time_datetime[i][index]):
                        busy = 1
                        subject_name = subject_list[i]
                        location_name = location[i]
                        class_type_name = {class_type_list[i]}
                        hours_left = datediff_to_h_min(full_end_time_datetime[i][index], user_given_date)
            
            if busy == 1:
                class_type_set = set()
                list_to_set_specified(class_type_list, class_type_set, subject_list, subject_name)
                if len(class_type_set) == 1:
                    class_type_name = ""
                    
                print("")
                print(f"At this time you have the \"{subject_name}, {class_type_name}\" class in {location_name}. The class will end in {hours_left} from the specified time.")
                time.sleep(2)
            else:
                possible_next_class = []
                flag = 0 # initialization of a variable that determines whether there will be classes after a given hour on a certain day
                
                for i in range(1, 21):
                    time_diff = user_given_date + timedelta(hours = i)
                    possible_next_class.append(time_diff)
                    if time_diff > user_given_date.replace(hour = 20): # after 8pm there are no classes that are just starting
                        break
                
                for date in possible_next_class:
                    for i in range(len(start_day)):
                        for index in range(len(full_start_time_datetime[i])):
                            if (date <= full_end_time_datetime[i][index])\
                                and (date >= full_start_time_datetime[i][index]):
                                flag = 1 # found nearest class
                                next_class = full_start_time_datetime[i][index]
                                break
                        if flag == 1: # breaking the loop because the nearest class was found
                            break
                    if flag == 1:
                        break
                
                if flag == 1:
                    hours_until = datediff_to_h_min(next_class, user_given_date)
                    next_class = "{:d}:{:02d}".format(next_class.hour, next_class.minute)
                    string = f"The next closest class of the day is at {next_class}, {hours_until} from now." # these sound so awkward, change them
                elif flag == 0:
                    string = "After the specified time, you have no more classes for that day." # ^ what i said before
                
                print("")
                print(f"You don't have classes at that time. {string}")
                time.sleep(2)
        elif user_choice == "2":
            # the program takes subjects from the csv file, so if the file is changed, everything still works
            subject_set = set(subject_list)
            subject_pool_dict = {} # to be able to match the selected number to the correct subject
            number_subject = 0
            
            for subject in subject_set:
                number_subject += 1
                subject_pool_dict[number_subject] = subject

            print("\nChoose the subject you are interested in:")        
            for key in subject_pool_dict:
                print(f"{key} - {subject_pool_dict[key]}")
            user_given_subject = int(input("\n"))
            
            # searching for a subject corresponding to the selected number
            for key in subject_pool_dict:
                if key == user_given_subject:
                    user_given_subject = subject_pool_dict[key]
            
            # option to choose a lecture/exercises/workshop/etc for a subject
            class_type_set = set()
            class_type_pool_dict = {}
            number_type = 0

            list_to_set_specified(class_type_list, class_type_set, subject_list, user_given_subject)

            # if given classes have only one type, it makes no sense to give the user a choice
            if len(class_type_set) == 1:
                type_choice = 0
            else:
                type_choice = 1

            if type_choice == 1:
                for class_type in class_type_set:
                    number_type += 1
                    class_type_pool_dict[number_type] = class_type
                
                print("\nChoose the type of classes you are interested in:")
                for key in class_type_pool_dict:
                    print(f"{key} - {class_type_pool_dict[key]}")
                user_given_type = int(input("\n"))

                # searching for a class type corresponding to the selected number
                for key in class_type_pool_dict:
                    if key == user_given_type:
                        user_given_type = class_type_pool_dict[key]
            
                class_type_name = f", {user_given_type}"
                time.sleep(2)
            else:
                user_given_type = list(class_type_set)[0]
                class_type_name = ""

            # looking for the nearest future date on which a subject in the given form begins
            dates_after = []

            for i in range(len(subject_list)):
                if (subject_list[i] == user_given_subject) and (class_type_list[i] == user_given_type):
                    for index in range(len(full_start_time_datetime[i])):
                        if full_start_time_datetime[i][index] > user_given_date:
                            dates_after.append(full_start_time_datetime[i][index])

            ordered_dates_after = sorted(dates_after)
            closest_date = datetime.strftime(ordered_dates_after[0], "%d/%m/%Y %H:%M")

            print("")
            print(f"The closest \"{user_given_subject}{class_type_name}\" classes will be held on the day {closest_date}.\n\n")
            time.sleep(2)
        else:
            raise ValueError()
    
    # gives valueerror if date given in the wrong format, or if the given date cannot exist at all
    # or if the user enters something not included in the options
    except ValueError:
        print("")
        print("Read the instructions carefully and try again.\n")
        time.sleep(2)
    
