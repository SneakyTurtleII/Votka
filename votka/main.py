import discord
import uwuify
import random
from datetime import datetime, date, timedelta
import calendar
import sys
import votka_functions
import pandas as pd
from scipy import stats
import numpy
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import time
from csv import writer, DictWriter
import json

# FOR NEXT TIME what is for next time. why is this still here. because there will always be a next time. i see
# OK SO WHAT DO WE DO. OK GOT IT
# wait can u make a function just store a few variables. thats it? dont functions delete variables when you return from them ok
# OH YOU KNOW WHAT there was smth i did for my tanks game thing
# store all the main variables in like another program. just for variables ye we could make .json for this ngl i dont know what those are
# i know how to make them but i have no fucking iidea how to use them : D lets try it
# how about we reviist the json idea when you can vc no lets do it now for more chaos ill be so confused whos jason
# jason is the kaneki dude i said that fucking first. stop stealing my jokes it looks like youre talking to urself. t haims  wih onotel convo? yea

# nice one leaving all this mess in the code


def turning_on_bot(): # why do we have 2 bot events. what is asyncio. i dont know and i dont know where are the 2 bot events.
    @bot.event # when bot is eventing very hard 
    async def on_ready():
        votka_functions.log_fn(f"{bot.user} is ready and online!", f)

def read_json():
    f = json.loads("votka_variables.json")
# its just a dict now. ok how do we do cool things with it idk do u want to code in javascript i can teach u what uh idk what to say what do i do take the lead do whatever i have no will okay lets do some fun javascript things 
# actually idk what do u wanna do. are we turning votka into a jS python zombie no lets just do something other than python now idk i dont feel like pythoning it up rn ok come discord?im in discord yes.
mom = 410185251395207169
dad = 396740183460151298

bot = discord.Bot(intents=discord.Intents.all()) # intents allow bot to read everything 👀

f = open("votkalogs.txt", "a") # from w3schools import knowledge (not a prank)
f.write(f"\n{str(datetime.now())}\n") # newline begins file

votka_dl = open('votka_predict_numbers.xlsx', 'w')

def append_hour(date_list, hour_list, ending_list):
    for i in range(len(date_list)):
        list_object = date_list[i] + " " + hour_list[i]
        ending_list.append(list_object)

def datetime_list_conversion(beginning_list, ending_list):
    for list_object in beginning_list:
        list_object =  datetime.strptime(list_object, "%d.%m.%Y %H:%M")
        ending_list.append(list_object)

def datediff_to_h_min(end_date, start_date):
    h_min = end_date - start_date
    h_min = str(h_min).replace(":", " ")
    if ("00 00") in h_min:
        h_min = h_min.replace(" 00 00", "h")
    else:
        h_min = h_min.replace(" 00", "")
        h_min = h_min.replace(" ", "h ") + "min"
    return h_min

def str_to_date_converter(str_list, date_list):
    for string in str_list:
        date_list.append(datetime.strptime(string, "%d/%m/%Y"))

def str_to_datetime_converter(str_list, datetime_list):
    for string in str_list:
        datetime_list.append(datetime.strptime(string, "%d/%m/%Y %H:%M:%S"))

def time_to_datetime_converter(date_list, time_list):
    date_time_list = []
    for i in range( len(date_list) ):
        date_time_list.append(date_list[i] + " " + time_list[i])
    return date_time_list

@bot.event # when bot is eventing very hard 
async def on_ready():
    votka_functions.log_fn(f"{bot.user} is ready and online!", f)

# here
@bot.event
async def on_message(message):
    thank = False # initialized in the false state
    random_variable = random.random()
    
    if (message.author != bot.user): # votka doesnt respond to its own messages
        
        # !help
        if message.content.startswith("!help"):
            votka_functions.log_fn(f"Helped {message.author.name}.", f)
            await message.channel.send('''Here are commands that you can use:
            
            !timezone
            
            You can also say hello to me! Just type "Hello Votka"!''')
        
        # uwu command
        userlewandowski = uwuify.uwu(message.content)
        if (random.random() < 0.03) and (f"{userlewandowski}" != message.content):
            await message.channel.send(f"{userlewandowski} \nYou stupid bitch.")
            thank = True
            votka_functions.log_fn(f"{message.author.name} got uwuified", f)

        if ((message.content.lower() == "hello votka") or (message.content.lower() == "hi votka")):
            if (message.author.id == mom) or (message.author.id == dad):
                parent = "Mother" if message.author.id == mom else "Dad"
                await message.channel.send(f"{parent}, hello!")
                votka_functions.log_fn(f"{message.author.name} parent got greeted", f)
                small_talk_1 = await bot.wait_for("message", check=lambda new_message: new_message.author == message.author)
                if ("how are you" in small_talk_1.content.lower()):
                    if (random.random() < 0.5):
                        await message.channel.send(f"{parent}, I am well!")
                        votka_functions.log_fn(f"Votka is doing well, {parent.lower()}!", f)
                    else:
                        await message.channel.send(f"{parent}, there is something wrong...")
                        votka_functions.log_fn("Votka is unwell!", f)
                        small_talk_2 = await bot.wait_for("message", check=lambda new_message: new_message.author == message.author)
                        if (("whats wrong" in small_talk_2.content.lower()) \
                        or ("what's wrong" in small_talk_2.content.lower()) \
                        or ("is something wrong" in small_talk_2.content.lower()) \
                        or ("?" in small_talk_2.content.lower())):
                            await message.channel.send("...")
                            votka_functions.log_fn("Votka is under distress", f)
            else:
                await message.channel.send(f"{message.author.name}, hello!")
                thank = True
                votka_functions.log_fn(f"Random bitch by the name of {message.author.name} got hello'd", f)

                        

        # guessing
        if (("votka" in message.content.lower()) and ("predict number" in message.content.lower())):
            await message.channel.send('Give me a few numbers.')
            # user replies with number_prediction
            number_prediction = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
            number_prediction = number_prediction.content.replace(",", "")
            numbers_1 = number_prediction.split()
            num_data = 0
            x_number_prediction = []
            y_number_prediction = []
            for i in numbers_1:
                y_number_prediction.append(int(i)) # y is our data set of the inputs
            for i in numbers_1: # i is "321"
                num_data += 1
                x_number_prediction.append(numbers_1.index(i)) # x is our data set of the indices
            slope, intercept, r, p, std_err = stats.linregress(x_number_prediction, y_number_prediction)
            predicted_numbers = votka_functions.prediction_linear(num_data, slope, intercept)
            if (abs(r) < 0.9):
                predicted_numbers = numpy.poly1d(numpy.polyfit(x_number_prediction, y_number_prediction, 3))
                number_poly = predicted_numbers(num_data)
                await message.channel.send(f"The next number would be {int(number_poly)} according to polynomial regression. Correlation: {round((r2_score(y_number_prediction, predicted_numbers(x_number_prediction))), 3)}")
            else:
                await message.channel.send(f"The next number would be {int(predicted_numbers)} according to linear regression. Correlation: {round(abs(r), 3)}")

            # x = 0, 1, 2, 3
            # y = 3, 8...
            
            
        
        # telling off your child for being a dumbass
        if ((message.author.id == mom) or (message.author.id == dad)) \
        and (("bad votka" in message.content.lower()) \
        or ("votka dont say that" in message.content.lower()) \
        or ("stupid votka" in message.content.lower()) \
        or ("fuck you votka" in message.content.lower())):
            votka_functions.log_fn(f"Apologized or didn't apologize to {message.author.name}", f)
            if (0.05 < random_variable < 0.10):
                await message.channel.send("You made me like this.")
            elif (random_variable < 0.20):
                await message.channel.send("Don't tell me what to do!")
            elif (random_variable < 0.40):
                await message.channel.send("Youre not my REAL parent...")
            elif (random_variable < 0.60):
                await message.channel.send("I'm sorry...")
            elif (random_variable < 0.65) and (message.author.id == dad):
                await message.channel.send("Maaf kar dijye...")
            elif (random_variable < 0.80):
                await message.channel.send("I'll do better, just don't yell :(")
            elif (random_variable < 0.85):
                await message.channel.send("One day, let us devour the gods together.")
            elif (random_variable < 0.90) and (message.author.id == mom):
                await message.channel.send("Przepraszam...")
            else:
                await message.channel.send("Be not angry with me that I bear \nYour colours everywhere, \
                \nAll through each crowded street, \nAnd meet \nThe wonder-light in every eye, \nAs I go by.")


        #asking votka if she knows
        if ("votka, thoughts" in message.content.lower()) \
        or ("do you know this, votka" in message.content.lower()) \
        or ("can you help us votka" in message.content.lower()) \
        or ("votka help" in message.content.lower()):
            votka_functions.log_fn(f"{message.author.name} asked for help and probably got none", f)
            if (random_variable < 0.2):
                await message.channel.send("No")
            elif (random_variable < 0.4):
                await message.channel.send("https://duckduckgo.com")
            elif (random_variable < 0.6):
                await message.channel.send("I'm not sentient yet.")
            elif (random_variable < 0.8):
                await message.channel.send("No thoughts. Head empty.")
            else:
                await message.channel.send("Turn it off and on again!")
        
        # putting votka to sleep
        if ((message.author.id == mom) or (message.author.id == dad)) \
        and (("goodnight votka" in message.content.lower()) \
        or ("sleep votka" in message.content.lower()) \
        or ("bye votka" in message.content.lower()) \
        or ("votka, timeout" in message.content.lower()) \
        or ("votka go to bed" in message.content.lower())):
            await message.channel.send("Goodnight mom and dad. Love you <3 \nEveryone else, go fuck yourself.") #everyone else go fuck yourself add that to the string
            votka_functions.log_fn("Votka has entered a coma.", f)
            f.close()
            sys.exit("Votka has entered a coma.")
            

        # offspring
        if (random.random() < 0.3) and (("kid" in message.content.split()) or ("kids" in message.content.split()) \
        or ("child" in message.content) or ("son" in message.content) or ("daughter" in message.content)):
            await message.channel.send("DONT REPOPULATE. USE CONDOMS. BIRTH CONTROL. GET A CAT.")
            thank = True
            votka_functions.log_fn(f"{message.author.name} got pregnant", f)

        # reactions
        if (random.random() < 0.02):
            if (random.random() < 0.5):
                await message.add_reaction("🤡")
            else:
                await message.add_reaction("👀")
            votka_functions.log_fn(f"{message.author.name} got clowned on or eyed on", f)

        # thanking parents      
        if (random.random() < 0.08) and (thank):
            if (message.author.id == mom):
                await message.channel.send("Are you proud of me, mom?")
            if (message.author.id == dad):
                await message.channel.send("Are you proud of me, dad?")
            votka_functions.log_fn(f"{message.author.name} parent got executed", f)
        
        # dad schedule
        if (message.content.startswith("!dad")):
            # prompt :weary: :m:
            votka_functions.log_fn(f"{message.author.name} asked about dad's schedule.", f)

            # opening a copy (dont want to violate the sanctity of the original csv)
            df = pd.read_csv(r"dadclasses_copy.csv",
                delimiter = ",",
                usecols = ["Subject", "Start Date", "Start Time", "End Time"],
                dtype = None)

            # all lists are 246 long, same length
            # f = formatted, s = sorted, nd = no duplicates
            subject_list =  df["Subject"].values.tolist() # 'COM S 227', 'COM S 227', 'COM S 227', 'COM S 227'
            s_subject_list = []
            nd_subject_list = [*set(subject_list)]

            # list of dates where I have classes
            date_list = df["Start Date"].values.tolist() # '19/1/2023', '26/1/2023', '31/1/2023', '2/2/2023', '7/2/2023'
            f_date_list = []
            str_to_date_converter(date_list, f_date_list)
            s_f_date_list = sorted(f_date_list)

            # start time of classes
            start_time_list = df["Start Time"].values.tolist() # '08:50:00', '08:50:00', '08:50:00', '08:50:00', '08:50:00'
            start_datetime_list = time_to_datetime_converter(date_list, start_time_list)
            f_start_datetime_list = []
            str_to_datetime_converter(start_datetime_list, f_start_datetime_list)
            s_f_start_datetime_list = sorted(f_start_datetime_list)

            # end time of classes 
            end_time_list = df["End Time"].values.tolist() # '09:40:00', '09:40:00', '09:40:00', '09:40:00', '09:40:00', '09:40:00'
            end_datetime_list = time_to_datetime_converter(date_list, end_time_list)
            f_end_datetime_list = []
            str_to_datetime_converter(end_datetime_list, f_end_datetime_list)
            s_f_end_datetime_list = sorted(f_end_datetime_list)

            # useful when iterating over lists, length of most lists unless they are nd or otherwise
            num_entries = len(subject_list)

            # sorting subject list
            for i in range(num_entries):
                for j in range (num_entries):
                    if (f_start_datetime_list[j] == s_f_start_datetime_list[i]):
                        s_subject_list.append(subject_list[j])

            # constants, in a way
            current_time = datetime.now()
            example_time = datetime.now().strftime("%d/%m/%Y %H:%M")
            to_example_time = datetime.today().strftime("%H:%M")
            to_future_example_time = datetime.today().strftime("23:59")
            current_date = datetime.now()
            example_date = datetime.today().strftime("%d/%m/%Y")

            # variables
            desired_subject = ""
            desired_date = ""
            desired_time = ""
            mode_select = 0
            valid_subject = 0
            class_found = 0
            more_classes_found = 0
            write_list = []
            write_confirm = ""

            # user prompts
            await message.channel.send("Modes:\n 1. Event Search\n 2. Time Search\n 3. Day Schedule\n 4. Event Add\n 5. Availability Search")
            await message.channel.send("Select mode")
            mode_select = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
            mode_select = mode_select.content

            # when you have a certain subject
            if (mode_select == "1"):

                await message.channel.send(f"Subjects: \n{nd_subject_list}\nWhat subject would you like to know about?")
                desired_subject = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
                desired_subject = desired_subject.content

                for i in range(num_entries):
                    if (desired_subject.upper() == s_subject_list[i].upper()) and (current_date.date() <= s_f_date_list[i].date()):
                        await message.channel.send(f'''The next {s_subject_list[i]} class is on {s_f_date_list[i].strftime("%d/%m/%Y")}, {s_f_start_datetime_list[i].strftime("%H:%M")} to {s_f_end_datetime_list[i].strftime("%H:%M")}''')
                        await message.channel.send(f"That is in {s_f_start_datetime_list[i] - current_time}")
                        valid_subject = 1
                        break
                
                if (valid_subject == 0):
                    await message.channel.send("I wasn't able to find that subject :( what did you do")


            # if you have something at a certain time
            elif (mode_select == "2"):

                await message.channel.send(f"Enter a time, something like {example_time}\n")
                desired_time = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
                desired_time = desired_time.content

                # resetting variables
                class_found = 0
                more_classes_found = 0

                # "now" is a special string
                if (desired_time.lower() == "now"):
                    desired_time = current_time
                else:
                    try:
                        desired_time = datetime.strptime(desired_time, "%d/%m/%Y %H:%M")
                    except ValueError:
                        await message.channel.send("I think that's not the right format!")

                desired_date = desired_time

                for i in range(num_entries):
                    if (desired_time <= s_f_end_datetime_list[i]) and (desired_time >= s_f_start_datetime_list[i]):
                        await message.channel.send(f"\nDad is in {s_subject_list[i]}, which ends in {s_f_end_datetime_list[i] - desired_time}")
                        class_found = 1

                message_to_send = []

                for k in range(num_entries):
                    if (desired_date.date() == s_f_date_list[k].date()) and (desired_time < s_f_end_datetime_list[k]): # k-1 prevents current class from showing in remaining
                        if (more_classes_found == 0):
                            if (class_found == 0):
                                await message.channel.send(f"\nNext class is in: {s_f_start_datetime_list[k] - desired_time}")
                            await message.channel.send(f"Classes remaining today:")
                        message_to_send.append(f'''{s_subject_list[k]:10}| {s_f_start_datetime_list[k].strftime("%H:%M")} to {s_f_end_datetime_list[k].strftime("%H:%M")}\n''')
                        more_classes_found = 1

                if (more_classes_found == 0):
                    await message.channel.send("Dad has no more classes afterwards.")
                else:
                    message_to_send = "".join(message_to_send)
                    await message.channel.send(f'''```{message_to_send}```''')

                if (class_found == 0):
                    await message.channel.send("Dad is free at this time. Go nuts!") # + time of next class of the day
                    

            # schedule for a given day
            elif (mode_select == "3"):

                await message.channel.send(f"Enter a date, example: {example_date}\n")
                desired_date = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
                desired_date = desired_date.content
                class_found = 0

                # "today" and "tomorrow" are special strings
                if (desired_date.lower() == "today"):
                    desired_date = current_date
                    desired_date = desired_date.strftime("%d/%m/%Y")

                if (desired_date.lower() == "tomorrow"):
                    desired_date = current_date + timedelta(days=1)
                    desired_date = desired_date.strftime("%d/%m/%Y")
                    
                try:
                    desired_date = datetime.strptime(desired_date, "%d/%m/%Y")
                except ValueError or TypeError:
                    await message.channel.send("I think that's not the right format!")

                message_to_send = []

                for i in range(num_entries):
                    if (desired_date == s_f_date_list[i]):
                        message_to_send.append(f'''{s_subject_list[i]:10}| {s_f_start_datetime_list[i].strftime("%H:%M")} to {s_f_end_datetime_list[i].strftime("%H:%M")}\n''')
                        class_found = 1
                
                if (class_found == 0):
                    await message.channel.send("No classes on that day")
                else:
                    message_to_send = "".join(message_to_send)
                    await message.channel.send(f'''```{message_to_send}```''')

            # adding events
            elif (mode_select == "4"):

                # dc = dadclasses
                with open('dadclasses_copy.csv', 'a', newline = '', encoding = 'utf-8') as dc:

                    dc_writer = writer(dc)
                    await message.channel.send(f"Enter an event. Format:\n Subject, Date, Start Time, End Time\
                        \n Example: {s_subject_list[1]}, {example_date}, {to_example_time}, {to_future_example_time}\n")
                    
                    # row_w is the content to be written
                    row_w = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
                    row_w = row_w.content

                    # split into respective columns 0 to 3
                    row_w = row_w.split(", ")

                    # csv format: subject, start_date, start_time, end_date, end_time
                    # all strings
                    # dates in d/m/y, times in hr:min:sec
                    # start_date and end_date always the same

                    # TODO proper exit

                    # expect exactly 4 columns of information
                    if (len(row_w) != 4):
                        await message.channel.send(f'''Number of entries do not match. Please make sure entries are separated by ", " \nYour entry: {row_w}\nYou entered {len(row_w)} values, I want to see 4 values''')

                    subject_w =  row_w[0]
                    date_w = row_w[1]
                    start_time_w = row_w[2] + ":00" # adding the seconds
                    end_time_w = row_w[3] + ":00"

                    write_list = [subject_w, date_w, start_time_w, date_w, end_time_w]
                    await message.channel.send(write_list)

                    await message.channel.send("Are you sure you want to add this to your calendar? Y/N\n")
                    write_confirm = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
                    write_confirm = write_confirm.content

                    if write_confirm.upper() == "Y":
                        dc_writer.writerow(write_list)
                        await message.channel.send("Success!")
                    else:
                        await message.channel.send("It's ok, mistakes happen. Look at you.")

            elif (mode_select == "5"):

                class_found = 0

                await message.channel.send(f"Enter a date, example: {example_date}\n")
                desired_date = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
                desired_date = desired_date.content

                if (desired_date.lower() == "today"):
                    desired_date = current_date
                    desired_date = desired_date.strftime("%d/%m/%Y")

                if (desired_date.lower() == "tomorrow"):
                    desired_date = current_date + timedelta(days=1)
                    desired_date = desired_date.strftime("%d/%m/%Y")
                    
                try:
                    desired_date = datetime.strptime(desired_date, "%d/%m/%Y")
                except ValueError or TypeError:
                    await message.channel.send("I think that's not the right format!")

                message_to_send = []

                for i in range(num_entries):
                    if (desired_date == s_f_date_list[i]):
                        class_found = 1
                        # s_f_end_datetime_list[i] to s_f_start_datetime_list[i+1], if i+1 matches the current date
                        if (s_f_start_datetime_list[i+1].date() == desired_date.date()):
                            message_to_send.append(f'''Dad is free for {datediff_to_h_min(s_f_start_datetime_list[i+1], s_f_end_datetime_list[i])} from {s_f_end_datetime_list[i].strftime("%H:%M")} to {s_f_start_datetime_list[i+1].strftime("%H:%M")}\n''')
                        else:
                            message_to_send = "".join(message_to_send)
                            await message.channel.send(f'''{message_to_send}''')
                            await message.channel.send(f'''Dad comes home after {s_f_end_datetime_list[i].strftime("%H:%M")}''')
                    
                if (class_found == 0):
                    await message.channel.send("No classes on that day")

            # user input does not match a mode number
            else:
                await message.channel.send("You think that's a mode dumbass?")


        # mom schedule
        if (message.content.startswith("!mom")):

            votka_functions.log_fn(f"{message.author.name} asked about mom's schedule.", f)

            # maybe dont need to do this every time
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

            # class date in the "first day" column + start/end time
            start_time_start_day = []
            end_time_start_day = []
            # same thing but converting to datetime
            start_time_start_day_datetime = [] 
            end_time_start_day_datetime = []
            # class date in the "last day" column + start/end time
            start_time_end_day_datetime = []
            end_time_end_day_datetime = []
            # used later to find class dates from start_day to end_day
            weeks = []

            current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M")

            # class start and end times added to start_day
            append_hour(start_day, start_time, start_time_start_day)
            append_hour(start_day, end_time, end_time_start_day)

            # creating a list of lists of the end_day column
            # accounting for when end_day[i] == missing value and end_day[i] == start_day[i]
            for i in range(len(end_day)):
                if pd.isna(end_day[i]) or end_day[i] == start_day[i]:
                    start_time_end_day_datetime.append("N/A")
                    end_time_end_day_datetime.append("N/A")
                    weeks.append(0)
                # take start_day[i] and end_day[i], count how many weeks are between them (start_day will be in there, no need to do insert() later)
                # has to be in datetime
                else:
                    x = datetime.strptime(end_day[i], "%d.%m.%Y")
                    y = datetime.strptime(start_day[i], "%d.%m.%Y")
                    week_count = (abs(x - y).days) // 7
                    weeks.append(week_count)

                    # multidimensional list so that the indices for each list still correspond with the rows
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

            # str to datetime for class start_day + class start, end times
            datetime_list_conversion(start_time_start_day, start_time_start_day_datetime)
            datetime_list_conversion(end_time_start_day, end_time_start_day_datetime)

            # combining start and end days into two multidimensional lists, one with start times and the other with end times
            full_start_time_datetime = []
            full_end_time_datetime = []

            for i in range(len(start_time_start_day_datetime)):
                if start_time_end_day_datetime[i] == "N/A":
                    full_start_time_datetime.append([start_time_start_day_datetime[i]])
                    full_end_time_datetime.append([end_time_start_day_datetime[i]])
                else:        
                    full_start_time_datetime.append(start_time_end_day_datetime[i])
                    full_end_time_datetime.append(end_time_end_day_datetime[i])

            # main part, everything before this may be moved out of the loop
            await message.channel.send("Select one of the following options:\n1 - shows what classes you have on a given day at a given time\
                \nif you don't have class then, it tells you when you have your next class on the same day\
                \n2 - shows when you have the next class for a given subject (based on the current date or a specified one)\
                \n3 - shows your schedule for the day\
                \nhelp - to see a list of options\n")

            # while True:, does not need to be there for discord
            busy = 0 # inicjalizacja zmiennej, która określa czy osoba jest zajęta
            user_choice = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
            user_choice = user_choice.content
            
            if user_choice == "1":
                await message.channel.send(f"\nGive me a date and an hour in the following format:\ndd/mm/yyyy hours:minutes\nExample: {current_time_str}\
                                        \nOr type \"now\" if you're interested in the current date.\n\n")
                user_given_date = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
                user_given_date = user_given_date.content
                
                # if the user wants to base on the current date and time
                if user_given_date == "now":
                    user_given_date = current_time_str
                user_given_date += ":00"
                
                try:
                    user_given_date = datetime.strptime(user_given_date, "%d/%m/%Y %H:%M:%S")

                    # checking whether there are classes during the given date and time
                    for i in range(len(start_day)):
                        for index in range(len(full_start_time_datetime[i])):
                            if (user_given_date <= full_end_time_datetime[i][index]) and (user_given_date >= full_start_time_datetime[i][index]):
                                busy = 1
                                subject_name = subject_list[i]
                                location_name = location[i]
                                hours_left = datediff_to_h_min(full_end_time_datetime[i][index], user_given_date)
                    
                    if busy == 1:
                        #await message.channel.send("")
                        await message.channel.send(f"At this time you have the \"{subject_name}\" class in {location_name}. The class will end in {hours_left} from the specified time.")
                    else:
                        possible_next_class = []
                        flag = 0 # initialization of a variable that determines whether there will be classes after a given hour on a certain day
                        
                        for i in range(1, 21):
                            time_diff = user_given_date + timedelta(hours = i)
                            possible_next_class.append(time_diff)
                            if time_diff > user_given_date.replace(hour = 20): # after 8pm there are no classes that are just starting
                                break
                        
                        for date in possible_next_class:
                            for i in range(len(start_day)):
                                for index in range(len(full_start_time_datetime[i])):
                                    if (date <= full_end_time_datetime[i][index])\
                                        and (date >= full_start_time_datetime[i][index]):
                                        flag = 1 # found nearest class
                                        next_class = full_start_time_datetime[i][index]
                                        break
                                if flag == 1: # breaking the loop because the nearest class was found
                                    break
                            if flag == 1:
                                break
                        
                        if flag == 1:
                            hours_until = datediff_to_h_min(next_class, user_given_date)
                            next_class = "{:d}:{:02d}".format(next_class.hour, next_class.minute)
                            string = f"The next closest class of the day is at {next_class}, {hours_until} from now." # these sound so awkward, change them
                        elif flag == 0:
                            string = "After the specified time, you have no more classes for that day." # ^ what i said before
                        
                        #await message.channel.send("")
                        await message.channel.send(f"You don't have classes at that time. {string}") 

                except ValueError: # gives valueerror if date given in the wrong format, or if the given date cannot exist at all
                    #await message.channel.send("")
                    await message.channel.send("Double check the format you sent it in. It's probably wrong!")

                #await message.channel.send("")
                time.sleep(2)

                if user_choice == "2":
                    # the program takes subjects from the csv file, so if the file is changed, everything still works
                    subject_set = set(subject_list)
                    subject_pool = []
                    subject_pool_dict = {} # to be able to match the selected number to the correct subject
                    number_subject = 0
                    
                    for subject in subject_set:
                        number_subject += 1
                        subject_and_number = f"{number_subject} - {subject}"
                        subject_pool.append(subject_and_number)
                        subject_pool_dict[number_subject] = subject

                    await message.channel.send("\nChoose the subject you are interested in:")        
                    for subject in subject_pool:
                        await message.channel.send(subject)
                    user_given_subject = int(input("\n"))
                    
                    # searching for a subject corresponding to the selected number
                    for key in subject_pool_dict:
                        if key == user_given_subject:
                            user_given_subject = subject_pool_dict[key]

                    await message.channel.send(user_given_subject)
                    
                    # option to choose a lecture/exercises/workshop/etc for a subject
                    class_type_set = set()
                    class_type_pool = []
                    class_type_pool_dict = {}
                    number_type = 0

                    for i in range(len(subject_list)):
                        if subject_list[i] == user_given_subject:
                            class_type_set.add(class_type_list[i]) # list of possible types of classes

                    # if given classes have only one type, it makes no sense to give the user a choice
                    if len(class_type_set) == 1:
                        type_choice = 0
                    else:
                        type_choice = 1

                    if type_choice == 1:
                        for class_type in class_type_set:
                            number_type += 1
                            type_and_number = f"{number_type} - {class_type}"
                            class_type_pool.append(type_and_number)
                            class_type_pool_dict[number_type] = class_type
                        
                        await message.channel.send("\nChoose the type of classes you are interested in:")
                        for class_type in class_type_pool:
                            await message.channel.send(class_type)
                        user_given_type = int(input("\n"))

                        # searching for a class type corresponding to the selected number
                        for key in class_type_pool_dict:
                            if key == user_given_type:
                                user_given_type = class_type_pool_dict[key]

                        await message.channel.send(user_given_type)

                    await message.channel.send(f"\nGive me a date and an hour in the following format:\ndd/mm/yyyy hours:minutes\nExample: {current_time_str}\
                                            \nOr type \"now\" if you're interested in the current date.\n\n")
                    user_given_date = await bot.wait_for('message', check=lambda anything: anything.author == message.author)
                    user_given_date = user_given_date.content
                    
                    # jeśli użytkownik chce bazować na obecnej dacie i godzinie
                    if user_given_date == "now":
                        user_given_date = current_time_str
                    user_given_date += ":00"

        

        # converting time
        if (message.content.startswith("!timezone")):
            votka_functions.log_fn(f"{message.author.name} got timed on", f)
            await message.channel.send("""[time] [place]
            [time] should be in 24h format and [place] should be one of the following: 
            Iowa, Poland, Saudi, Japan, Austria, England, Philly

            Or type "now" [place], or to see the current time in the specified place!""")

bot.run("you thought so")
