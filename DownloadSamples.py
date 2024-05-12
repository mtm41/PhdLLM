import requests as req
import json
initial = 2284697
types = (0,1)
urlFormat = 'https://raw.githubusercontent.com/mtm41/dataset/master/{}_{}.json'

while initial < 2400000:
    for type in types:
        url = urlFormat.format(initial,type)
        reportData = req.get(url=url)
        if (reportData.status_code == 200):
            print('{} found!'.format(initial))
            jsonReport = reportData.json()
            with open('./llm/{}_{}.json'.format(initial, type), 'a', encoding='utf-8') as reportFile:
                json.dump(jsonReport, reportFile, ensure_ascii=False, indent=4)
    initial += 1