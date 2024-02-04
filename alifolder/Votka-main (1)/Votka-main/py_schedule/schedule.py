import numpy as np
from csv import DictWriter
from main_functions import *
from option_1 import *
from option_2 import *
from option_3 import *

# for option 2 what if the event never happens after this day
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
            user_chose_option_3()

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