# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import string
import googleapiclient.discovery
import json


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAwfyIG_RDJymt6j7Ic9slOvOjmZtlwc0k"

    youtube: googleapiclient.discovery.Resource = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    youtubeID = "igu4JFZ9MhU"
    # malyalam aa
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=youtubeID,
        maxResults=2000,
        textFormat='plainText'
    )
    response = request.execute()
    print(response)

    x = json.dumps(response, indent=4)
    f = open('response.json', 'w')
    f.write(x)


if __name__ == "__main__":
    main()
