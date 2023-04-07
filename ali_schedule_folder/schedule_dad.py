from event_search import *
from time_search import *
from day_schedule import *
from event_add import *
from availability_search import *

print("Modes:\n 1. Event Search\n 2. Time Search\n 3. Day Schedule\n 4. Event Add\n 5. Availability Search")
mode_select = input("Select mode")

if (mode_select == "1"):
    EventSearch()

elif (mode_select == "2"):
    TimeSearch()

elif (mode_select == "3"):
    DaySchedule()

elif (mode_select == "4"):
    EventAdd()

elif (mode_select == "5"):
    AvailabilitySearch()

else:
    print("You think that's a mode dumbass?")