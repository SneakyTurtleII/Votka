from dad_functions import *

def get_next_class(desired_subject):
    valid_subject = 0
    for i in range(num_entries):
        if ( (compare_strings_case_insensitive(desired_subject, s_subject_list[i])) and (compare_dates_only(current_datetime, s_f_date_list[i], "lesser or equal")) ):
            Subject = s_subject_list[i]
            Date = datetime_to_str(s_f_date_list[i], "date")
            Start_time = datetime_to_str(s_f_start_datetime_list[i], "datetime")
            End_time = datetime_to_str(s_f_end_datetime_list[i], "datetime")
            print(f'''The next {Subject} class is on {Date}, {Start_time} to {End_time}''')
            print(f"That is in {s_f_start_datetime_list[i] - current_datetime}")
            valid_subject = 1
            break
    if (valid_subject == 0):
        print("I wasn't able to find that subject :( what did you do")

def EventSearch():
    desired_subject = input(f"Subjects: \n{nd_subject_list}\n What subject would you like to know about")
    get_next_class(desired_subject)