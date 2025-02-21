
import datetime

now = datetime.datetime.now()
print("Yesterday: ", now.day - 1, now.strftime("%m"))
print("Today: ", now.day, now.strftime("%m"))
print("Tomorrow: ", now.day + 1, now.strftime("%m"))