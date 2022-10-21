import json
import os
import re
import requests

FILE_PATH = os.path.join('data', 'captions.json')


def importCaptions():
    """
    Imports the captions from captions.json and returns it as dict
    """
    with open(FILE_PATH, 'r') as f:
        comments: dict = json.loads(f.read())
        return comments


def fetchCaptions(youtubeId: str):
    """
    Returns a dictionary of caption unqiue words with count. Can be empty if no subtitle for english found
    """
    res = requests.get(url=f'https://youtu.be/{youtubeId}')
    urls = re.findall("\"(https:\/\/www.youtube.com\/api\/timedtext.*?)\"", res.text)

    captionUrl: str = None

    for url in list(map(lambda y: y.replace('\\u0026', '&'), urls)):
        if "lang=en" in url:
            captionUrl = url
            break

    wordMap = {}

    if captionUrl:
        res = requests.get(captionUrl+'&fmt=json3')
        data = res.json()

        # Extracting subtitle
        data = list(map(lambda x: x['segs'][0]['utf8'].replace('\n', ''), data['events']))

        # Converiting it to keys
        subtitle: str
        for subtitle in data:
            for word in subtitle.lower().split(' '):
                wordMap[word] = wordMap.get(word, 1) + 1
    else:
        print("No Subtitle Found")

    print(f'Dumping file to {FILE_PATH}')
    data = json.dumps(wordMap, indent=4)
    f = open(FILE_PATH, 'w')
    f.write(data)

    return wordMap
