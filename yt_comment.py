import os
import pandas as pd
from datetime import datetime as dt
from dotenv import load_dotenv
from googleapiclient.discovery import build
from utils.comments import process_comments

load_dotenv()
API_KEY = os.environ.get('API_KEY')
api_service_name = "youtube"
api_version = "v3"
youtube = build(
    api_service_name, api_version, developerKey=API_KEY)

today = dt.today().strftime('%Y-%m-%d')


def get_comments(video_id):
    comments_list = []
    request = youtube.commentThreads().list(
        part="id, snippet, replies",
        videoId=video_id,
    )
    response = request.execute()
    comments_list.extend(process_comments(response['items']))

    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=video_id,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))

    print(
        f'Finished fetching comments for video {video_id}. {len(comments_list)} comments found.')

    df = pd.DataFrame(comments_list)
    df.to_csv(f'comments_{video_id}_{today}.csv', index=False)

    print(
        f'Check out the csv file in the folder for your video comments.')


def main():
    video_id = input("Enter the video ID: ")
    get_comments(video_id)


if __name__ == "__main__":
    main()
