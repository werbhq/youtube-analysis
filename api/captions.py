import json
import os
import re
import requests
import sklearn
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

__FILE_PATH = os.path.join('data', 'captions.json')


def load():
    """
    Loads the captions from captions.json

    Returns (dict) : captions
    """
    with open(__FILE_PATH, 'r') as f:
        comments: dict = json.loads(f.read())
        return comments


def fetch(youtubeId: str):
    """
    Returns (dict) : caption unqiue words with it's frequency count. Empty {} if no subtitle for english found.
    """
    res = requests.get(url=f'https://youtu.be/{youtubeId}')
    urls = re.findall("\"(https:\/\/www.youtube.com\/api\/timedtext.*?)\"", res.text)  # Extracting caption lang urls

    caption_url: str = None

    for url in list(map(lambda y: y.replace('\\u0026', '&'), urls)):
        if "lang=en" in url:
            caption_url = url
            break

    word_map = {}

    if caption_url:
        res = requests.get(caption_url+'&fmt=json3')
        data = res.json()

        # Extracting subtitle
        data = list(map(lambda x: x['segs'][0]['utf8'].replace('\n', ''), data['events']))

        # Converiting it to keys
        subtitle: str
        for subtitle in data:
            for word in subtitle.lower().split(' '):
                  if word not in ENGLISH_STOP_WORDS :
                     word_map[word] = word_map.get(word, 1) + 1
    else:
        print("No Subtitle Found")

    print(f'Dumping file to {__FILE_PATH}')
    with open(__FILE_PATH, 'w') as f:
        f.write(json.dumps(word_map, indent=4))

    return word_map
