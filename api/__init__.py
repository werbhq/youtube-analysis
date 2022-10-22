import os
import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()

__API_NAME = "youtube"
__API_VER = "v3"
__API_KEY = os.environ["API_KEY"]

__youtube_api = googleapiclient.discovery.build(__API_NAME, __API_VER, developerKey=__API_KEY)
