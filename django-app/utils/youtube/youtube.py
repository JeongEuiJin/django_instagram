
import requests
from googleapiclient.discovery import build

__all__ = (
    'search',
)
DEVELOPER_KEY = 'AIzaSyAokgs8K0D61OeXwJaFnf3L_PFrMSabF80'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search_origin(q):
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    search_params = {
        'part': 'snippet',
        'key': 'AIzaSyAokgs8K0D61OeXwJaFnf3L_PFrMSabF80',
        'maxResult': '10',
        'type': 'video',
        'q': q,

    }
    response = requests.get(url_api_search, params=search_params)
    data = response.json()
    return data


def search(q):
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    search_response = youtube.search().list(
        q=q,
        part='id,snippet',
        maxResults=10,
        type='video',
    ).execute()
    return search_response