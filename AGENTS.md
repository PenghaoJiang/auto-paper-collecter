# AGENTS.md — auto-paper-collecter

Guidance for coding agents (Codex, OpenAI-based agents, Cursor, etc.) working in
or running this repository. Claude Code users: see [`skills/auto-paper-collecter/SKILL.md`](skills/auto-paper-collecter/SKILL.md)
(this file mirrors it in the cross-platform [agents.md](https://agentskills.io) style).

## What this repo is
A self-hosted **research-paper radar**. Two ways to use it:
- **Web app** — FastAPI + SQLite dashboard (`app/`, `static/`, `run.py`).
- **Agent skill** — `skills/auto-paper-collecter/`: deterministic Python fetch/render scripts + a
  pipeline that *you, the agent, drive* (you do the LLM judgement). **No AI API
  key is required** — whichever model is running you is the LLM.

## Running the paper-radar pipeline (agent skill)

All scripts are **pure Python stdlib** (no `pip install`). Run them from
`skills/auto-paper-collecter/scripts/`. Follow these steps in order:

1. **Read config & expand queries (you).** Read `skills/auto-paper-collecter/state/config.json`. For
   each keyword, write 2–3 associative English search queries (synonyms, full
   forms, adjacent sub-topics) to `skills/auto-paper-collecter/state/queries.json` as
   `{"<keyword>": ["q1","q2",...]}`.
2. **Fetch (script).** `cd skills/auto-paper-collecter/scripts && python3 fetch.py` → writes
   `skills/auto-paper-collecter/state/candidates.json` (deduped vs `seen.json`, recency-filtered). If
   it reports 0 candidates, tell the user "no new papers" and stop.
3. **Filter + summarize (you).** Read `candidates.json`. Drop anything that is
   not computer-science OR not on-topic for its `topic`. For each kept item
   write a concise summary and assemble `skills/auto-paper-collecter/state/curated.json` — objects of
   `{source,topic,title,url,venue,authors,published,tldr,method,contributions[]}`.
   Put papers first, GitHub repos last.
4. **Hot topics (you, optional).** Cluster kept items into a few coarse CS
   sub-fields; write `skills/auto-paper-collecter/state/trends.json`:
   `{"top":[{"name","delta","summary","papers":[...]}, ...]}`.
5. **Render (script).** `cd skills/auto-paper-collecter/scripts && python3 render.py` → writes
   `skills/auto-paper-collecter/digests/YYYY-MM-DD.md` + `.html` and records shown items into `seen.json`.
6. **Notify (script, optional).** `python3 notify.py` emails the digest if the
   `SMTP_*` / `EMAIL_TO` env vars are set.
7. **Report back (you).** How many kept, the top directions, and the digest path.

## Optional environment variables (never commit them)
`SEMANTIC_SCHOLAR_KEY` (lifts S2 limits) · `GITHUB_TOKEN` (lifts GitHub limits) ·
`SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASS` / `EMAIL_FROM` / `EMAIL_TO`.

## Conventions for contributors
- Scripts in `skills/auto-paper-collecter/scripts/` must stay **stdlib-only** and side-effect-free
  except for reading/writing `skills/auto-paper-collecter/state/` and `skills/auto-paper-collecter/digests/`.
- Never hard-code secrets; read them from environment variables.
- The web app (`app/`) uses an OpenAI-compatible gateway via `.env`; the skill
  does **not** — keep that separation.
