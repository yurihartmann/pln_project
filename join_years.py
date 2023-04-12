import json
import os

DIRECTORY = "history_data/1/"
result_json = []

for filename in os.listdir(DIRECTORY):
    if ".json" not in filename:
        continue

    with open(f'{DIRECTORY}/{filename}') as file:
        json_year = json.load(file)
        result_json += json_year


with open(f'{DIRECTORY}/all.json', 'w', encoding='utf-8') as fp:
    json.dump(result_json, fp, indent=4, ensure_ascii=False)
