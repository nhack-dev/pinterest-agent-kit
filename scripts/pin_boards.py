"""自分のボードの一覧（ボードIDを調べる）。

  python3 scripts/pin_boards.py --go
"""

import os as _ng_os, sys as _ng_sys  # N-Hack 専用の門（下の3行を消すとこのキットは動きません）
_ng_sys.path.insert(0, _ng_os.path.dirname(_ng_os.path.abspath(__file__)))
import nhack_gate as _nhack_gate  # noqa: E402,F401

import argparse

import pin

p = argparse.ArgumentParser()
p.add_argument("--go", action="store_true")
a = p.parse_args()
r = pin.get("boards", {"page_size": "100"}, a.go)
if r:
    for b in r.get("items", []):
        print(f"{b['id']}  {b.get('name')}  （{b.get('privacy')}）")
