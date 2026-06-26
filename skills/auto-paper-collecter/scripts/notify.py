#!/usr/bin/env python3
"""Optionally email today's HTML digest. Reads SMTP settings from environment
variables (so no secrets live in the repo):

  SMTP_HOST  SMTP_PORT(=587)  SMTP_USER  SMTP_PASS  EMAIL_FROM  EMAIL_TO

No-op (prints a hint) if SMTP isn't configured.

Usage:  cd skill/scripts && python3 notify.py
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import common as C


def main():
    host = os.environ.get("SMTP_HOST", "")
    user = os.environ.get("SMTP_USER", "")
    pw = os.environ.get("SMTP_PASS", "")
    to = os.environ.get("EMAIL_TO", "") or user
    if not (host and user and pw and to):
        print("[notify] SMTP env not set (SMTP_HOST/SMTP_USER/SMTP_PASS/EMAIL_TO) — skipping email.")
        return

    day = C.today()
    html_path = os.path.join(C.DIGESTS, f"{day}.html")
    try:
        with open(html_path, encoding="utf-8") as f:
            body = f.read()
    except FileNotFoundError:
        print(f"[notify] no digest at {html_path} — run render.py first.")
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


if __name__ == "__main__":
    main()
