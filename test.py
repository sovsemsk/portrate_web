import locale
from datetime import datetime


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

date_string = "5 декабря 2023"

splitted_date_string = date_string.split()
splitted_date_string[1] = splitted_date_string[1][:3]
cutted_date_string = " ".join(splitted_date_string)
datetime = datetime.strptime(cutted_date_string, "%d %b %Y")

print(datetime)
