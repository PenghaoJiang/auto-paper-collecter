---
name: auto-paper-collecter
description: Personal research-paper radar. Fetches the latest papers and code repos for the user's keyword subscriptions across arXiv, Crossref (IEEE/ACM), Semantic Scholar, GitHub and RSS; deduplicates against history; then YOU (the assistant) expand the queries, filter for computer-science relevance, write Chinese summaries, detect hot sub-fields, and emit a Markdown + HTML digest (optionally emailed). Use when the user asks to "run my paper radar / 文献雷达", "check for new papers", "what's new in my topics", "今天有什么新论文 / 最新文献", "today's research digest", or to configure their keyword subscriptions / sources / schedule.
---

# auto-paper-collecter (skill)

A self-hosted research-literature radar that runs inside a coding agent.
**The Python scripts do only the deterministic work** (API fetch, dedup, render,
email). **YOU — the assistant running this skill — do all the judgement work**:
query expansion, computer-science relevance filtering, Chinese summaries, and
hot-topic synthesis. That means **no AI API key is needed** — whichever model is
running this skill (Claude in Claude Code, GPT in Codex, …) is the LLM.

## Layout
```
skill/
├── SKILL.md
├── scripts/   common.py · fetch.py · render.py · notify.py   (stdlib only)
├── state/     config.json · (queries/candidates/curated/trends/seen .json)
└── digests/   YYYY-MM-DD.md  +  .html
```
Run scripts from `scripts/`:  `cd skill/scripts && python3 <script>.py`

## Config — `state/config.json`
- `keywords`: up to ~3 topic strings to track.
- `domain`: the field to constrain relevance to (default `computer science`).
- `sources`: toggle `arXiv / Crossref / Semantic Scholar / GitHub / RSS`.
- `lookback_days`: how far back to fetch (dedup stops repeats anyway).
- `max_per_source`, `rss_feeds`.

When the user asks to change keywords / sources / field, **edit this file** and
confirm the change back to them.

> Optional env vars (never stored in the repo): `SEMANTIC_SCHOLAR_KEY` (lifts S2
> rate limits), `GITHUB_TOKEN` (lifts GitHub limits), and `SMTP_*` / `EMAIL_TO`
> for emailing the digest.

## The run pipeline — follow IN ORDER

### 1 · Read config & expand queries  *(you)*
Read `state/config.json`. For **each** keyword, think of **2–3 associative
English search queries** — synonyms, full forms, adjacent sub-topics — so recall
isn't limited to the literal term (e.g. `C2Rust` → `["C2Rust", "C-to-Rust
translation", "migrating legacy C code to Rust"]`). Write them to
`state/queries.json` as `{"<keyword>": ["q1", "q2", ...], ...}`.

### 2 · Fetch candidates  *(script)*
```bash
cd skill/scripts && python3 fetch.py
```
Fetches every enabled source for those queries, drops anything already in
`state/seen.json` or older than `lookback_days`, and writes
`state/candidates.json`. **If it reports 0 candidates, tell the user "暂无新文献"
and stop** (nothing else to do).

### 3 · Filter relevance & summarize  *(you)*
Read `state/candidates.json`. For each item decide: is it **(a) computer-science**
and **(b) genuinely on-topic** for its `topic` keyword? Drop the rest (medical
"translation", finance "AI", random GitHub star-lists, etc.). For every **kept**
item write a concise **Chinese** summary and assemble `state/curated.json` — a
list of objects:
```json
{"source","topic","title","url","venue","authors","published",
 "tldr":"一句话核心 (<=60字)","method":"方法简述 (<=80字)",
 "contributions":["核心贡献1","核心贡献2"]}
```
Keep papers first, GitHub repos last (they are a supplementary signal). If a
source gave a `tldr` already, you may build on it.

### 4 · Hot-topic synthesis  *(you, optional but recommended)*
Cluster the kept items into a handful of **coarse CS sub-fields** (自然语言处理 /
计算机视觉 / 系统与编译 …; merge aggressively). Write `state/trends.json`:
`{"top": [{"name","delta": <count>, "summary": "<=80字方向总结",
"papers": ["title", ...]}, ... up to 3]}`.

### 5 · Render the digest  *(script)*
```bash
cd skill/scripts && python3 render.py
```
Writes `digests/YYYY-MM-DD.md` + `.html` from `curated.json` (+ `trends.json`)
and records everything shown into `seen.json` so it won't repeat.

### 6 · Notify  *(script, optional)*
```bash
cd skill/scripts && python3 notify.py     # emails the HTML digest if SMTP_* env is set
```

### 7 · Report back  *(you)*
Tell the user how many papers were kept, the top hot directions, and the digest
path. Offer to open the HTML or adjust keywords.

## Notes
- Scripts are **pure Python stdlib** — no `pip install` required.
- `fetch.py` already filters garbage future dates and de-duplicates across runs.
- This skill is the agent-driven counterpart of the project's FastAPI web
  dashboard; both share the same sources and pipeline philosophy.
