from main_functions import *

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

    user_input = int(input("\n"))

    return user_input

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

def search_for_closest_class_for_given_subject(subject: str, class_type: str, full_start: list):
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

    date = search_for_closest_class_for_given_subject(subject, class_type, full_start)

    print("")
    print(f"Najbliższe zajęcia \"{subject}{class_type_str}\" odbędą się dnia {date}.\n\n")