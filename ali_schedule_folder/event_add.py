from dad_functions import *

def EventAdd():
    with open('dadclasses_copy.csv', 'a', newline = '', encoding = 'utf-8') as dc:

        num_columns = 4
        dc_writer = writer(dc)

        print(f'''Enter an event. Format:\n Subject, Date, Start Time, End Time\
            \n Example: {s_subject_list[1]}, {example_date}, {datetime_to_str(current_datetime, "time")}, {"23:69"}\n''')
        
        row_w = input()
        row_w = row_w.split(", ")

        # csv format: subject, start_date, start_time, end_date, end_time
        # all strings
        # dates in d/m/y, times in hr:min:sec
        # start_date and end_date always the same

        if (len(row_w) != num_columns):
            print(f'''Number of entries do not match. Please make sure entries are separated by ", " \n
            Your entry: {row_w}\nYou entered {len(row_w)} values, I want to see 4 values''')

        subject_w =  row_w[0]
        date_w = row_w[1]
        start_time_w = row_w[2] + ":00" # adding the seconds
        end_time_w = row_w[3] + ":00"

        write_list = [subject_w, date_w, start_time_w, date_w, end_time_w]
        print(write_list)

        print("Are you sure you want to add this to your calendar? Y/N\n")
        write_confirm = input()

        if write_confirm.upper() == "Y":
            dc_writer.writerow(write_list)
            print("Success!")
        else:
            print("It's ok, mistakes happen. Look at you.")