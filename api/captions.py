import json
import os
import re
import requests
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

__FILE_PATH = os.path.join('data', 'captions.json')


def load(return_list=False):
    """
    Loads the captions from captions.json

    Returns (dict | list) : captions. 
        Default is dict. Use {return_list} to return as list
    """
    with open(__FILE_PATH, 'r') as f:
        comments: dict = json.loads(f.read())
        if return_list:
            return comments['list']
        else:
            return comments['dict']


def fetch(youtube_id: str, return_list=False):
    """
    Returns (dict) : caption unqiue words with it's frequency count. Empty {} if no subtitle for english found.
    """
    res = requests.get(url=f'https://youtu.be/{youtube_id}')
    urls = re.findall("\"(https:\/\/www.youtube.com\/api\/timedtext.*?)\"", res.text)  # Extracting caption lang urls

    caption_url: str = None

    for url in list(map(lambda y: y.replace('\\u0026', '&'), urls)):
        if "lang=en" in url:
            caption_url = url
            break

    word_map = {}
    subtitles: list

    if caption_url:
        res = requests.get(caption_url+'&fmt=json3')
        subtitles = res.json()

        # Extracting subtitle
        subtitles = list(map(lambda x: x['segs'][0]['utf8'].replace('\n', ''), subtitles['events']))

        # Converiting it to keys
        subtitle: str
        for subtitle in subtitles:
            for word in subtitle.lower().split(' '):
                if word not in ENGLISH_STOP_WORDS:
                    word = re.sub(r'[^A-Za-z0-9 ]+', '', word)
                    word_map[word] = word_map.get(word, 1) + 1
    else:
        print("No Subtitle Found")

    print(f'Dumping file to {__FILE_PATH}')
    with open(__FILE_PATH, 'w') as f:
        f.write(json.dumps({'dict': word_map, 'list': subtitles}, indent=4))

    if return_list:
        return subtitles
    else:
        return word_map
