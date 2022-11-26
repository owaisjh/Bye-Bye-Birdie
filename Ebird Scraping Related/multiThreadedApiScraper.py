import multiprocessing
import datetime
import pandas as pd
import requests
import json
import os


def req(i):
    url = "https://api.ebird.org/v2/data/obs/CA-BC/historic/"

    headers = {'Content-Type': 'application/json',
               'X-eBirdApiToken': 'p6otupunpquj'}

    date = i.strftime("%Y/%m/%d")
    response = requests.get(url+date, headers=headers)
    if response.status_code != 200:
        print(date + " FAILED")
    else:
        json_object = json.dumps(response.json())

        if not os.path.isdir('data/'+date[:-2]):
            os.makedirs('data/'+date[:-2])

        with open("data/"+date+".json", "w") as outfile:
            outfile.write(json_object)


if __name__ == '__main__':
    start = datetime.datetime.strptime("01-02-2022", "%d-%m-%Y")
    end = datetime.datetime.strptime("28-02-2022", "%d-%m-%Y")
    date_generated = pd.date_range(start, end)



    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=6)


    outputs = pool.map(req, date_generated)
