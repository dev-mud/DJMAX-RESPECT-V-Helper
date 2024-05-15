import pandas as pd
import json

df = pd.read_csv('songs.csv', encoding='cp949')
with open('songs.json', 'r', encoding='utf-8') as f:
    song_json = json.load(f, strict=False)  

count = 0

level = []
temp = []

for i in range(len(df)):
    #4 BUTTON
    temp.append(str(df.iloc[i, 1]))
    temp.append(str(df.iloc[i, 2]))
    temp.append(str(df.iloc[i, 3]))
    temp.append(str(df.iloc[i, 4]))
    level.append(temp)

    temp = []

    #5 BUTTON
    temp.append(str(df.iloc[i, 5]))
    temp.append(str(df.iloc[i, 6]))
    temp.append(str(df.iloc[i, 7]))
    temp.append(str(df.iloc[i, 8]))
    level.append(temp)

    temp = []

    #6 BUTTON
    temp.append(str(df.iloc[i, 9]))
    temp.append(str(df.iloc[i, 10]))
    temp.append(str(df.iloc[i, 11]))
    temp.append(str(df.iloc[i, 12]))
    level.append(temp)

    temp = []

    #8 BUTTON
    temp.append(str(df.iloc[i, 13]))
    temp.append(str(df.iloc[i, 14]))
    temp.append(str(df.iloc[i, 15]))
    temp.append(str(df.iloc[i, 16]))
    level.append(temp)

    song_json[df.iloc[i, 0]]['difficulty'] = level

    level = []
    temp = []

with open("songs_TEST.json", "w", encoding='utf-8') as f:
    json.dump(song_json, f, ensure_ascii=False, indent=4)