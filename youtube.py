# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

from asyncio.windows_events import NULL
from itertools import count
import os
from pydoc import doc
import string
import googleapiclient.discovery
import json

from utils.comment import process_comments


def getComments(channelId):
    # # Disable OAuthlib's HTTPS verification when running locally.
    # # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    comment_list = []
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAwfyIG_RDJymt6j7Ic9slOvOjmZtlwc0k"
    MAX_COMMENT=2000

    youtube: googleapiclient.discovery.Resource = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=channelId,
        pageToken="",
        textFormat='plainText',
        order='relevance',
        maxResults=100,  # 100 Is MAX limit possible, default is 20
    )
    response = request.execute()

    comment_list.extend(process_comments(response['items']))

    while (response['nextPageToken'] != NULL and len(comment_list) < MAX_COMMENT):  
        comment_list.extend(process_comments(response['items']))
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=channelId,
            pageToken=response['nextPageToken'],
            textFormat='plainText',
            order='relevance',
            maxResults=100,  # 100 Is MAX limit possible, default is 20
        )
        response = request.execute()

    x = json.dumps(comment_list, indent=4)
    f = open('response.json', 'w')
    f.write(x)

def main():
    getComments('zYc83YbeU-U')


if __name__ == "__main__":
    main()
