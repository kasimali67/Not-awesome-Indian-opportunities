#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (the licence text is in examples/LICENSE)
"""A small command-line companion to this repository, written for people learning Python.

It uses only the Python standard library, so there is nothing to install: just Python 3.10 or newer.

    python app.py stats                        how many listings in each category, and the nearest deadlines
    python app.py closing --days 14            everything with a deadline in the next 14 days
    python app.py greenhouse <board-token>     live roles from a company's public Greenhouse job board
    python app.py lever <site>                 live roles from a company's public Lever job board
    python app.py --help                       all the options

What you can learn from reading it:
  * how a markdown table is just text that a program can split into rows and cells (stats, closing);
  * how a public JSON API is called politely: one request, a clear User-Agent, a timeout (greenhouse, lever).

The first two commands read only the files in listings/, so they work offline. The listings are refreshed
regularly; for the newest data, run `git pull` first or use the live app at https://roziqair.vercel.app.
"""
import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LISTINGS = ROOT / "listings"
# These two pages repeat rows from the others, so they are skipped when counting.
SUMMARY_PAGES = {"README.md", "closing-soon.md"}

# Be polite to the API: say who you are (put your own contact link here) and never wait forever.
USER_AGENT = "not-awesome-indian-opportunities-app/1.0 (+https://github.com/kasimali67/Not-awesome-Indian-opportunities)"
TIMEOUT_SECONDS = 15

# Words that mark a job as open to someone in India. "remote" is included, but always check the region a remote
# role allows: many are remote within one country only.
INDIA_WORDS = ("india", "remote", "bengaluru", "bangalore", "hyderabad", "pune", "mumbai", "delhi", "gurugram",
               "gurgaon", "noida", "chennai", "kolkata", "ahmedabad")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")
LINK_RE = re.compile(r"\]\(<?(https?://[^)>\s]+)>?\)")


# --- Reading the markdown listings --------------------------------------------------------------------------------

def split_row(line):
    """Split one markdown table row into its cells.

    A row looks like `| Title | Org | 2026-11-01 |`. A `|` inside a cell is written `\\|`, so we walk the line
    character by character and treat anything after a backslash as plain text.
    """
    cells, current, chars = [], "", iter(line.strip().strip("|"))
    for char in chars:
        if char == "\\":
            current += next(chars, "")          # keep the escaped character, drop the backslash
        elif char == "|":
            cells.append(current.strip())
            current = ""
        else:
            current += char
    cells.append(current.strip())
    return [cell.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&") for cell in cells]


def read_listing(path):
    """Return (page title, list of rows) for one listing file. Each row is a dict: {column name: cell text}."""
    title, rows, header = path.stem, [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        elif not line.startswith("|"):
            header = None                       # any other line ends the current table
        elif header is None:
            header = split_row(line)            # the first row of a table names the columns
        elif not set(line) <= set("|-: "):      # skip the |---|---| line under the header
            rows.append(dict(zip(header, split_row(line))))
    return title, rows


def listing_files():
    if not LISTINGS.is_dir():
        sys.exit("No listings/ folder next to app.py. Run this from a copy of the repository.")
    return [path for path in sorted(LISTINGS.rglob("*.md")) if path.name not in SUMMARY_PAGES]


def deadline_of(row):
    """The row's deadline as a date, or None. The column is called "Next deadline" or "Deadline"."""
    for column, value in row.items():
        if "deadline" in column.lower() and DATE_RE.match(value):
            return dt.date.fromisoformat(value[:10])
    return None


def describe(row):
    """A short one-line description of a row: its title, its organisation and its first link."""
    columns = list(row)
    title = row[columns[0]] if columns else "?"
    org = next((row[c] for c in ("Organisation", "Organiser", "Company") if c in row), "")
    link = next((m.group(1) for value in row.values() for m in [LINK_RE.search(value)] if m), "")
    return f"{title}" + (f" - {org}" if org and org != "—" else "") + (f"\n             {link}" if link else "")


def upcoming(today, days=None):
    """Every (deadline, page title, row) from today onwards, earliest first; only the next `days` if given."""
    found = []
    for path in listing_files():
        title, rows = read_listing(path)
        for row in rows:
            due = deadline_of(row)
            if due and due >= today and (days is None or due <= today + dt.timedelta(days=days)):
                found.append((due, title, row))
    return sorted(found, key=lambda item: (item[0], item[1]))


def stats(today, top=5):
    """Lines of text: one count per listing page, then the nearest deadlines."""
    lines, total = ["Listings in this copy of the repository:", ""], 0
    for path in listing_files():
        title, rows = read_listing(path)
        total += len(rows)
        lines.append(f"  {len(rows):>5}  {title}")
    lines += [f"  {total:>5}  in total", "", f"The next {top} deadlines (from {today}):", ""]
    soon = upcoming(today)[:top]
    lines += [f"  {due}  {describe(row)}" for due, _, row in soon] or ["  none found"]
    return lines


def closing(today, days):
    soon = upcoming(today, days)
    lines = [f"{len(soon)} deadline(s) from {today} to {today + dt.timedelta(days=days)}:", ""]
    lines += [f"  {due}  [{title}] {describe(row)}" for due, title, row in soon]
    return lines


# --- Calling public job-board APIs -------------------------------------------------------------------------------

def get_json(url):
    """Download a URL and parse it as JSON, with our User-Agent and a timeout."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            sys.exit("Not found: check the board name (it is the last part of the job board's address).")
        sys.exit(f"The API answered with HTTP {error.code}. Try again later.")
    except (urllib.error.URLError, TimeoutError) as error:
        sys.exit(f"Could not reach the API: {error}")


def looks_indian(location):
    text = (location or "").lower()
    return any(word in text for word in INDIA_WORDS)


def check_name(name):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        sys.exit(f"{name!r} doesn't look like a board name: use letters, digits, '-' or '_' only.")
    return urllib.parse.quote(name)


def greenhouse(token):
    """Greenhouse Job Board API: https://developers.greenhouse.io/job-board.html"""
    body = get_json(f"https://boards-api.greenhouse.io/v1/boards/{check_name(token)}/jobs")
    return [{"title": job.get("title", ""), "location": (job.get("location") or {}).get("name", ""),
             "url": job.get("absolute_url", "")} for job in body.get("jobs", [])]


def lever(site, eu=False):
    """Lever Postings API: https://github.com/lever/postings-api"""
    host = "https://api.eu.lever.co" if eu else "https://api.lever.co"
    postings = get_json(f"{host}/v0/postings/{check_name(site)}?mode=json")
    jobs = []
    for posting in postings:
        categories = posting.get("categories") or {}
        places = [categories.get("location") or ""] + list(categories.get("allLocations") or [])
        if posting.get("workplaceType") == "remote":
            places.append("Remote")
        jobs.append({"title": posting.get("text", ""), "location": " / ".join(dict.fromkeys(p for p in places if p)),
                     "url": posting.get("hostedUrl", "")})
    return jobs


def print_jobs(name, jobs, india_only):
    shown = [job for job in jobs if not india_only or looks_indian(job["location"])]
    print(f"{name}: {len(jobs)} open role(s)" + (f", {len(shown)} in India or remote" if india_only else ""))
    for job in shown:
        print(f"\n  {job['title']}\n  {job['location'] or 'location not stated'}\n  {job['url']}")
    if india_only and shown:
        print("\nRemote roles may be limited to one country: check each posting.")


# --- The command line --------------------------------------------------------------------------------------------

def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")    # some Windows terminals can't print every character
    parser = argparse.ArgumentParser(description="Browse this repository's listings and public job boards.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("stats", help="count the listings and show the nearest deadlines")
    closing_parser = commands.add_parser("closing", help="list deadlines in the next N days")
    closing_parser.add_argument("--days", type=int, default=14, help="how many days ahead (default 14)")
    gh_parser = commands.add_parser("greenhouse", help="live roles from a public Greenhouse job board")
    gh_parser.add_argument("board_token", help="as in boards.greenhouse.io/<board_token>")
    gh_parser.add_argument("--india", action="store_true", help="only roles in India or remote")
    lever_parser = commands.add_parser("lever", help="live roles from a public Lever job board")
    lever_parser.add_argument("site", help="as in jobs.lever.co/<site>")
    lever_parser.add_argument("--india", action="store_true", help="only roles in India or remote")
    lever_parser.add_argument("--eu", action="store_true", help="the company uses Lever's EU site (jobs.eu.lever.co)")
    args = parser.parse_args(argv)

    today = dt.date.today()
    if args.command == "stats":
        print("\n".join(stats(today)))
    elif args.command == "closing":
        if args.days < 0:
            parser.error("--days must be 0 or more")
        print("\n".join(closing(today, args.days)))
    elif args.command == "greenhouse":
        print_jobs(args.board_token, greenhouse(args.board_token), args.india)
    elif args.command == "lever":
        print_jobs(args.site, lever(args.site, args.eu), args.india)
    return 0


if __name__ == "__main__":
    sys.exit(main())
