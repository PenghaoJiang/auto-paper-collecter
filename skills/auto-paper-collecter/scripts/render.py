#!/usr/bin/env python3
"""Render the agent-curated papers into a Markdown + HTML digest, and append the
rendered items to state/seen.json so they aren't shown again.

Reads:
  state/curated.json  – list the AGENT wrote: kept papers, each with
                        {source, topic, title, url, venue, authors, published,
                         tldr, method, contributions[]}
  state/trends.json   – optional: {"top": [{name, delta, summary, papers[]}...]}

Usage:  cd skill/scripts && python3 render.py
"""
import os
import html
import common as C

SRC_COLOR = {"arXiv": "#B31B1B", "Crossref": "#5B6470", "Semantic Scholar": "#1A73E8",
             "GitHub": "#1F2328", "RSS": "#7C4DD9"}


def _md(curated, trends, day):
    lines = [f"# 📚 文献雷达 · {day}\n", f"今日精选 **{len(curated)}** 篇。\n"]
    if trends and trends.get("top"):
        lines.append("\n## 🔥 领域热点\n")
        for t in trends["top"]:
            lines.append(f"- **{t.get('name','')}** (+{t.get('delta','')}) — {t.get('summary','')}")
        lines.append("")
    lines.append("\n## 📰 今日文献\n")
    for p in curated:
        au = ", ".join((p.get("authors") or [])[:4])
        head = f"### [{p.get('title','')}]({p.get('url','')})"
        meta = f"`{p.get('source','')}` · {p.get('published','')} · {au} {('· '+p['venue']) if p.get('venue') else ''}"
        lines.append(head)
        lines.append(meta + "\n")
        if p.get("tldr"):
            lines.append(f"> **TL;DR** {p['tldr']}")
        if p.get("method"):
            lines.append(f"> **方法** {p['method']}")
        for c in (p.get("contributions") or []):
            lines.append(f"> - {c}")
        lines.append("")
    return "\n".join(lines)


def _html(curated, trends, day):
    def esc(s):
        return html.escape(str(s or ""))
    parts = ['<div style="font-family:system-ui,sans-serif;max-width:720px;margin:0 auto;color:#16181D">',
             f'<h1 style="color:#2A5BD7">📚 文献雷达 · {esc(day)}</h1>',
             f'<p style="color:#5B6470">今日精选 <b>{len(curated)}</b> 篇。</p>']
    if trends and trends.get("top"):
        parts.append('<h2>🔥 领域热点</h2><ul>')
        for t in trends["top"]:
            parts.append(f'<li><b>{esc(t.get("name"))}</b> (+{esc(t.get("delta"))}) — {esc(t.get("summary"))}</li>')
        parts.append('</ul>')
    parts.append('<h2>📰 今日文献</h2>')
    for p in curated:
        color = SRC_COLOR.get(p.get("source"), "#5B6470")
        au = esc(", ".join((p.get("authors") or [])[:4]))
        parts.append('<div style="border:1px solid #EAEDF1;border-radius:12px;padding:14px 16px;margin:0 0 14px">')
        parts.append(f'<div style="font-size:12px"><span style="color:{color};font-weight:700">{esc(p.get("source"))}</span> '
                     f'<span style="color:#888">· {esc(p.get("published"))} · {au}</span></div>')
        parts.append(f'<a href="{esc(p.get("url"))}" style="font-size:17px;font-weight:600;color:#16181D;text-decoration:none">{esc(p.get("title"))}</a>')
        if p.get("tldr"):
            parts.append(f'<p style="font-size:14px;color:#333;margin:8px 0 4px"><b>TL;DR</b> {esc(p["tldr"])}</p>')
        if p.get("method"):
            parts.append(f'<p style="font-size:13px;color:#555;margin:2px 0"><b>方法</b> {esc(p["method"])}</p>')
        if p.get("contributions"):
            parts.append('<ul style="font-size:13px;color:#444;margin:6px 0">'
                         + "".join(f"<li>{esc(c)}</li>" for c in p["contributions"]) + '</ul>')
        parts.append('</div>')
    parts.append('</div>')
    return "\n".join(parts)


def main():
    day = C.today()
    curated = C.load_json(os.path.join(C.STATE, "curated.json"), [])
    trends = C.load_json(os.path.join(C.STATE, "trends.json"), None)
    if not curated:
        print("[render] curated.json is empty — nothing to render. "
              "Did the agent write its kept+summarized papers there?")
        return

    C._ensure_dirs()
    md_path = os.path.join(C.DIGESTS, f"{day}.md")
    html_path = os.path.join(C.DIGESTS, f"{day}.html")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(_md(curated, trends, day))
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(_html(curated, trends, day))

    # remember everything we just showed so it won't repeat
    seen = C.load_json(os.path.join(C.STATE, "seen.json"), [])
    seen_set = set(seen)
    for p in curated:
        k = C.dedup_key(p)
        if k not in seen_set:
            seen.append(k)
            seen_set.add(k)
    C.save_json(os.path.join(C.STATE, "seen.json"), seen[-5000:])  # cap history

    print(f"[render] wrote {md_path}")
    print(f"[render] wrote {html_path}")
    print(f"[render] seen history now {len(seen)} items")


if __name__ == "__main__":
    main()
