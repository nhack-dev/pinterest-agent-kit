"""ピンを作る（画像URLから）。

  python3 scripts/pin_create.py --file drafts/pin-2026-11-01.md          # 見るだけ
  python3 scripts/pin_create.py --file drafts/pin-2026-11-01.md --go     # 作る

md の形（templates/pin.md）：
  - board: <ボードID>
  - image: https://（公開URL）
  - link: https://（飛び先・任意）
  ## タイトル（100字まで） / ## 説明（800字まで） / ## 代替テキスト（500字まで）
公式の決まり：自分で作った新しいコンテンツを載せるための機能。他人の画像を載せない。
"""
from __future__ import annotations

import os as _ng_os, sys as _ng_sys  # N-Hack 専用の門（下の3行を消すとこのキットは動きません）
_ng_sys.path.insert(0, _ng_os.path.dirname(_ng_os.path.abspath(__file__)))
import nhack_gate as _nhack_gate  # noqa: E402,F401


import argparse
import re
import sys

import pin
from _common import append_log, read_text_arg


def parse(md: str) -> dict:
    d = {k: (re.search(rf"^- {k}:\s*(\S+)", md, re.M) or [None, None])[1] for k in ("board", "image", "link")}
    for key, name in (("title", "タイトル"), ("description", "説明"), ("alt_text", "代替テキスト")):
        m = re.search(rf"^## {name}\s*\n(.*?)(?=^## |\Z)", md, re.S | re.M)
        d[key] = m.group(1).strip() if m else None
    return d


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    p.add_argument("--go", action="store_true")
    a = p.parse_args()
    d = parse(read_text_arg(None, a.file))
    for k, lim in (("title", 100), ("description", 800), ("alt_text", 500), ("link", 2048)):
        if d.get(k) and len(d[k]) > lim:
            sys.exit(f"[止めました] {k} が {len(d[k])} 字（上限 {lim}）")
    if not d.get("board") or not d.get("image"):
        sys.exit("[止めました] board と image は必ず書く")
    body = {"board_id": d["board"], "media_source": {"source_type": "image_url", "url": d["image"]}}
    for k in ("title", "description", "alt_text", "link"):
        if d.get(k):
            body[k] = d[k]
    r = pin.post_json("pins", body, a.go)
    if r:
        append_log("pin-created.jsonl", {"id": r.get("id"), "title": d.get("title")})
        print("作りました:", r.get("id"))


if __name__ == "__main__":
    main()
