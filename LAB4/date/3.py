import datetime

now = datetime.datetime.now()
micro_rep = now.replace(microsecond = 0)
print(now)
print(micro_rep)