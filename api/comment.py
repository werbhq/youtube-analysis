import os
import json
from api import youtubeApi

FILE_PATH = os.path.join('data', 'comments.json')


def process_comments(response_items):
    comments = []

    for res in response_items:
        comment = {}
        comment['snippet'] = res['snippet']['topLevelComment']['snippet']
        comment['snippet']['id'] = res['snippet']['topLevelComment']['id']

        data = comment['snippet']
        data['authorChannelId'] = data['authorChannelId']['value']
        del data['canRate']

        comments.append(data)

    comments.sort(key=lambda x: x['likeCount'], reverse=True)
    return comments


def importComments():
    """
    Imports the comments from response.json and returns it as list
    """
    with open(FILE_PATH, 'r') as f:
        comments: list = json.loads(f.read())
        return comments


def fetchComments(youtubeVideoId: str, MAX_COMMENT=1000):
    """
    Returns a list of MAX_COMMENT number of comments. Saves the comments in response.json
    """
    comment_list = []

    response = {'nextPageToken': ''}

    while (response.get('nextPageToken', None) != None and len(comment_list) < MAX_COMMENT):
        request = youtubeApi.commentThreads().list(
            part="snippet",
            videoId=youtubeVideoId,
            pageToken=response['nextPageToken'],
            textFormat='plainText',
            order='relevance',
            maxResults=MAX_COMMENT - len(comment_list),
        )
        response = request.execute()
        comment_list.extend(process_comments(response['items']))
        print(f'Extracted : {len(comment_list)} Comments')

    print(f'Dumping file to {FILE_PATH}')
    data = json.dumps(comment_list, indent=4)
    f = open(FILE_PATH, 'w')
    f.write(data)

    return comment_list
