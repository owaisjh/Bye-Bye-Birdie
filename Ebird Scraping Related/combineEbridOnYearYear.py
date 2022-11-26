import glob, os
import json

inputFolder = 'ebirdData'

outputFolder = 'ebirdDataYearly/'



for year in glob.glob(inputFolder + '/**'):

    yearNum = year.split('/')[1]
    print(yearNum)
    output = []

    for month in glob.glob(year + '/**'):
        for dateFile in glob.glob(month + '/**'):
            f = open(dateFile)
            data = json.load(f)
            if data:
                output.extend(data)

    json_object = json.dumps(output)
    with open(outputFolder+yearNum+".json", "w") as outfile:
            outfile.write(json_object)


