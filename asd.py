import datetime

string = '12/12/2001'
asd = str(12122001)

data = string.split("/")
fecha = data[0]+"-"+data[1]+"-"+data[2]
date = datetime.date(day=int(asd[0:2]), month=int(asd[2:4]), year=int(asd[4:8]))
date = date.strftime("%m/%d/%Y")
print(date)
