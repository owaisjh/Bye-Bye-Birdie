import os
import datetime
import pandas as pd



start = datetime.datetime.strptime("01-01-1959", "%d-%m-%Y")
end = datetime.datetime.strptime("12-11-2022", "%d-%m-%Y")
date_generated = pd.date_range(start, end)


for i in date_generated:
    date = i.strftime("%Y/%m/%d")

    if not os.path.exists('data/' + date+".json"):
        print("does not exists: "+date)