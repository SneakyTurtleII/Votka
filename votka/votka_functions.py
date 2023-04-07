def time_24hr(hour):
    if (hour > 23): # because no such thing as 24:12
        hour = hour - 24
    if (hour < 0):
        hour = hour + 24
    return hour

def log_fn(str_input, file_input):
    print(str_input)
    file_input.write(f"{str_input}\n")
    file_input.flush()

def prediction_linear(x, slope, intercept):
    return (slope * x + intercept)
