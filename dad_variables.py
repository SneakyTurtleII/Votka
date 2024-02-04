from datetime import datetime
import pandas as pd
from dad_functions import str_to_date_list, str_to_datetime_list, time_to_datetime_list, datetime_to_str

df = pd.read_csv(r"dadclasses_copy.csv",
    delimiter = ",",
    usecols = ["Subject", "Start Date", "Start Time", "End Time"],
    dtype = None)

subject_list =  df["Subject"].values.tolist() # 'COM S 227', 'COM S 227', 'COM S 227', 'COM S 227'
s_subject_list = []
nd_subject_list = [*set(subject_list)]

# list of dates where I have classes
date_list = df["Start Date"].values.tolist() # '19/1/2023', '26/1/2023', '31/1/2023', '2/2/2023', '7/2/2023'
f_date_list = []
str_to_date_list(date_list, f_date_list)
s_f_date_list = sorted(f_date_list)

# start time of classes
start_time_list = df["Start Time"].values.tolist() # '08:50:00', '08:50:00', '08:50:00', '08:50:00', '08:50:00'
start_datetime_list = time_to_datetime_list(date_list, start_time_list)
f_start_datetime_list = []
str_to_datetime_list(start_datetime_list, f_start_datetime_list)
s_f_start_datetime_list = sorted(f_start_datetime_list)

# end time of classes 
end_time_list = df["End Time"].values.tolist() # '09:40:00', '09:40:00', '09:40:00', '09:40:00', '09:40:00', '09:40:00'
end_datetime_list = time_to_datetime_list(date_list, end_time_list)
f_end_datetime_list = []
str_to_datetime_list(end_datetime_list, f_end_datetime_list)
s_f_end_datetime_list = sorted(f_end_datetime_list)

# useful when iterating over lists, length of most lists unless they are nd or otherwise
num_entries = len(subject_list)

# sorting subject list
for i in range(num_entries):
    for j in range (num_entries):
        if (f_start_datetime_list[j] == s_f_start_datetime_list[i]):
            s_subject_list.append(subject_list[j])

current_datetime = datetime.now()
example_datetime = datetime_to_str(current_datetime, "datetime")

current_date = datetime.now().date()
example_date = datetime_to_str(current_datetime, "date")