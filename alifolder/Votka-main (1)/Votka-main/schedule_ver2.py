import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate
from operator import itemgetter
from vardata import *

def append_hour(date_list, hour_list, ending_list):
    for i in range(len(date_list)):
        list_object = date_list[i] + " " + hour_list[i]
        ending_list.append(list_object)

def datetime_list_conversion(beginning_list):
    for i in range(len(beginning_list)):
        list_object_datetime =  datetime.strptime(beginning_list[i], "%d.%m.%Y %H:%M")
        beginning_list[i] = list_object_datetime

def datediff_to_h_min(end_date: datetime, start_date: datetime):
    h_min = end_date - start_date
    h_min = str(h_min).replace(":", " ")
    if ("00 00") in h_min:
        h_min = h_min.replace(" 00 00", "h")
    else:
        h_min = h_min.replace(" 00", "")
        h_min = h_min.replace(" ", "h ") + "min"
    return h_min

def if_only_one_date_occurence(start_time_end_day: list, end_time_end_day: list, weeks: list):
    start_time_end_day.append("N/A")
    end_time_end_day.append("N/A")
    weeks.append(0)

def make_multidimensional_list_for_end_days(start_time_end_day: list, end_time_end_day: list, weeks: list, i: int):
    end_day = datetime.strptime(end_days[i], "%d.%m.%Y")
    start_day = datetime.strptime(start_days[i], "%d.%m.%Y")
    week_count = (abs(end_day - start_day).days) // 7
    weeks.append(week_count)
    
    start_time_end_day.append([])
    end_time_end_day.append([])

    for number in range(0, (week_count + 1)):
        date = start_day + timedelta(weeks = number)
        date = datetime.strftime(date, "%d.%m.%Y")
        date_begin = date + " " + start_time[i]
        date_end = date + " " + end_time[i]
        date_begin = datetime.strptime(date_begin, "%d.%m.%Y %H:%M")
        date_end = datetime.strptime(date_end, "%d.%m.%Y %H:%M")
        start_time_end_day[i].append(date_begin)
        end_time_end_day[i].append(date_end)

def end_days_datetime_list_conversion(return_start: bool):
    # utworzenie dwuwymiarowej listy dla kolumny end_days
    # + co jeśli end_days == missing value albo jest takie samo jak start_days
    start_time_end_days = []
    end_time_end_days = []

    weeks = []

    for i in range(len(end_days)):
        if pd.isna(end_days[i]) or end_days[i] == start_days[i]:
            if_only_one_date_occurence(start_time_end_days, end_time_end_days, weeks)
        # wzięcie start_days[i] i end_days[i], policzenie ile jest między nimi tygodni (start_days wliczone, więc nie trzeba potem robić insert)
        # musi być w datetime
        else:
            make_multidimensional_list_for_end_days(start_time_end_days, end_time_end_days, weeks, i)

    if return_start:
        return start_time_end_days
    else:
        return end_time_end_days

def start_days_datetime_list_conversion(return_start: bool):
    # data zajęć w kolumnie "pierwszy dzień" + godzina rozpoczęcia/zakończenia
    start_time_start_days = []
    end_time_start_days = []

    # godziny rozpoczęcia, zakończenia zajęć dodane do start_days
    append_hour(start_days, start_time, start_time_start_days)
    append_hour(start_days, end_time, end_time_start_days)

    # str na datetime dla start_days zajęć + godziny rozpoczęcia, zakończenia zajęć
    datetime_list_conversion(start_time_start_days)
    datetime_list_conversion(end_time_start_days)

    if return_start:
        return start_time_start_days
    else:
        return end_time_start_days

def final_datetime_list_conversion(return_start: bool):
    # łączenie dni początkowych i końcowych w dwie dwuwymiarowe listy, jedna z godzinami rozpoczęcia i druga zakończenia
    full_start = []
    full_end = []

    start_time_start_days_list = start_days_datetime_list_conversion(True)
    end_time_start_days_list = start_days_datetime_list_conversion(False)

    start_time_end_days_list = end_days_datetime_list_conversion(True)
    end_time_end_days_list = end_days_datetime_list_conversion(False)

    for i in range(len(start_time_start_days_list)):
        if start_time_end_days_list[i] == "N/A":
            full_start.append([start_time_start_days_list[i]])
            full_end.append([end_time_start_days_list[i]])
        else:        
            full_start.append(start_time_end_days_list[i])
            full_end.append(end_time_end_days_list[i])

    if return_start:
        return full_start
    else:
        return full_end

# część główna
def main_part_instructions():
    print("Wybierz jedną z poniższych opcji:\n1 - podaje jakie masz zajęcia w podanym dniu o danej godzinie\
        \njeśli nie masz wtedy zajęć, podaje kiedy masz następne zajęcia tego samego dnia\
        \n2 - podaje kiedy masz najbliższe zajęcia z danego przedmiotu (w oparciu o obecną datę lub sprecyzowaną)\
        \n3 - podaje twój plan zajęć na dany dzień\
        \n4 - dodaje wydarzenie\
        \n5 - usuwa wydarzenie\
        \n6 - wyszukaj wolne sloty w podanym terminie\
        \n7 - podaje ile w danym okresie czasowym masz zaplanowanych wydarzeń\
        \nhelp - pokazuje ponownie listę opcji\n")

def option_1_user_input():
    user_input = input(f"\nPodaj datę i godzinę w następującym formacie:\ndd/mm/yyyy hours:minutes\nPrzykład: {current_time_str}\
                                    \nLub wpisz \"teraz\", jeśli interesuje cię obecna data.\n\n")
    
    return user_input

def check_if_during_datetime_there_is_event(datetime_date: datetime):
    full_start = final_datetime_list_conversion(True)
    full_end = final_datetime_list_conversion(False)
    busy = 0
    
    for i in range(len(start_days)):
        for j in range(len(full_start[i])):
            if (datetime_date <= full_end[i][j]) and (datetime_date >= full_start[i][j]):
                busy = 1
                subject_name = subject_list[i]
                location_name = location[i]
                class_type_name = f", {class_type_list[i]}"
                hours_left = datediff_to_h_min(full_end[i][j], datetime_date)
    
    if busy:
        return [subject_name, class_type_name, location_name, hours_left]
    else:
        return []

def search_through_rest_of_day(datetime_date: datetime):
    possible_next_class = []
    for i in range(1, 21):
        time_diff = datetime_date + timedelta(hours = i)
        possible_next_class.append(time_diff)
        if time_diff > datetime_date.replace(hour = 20): # po 20 nie ma zajęć które dopiero się zaczynają
            break

    return possible_next_class

def if_next_class_found(busy: bool, next_class):
    if busy == True:
        hours_until = datediff_to_h_min(next_class, user_given_date)
        next_class_str = "{:d}:{:02d}".format(next_class.hour, next_class.minute)
        string = f"Następne najbliższe zajęcia tego dnia są o godzinie {next_class_str}, {hours_until} od teraz."
    else:
        string = "Po podanej godzinie nie masz już zajęć tego dnia."
    
    return string

full_start = final_datetime_list_conversion(True)
full_end = final_datetime_list_conversion(False)

def find_next_class_if_no_class_when_specified(datetime_date: datetime):
    full_start = final_datetime_list_conversion(True)
    full_end = final_datetime_list_conversion(False)
    busy = 0 # inicjalizacja zmiennej, która określa czy osoba będzie miała zajęcia po danej godzinie w określonym dniu

    possible_next_class = search_through_rest_of_day(datetime_date)

    for date in possible_next_class:
        for i in range(len(start_days)):
            for j in range(len(full_start[i])):
                if (date <= full_end[i][j])\
                    and (date >= full_start[i][j]):
                    busy = True # znaleziono zajęcia
                    next_class = full_start[i][j]
                    break
            if busy == True: # przerwanie pętli, bo znaleziono najbliższe zajęcia
                break
        if busy == True:
            break
        
        return if_next_class_found(True, next_class)

def list_to_set_specified(list_from_set: list, new_set: set, specified_list: list, specified_variable):
    for i in range(len(specified_list)):
        if specified_list[i] == specified_variable:
            new_set.add(list_from_set[i])

def instructions_whether_class_was_found(list_to_check: list, datetime_date: datetime):
    if list_to_check:
        # sprecyzowanie formy zajęć, jeśli dany przedmiot ma tylko jedną formę, str class_type_name jest pusty
        class_type_set = set()
        list_to_set_specified(class_type_list, class_type_set, subject_list, list_to_check[1])
        if len(class_type_set) == 1:
            list_to_check[1] = ""

        print(f"\nW tym czasie masz zajęcia \"{list_to_check[0]}{list_to_check[1]}\" w {list_to_check[2]}.\
              \nTe zajęcia skończą się w {list_to_check[3]} od sprecyzowanego czasu.\n\n")
    else:
        result = find_next_class_if_no_class_when_specified(datetime_date)

        print(f"\nNie masz wtedy zajęć.\n{result}\n\n")

def user_chose_option_1():
    user_given_date = option_1_user_input()
    
    # jeśli użytkownik chce bazować na obecnej dacie i godzinie
    if user_given_date == "teraz":
        user_given_date = current_time_str
    user_given_date += ":00"

    user_given_date = datetime.strptime(user_given_date, "%d/%m/%Y %H:%M:%S")

    event_list = check_if_during_datetime_there_is_event(user_given_date)

    instructions_whether_class_was_found(event_list, user_given_date)

def generate_subject_options():
    subject_set = set(subject_list)
    subject_pool_dict = {} # żeby móc dopasować wybrany numer do odpowiedniego przedmiotu
    number_subject = 0
        
    for subject in subject_set:
        number_subject += 1
        subject_pool_dict[number_subject] = subject

    return subject_pool_dict

def option_2_user_input():
    possible_subjects = generate_subject_options()

    print("\nWybierz przedmiot, który cię interesuje:")        
    for key in possible_subjects:
        print(f"{key} - {possible_subjects[key]}")

    user_given_subject = int(input("\n"))

    return user_given_subject

def search_for_subject_corresponding_to_user_choice():
    possible_subjects = generate_subject_options()
    subject = option_2_user_input()

    for key in possible_subjects:
        if key == subject:
            subject_name = possible_subjects[key]

    return subject_name

def search_for_number_of_different_class_types(class_type_set: set):
    # jeśli dane zajęcia mają tylko jeden typ nie ma sensu dawać użytkownikowi wybór

    if len(class_type_set) == 1:
        type_choice = 0
    else:
        type_choice = 1

    return type_choice

def create_class_type_dict_for_classes_with_more_than_one_type(class_type_set: set, class_type_dict: dict):
    number_type = 0

    for class_type in class_type_set:
        number_type += 1
        class_type_dict[number_type] = class_type

    return class_type_dict

def give_user_class_type_options(class_type_dict: dict):
    # opcja wybrania wykładu/ćwiczeń/warsztatu/etc dla przedmiotu

    print("\nWybierz formę zajęć, która cię interesuje:")
    for key in class_type_dict:
        print(f"{key} - {class_type_dict[key]}")
    
    user_given_type = int(input("\n"))

    return user_given_type

def search_for_class_type_corresponding_to_user_choice(class_type_dict: dict):
    class_type = give_user_class_type_options(class_type_dict)

    # szukanie typu odpowiadającemu wybranemu numerowi
    for key in class_type_dict:
        if key == class_type:
            class_type_name = class_type_dict[key]

    return class_type_name

def get_class_type_and_subject_name():
    class_type_set = set()
    class_type_dict = {}
    subject = search_for_subject_corresponding_to_user_choice()

    list_to_set_specified(class_type_list, class_type_set, subject_list, subject)
    type_choice = search_for_number_of_different_class_types(class_type_set)

    if type_choice == 1:
        create_class_type_dict_for_classes_with_more_than_one_type(class_type_set, class_type_dict)
        class_type = search_for_class_type_corresponding_to_user_choice(class_type_dict)
        class_type_str = f", {class_type}"
    else:
        class_type = list(class_type_set)[0]
        class_type_str = ""

    return class_type, subject, class_type_str

def search_for_closest_class_for_given_subject(subject: str, class_type: str):
    full_start = final_datetime_list_conversion(True)

    # szukanie najbliższej przyszłej daty podczas której zaczyna się dany przedmiot w danej formie
    dates_after = []

    for i in range(len(subject_list)):
        if (subject_list[i] == subject) and (class_type_list[i] == class_type):
            for j in range(len(full_start[i])):
                if full_start[i][j] > current_time:
                    dates_after.append(full_start[i][j])

    ordered_dates_after = sorted(dates_after)
    closest_date = datetime.strftime(ordered_dates_after[0], "%d/%m/%Y %H:%M")

    return closest_date


def user_chose_option_2():
    class_type_and_subject = get_class_type_and_subject_name()
    (class_type, subject, class_type_str) = class_type_and_subject

    date = search_for_closest_class_for_given_subject(subject, class_type)

    print("")
    print(f"Najbliższe zajęcia \"{subject}{class_type_str}\" odbędą się dnia {date}.\n\n")


main_part_instructions()

while True:
    busy = 0 # inicjalizacja zmiennej, która określa czy osoba jest zajęta
    user_choice = input()
    
    try:
        if user_choice == "1":
            user_chose_option_1()
        elif user_choice == "2": 
            user_chose_option_2()
            
        elif user_choice == "3":
            print(f"\nPodaj datę (format: dd/mm/yyyy).\
                  \nPrzykład: {current_date_str}\
                  \nLub wpisz \"dzisiaj\" albo \"jutro\".\n")
            user_given_date = input()

            # jeśli użytkownik chce bazować na obecnej/jutrzejszej dacie
            if user_given_date == "dzisiaj":
                user_given_date = current_date
            elif user_given_date == "jutro":
                user_given_date = current_time + timedelta(days = 1)
            else:
                user_given_date = datetime.strptime(user_given_date, "%d/%m/%Y")

            # inicjalizacja potrzebnych list
            class_full_list = []
            class_type = []
            classes_start = []
            classes_end = []
            subject_name = []
            location_name = []
            if_class_day = 0

            # szukanie dat/godzin zajęć dla sprecyzowanego dnia
            for i in range(len(subject_list)):
                for j in range(len(full_start[i])):
                    if user_given_date.date() == full_start[i][j].date():
                        if_class_day = 1 # w podanym dniu są zajęcia

                        # tworzenie wielowymiarowej listy i list z informacjami o zajęciach
                        class_full_list.append([])
                        subject_name.append(subject_list[i])
                        class_type.append(class_type_list[i])
                        location_name.append(location[i])
                        classes_start.append(full_start[i][j])
                        classes_end.append(full_end[i][j])

            # dodawanie informacji o poszczególnych zajęciach do wewnętrznych list
            # w formacie [nazwa przedmiotu, forma zajęć etc] żeby łatwo zrobić z całości tabelkę
            for i in range(len(class_full_list)):
                class_full_list[i].append(subject_name[i])
                class_full_list[i].append(class_type[i])
                class_full_list[i].append(location_name[i])
                class_full_list[i].append(classes_start[i])
                class_full_list[i].append(classes_end[i])

            # sortowanie zewnętrznej listy wg. indeksu obiektu z zewnętrznej listy, czyli godziny rozpoczęcia zajęć
            sorted_class_full_list = sorted(class_full_list, key=itemgetter(3))

            # konwersja datetime na str by pokazywał tylko godziny i minuty
            for i in range(len(sorted_class_full_list)):
                sorted_class_full_list[i][3] = "{:d}:{:02d}".format(sorted_class_full_list[i][3].hour, sorted_class_full_list[i][3].minute)
                sorted_class_full_list[i][4] = "{:d}:{:02d}".format(sorted_class_full_list[i][4].hour, sorted_class_full_list[i][4].minute)

            # jeśli są zajęcia, tworzymy tabelkę
            if if_class_day == 1:
                table = [["Przedmiot", "Forma zajęć", "Miejsce", "Godzina rozpoczęcia", "Godzina zakończenia"]]

                for i in range(len(sorted_class_full_list)):
                    table.append(sorted_class_full_list[i])

                print("")
                print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
                print("")
                print("")

            else:
                print("\nNie masz wtedy zajęć.\n")

        elif user_choice == "6": # wyszukaj wolne sloty w podanym terminie
            # take input from the user (lets say look at a given day + option to look at specific hours)
            # search for 
            print("\nPodaj dzień, który chcesz sprawdzić (format dd/mm/yyyy).\n")
            user_day = input()
            print("\nPodaj przedział godzinowy (jeśli chcesz zobaczyć wolne sloty dla całego dnia, napisz \"brak\").\
                  \nPrzykład: 12:30 - 16:00\n")
            user_hours = input()

            # make this into a function
            if user_hours != "brak":
                user_hours = user_hours.split(" - ")

                for i in range(len(user_hours)):
                    user_hours[i] = user_day + " " + user_hours[i]
                    user_hours[i] = datetime.strptime(user_hours[i], "%d/%m/%Y %H:%M")
                
                start_busy_time = []
                end_busy_time = []

                for i in range(len(full_start)): # consider making a function for looking for days
                    for j in range(len(full_start[i])):
                        if full_start[i][j].date == user_hours[0].date:
                            start_busy_time.append(full_start[i][j])
                            end_busy_time.append(full_end[i][j])

                start_busy_time = sorted(start_busy_time)
                end_busy_time = sorted(end_busy_time)



        else: # użytkownik wpisuje coś innego niż 1, 2, 3 etc.
            raise ValueError()
        
    # daje valueerror jesli uzytkownik niewłaściwy format, albo jeśli podana data w ogóle nie może istnieć
    # albo jeśli wybierając opcje użytkownik wpisuje coś nieuwzględnionego
    except ValueError: 
        print("")
        print("Przeczytaj uważnie instrukcje i spróbuj ponownie.\n\n")