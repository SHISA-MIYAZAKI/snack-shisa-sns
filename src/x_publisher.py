"""X (Twitter) API v2 経由で画像付き投稿を行う。

前提:
- Xアプリの権限が「Read and Write」になっていること
- アクセストークンが権限変更後に再発行されていること
"""
import os

import tweepy


def publish_photo(image_path: str, caption: str) -> str:
    auth = tweepy.OAuth1UserHandler(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    api_v1 = tweepy.API(auth)
    media = api_v1.media_upload(filename=image_path)

    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    response = client.create_tweet(text=caption, media_ids=[media.media_id])
    return str(response.data["id"])
