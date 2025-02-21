import datetime

def days():
    now = datetime.datetime.now()
    new_date = now.day- 5
    return new_date

print(days())