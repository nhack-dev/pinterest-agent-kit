"""ピンの数字（表示・保存・クリック）を取る。

  python3 scripts/pin_analytics.py --days 30 --go     # data/pin-created.jsonl のピン全部
公式の名前：IMPRESSION SAVE PIN_CLICK OUTBOUND_CLICK
"""
from __future__ import annotations

import os as _ng_os, sys as _ng_sys  # N-Hack 専用の門（下の3行を消すとこのキットは動きません）
_ng_sys.path.insert(0, _ng_os.path.dirname(_ng_os.path.abspath(__file__)))
import nhack_gate as _nhack_gate  # noqa: E402,F401


import argparse
import csv
import datetime as dt

import pin
from _common import DATA, read_log, today

p = argparse.ArgumentParser()
p.add_argument("--days", type=int, default=30)
p.add_argument("--pin", action="append", help="ピンID（省略時は作った記録のピン全部）")
p.add_argument("--go", action="store_true")
a = p.parse_args()
end = dt.date.today()
start = end - dt.timedelta(days=min(a.days, 90))
ids = a.pin or [x["id"] for x in read_log("pin-created.jsonl") if x.get("id")] or ["<PIN_ID>"]
M = ["IMPRESSION", "SAVE", "PIN_CLICK", "OUTBOUND_CLICK"]
rows = []
for pid in ids:
    r = pin.get(f"pins/{pid}/analytics", {"start_date": start.isoformat(), "end_date": end.isoformat(),
                                          "metric_types": ",".join(M)}, a.go)
    if r:
        block = r.get("all") or next(iter(r.values()), {})  # 返り値は {"all": {...}} の形（アプリ種別ごと）
        lifetime = block.get("summary_metrics") or block.get("lifetime_metrics") or {}
        rows.append({"pin": pid, **{m: lifetime.get(m) for m in M}})
if rows:
    DATA.mkdir(exist_ok=True)
    path = DATA / f"pin-{today()}.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pin"] + M)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} 本 → data/{path.name}")
