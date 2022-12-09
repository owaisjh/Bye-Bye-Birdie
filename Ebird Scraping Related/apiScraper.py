import datetime
import pandas as pd
import requests
import json
import os


from dotenv import load_dotenv
load_dotenv()
import os
token = os.environ.get("api-token")



start = datetime.datetime.strptime("01-01-1960", "%d-%m-%Y")
end = datetime.datetime.strptime("31-12-1960", "%d-%m-%Y")
date_generated = pd.date_range(start, end)
url = "https://api.ebird.org/v2/data/obs/CA-BC/historic/"

headers = {'Content-Type' : 'application/json',
            'X-eBirdApiToken' : token}


for i in date_generated:
    date = i.strftime("%Y/%m/%d")
    response = requests.get(url+date, headers=headers)
    if response.status_code != 200:
        print(date + " FAILED")
        break

    json_object = json.dumps(response.json())

    if not os.path.isdir('data/'+date[:-2]):
        os.makedirs('data/'+date[:-2])

    with open('data/'+date+".json", "w") as outfile:
        outfile.write(json_object)



