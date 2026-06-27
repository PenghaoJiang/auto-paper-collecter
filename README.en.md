<div align="center">

🌐 [简体中文](./README.md) ｜ **English**

# 📚🔭 auto-paper-collecter

### *Your Personal Research Radar*

Every morning, let AI sweep arXiv for you and bring the latest, most relevant papers to your door ☕✨

<br>

<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/LLM-powered-8A5CF6?logo=openai&logoColor=white" alt="LLM">
<img src="https://img.shields.io/badge/License-MIT-22c55e" alt="License">
<img src="https://img.shields.io/badge/PRs-welcome-ff69b4" alt="PRs Welcome">
<img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20%26%20%E2%98%95-red" alt="Made with love">
<a href="https://skillhub.cn/skills/auto-paper-collecter"><img src="https://img.shields.io/badge/SkillHub-listed-22c55e" alt="SkillHub"></a>

<br>
<sub>If it saves you time scrolling arXiv, a ⭐ would mean a lot to the author!</sub>

</div>

---

## 🆕 What's New

### ✨ v1.1 — UX & smarts upgrade · 2026-06-27

<table>
<tr><td>🎨&nbsp;<b>UX</b></td><td>Responsive mobile layout · polished <b>dark mode</b> (elegant dark-gray cards, not black) · live <b>refresh progress</b> (summarizing 12/20…)</td></tr>
<tr><td>🧠&nbsp;<b>Smarter</b></td><td><b>👍/👎 feedback learning</b> (down-voted topics get pushed less) · sort by newest / oldest / source · all / unread / read filter</td></tr>
<tr><td>🛰️&nbsp;<b>More sources</b></td><td>added <b>HuggingFace</b> & <b>Papers with Code</b>; GitHub now <b>ranked by stars</b> — only substantive repos</td></tr>
<tr><td>🔔&nbsp;<b>Multi-channel push</b></td><td><b>WeChat</b> (WeCom robot / Server酱) · <b>Telegram</b> · <b>Slack</b></td></tr>
<tr><td>⚡&nbsp;<b>Faster & sturdier</b></td><td>concurrent summaries with fail-fast fallback; GitHub uses repo description, no AI summary (fixes garbled text)</td></tr>
<tr><td>🐳&nbsp;<b>One-command deploy</b></td><td><code>docker compose up -d</code>, DB persisted to <code>./data</code></td></tr>
<tr><td>🤖&nbsp;<b>Skill in sync</b></td><td>all fetch / push improvements mirrored into the Agent Skill</td></tr>
</table>

> **2026-06-27 · Now listed on SkillHub** 🎉
>
> This skill is now live on **[SkillHub](https://skillhub.cn/skills/auto-paper-collecter)** — browse / get it right from the platform.

> **2026-06-26 · The Agent Skill is now a one-command Claude Code plugin, with Codex support** 🤖🔌
>
> Besides the web app, the repo ships a **Claude Code / Codex–compatible Agent Skill** — just say **"run my paper radar"**
> and it runs the whole pipeline and produces today's digest, **pure Python stdlib, zero deps, no AI API key**.
> **Install in one line:** `/plugin marketplace add PenghaoJiang/auto-paper-collecter` → `/plugin install auto-paper-collecter@auto-paper-collecter`.
> Also added [`AGENTS.md`](AGENTS.md) so **Codex / OpenAI agents work out of the box**. 👉 See **"🤖 Use as an Agent Skill"** below.

---

## 🌟 What is this

**auto-paper-collecter** is a lightweight, self-hosted **academic-paper aggregator**.

Tell it a few keywords you care about, and every day it automatically:

> 🛰️ Searches across **arXiv / Crossref (incl. IEEE·ACM) / Semantic Scholar / GitHub / RSS**
> 🧠 Uses an **LLM for "associative" query expansion** — not just literal keyword matching
> 🎯 Uses an **LLM to filter out off-domain / irrelevant papers** — keeping only on-topic CS work
> ✍️ Writes a **summary** for each (one-line TL;DR / method / key contributions)
> 📊 Analyzes **hot topics**, generates **weekly reports**, and **emails / browser-notifies** you

A zero-build single-page dashboard, same-origin front + back, ready out of the box.

> Note: the dashboard UI and built-in summaries default to Chinese — adapt the prompts/templates for other languages.

---

## 🎯 Motivation

> [!NOTE]
> One of the most tiring parts of research is **keeping up with the literature**.
> arXiv adds hundreds of papers a day; keyword search either misses synonymous phrasings or drowns you
> in cross-domain noise. Doing it by hand is slow and easy to miss things.

So this little tool **automates** "reading the latest papers every day", and hands the two dirtiest jobs to an LLM:

1. **Think broader**: `C2Rust` should also match `C-to-Rust translation`, `migrating legacy C code to Rust`…
2. **Filter sharper**: keep out same-name cross-domain noise like *translation* in medicine or *AI* in finance.

So when you open the page, you see **a clean, time-sorted, summarized daily feed**. 🫧

---

## ✨ Features

| | Feature | Description |
|:--:|---|---|
| 📰 | **Daily feed** | Multi-source aggregation sorted by real publication date; smart backfill when nothing is new; live top-bar search |
| 🧠 | **LLM-smart fetching** | Keyword associative expansion + CS-domain relevance filtering — broader recall, less noise |
| 🔥 | **Hot topics** | LLM clusters into mainstream sub-fields, counts the last 7/30 days, Top 3 get a **detailed summary** + their papers |
| ⭐ | **Library & notes** | One-click save, take notes, copy **BibTeX** |
| 🗞️ | **Weekly report** | Weekly picks + per-direction recap, auto-archived |
| 🔔 | **Notifications** | Browser notifications + optional **SMTP email digest** (scheduled) |
| 🛰️ | **Live GitHub source** | Also tracks the latest topic-relevant repos / paper code |
| 🌏 | **Localization** | Chinese-friendly UI & summaries, configurable timezone |

---

## 🧩 How it works

```mermaid
flowchart LR
    A([🔑 Your keywords]) --> B{{🧠 LLM query expansion}}
    B --> S1[arXiv]
    B --> S2[Crossref]
    B --> S3[Semantic Scholar]
    B --> S4[GitHub]
    B --> S5[RSS]
    S1 --> M[🧹 Cross-source dedup]
    S2 --> M
    S3 --> M
    S4 --> M
    S5 --> M
    M --> F{{🎯 LLM relevance filter}}
    F --> Z{{✍️ LLM summaries}}
    Z --> DB[(🗄️ SQLite)]
    DB --> UI([📊 Dashboard / Email / Weekly])
```

<div align="center"><sub>Deterministic steps in plain Python; the "judgement" goes to the LLM — fast and accurate.</sub></div>

---

## 🚀 Quick Start

```bash
# 1) Clone & enter
git clone https://github.com/PenghaoJiang/auto-paper-collecter.git
cd auto-paper-collecter

# 2) venv & deps
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3) Configure (copy the template, then edit .env with your AI gateway etc.)
cp .env.example .env

# 4) Take off 🛫
python run.py
```

Open **http://localhost:8000** → go to "Settings" to add keywords → click "Save & Fetch".

> 🐳 **Or one-line with Docker:** `cp .env.example .env` (optional) → `docker compose up -d`; the DB persists to `./data`.

> [!TIP]
> Use **English** keywords (higher recall across sources). The first fetch + summaries take ~1–3 min in the background; the page updates automatically when done.

---

## 🤖 Use as an Agent Skill

Besides the web app, the repo ships a **Claude Code / Codex–compatible Agent Skill** (the [`skills/auto-paper-collecter/`](skills/auto-paper-collecter/) directory) —
just tell your AI assistant **"run my paper radar"** and it runs the whole pipeline and produces today's digest,
with **no AI API key needed** (the model running the skill *is* the LLM).

**Option 1 · Install as a Claude Code plugin (recommended, one-liner)**

```bash
/plugin marketplace add PenghaoJiang/auto-paper-collecter
/plugin install auto-paper-collecter@auto-paper-collecter
```

**Option 2 · Copy the skill directory directly**

```bash
cp -r skills/auto-paper-collecter ~/.claude/skills/auto-paper-collecter
$EDITOR ~/.claude/skills/auto-paper-collecter/state/config.json   # edit your keywords
```

Then tell Claude Code **"run my paper radar / what's new today"**. The scripts are **pure Python stdlib, zero-dep**;
deterministic fetching is done by the scripts, while the LLM judgement (expansion / relevance filter / summaries /
hot-topics) is done by the model running the skill (Claude Code → Claude; Codex → GPT). See [`skills/auto-paper-collecter/SKILL.md`](skills/auto-paper-collecter/SKILL.md).

> 📦 This skill is also listed on **[SkillHub](https://skillhub.cn/skills/auto-paper-collecter)** — browse / get it there.

---

## ⚙️ Configuration

Everything lives in `.env` (see `.env.example`):

| Variable | Required | Description |
|---|:--:|---|
| `AI_BASE_URL` / `AI_API_KEY` / `AI_MODEL` | ✅ | Any **OpenAI-compatible** gateway. With `AI_ENABLED=false` it falls back to raw summaries and skips the LLM |
| `SEMANTIC_SCHOLAR_KEY` | ⬜ | Optional; works without one, just stricter rate limits |
| `GITHUB_TOKEN` | ⬜ | Optional; raises the GitHub search rate limit |
| `SMTP_*` / `EMAIL_*` | ⬜ | Optional; the scheduler emails the daily digest (Gmail needs an **App Password**) |
| `REFRESH_TIMES` / `TIMEZONE` | ⬜ | Daily refresh times & timezone (default `10:00,22:00` / `Asia/Shanghai`) |
| `BACKFILL_N` / `RSS_FEEDS` | ⬜ | Backfill count / academic-news RSS feeds |

> [!IMPORTANT]
> `.env` is gitignored — **your keys are never committed**. Keep them safe 🔐

---

## 🛰️ Data Sources

| Source | Content | Notes |
|---|---|---|
| **arXiv** | Preprints (official API) | The CS workhorse |
| **Crossref** | Journal/conference metadata | Incl. IEEE·ACM; metadata + abstract only |
| **Semantic Scholar** | General scholarly search | Built-in TLDR; constrained to CS |
| **GitHub** | Live repos / paper code | A supplementary signal |
| **HuggingFace** | Trending preprints (upvoted) | Complements arXiv |
| **Papers with Code** | Papers + official code | When the public API is up |
| **RSS** | Academic news / blogs | Custom feeds supported |

---

## 📡 API

<details>
<summary>Click to expand all endpoints</summary>

| Method | Path | Description |
|---|---|---|
| `GET`  | `/api/bootstrap` | Everything the dashboard needs in one shot (feed / library / trends / weekly / settings) |
| `POST` | `/api/refresh` | Trigger a background fetch (returns immediately; front-end polls `refreshing`) |
| `GET`  | `/api/trends?domain=&window=7` | Hot topics (Top 3 + per-direction deltas + papers) |
| `GET`  | `/api/report/weekly` | Generate / get the latest weekly report |
| `POST` | `/api/library/{paper_id}` | `{saved, read, note}` save / read / note |
| `GET·PUT` | `/api/settings` | Keywords / sources / times / backfill N / push / email |
| `POST` | `/api/test-email` | Send a test email to verify SMTP |

</details>

---

## 🗺️ Roadmap

- [x] Multi-source aggregation + LLM expansion + relevance filter
- [x] Hot topics (sub-fields + detailed summaries + paper lists)
- [x] Library / notes / BibTeX / weekly report
- [x] Browser + email push, scheduled jobs
- [x] More sources (HuggingFace · Papers with Code)
- [x] One-click Docker deploy
- [x] Mobile layout + dark mode + 👍/👎 feedback learning + multi-channel push
- [ ] Multi-user + auth (PostgreSQL)
- [ ] Mobile-friendly layout

> Request features in [Issues](../../issues)! 🙌

---

## 🤝 Contributing

This is a **side-project polished in spare time**, and it grows with your help — **contributions of any kind are very welcome!** 🌱✨

- 🐛 **Found a bug** → open an [Issue](../../issues)
- 💡 **Have an idea / want to chat** → brainstorm in [Discussions](../../discussions) 🧠
- ✨ **Want a feature** → make a wish in [Issues](../../issues)
- 🔧 **Want to build** → Fork → change → open a **Pull Request**

Whether it's fixing a typo, improving a doc, or adding a new source — **every contribution counts** 💗
You're also welcome to just drop by [Discussions](../../discussions) to share your research workflow and keyword setups — let's grow this little radar together 🚀

---

<div align="center">

### ⭐ If you find it useful, please drop a Star!

<sub>Every Star keeps the author motivated 🌱</sub>

<sub>Ideas, questions, or want to co-build? Come hang out in <a href="../../discussions">💬 Discussions</a>!</sub>

<br><br>

**📚 Read less, know more. Let the radar do the scanning.** 🔭

<br>

<sub>Made with ❤️ & ☕ · Licensed under <a href="./LICENSE">MIT</a></sub>

</div>
