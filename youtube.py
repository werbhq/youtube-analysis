import os
import googleapiclient.discovery
import json
from utils.comment import process_comments

API_NAME = "youtube"
API_VER = "v3"
with open('.env', 'r') as f:
    KEY = f.read()
    os.environ["KEY"] = KEY


def importComments():
    """
    Imports the comments from response.json and returns it as list
    """
    with open('response.json', 'r') as json_file:
        user_data: list = json.loads(json_file.read())
        return user_data


def getComments(youtubeVideoId: str, MAX_COMMENT=2000):
    """
    Returns a list of 2000 comments. Saves the comments in response.json
    """
    comment_list = []

    youtube = googleapiclient.discovery.build(API_NAME, API_VER, developerKey=os.environ["KEY"])

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=youtubeVideoId,
        pageToken="",
        textFormat='plainText',
        order='relevance',
        maxResults=100,
    )
    response = request.execute()

    comment_list.extend(process_comments(response['items']))

    while (response.get('nextPageToken', None) != None and len(comment_list) < MAX_COMMENT):
        comment_list.extend(process_comments(response['items']))
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=youtubeVideoId,
            pageToken=response['nextPageToken'],
            textFormat='plainText',
            order='relevance',
            maxResults=100,  # 100 Is MAX limit possible, default is 20
        )
        response = request.execute()
        print(f'Extracted : {len(comment_list)} Comments')

    data = json.dumps(comment_list, indent=4)
    f = open('response.json', 'w')
    f.write(data)

    return comment_list


def main():
    # Only use getComments() once. Then use importComments() for testing
    # getComments('Ntn1-SocNiY')
    comments = importComments()
    print(comments[0])


if __name__ == "__main__":
    main()
