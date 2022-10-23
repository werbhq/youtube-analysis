import os
import json
from api import __youtube_api

__FILE_PATH = os.path.join('data', 'comments.json')


def __process_comments(response_items):
    comments = []

    # Extracts top level comments and its id
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


def load():
    """
    Loads the comments from comments.json

    Returns (list) : comments
    """
    with open(__FILE_PATH, 'r') as f:
        comments: list = json.loads(f.read())
        return comments


def fetch(youtube_video_id: str, MAX_COMMENT=1500):
    """
    Fetches comments from {youtubeVideoId} with {MAX_COMMENT} limit and saves the comments in comments.json

    Returns (list) : MAX_COMMENT number of comments.
    """

    comment_list = []
    response = {'nextPageToken': ''}

    while (response.get('nextPageToken', None) != None and len(comment_list) < MAX_COMMENT):
        request = __youtube_api.commentThreads().list(
            part="snippet",
            videoId=youtube_video_id,
            pageToken=response['nextPageToken'],
            textFormat='plainText',
            order='relevance',
            maxResults=MAX_COMMENT - len(comment_list),
        )
        response = request.execute()
        comment_list.extend(__process_comments(response['items']))
        print(f'Extracted : {len(comment_list)} Comments')

    print(f'Dumping file to {__FILE_PATH}')
    with open(__FILE_PATH, 'w') as f:
        f.write(json.dumps(comment_list, indent=4))

    return comment_list
