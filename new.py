import pandas as pd
from datetime import datetime, date, timedelta
from tabulate import tabulate
from operator import itemgetter
import numpy as np
from csv import DictWriter

def append_hour(date_list, hour_list, ending_list):
    for i in range(len(date_list)):
        list_object = date_list[i] + " " + hour_list[i]
        ending_list.append(list_object)

def datetime_list_conversion(beginning_list, ending_list):
    for list_object in beginning_list:
        list_object =  datetime.strptime(list_object, "%d.%m.%Y %H:%M")
        ending_list.append(list_object)

def datediff_to_h_min(end_date: datetime, start_date: datetime):
    h_min = end_date - start_date
    h_min = str(h_min).replace(":", " ")
    if ("00 00") in h_min:
        h_min = h_min.replace(" 00 00", "h")
    else:
        h_min = h_min.replace(" 00", "")
        h_min = h_min.replace(" ", "h ") + "min"
    return h_min

df = pd.read_csv(r"momclasses.csv",
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

# data zajęć w kolumnie "pierwszy dzień" + godzina rozpoczęcia/zakończenia
start_time_start_day = []
end_time_start_day = []
# to samo, ale konwersja na datetime
start_time_start_day_datetime = [] 
end_time_start_day_datetime = []
# data zajęć w kolumnie "ostatni dzień" + godzina rozpoczęcia/zakończenia
start_time_end_day_datetime = []
end_time_end_day_datetime = []
# użyte potem do znalezienia dat zajęć od start_day do end_day
weeks = []

current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M")
current_time = datetime.now()

# godziny rozpoczęcia, zakończenia zajęć dodane do start_day
append_hour(start_day, start_time, start_time_start_day)
append_hour(start_day, end_time, end_time_start_day)

# utworzenie dwuwymiarowej listy dla kolumny end_day
# + co jeśli end_day == missing value albo jest takie samo jak start_day
for i in range(len(end_day)):
    if pd.isna(end_day[i]) or end_day[i] == start_day[i]:
        start_time_end_day_datetime.append("N/A")
        end_time_end_day_datetime.append("N/A")
        weeks.append(0)
    # wzięcie start_day[i] i end_day[i], policzenie ile jest między nimi tygodni (start_day wliczone, więc nie trzeba potem robić insert)
    # musi być w datetime
    else:
        x = datetime.strptime(end_day[i], "%d.%m.%Y")
        y = datetime.strptime(start_day[i], "%d.%m.%Y")
        week_count = (abs(x - y).days) // 7
        weeks.append(week_count)

        # tworzenie dwuwymiarowej listy tak aby indeksy dla każdej zewnętrznej listy nadal odpowiadały wierszom w tabeli csv
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

# str na datetime dla start_day zajęć + godziny rozpoczęcia, zakończenia zajęć
datetime_list_conversion(start_time_start_day, start_time_start_day_datetime)
datetime_list_conversion(end_time_start_day, end_time_start_day_datetime)

# łączenie dni początkowych i końcowych w dwie dwuwymiarowe listy, jedna z godzinami rozpoczęcia i druga zakończenia
full_start_time_datetime = []
full_end_time_datetime = []

for i in range(len(start_time_start_day_datetime)):
    if start_time_end_day_datetime[i] == "N/A":
        full_start_time_datetime.append([start_time_start_day_datetime[i]])
        full_end_time_datetime.append([end_time_start_day_datetime[i]])
    else:        
        full_start_time_datetime.append(start_time_end_day_datetime[i])
        full_end_time_datetime.append(end_time_end_day_datetime[i])

# część główna
print("Wybierz jedną z poniższych opcji:\n1 - podaje jakie masz zajęcia w podanym dniu o danej godzinie\
      \njeśli nie masz wtedy zajęć, podaje kiedy masz następne zajęcia tego samego dnia\
      \n2 - podaje kiedy masz najbliższe zajęcia z danego przedmiotu (w oparciu o obecną datę lub sprecyzowaną)\
      \n3 - podaje zaplanowane wydarzenia na dany dzień\
      \n4 - dodaje wydarzenie\
      \n5 - usuwa wydarzenie\
      \n6 - wyszukaj wolne sloty w podanym terminie\
      \n7 - podaje ile w danym okresie czasowym masz zaplanowanych wydarzeń\
      \nhelp - ponownie wyświetla listę opcji\
      \nexit - żeby zakończyć program\n")

while True:
    user_choice = input()
    
    try:
        if user_choice == "1":
            busy = 0 # inicjalizacja zmiennej, która określa czy osoba jest zajęta

            user_given_date = input(f"\nPodaj datę i godzinę w następującym formacie:\ndd/mm/yyyy hours:minutes\nPrzykład: {current_time_str}\
                                    \nLub wpisz \"teraz\", jeśli interesuje cię obecna data.\n\n")
            
            # jeśli użytkownik chce bazować na obecnej dacie i godzinie
            if user_given_date == "teraz":
                user_given_date = current_time_str
            user_given_date += ":00"
            
            user_given_date = datetime.strptime(user_given_date, "%d/%m/%Y %H:%M:%S")

            # sprawdzanie czy podczas podanej daty i godziny są zajęcia 
            for i in range(len(start_day)):
                for j in range(len(full_start_time_datetime[i])):
                    if (user_given_date <= full_end_time_datetime[i][j]) and (user_given_date >= full_start_time_datetime[i][j]):
                        busy = 1
                        subject_name = subject_list[i]
                        location_name = location[i]
                        class_type_name = f", {class_type_list[i]}"
                        hours_left = datediff_to_h_min(full_end_time_datetime[i][j], user_given_date)

            if busy == 1:
                # sprecyzowanie formy zajęć, jeśli dany przedmiot ma tylko jedną formę, str class_type_name jest pusty
                class_type_set = set()

                for i in range(len(subject_list)):
                    if subject_list[i] == subject_name:
                        class_type_set.add(class_type_list[i])

                if len(class_type_set) == 1:
                    class_type_name = ""

                print("")
                print(f"W tym czasie masz zajęcia \"{subject_name}{class_type_name}\" w {location_name}. Te zajęcia skończą się w {hours_left} od sprecyzowanego czasu.\n\n")
            else:
                possible_next_class = []
                busy = 0 # inicjalizacja zmiennej, która określa czy osoba będzie miała zajęcia po danej godzinie w określonym dniu
                
                for i in range(1, 21):
                    time_diff = user_given_date + timedelta(hours = i)
                    possible_next_class.append(time_diff)
                    if time_diff > user_given_date.replace(hour = 20): # po 20 nie ma zajęć które dopiero się zaczynają
                        break
                
                for date in possible_next_class:
                    for i in range(len(start_day)):
                        for j in range(len(full_start_time_datetime[i])):
                            if (date <= full_end_time_datetime[i][j])\
                                and (date >= full_start_time_datetime[i][j]):
                                busy = 1 # znaleziono zajęcia
                                next_class = full_start_time_datetime[i][j]
                                break
                        if busy == 1: # przerwanie pętli, bo znaleziono najbliższe zajęcia
                            break
                    if busy == 1:
                        break
                
                if busy == 1:
                    hours_until = datediff_to_h_min(next_class, user_given_date)
                    next_class = "{:d}:{:02d}".format(next_class.hour, next_class.minute)
                    string = f"Następne najbliższe zajęcia tego dnia są o godzinie {next_class}, {hours_until} od teraz."
                else:
                    string = "Po podanej godzinie nie masz już zajęć tego dnia."
                
                print("")
                print(f"Nie masz wtedy zajęć. {string}\n\n")

        elif user_choice == "2": 
            # program ​pobiera tematy z pliku csv, więc jeśli plik zostanie zmieniony, wszystko nadal działa
            subject_set = set(subject_list)
            subject_pool_dict = {} # żeby móc dopasować wybrany numer do odpowiedniego przedmiotu
            number_subject = 0
                
            for subject in subject_set:
                number_subject += 1
                subject_pool_dict[number_subject] = subject

            print("\nWybierz przedmiot, który cię interesuje:")        
            for key in subject_pool_dict:
                print(f"{key} - {subject_pool_dict[key]}")
            user_given_subject = int(input("\n"))
            
            # szukanie przedmiotu odpowiadającemu wybranemu numerowi
            for key in subject_pool_dict:
                if key == user_given_subject:
                    user_given_subject = subject_pool_dict[key]
            
            # opcja wybrania wykładu/ćwiczeń/warsztatu/etc dla przedmiotu
            class_type_set = set()
            class_type_pool_dict = {}
            number_type = 0

            for i in range(len(subject_list)):
                if subject_list[i] == user_given_subject:
                    class_type_set.add(class_type_list[i])

            # jeśli dane zajęcia mają tylko jeden typ nie ma sensu dawać użytkownikowi wybór
            if len(class_type_set) == 1:
                type_choice = 0
            else:
                type_choice = 1

            if type_choice == 1:
                for class_type in class_type_set:
                    number_type += 1
                    class_type_pool_dict[number_type] = class_type
                
                print("\nWybierz formę zajęć, która cię interesuje:")
                for key in class_type_pool_dict:
                    print(f"{key} - {class_type_pool_dict[key]}")
                user_given_type = int(input("\n"))

                # szukanie typu odpowiadającemu wybranemu numerowi
                for key in class_type_pool_dict:
                    if key == user_given_type:
                        user_given_type = class_type_pool_dict[key]

                class_type_name = f", {user_given_type}"
            else:
                user_given_type = list(class_type_set)[0]
                class_type_name = ""

            # szukanie najbliższej przyszłej daty podczas której zaczyna się dany przedmiot w danej formie
            dates_after = []

            for i in range(len(subject_list)):
                if (subject_list[i] == user_given_subject) and (class_type_list[i] == user_given_type):
                    for j in range(len(full_start_time_datetime[i])):
                        if full_start_time_datetime[i][j] > current_time:
                            dates_after.append(full_start_time_datetime[i][j])

            ordered_dates_after = sorted(dates_after)
            closest_date = datetime.strftime(ordered_dates_after[0], "%d/%m/%Y %H:%M")

            print("")
            print(f"Najbliższe zajęcia \"{user_given_subject}{class_type_name}\" odbędą się dnia {closest_date}.\n\n")

        elif user_choice == "3":
            print(f"\nPodaj datę i godzinę w następującym formacie:\ndd/mm/yyyy hours:minutes\nPrzykład: {current_time_str}\
                    \nLub wpisz \"teraz\" albo \"jutro\".\n")
            user_given_date = input()

            # jeśli użytkownik chce bazować na obecnej/jutrzejszej dacie
            if user_given_date == "teraz":
                user_given_date = current_time_str
            elif user_given_date == "jutro":
                user_given_date = current_time + timedelta(days = 1)
                user_given_date = datetime.strftime(user_given_date, "%d/%m/%Y %H:%M")
            user_given_date += ":00"
            
            user_given_date = datetime.strptime(user_given_date, "%d/%m/%Y %H:%M:%S")

            # inicjalizacja potrzebnych list
            class_full_list = []
            class_type = []
            classes_start = []
            classes_end = []
            subject_name = []
            location_name = []
            busy = 0

            # szukanie dat/godzin zajęć dla sprecyzowanego dnia
            for i in range(len(subject_list)):
                for j in range(len(full_start_time_datetime[i])):
                    if user_given_date.date() == full_start_time_datetime[i][j].date():
                        busy = 1 # w podanym dniu są zajęcia

                        # tworzenie wielowymiarowej listy i list z informacjami o zajęciach
                        class_full_list.append([])
                        subject_name.append(subject_list[i])
                        class_type.append(class_type_list[i])
                        location_name.append(location[i])
                        classes_start.append(full_start_time_datetime[i][j])
                        classes_end.append(full_end_time_datetime[i][j])

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
            if busy == 1:
                table = [["Przedmiot", "Forma zajęć", "Miejsce", "Godzina rozpoczęcia", "Godzina zakończenia"]]

                for i in range(len(sorted_class_full_list)):
                    table.append(sorted_class_full_list[i])

                print("")
                print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
                print("")
                print("")

        elif user_choice == "4":
            user_title = input("\nŻeby dodać nowe wydarzenie, najpierw wpisz tytuł wydarzenia: ")
            user_type = input("\nWpisz typ wydarzenia (jeśli dodajesz przedmiot do planu zajęć, wpisujesz nazwę formy zajęć - np. CWA).\
                              \nJeśli chcesz, żeby to pole pozostało puste, wpisz \"brak\": ")
            user_start_day = input("\nWpisz dzień, w którym wydarzenie się rozpoczyna (format dd/mm/yyyy): ")
            datehour_test = datetime.strptime(user_start_day, "%d/%m/%Y") # test

            user_end_day = input("\nJeśli wydarzenie się powtarza co tydzień o tej samej godzinie, wpisz dzień, w którym się kończy (format dd/mm/yyyy).\
                                 \nJeśli wydarzenie trwa tylko jeden dzień, wpisz \"brak\": ")
            if user_end_day != "brak": # test
                datehour_test = datetime.strptime(user_end_day, "%d/%m/%Y")

            user_start_hour = input("\nWpisz godzinę rozpoczęcia wydarzenia (format hours:minutes): ")
            datehour_test = datetime.strptime(user_start_hour, "%H:%M") # test

            user_end_hour = input("\nWpisz godzinę zakończenia wydarzenia (format hours:minutes): ")
            datehour_test = datetime.strptime(user_end_hour, "%H:%M") # test

            user_location = input("\nWpisz miejsce, w którym wydarzenie ma mieć miejsce.\
                                  \nJeśli chcesz, żeby to pole pozostało puste, wpisz \"brak\": ")


            column_names = ["Typ", "Tytuł", "Pierwszy dzień", "Ostatni dzień", "Ogłoszony początek", "Ogłoszony koniec", "Miejsce"]

            with open('event.csv', 'a') as file_object:
                dictwriter_object = DictWriter(file_object, fieldnames = column_names)

                """ dictwriter_object.writerow() """

                file_object.close()

            df = df.replace('brak', np.nan)

            # remember to deal with NaN when looking for types in other options

        elif user_choice == "exit":
            exit()

        else: # użytkownik wpisuje coś innego niż 1, 2, 3 etc.
            raise ValueError()
        
    # daje valueerror jesli uzytkownik niewłaściwy format, albo jeśli podana data w ogóle nie może istnieć
    # albo jeśli wybierając opcje użytkownik wpisuje coś nieuwzględnionego
    except ValueError: 
        print("")
        print("Przeczytaj uważnie instrukcje i spróbuj ponownie.\n\n")