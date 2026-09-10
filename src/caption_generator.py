"""店舗情報と写真の説明から、Instagram/X用のキャプションを自動生成する。"""
import json
import os
from pathlib import Path

from anthropic import Anthropic

ROOT = Path(__file__).resolve().parent.parent


def load_store_profile() -> dict:
    with open(ROOT / "config" / "store_profile.json", encoding="utf-8") as f:
        return json.load(f)


def build_prompt(store: dict, photo: dict, platform: str) -> str:
    max_len = "120字以内" if platform == "x" else "500字以内" if platform == "threads" else "300字以内"
    always_tags = " ".join(store.get("hashtags_always", []))
    return f"""あなたは宮崎のスナック「{store['store_name']}」のSNS担当です。
以下の情報をもとに、{platform.upper()}投稿用の日本語キャプションを1案作成してください。

【店舗情報】
- エリア: {store.get('area', '')}
- ターゲット層: {store.get('target_customer', '')}
- トーン: {store.get('brand_voice', {}).get('tone', '')}
- 使ってはいけない表現: {', '.join(store.get('brand_voice', {}).get('ng_words', [])) or 'なし'}

【今回の写真】
- 説明: {photo.get('description', '')}
- 投稿シーン: {photo.get('occasion', '')}

【条件】
- {max_len}
- 誇張・虚偽の表現（実在しない在庫状況や誤解を招く価格表記など）は書かない
- 最後に必ずこのハッシュタグを含める: {always_tags}
- キャプション本文のみを出力し、前置きや説明文は書かない
"""


def generate_caption(store: dict, photo: dict, platform: str) -> str:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=400,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": build_prompt(store, photo, platform)}],
    )
    text_block = next(block for block in message.content if block.type == "text")
    return text_block.text.strip()


if __name__ == "__main__":
    store = load_store_profile()
    sample_photo = {"description": "テスト用サンプル写真", "occasion": "通常投稿"}
    print(generate_caption(store, sample_photo, "instagram"))
