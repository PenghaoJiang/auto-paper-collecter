#!/usr/bin/env python3
"""Fetch candidate papers/repos across all enabled sources, deduplicate against
history, and write state/candidates.json. Deterministic — NO LLM here.

The agent should first write its expanded queries to state/queries.json
(a JSON object: {"<keyword>": ["query1", "query2", ...]}). If that file is
absent, the raw keywords from config.json are used verbatim.

Usage:  cd skill/scripts && python3 fetch.py
"""
import os
import re
import datetime as dt
import xml.etree.ElementTree as ET

import common as C

A_NS = {"a": "http://www.w3.org/2005/Atom"}


def _recent(published, lookback_days):
    if not published:
        return True  # keep undated; agent can judge
    cutoff = dt.datetime.utcnow() - dt.timedelta(days=lookback_days)
    horizon = dt.datetime.utcnow() + dt.timedelta(days=2)  # drop garbage future dates
    return cutoff <= published <= horizon


# ---- per-source adapters (return list of dicts) ----------------------------

def src_arxiv(query, n):
    url = "http://export.arxiv.org/api/query?" + C.qs({
        "search_query": f'all:"{query}"', "sortBy": "submittedDate",
        "sortOrder": "descending", "max_results": n})
    txt = C.http_get(url)
    out = []
    if not txt:
        return out
    try:
        root = ET.fromstring(txt)
    except ET.ParseError:
        return out
    for e in root.findall("a:entry", A_NS):
        pub = e.findtext("a:published", default="", namespaces=A_NS)
        d = None
        if pub:
            try:
                d = dt.datetime.strptime(pub[:10], "%Y-%m-%d")
            except ValueError:
                pass
        out.append({
            "source": "arXiv",
            "title": " ".join((e.findtext("a:title", "", A_NS) or "").split()),
            "abstract": (e.findtext("a:summary", "", A_NS) or "").strip(),
            "url": e.findtext("a:id", "", A_NS),
            "authors": [a.findtext("a:name", "", A_NS) for a in e.findall("a:author", A_NS)],
            "venue": "arXiv", "doi": "", "published": d.isoformat() if d else "",
            "_d": d,
        })
    return out


def src_crossref(query, n):
    data = C.http_json("https://api.crossref.org/works?" + C.qs({
        "query": query, "sort": "published", "order": "desc", "rows": n,
        "select": "DOI,title,author,abstract,URL,container-title,published"}),
        headers={"User-Agent": "auto-paper-collecter-skill/1.0 (https://github.com/)"})
    out = []
    for it in ((data or {}).get("message", {}) or {}).get("items", []):
        titles = it.get("title") or []
        if not titles:
            continue
        parts = (it.get("published", {}) or {}).get("date-parts", [[None]])
        d = None
        if parts and parts[0] and parts[0][0]:
            p = parts[0] + [1, 1]
            try:
                d = dt.datetime(p[0], p[1], p[2])
            except (ValueError, TypeError):
                d = None
        doi = it.get("DOI", "")
        out.append({
            "source": "Crossref",
            "title": " ".join(titles[0].split()),
            "abstract": " ".join(re.sub(r"<[^>]+>", " ", it.get("abstract", "")).split()),
            "url": it.get("URL", ""),
            "authors": [" ".join(x for x in [a.get("given", ""), a.get("family", "")] if x)
                        for a in (it.get("author") or [])],
            "venue": (it.get("container-title") or [""])[0], "doi": doi,
            "published": d.isoformat() if d else "", "_d": d,
        })
    return out


def src_s2(query, n):
    headers = {}
    key = os.environ.get("SEMANTIC_SCHOLAR_KEY", "")
    if key:
        headers["x-api-key"] = key
    data = C.http_json("https://api.semanticscholar.org/graph/v1/paper/search?" + C.qs({
        "query": query, "limit": n, "fieldsOfStudy": "Computer Science",
        "fields": "title,abstract,authors,url,year,venue,tldr,publicationDate,externalIds"}),
        headers=headers)
    out = []
    for p in ((data or {}).get("data") or []):
        d = None
        if p.get("publicationDate"):
            try:
                d = dt.datetime.strptime(p["publicationDate"], "%Y-%m-%d")
            except ValueError:
                pass
        if not d and p.get("year"):
            d = dt.datetime(p["year"], 1, 1)
        out.append({
            "source": "Semantic Scholar",
            "title": " ".join((p.get("title") or "").split()),
            "abstract": (p.get("abstract") or "").strip(),
            "url": p.get("url", ""),
            "authors": [a.get("name", "") for a in (p.get("authors") or [])],
            "venue": p.get("venue", "") or "", "doi": (p.get("externalIds") or {}).get("DOI", "") or "",
            "tldr": ((p.get("tldr") or {}) or {}).get("text", "") if p.get("tldr") else "",
            "published": d.isoformat() if d else "", "_d": d,
        })
    return out


def src_github(query, n):
    headers = {"Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN", "")
    if tok:
        headers["Authorization"] = "Bearer " + tok
    # quality over recency: require traction (stars:>=10) + rank by stars
    data = C.http_json("https://api.github.com/search/repositories?" + C.qs({
        "q": f"{query} in:name,description stars:>=10", "sort": "stars", "order": "desc",
        "per_page": min(n, 12)}), headers=headers)
    out = []
    for it in ((data or {}).get("items") or []):
        pushed = it.get("pushed_at") or it.get("updated_at") or ""
        d = None
        if pushed:
            try:
                d = dt.datetime.strptime(pushed, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                pass
        out.append({
            "source": "GitHub",
            "title": it.get("full_name") or it.get("name", ""),
            "abstract": it.get("description") or "",
            "url": it.get("html_url", ""),
            "authors": [(it.get("owner") or {}).get("login", "")],
            "venue": f"★{it.get('stargazers_count', 0)}", "doi": "",
            "published": d.isoformat() if d else "", "_d": d,
        })
    return out


def src_huggingface(query, n):
    data = C.http_json("https://huggingface.co/api/papers/search?" + C.qs({"q": query}))
    out = []
    for entry in (data or [])[:n]:
        p = entry.get("paper", entry) if isinstance(entry, dict) else {}
        if not p or not p.get("title"):
            continue
        pid = p.get("id", "")
        d = None
        pub = p.get("publishedAt") or p.get("published_at") or ""
        if pub:
            try:
                d = dt.datetime.strptime(pub[:10], "%Y-%m-%d")
            except ValueError:
                pass
        out.append({
            "source": "HuggingFace",
            "title": " ".join((p.get("title") or "").split()),
            "abstract": (p.get("summary") or "").strip(),
            "url": f"https://huggingface.co/papers/{pid}" if pid else "",
            "authors": [a.get("name", "") if isinstance(a, dict) else str(a)
                        for a in (p.get("authors") or [])],
            "venue": "HuggingFace", "doi": "",
            "published": d.isoformat() if d else "", "_d": d,
        })
    return out


def src_paperswithcode(query, n):
    data = C.http_json("https://paperswithcode.com/api/v1/papers/?" + C.qs(
        {"q": query, "items_per_page": n}))
    out = []
    for p in ((data or {}).get("results") or [])[:n]:
        if not p.get("title"):
            continue
        d = None
        if p.get("published"):
            try:
                d = dt.datetime.strptime(p["published"][:10], "%Y-%m-%d")
            except ValueError:
                pass
        out.append({
            "source": "PapersWithCode",
            "title": " ".join((p.get("title") or "").split()),
            "abstract": (p.get("abstract") or "").strip(),
            "url": p.get("url_abs") or p.get("url_pdf") or "",
            "authors": p.get("authors") or [],
            "venue": "Papers with Code", "doi": p.get("doi", "") or "",
            "published": d.isoformat() if d else "", "_d": d,
        })
    return out


def src_rss(query, feeds, n):
    out = []
    kw = query.lower()
    for feed in feeds:
        txt = C.http_get(feed)
        if not txt:
            continue
        try:
            root = ET.fromstring(txt)
        except ET.ParseError:
            continue
        for item in root.iter():
            tag = item.tag.split("}")[-1]
            if tag not in ("item", "entry"):
                continue
            def t(name):
                for ch in item:
                    if ch.tag.split("}")[-1] == name:
                        return (ch.text or "").strip()
                return ""
            title, summ = t("title"), t("description") or t("summary")
            if kw not in (title + " " + summ).lower():
                continue
            link = t("link")
            out.append({"source": "RSS", "title": " ".join(title.split()),
                        "abstract": summ[:600], "url": link, "authors": [],
                        "venue": "RSS", "doi": "", "published": "", "_d": None})
            if len(out) >= n:
                break
    return out


SOURCES = {"arXiv": src_arxiv, "Crossref": src_crossref,
           "Semantic Scholar": src_s2, "GitHub": src_github,
           "HuggingFace": src_huggingface, "PapersWithCode": src_paperswithcode}


def main():
    cfg = C.config()
    enabled = cfg.get("sources", {})
    n = cfg.get("max_per_source", 15)
    lookback = cfg.get("lookback_days", 5)
    feeds = cfg.get("rss_feeds", [])

    # queries: agent-expanded if present, else raw keywords
    queries = C.load_json(os.path.join(C.STATE, "queries.json"), None)
    if not queries:
        queries = {kw: [kw] for kw in cfg.get("keywords", [])}

    seen = set(C.load_json(os.path.join(C.STATE, "seen.json"), []))
    by_key, candidates = {}, []
    for kw, qlist in queries.items():
        for q in qlist:
            for name, fn in SOURCES.items():
                if enabled.get(name, True):
                    for it in fn(q, n):
                        it["topic"] = kw
                        if not _recent(it.get("_d"), lookback):
                            continue
                        k = C.dedup_key(it)
                        if k in by_key or k in seen:
                            continue
                        by_key[k] = it
            if enabled.get("RSS", True) and feeds:
                for it in src_rss(q, feeds, n):
                    it["topic"] = kw
                    k = C.dedup_key(it)
                    if k not in by_key and k not in seen:
                        by_key[k] = it

    candidates = list(by_key.values())
    for it in candidates:
        it.pop("_d", None)
    candidates.sort(key=lambda x: x.get("published", ""), reverse=True)
    C.save_json(os.path.join(C.STATE, "candidates.json"), candidates)
    print(f"[fetch] {len(candidates)} new candidates across {len(queries)} keyword(s) "
          f"→ state/candidates.json")
    if not candidates:
        print("[fetch] nothing new since last run.")


if __name__ == "__main__":
    main()
