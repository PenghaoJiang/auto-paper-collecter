"""Shared helpers for the auto-paper-collecter skill. Python stdlib only."""
import os
import re
import json
import gzip
import datetime as dt
import urllib.request
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # skill/
STATE = os.path.join(ROOT, "state")
DIGESTS = os.path.join(ROOT, "digests")


def _ensure_dirs():
    os.makedirs(STATE, exist_ok=True)
    os.makedirs(DIGESTS, exist_ok=True)


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    _ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def config():
    return load_json(os.path.join(STATE, "config.json"), {
        "keywords": [], "domain": "computer science",
        "sources": {"arXiv": True, "Crossref": True, "Semantic Scholar": True,
                    "GitHub": True, "HuggingFace": True, "PapersWithCode": True,
                    "RSS": True},
        "lookback_days": 5, "max_per_source": 15,
        "rss_feeds": ["http://export.arxiv.org/rss/cs.PL"],
    })


def http_get(url, headers=None, timeout=30):
    """GET a URL → decoded text (handles gzip). Returns '' on failure."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "auto-paper-collecter-skill/1.0",
        "Accept-Encoding": "gzip", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return raw.decode("utf-8", "replace")
    except Exception as e:
        print(f"[fetch] GET failed {url[:80]}…: {e}")
        return ""


def http_json(url, headers=None, timeout=30):
    txt = http_get(url, headers, timeout)
    try:
        return json.loads(txt) if txt else None
    except json.JSONDecodeError:
        return None


def qs(params):
    return urllib.parse.urlencode(params)


_norm = re.compile(r"[^a-z0-9一-鿿]+")


def dedup_key(item):
    if item.get("doi"):
        return "doi:" + item["doi"].lower()
    return "title:" + _norm.sub("", (item.get("title") or "").lower())[:80]


def today(tz_hours=8):
    return (dt.datetime.utcnow() + dt.timedelta(hours=tz_hours)).date().isoformat()
