
import json
from api import youtubeApi

FILE_PATH = 'response.json'


def process_comments(response_items):
    comments = []
    for res in response_items:
        # for reply comments

        # if 'replies' in res.keys():
        #     for reply in res['replies']['comments']:
        #         comment = reply['snippet']
        #         comment['commentId'] = reply['id']
        #         comments.append(comment)

        # for non reply comments
        if 'replies' not in res.keys():
            comment = {}
            comment['snippet'] = res['snippet']['topLevelComment']['snippet']
            comment['snippet']['parentId'] = None
            comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']
            comments.append(comment['snippet'])

    return comments


def importComments():
    """
    Imports the comments from response.json and returns it as list
    """
    with open(FILE_PATH, 'r') as f:
        comments: list = json.loads(f.read())
        return comments


def getComments(youtubeVideoId: str, MAX_COMMENT=1000):
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
            maxResults=100,  # 100 Is MAX limit possible, default is 20
        )
        response = request.execute()
        comment_list.extend(process_comments(response['items']))
        print(f'Extracted : {len(comment_list)} Comments')

    print(f'Dumping file to {FILE_PATH}')
    data = json.dumps(comment_list, indent=4)
    f = open(FILE_PATH, 'w')
    f.write(data)

    return comment_list
