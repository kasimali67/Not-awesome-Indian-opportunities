#!/usr/bin/env python3
"""Read open roles from the public Greenhouse Job Board API (https://developers.greenhouse.io/job-board.html).

Python 3.9+, standard library only. One request at a time, with a pause and a timeout. MIT licence (see ../LICENSE).

    python greenhouse.py <board-token> [more tokens...] [--match india]

Prints one JSON object per job: {company, title, location, url, updated}.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "job-board-example/0.1 (+https://example.org/contact)"  # put your own contact link here
PAUSE_SECONDS = 1.5
TIMEOUT_SECONDS = 15


def fetch_board(token):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", token):
        raise ValueError(f"not a board token: {token}")
    url = f"https://boards-api.greenhouse.io/v1/boards/{urllib.parse.quote(token)}/jobs"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise ValueError(f"no public board called {token}") from error
        raise ValueError(f"{token}: HTTP {error.code}") from error
    return [{"company": token,
             "title": job.get("title"),
             "location": (job.get("location") or {}).get("name") or "",
             "url": job.get("absolute_url"),
             "updated": job.get("updated_at")}
            for job in body.get("jobs", [])]


def main():
    parser = argparse.ArgumentParser(description="list open roles from Greenhouse job boards")
    parser.add_argument("tokens", nargs="+", help="board tokens, as in boards.greenhouse.io/<token>")
    parser.add_argument("--match", help="keep only jobs whose location contains this word")
    args = parser.parse_args()
    match = (args.match or "").lower()
    for i, token in enumerate(args.tokens):
        if i:
            time.sleep(PAUSE_SECONDS)
        try:
            for job in fetch_board(token):
                if not match or match in job["location"].lower():
                    print(json.dumps(job, ensure_ascii=False))
        except (ValueError, OSError) as error:
            print(f"skipped {token}: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
