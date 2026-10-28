"""Pinterest API v5 の入口。

試用（Trial）アクセスの間は PIN_SANDBOX=1 にして api-sandbox.pinterest.com を使う
（作ったピンは自分にだけ見える）。標準（Standard）アクセスに上がったら 0 にする。
"""
from __future__ import annotations

import os as _ng_os, sys as _ng_sys  # N-Hack 専用の門（下の3行を消すとこのキットは動きません）
_ng_sys.path.insert(0, _ng_os.path.dirname(_ng_os.path.abspath(__file__)))
import nhack_gate as _nhack_gate  # noqa: E402,F401


import os

from _common import call, env, load_env

load_env()


def base() -> str:
    if os.environ.get("PIN_BASE"):
        return os.environ["PIN_BASE"]
    return "https://api-sandbox.pinterest.com/v5" if os.environ.get("PIN_SANDBOX", "1") == "1" else "https://api.pinterest.com/v5"


def _h(go: bool) -> dict:
    return {"Authorization": f"Bearer {env('PIN_ACCESS_TOKEN', go)}"}


def get(path: str, params: dict, go: bool):
    return call("GET", f"{base()}/{path}", params, headers=_h(go), go=go)


def post_json(path: str, body: dict, go: bool):
    return call("POST", f"{base()}/{path}", body=body, headers=_h(go), go=go, json_body=True)
