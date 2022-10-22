import os
import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()

API_NAME = "youtube"
API_VER = "v3"
API_KEY = os.environ["API_KEY"]

youtubeApi = googleapiclient.discovery.build(API_NAME, API_VER, developerKey=API_KEY)
