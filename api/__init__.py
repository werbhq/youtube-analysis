import os
import googleapiclient.discovery

API_NAME = "youtube"
API_VER = "v3"

# Reading .env file
with open('.env', 'r') as f:
    os.environ["KEY"] = f.read()

youtubeApi = googleapiclient.discovery.build(API_NAME, API_VER, developerKey=os.environ["KEY"])
