from dad_functions import *

def parse_input_to_datetime(desired_time):
    # "now" is a special string
    if (compare_strings_case_insensitive(desired_time, "now")):
        desired_time = current_datetime

    # "today" is a special string
    elif (desired_time.lower().startswith("today")):
        time_component = desired_time.split()[1]
        desired_time = datetime_to_str(current_datetime.date(), "date") + " " + time_component
        desired_time = str_to_datetime(desired_time, "datetime")

    # "tomorrow" is a special string
    elif (desired_time.lower().startswith("tomorrow")):
        time_component = desired_time.split()[1]
        desired_time = datetime_to_str(current_datetime.date() + timedelta(days=1), "date") + " " + time_component
        desired_time = str_to_datetime(desired_time, "datetime")

    else:
        try:
            desired_time = str_to_datetime(desired_time, "datetime")
        except ValueError:
            print("I think that's not the right format!")

    return desired_time

def get_class_in_time_slot(desired_time):
    class_found = False
    for i in range(num_entries):
        if (is_time_between(desired_time, s_f_start_datetime_list[i], s_f_end_datetime_list[i])):
            print(f"\nDad is in {s_subject_list[i]}, which ends in {s_f_end_datetime_list[i] - desired_time}")
            class_found = True
    return class_found
        
def get_time_of_next_class(desired_time, class_found, message_to_send):
    more_classes_found = False
    for k in range(num_entries):
        if ( (compare_dates_only(desired_time, s_f_date_list[k])) and (compare_datetime(desired_time, s_f_end_datetime_list[k], "lesser")) ):
            if (more_classes_found == 0):
                if (class_found == 0):
                    print(f"\nNext class is in: {s_f_start_datetime_list[k] - desired_time}")
                print(f"Classes remaining today:")
            Subject = f"{s_subject_list[k]:10}"
            Start_time = datetime_to_str(s_f_start_datetime_list[k], "time")
            End_time = datetime_to_str(s_f_end_datetime_list[k], "time")
            message_to_send.append(f'''{Subject} | {Start_time} to {End_time}\n''')
            more_classes_found = True
    return more_classes_found

def TimeSearch():
    print(f"Enter a time, something like {example_datetime}\n")
    desired_time = input()

    class_found = False
    more_classes_found = False

    desired_time = parse_input_to_datetime(desired_time)

    class_found = get_class_in_time_slot(desired_time)

    message_to_send = []

    more_classes_found = get_time_of_next_class(desired_time, class_found, message_to_send)

    if (not more_classes_found):
        print("Dad has no more classes afterwards.")
    else:
        message_to_send = "".join(message_to_send)
        print(f'''```{message_to_send}```''')

    if (not class_found):
        print("Dad is free at this time. Go nuts!") # + time of next class of the day