import datetime

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for i in range(7):
    now = datetime.datetime.now() + datetime.timedelta(days=i+1)
    print(now.strftime("%A"))

