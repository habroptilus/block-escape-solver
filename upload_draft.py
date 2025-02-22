import subprocess


def upload_draft(level: str, level_num: int):
    template = f"""---
Title: スマホアプリ『ナンバーパズル - ブロック脱出』{level} レベル{level_num} 解答
Category:
  - ブロック脱出-{level}
Draft: yes
---

スマホアプリ『ナンバーパズル』のブロック脱出の

**{level} レベル {level_num}** の解答例です。

# 解答 (gif)"""

    command = ["blogsync", "post", "guglilac.hatenablog.com"]
    process = subprocess.run(command, input=template, text=True, capture_output=True)

    if process.returncode == 0:
        print("Blog post successfully uploaded.")
    else:
        print("Error uploading blog post:", process.stderr)


if __name__ == "__main__":
    level = "ハード"
    level_num = "50"
    upload_draft(level=level, level_num=level_num)
