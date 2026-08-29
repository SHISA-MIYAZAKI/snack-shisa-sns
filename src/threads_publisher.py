"""Threads API 経由で画像投稿を行う。

前提:
- Meta開発者アプリに「Threads API」のユースケースが追加されていること
- 画像は公開URL（例: GitHub raw URL）からアクセス可能であること
"""
import os
import time

import requests

GRAPH_API_BASE = "https://graph.threads.net/v1.0"


def publish_photo(image_url: str, caption: str) -> str:
    threads_user_id = os.environ["THREADS_USER_ID"]
    access_token = os.environ["THREADS_ACCESS_TOKEN"]

    container_res = requests.post(
        f"{GRAPH_API_BASE}/{threads_user_id}/threads",
        data={
            "media_type": "IMAGE",
            "image_url": image_url,
            "text": caption,
            "access_token": access_token,
        },
        timeout=30,
    )
    container_res.raise_for_status()
    creation_id = container_res.json()["id"]

    # 画像処理が終わるまで少し待つ
    time.sleep(5)

    publish_res = requests.post(
        f"{GRAPH_API_BASE}/{threads_user_id}/threads_publish",
        data={"creation_id": creation_id, "access_token": access_token},
        timeout=30,
    )
    publish_res.raise_for_status()
    return publish_res.json()["id"]
