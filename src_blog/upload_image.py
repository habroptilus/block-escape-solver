import base64
import datetime
import hashlib
import os
import xml.etree.ElementTree as ET

import requests

POST_URI = "https://f.hatena.ne.jp/atom/post"  # はてなフォトライフのエンドポイント


def extract_image_url(xml_data) -> str | None:
    # XMLをパース
    root = ET.fromstring(xml_data)

    # 名前空間の辞書を定義
    namespaces = {
        "atom": "http://purl.org/atom/ns#",
        "hatena": "http://www.hatena.ne.jp/info/xmlns#",
        "dc": "http://purl.org/dc/elements/1.1/",
    }

    # hatena:syntax要素を取得
    syntax_elem = root.find("hatena:syntax", namespaces)
    if syntax_elem is not None:
        return syntax_elem.text
    else:
        return


def _generate_wsse_header(username: str, api_key: str):
    nonce = os.urandom(16)  # 16バイトのランダムデータ
    created = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    nonce_b64 = base64.b64encode(nonce).decode("utf-8")

    digest_source = nonce + created.encode("utf-8") + api_key.encode("utf-8")
    password_digest = base64.b64encode(hashlib.sha1(digest_source).digest()).decode(
        "utf-8"
    )

    wsse_header = f'UsernameToken Username="{username}", PasswordDigest="{password_digest}", Nonce="{nonce_b64}", Created="{created}"'

    return wsse_header


def upload_image(
    username: str,
    api_key: str,
    image_path: str,
    folder_name: str = "default",
    title: str = "Uploaded Image",
    generator: str = "MyUploader",
) -> str:
    with open(image_path, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode("utf-8")

    if image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
        content_type = "image/jpeg"
    elif image_path.lower().endswith(".png"):
        content_type = "image/png"
    elif image_path.lower().endswith(".gif"):
        content_type = "image/gif"
    else:
        raise ValueError("Unsupported file type")

    xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://purl.org/atom/ns#"
       xmlns:dc="http://purl.org/dc/elements/1.1/">
  <title>{title}</title>
  <content mode="base64" type="{content_type}">{image_data}</content>
  <dc:subject>{folder_name}</dc:subject>
  <generator>{generator}</generator>
</entry>"""

    headers = {
        "X-WSSE": _generate_wsse_header(username, api_key),
        "Content-Type": "application/xml",
    }

    response = requests.post(POST_URI, headers=headers, data=xml_data)

    return extract_image_url(response.text)


if __name__ == "__main__":
    # **使用例**
    username = os.environ.get("HATENA_USER_NAME")
    api_key = os.environ.get("HATENA_API_KEY")
    image_path = "solutions/expert_1.gif"  # アップロードする画像のパス
    folder_name = "MyFolder"  # アップロード先フォルダ名（任意）

    image_url = upload_image(username, api_key, image_path, folder_name)
    print(image_url)
