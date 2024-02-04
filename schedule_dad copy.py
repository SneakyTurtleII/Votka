from datetime import datetime, date, timedelta, timezone
import pytz

# what do we need to do
# convert between timezones
# current time in multiple given places
# user chooses a time in place, program gives them the MOST important places. if not, then bigger list comes in

y = pytz.country_timezones['us']
number = 0
timezone_dict = {}

print("Enter a time: [time] [place].\
    \n[time] should be in hours:minutes format\
    \n[place] should be in ISO 3166.\n")

user_time_place = input()

user_time_place = user_time_place.split(" ")

user_time = user_time_place[0]
user_place = user_time_place[1]



# now we can convert
current_time_str = datetime.now().strftime("%d/%m/%Y")
user_datetime_str = current_time_str + " " + user_time + ":00"
user_datetime_datetime = datetime.strptime(user_datetime_str, "%d/%m/%Y %H:%M:%S")

utcmoment_naive = user_datetime_datetime # utc naive is gmt
utcmoment_aware = pytz.timezone(f"{user_place}").localize(utcmoment_naive)
""" utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc) """

# print "utcmoment_naive: {0}".format(utcmoment_naive)
print("utcmoment_naive: {0}".format(utcmoment_naive))
print("utcmoment:       {0}".format(utcmoment_aware))

localFormat = "%d/%m %H:%M"

timezones = ['America/Chicago', 'Europe/Warsaw']

for tz in timezones:
    localDatetime = utcmoment_aware.astimezone(pytz.timezone(tz))
    print(localDatetime.strftime(localFormat))

# utcmoment_naive: 2017-05-11 17:43:30.802644
# utcmoment:       2017-05-11 17:43:30.802644+00:00
# 2017-05-11 10:43:30
# 2017-05-11 19:43:30
# 2017-05-11 13:43:30

""" for timezone in y:
    number += 1
    timezone_dict[number] = timezone

for key in timezone_dict:
    print(f"{key} - {timezone_dict[key]}") """

