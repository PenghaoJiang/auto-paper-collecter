#!/usr/bin/env python3
"""Optionally deliver today's digest to email + push channels. All credentials
come from environment variables (no secrets in the repo); each channel no-ops
if unconfigured. Python stdlib only.

  Email   : SMTP_HOST SMTP_PORT(=587) SMTP_USER SMTP_PASS EMAIL_FROM EMAIL_TO
  Telegram: TELEGRAM_BOT_TOKEN TELEGRAM_CHAT_ID
  Slack   : SLACK_WEBHOOK_URL
  WeChat  : WECHAT_WEBHOOK (企业微信群机器人, recommended)  or  SERVERCHAN_KEY (Server酱)

Usage:  cd skill/scripts && python3 notify.py
"""
import os
import json
import smtplib
import urllib.request
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import common as C


def _post_json(url, payload, timeout=20):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status


def _post_form(url, data, timeout=20):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode("utf-8"))
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status


def _digest_text():
    cur = C.load_json(os.path.join(C.STATE, "curated.json"), [])
    lines = [f"📚 文献雷达 · {C.today()}", ""]
    for p in cur[:15]:
        lines.append(f"• {p.get('title', '')}")
        if p.get("tldr"):
            lines.append(f"  {p['tldr']}")
        if p.get("url"):
            lines.append(f"  {p['url']}")
        lines.append("")
    return "\n".join(lines).strip()


def _email():
    host = os.environ.get("SMTP_HOST", "")
    user = os.environ.get("SMTP_USER", "")
    pw = os.environ.get("SMTP_PASS", "")
    to = os.environ.get("EMAIL_TO", "") or user
    if not (host and user and pw and to):
        return
    day = C.today()
    try:
        with open(os.path.join(C.DIGESTS, f"{day}.html"), encoding="utf-8") as f:
            body = f.read()
    except FileNotFoundError:
        print("[notify] no digest html — run render.py first.")
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📚 文献雷达 · {day}"
    msg["From"] = os.environ.get("EMAIL_FROM", "") or user
    msg["To"] = to
    msg.attach(MIMEText(body, "html", "utf-8"))
    try:
        with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=30) as s:
            s.starttls()
            s.login(user, pw)
            s.sendmail(msg["From"], [to], msg.as_string())
        print(f"[notify] emailed digest to {to}")
    except Exception as e:
        print(f"[notify] email failed: {e}")


def _push():
    text = _digest_text()
    if not text:
        return
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN", ""), os.environ.get("TELEGRAM_CHAT_ID", "")
    if tok and chat:
        try:
            _post_json(f"https://api.telegram.org/bot{tok}/sendMessage",
                       {"chat_id": chat, "text": text, "disable_web_page_preview": True})
            print("[notify] telegram sent")
        except Exception as e:
            print(f"[notify] telegram failed: {e}")
    slack = os.environ.get("SLACK_WEBHOOK_URL", "")
    if slack:
        try:
            _post_json(slack, {"text": text})
            print("[notify] slack sent")
        except Exception as e:
            print(f"[notify] slack failed: {e}")
    hook = os.environ.get("WECHAT_WEBHOOK", "")
    if hook:
        try:
            _post_json(hook, {"msgtype": "text", "text": {"content": text[:2000]}})
            print("[notify] wechat (企业微信) sent")
        except Exception as e:
            print(f"[notify] wechat failed: {e}")
    elif os.environ.get("SERVERCHAN_KEY", ""):
        try:
            _post_form(f"https://sctapi.ftqq.com/{os.environ['SERVERCHAN_KEY']}.send",
                       {"title": f"文献雷达 · {C.today()}", "desp": text})
            print("[notify] wechat (Server酱) sent")
        except Exception as e:
            print(f"[notify] wechat failed: {e}")


def main():
    _email()
    _push()


if __name__ == "__main__":
    main()
