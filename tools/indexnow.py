#!/usr/bin/env python3
"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver and others) which pages changed.

Bing's index feeds ChatGPT search and Microsoft Copilot, so this is the shortest path from a commit
to an AI answer engine noticing it. The key file lives in tools/static/ and is published at the
site root by build_site.py.

    python tools/indexnow.py BASE_SHA [HEAD_SHA]   # pages whose docs/ HTML changed in that range
    python tools/indexnow.py all                   # every URL in docs/sitemap.xml
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "tools" / "static"
SITEMAP = ROOT / "docs" / "sitemap.xml"


def site() -> str:
    """The site root: the shortest URL in the sitemap is the home page."""
    return min(all_urls(), key=len).rstrip("/")


def key() -> str:
    for f in STATIC.glob("*.txt"):
        if re.fullmatch(r"[0-9a-f]{32}", f.stem) and f.read_text().strip() == f.stem:
            return f.stem
    sys.exit("No IndexNow key file found in tools/static/")


def all_urls() -> list[str]:
    return re.findall(r"<loc>(.*?)</loc>", SITEMAP.read_text(encoding="utf-8"))


def changed_urls(base: str, head: str) -> list[str]:
    files = subprocess.run(
        ["git", "diff", "--name-only", base, head, "--", "docs"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    root = site()
    return [
        f"{root}/{f.removeprefix('docs/').removesuffix('index.html')}"
        for f in files
        if f.endswith("index.html")
    ]


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] == "all" or set(sys.argv[1]) == {"0"}:
        urls = all_urls()
    else:
        urls = changed_urls(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "HEAD")
    if not urls:
        print("IndexNow: no changed pages to submit.")
        return
    root, k = site(), key()
    body = {
        "host": urlparse(root).netloc,
        "key": k,
        "keyLocation": f"{root}/{k}.txt",
        "urlList": urls[:10000],
    }
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: HTTP {r.status} for {len(urls)} URL(s).")
    except urllib.error.HTTPError as e:
        # 403 means the key file is not live yet (first deploy); the next run will succeed.
        print(f"IndexNow: HTTP {e.code} {e.reason}. Submitted nothing.")


if __name__ == "__main__":
    main()
