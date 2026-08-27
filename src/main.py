"""定期実行のエントリーポイント。
未投稿の写真を1件選び、Instagram/Xそれぞれにキャプションを生成して投稿し、
photo_manifest.json を更新する。
"""
import json
import os
from pathlib import Path

from caption_generator import generate_caption, load_store_profile
import instagram_publisher
import x_publisher

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "content" / "photo_manifest.json"


def load_manifest() -> list[dict]:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: list[dict]) -> None:
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def public_image_url(relative_path: str) -> str:
    repo = os.environ["GITHUB_REPOSITORY"]  # 例: "user/BARSHISA"
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{relative_path}"


def main() -> None:
    manifest = load_manifest()
    target = next((p for p in manifest if not p.get("posted")), None)
    if target is None:
        print("投稿可能な未投稿写真がありません。content/photo_manifest.json に追加してください。")
        return

    store = load_store_profile()
    local_path = ROOT / target["file"]

    ig_caption = generate_caption(store, target, "instagram")
    ig_id = instagram_publisher.publish_photo(public_image_url(target["file"]), ig_caption)
    print(f"Instagram投稿完了: {ig_id}")

    x_caption = generate_caption(store, target, "x")
    x_id = x_publisher.publish_photo(str(local_path), x_caption)
    print(f"X投稿完了: {x_id}")

    target["posted"] = True
    save_manifest(manifest)


if __name__ == "__main__":
    main()
