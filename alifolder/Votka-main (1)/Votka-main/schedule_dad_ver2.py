import dad_functions as dadf

print("Modes:\n 1. Event Search\n 2. Time Search\n 3. Day Schedule\n 4. Event Add\n 5. Availability Search")
mode_select = input("Select mode")

if (mode_select == "1"):
    dadf.EventSearch()

elif (mode_select == "2"):
    dadf.TimeSearch()

elif (mode_select == "3"):
    dadf.DaySchedule()

elif (mode_select == "4"):
    dadf.EventAdd()

elif (mode_select == "5"):
    dadf.AvailabilitySearch()
