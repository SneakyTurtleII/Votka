from dad_functions import *

def parse_input_to_datetime(desired_date):
    if (compare_strings_case_insensitive(desired_date, "today")):
        desired_date = datetime_to_str(current_datetime, "date")

    if (compare_strings_case_insensitive(desired_date, "tomorrow")):
        desired_date = datetime_to_str(current_datetime + timedelta(days=1), "date")
        
    try:
        desired_date = str_to_datetime(desired_date, "date")
    except ValueError or TypeError:
        print("I think that's not the right format!")

    return desired_date

def get_available_times(desired_date, message_to_send):
    class_found = False
    for i in range(num_entries):
        if (compare_dates_only(desired_date, s_f_date_list[i])):
            class_found = True
            # s_f_end_datetime_list[i] to s_f_start_datetime_list[i+1], if i+1 matches the current date
            if (compare_dates_only(desired_date, s_f_start_datetime_list[i+1])):
                Free_time_length = datediff_to_h_min(s_f_start_datetime_list[i+1], s_f_end_datetime_list[i])
                Start_time = datetime_to_str(s_f_end_datetime_list[i], "time")
                End_time = datetime_to_str(s_f_start_datetime_list[i+1], "time")
                message_to_send.append(f'''Dad is free for {Free_time_length} from {Start_time} to {End_time}\n''')
            else:
                message_to_send = "".join(message_to_send)
                print(f'''{message_to_send}''')
                print(f'''Dad comes home after {datetime_to_str(s_f_end_datetime_list[i], "time")}''')

    return class_found

def AvailabilitySearch():
    
    class_found = False

    print(f"Enter a date, example: {example_date}\n")
    desired_date = input()
    desired_date = parse_input_to_datetime(desired_date)

    message_to_send = []

    class_found = get_available_times(desired_date, message_to_send)
        
    if (not class_found):
        print("No classes on that day")
