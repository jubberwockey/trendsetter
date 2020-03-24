from src.trendsetter import Trendsetter
import datetime
import json
import os

path = '/home/boris/git/trendsetter/data/trends.json'


ts = Trendsetter()
trending_now = {'date': str(datetime.datetime.now())}
for country in ts.countries.keys():
    trending_now.update({country: ts.get_trending(country)})


if os.path.exists(path):
    with open(path, mode='r', encoding='utf-8') as file:
        trending_json = json.load(file)
else:
    with open(path, mode='w+', encoding='utf-8') as file:
        trending_json = list()
        json.dump(trending_json, file)

trending_json.append(trending_now)

with open(path, mode='w', encoding='utf-8') as file:
    json.dump(trending_json, file)
