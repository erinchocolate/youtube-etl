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
