from dad_functions import *

def parse_input_to_datetime(desired_date):

    # "today" and "tomorrow" are special strings
    if (compare_strings_case_insensitive(desired_date, "today")):
        desired_date = datetime_to_str(current_datetime, "date")

    if (compare_strings_case_insensitive(desired_date, "tomorrow")):
        desired_date = datetime_to_str(current_datetime + timedelta(days=1), "date")
        
    try:
        desired_date = str_to_datetime(desired_date, "date")
    except ValueError or TypeError:
        print("I think that's not the right format!")

    return desired_date

def get_schedule_on_day(desired_date, message_to_send):

    class_found = False
    for i in range(num_entries):
        if (compare_dates_only(desired_date, s_f_date_list[i])):
            Subject = f"{s_subject_list[i]:10}"
            Start_time = datetime_to_str(s_f_start_datetime_list[i], "time")
            End_time = datetime_to_str(s_f_end_datetime_list[i], "time")
            message_to_send.append(f'''{Subject} | {Start_time} to {End_time}\n''')
            class_found = True

    return class_found

def DaySchedule():

    print(f"Enter a date, example: {example_date}\n")
    desired_date = input()
    class_found = False

    desired_date = parse_input_to_datetime(desired_date)

    message_to_send = []

    class_found = get_schedule_on_day(desired_date, message_to_send)
    
    if (not class_found):
        print("No classes on that day")
    else:
        message_to_send = "".join(message_to_send)
        print(f'''```{message_to_send}```''')