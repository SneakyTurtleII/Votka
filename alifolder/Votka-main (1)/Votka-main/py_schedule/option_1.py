from main_functions import *

def option_1_user_input():
    user_input = input(f"\nPodaj datę i godzinę w następującym formacie:\ndd/mm/yyyy hours:minutes\nPrzykład: {current_time_str}\
                                    \nLub wpisz \"teraz\", jeśli interesuje cię obecna data.\n\n")
    
    return user_input

def check_if_during_datetime_there_is_event(datetime_date: datetime):
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

def if_next_class_found(busy: bool, next_class, datetime_date: datetime):
    if busy == True:
        hours_until = datediff_to_h_min(next_class, datetime_date)
        next_class_str = "{:d}:{:02d}".format(next_class.hour, next_class.minute)
        string = f"Następne najbliższe zajęcia tego dnia są o godzinie {next_class_str}, {hours_until} od teraz."
    else:
        string = "Po podanej godzinie nie masz już zajęć tego dnia."
    
    return string

def find_next_class_if_no_class_when_specified(datetime_date: datetime):
    busy = 0 # inicjalizacja zmiennej, która określa czy osoba będzie miała zajęcia po danej godzinie w określonym dniu
    next_class = ""

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
        
    return if_next_class_found(busy, next_class, datetime_date)

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