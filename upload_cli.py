import argparse
import os
from pathlib import Path

from src_blog.upload_draft import upload_draft
from src_blog.upload_image import upload_image

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Solution GIF")
    parser.add_argument(
        "input_gif",
        type=str,
        help="Path for the gif file.",
    )
    args = parser.parse_args()
    project_name = Path(args.input_gif).stem
    level, level_num = project_name.split("_")

    mapping = {
        "expert": "エキスパート",
        "pro": "プロ",
        "hard": "ハード",
        "master": "マスター",
    }
    if level not in mapping:
        print(f"{level} is not supported. So Uploading draft is skipped.")

    username = os.environ.get("HATENA_USER_NAME")
    api_key = os.environ.get("HATENA_API_KEY")
    folder_name = "MyFolder"  # アップロード先フォルダ名（任意）

    # Upload
    print("Uploading Gif file...")
    image_url = upload_image(
        username=username,
        api_key=api_key,
        image_path=args.input_gif,
        folder_name=folder_name,
    )
    print("Uploading blog post...")
    upload_draft(level=mapping[level], level_num=int(level_num), image_url=image_url)
