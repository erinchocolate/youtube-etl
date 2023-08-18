# YouTube Comment ETL

## Why I started this project

I came across a tutorial that taught me how to create a simple data pipeline. Upon completing the tutorial, I realized it would be an awesome idea to give back to the YouTuber who had helped me learn so much from his content!

Through some Google searching, I discovered that I could retrieve comments from specific YouTube videos. This got me thinking about developing a simple ETL to extract data from the Google Data API and use the data to get some actionable insights that might help him to improve the content.

## How I built the project

### Data extraction

Google has simplified their API usage, providing an API explorer that lets me experiment with queries and see the returned data directly within the explorer itself.

Additionally, they provide a starter code demonstrating how to retrieve data from the API based on my explorations in the API explorer. Here is the starter code I used👇🏽

```python
# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "YOUR_API_KEY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet, replies",
        videoId="q8q3OFFfY6c"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()
```

### Data transformation

Once I had obtained the data, the next step was understanding its structure and getting the data I needed. Since the CommentThreads endpoint offers a list of comment threads, I needed to extract each comment from the list.

Below is an example of a comment(item):

```json
{
  "items": [
    {
      "kind": "youtube#commentThread",
      "etag": "aG4xa0IW0jNjuZRQhpE1-i4n7ww",
      "id": "UgwG6AJegM6Xg6EGW254AaABAg",
      "snippet": {
        "videoId": "q8q3OFFfY6c",
        "topLevelComment": {
          "kind": "youtube#comment",
          "etag": "DBxVkPxE9M49g_COQbNJ7i70mtk",
          "id": "UgwG6AJegM6Xg6EGW254AaABAg",
          "snippet": {
            "videoId": "q8q3OFFfY6c",
            "textDisplay": "getting the below error can any one help:                                                                                                                                                                                                                                                                                             File &quot;C:\\Users\\Saliybe\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\tweepy\\\u003ca href=\"http://api.py/\"\u003eapi.py\u003c/a\u003e&quot;, line 46, in wrapper       \r\u003cbr\u003e    return method(*args, **kwargs)\r\u003cbr\u003e           ^^^^^^^^^^^^^^^^^^^^^^^\r\u003cbr\u003e  File &quot;C:\\Users\\Saliybe\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\tweepy\\\u003ca href=\"http://api.py/\"\u003eapi.py\u003c/a\u003e&quot;, line 414, in user_timeline\r\u003cbr\u003e    return self.request(\r\u003cbr\u003e           ^^^^^^^^^^^^^\r\u003cbr\u003e  File &quot;C:\\Users\\Saliybe\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\tweepy\\\u003ca href=\"http://api.py/\"\u003eapi.py\u003c/a\u003e&quot;, line 271, in request\r\u003cbr\u003e    raise Forbidden(resp)\r\u003cbr\u003etweepy.errors.Forbidden: 403 Forbidden\r\u003cbr\u003e453 - You currently have access to a subset of Twitter API v2 endpoints and limited v1.1 endpoints (e.g. media post, oauth) only. If you need access to this endpoint, you may need a different access level. You can learn more here: \u003ca href=\"https://developer.twitter.com/en/portal/product\"\u003ehttps://developer.twitter.com/en/portal/product\u003c/a\u003e",
            "textOriginal": "getting the below error can any one help:                                                                                                                                                                                                                                                                                             File \"C:\\Users\\Saliybe\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\tweepy\\api.py\", line 46, in wrapper       \r\n    return method(*args, **kwargs)\r\n           ^^^^^^^^^^^^^^^^^^^^^^^\r\n  File \"C:\\Users\\Saliybe\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\tweepy\\api.py\", line 414, in user_timeline\r\n    return self.request(\r\n           ^^^^^^^^^^^^^\r\n  File \"C:\\Users\\Saliybe\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\tweepy\\api.py\", line 271, in request\r\n    raise Forbidden(resp)\r\ntweepy.errors.Forbidden: 403 Forbidden\r\n453 - You currently have access to a subset of Twitter API v2 endpoints and limited v1.1 endpoints (e.g. media post, oauth) only. If you need access to this endpoint, you may need a different access level. You can learn more here: https://developer.twitter.com/en/portal/product",
            "authorDisplayName": "Saliyuk Benjamin",
            "authorProfileImageUrl": "https://yt3.ggpht.com/ytc/AOPolaSTzOdfMvzF-EfoYg6As89zNC33b2kBTJVk3AzgDw=s48-c-k-c0x00ffffff-no-rj",
            "authorChannelUrl": "http://www.youtube.com/channel/UCfINCRa-pt9E11oKoOw0bYw",
            "authorChannelId": {
              "value": "UCfINCRa-pt9E11oKoOw0bYw"
            },
            "canRate": true,
            "viewerRating": "none",
            "likeCount": 0,
            "publishedAt": "2023-08-13T23:06:27Z",
            "updatedAt": "2023-08-13T23:06:27Z"
          }
        },
        "canReply": true,
        "totalReplyCount": 0,
        "isPublic": true
      }
    },
```

For this project, I only focused on collecting data like the author's name, the comment content, and the timestamp of each comment. 

```python
def process_comments(response_items):
		comments = []
		for comment in response_items:
				author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
				comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
				publish_time = comment['snippet']['topLevelComment']['snippet']['publishedAt']
				comment_info = {'author': author, 
						'comment': comment_text, 'published_at': publish_time}
				comments.append(comment_info)
		print(f'Finished processing {len(comments)} comments.')
		return comments
```

### Data load

For loading the data, I used Pandas, a powerful library that helped me transform the list of comments into a neat CSV file.

Some videos had more than one page of comments. I used a while loop to retrieve all comments that looked for the nextPageToken in each response. Whenever another page of comments was available, the response would include a nextPageToken.

```python
while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=video_id,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
```

