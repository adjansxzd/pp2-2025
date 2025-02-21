import datetime

now = datetime.datetime.now()
my_date = datetime.datetime(2007, 5, 20)

diff = now - my_date
print(diff.total_seconds())