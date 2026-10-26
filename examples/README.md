# Examples: reading public job-board APIs

Many companies publish their open roles through an applicant tracking system (ATS) that offers a **public, documented
API** for exactly this purpose: showing jobs on the company's own website and on job sites. These scripts show how to
read two of them. They are short teaching examples with no dependencies; they are **not** the Roziqair pipeline.

| Script | API | Runtime |
|---|---|---|
| [`ats-public-apis/greenhouse.mjs`](ats-public-apis/greenhouse.mjs) | [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html) | Node.js 18+ |
| [`ats-public-apis/greenhouse.py`](ats-public-apis/greenhouse.py) | Greenhouse Job Board API | Python 3.9+ |
| [`ats-public-apis/lever.mjs`](ats-public-apis/lever.mjs) | [Lever Postings API](https://github.com/lever/postings-api) | Node.js 18+ |

```sh
node examples/ats-public-apis/greenhouse.mjs <board-token> [more tokens…] [--match india]
python examples/ats-public-apis/greenhouse.py <board-token> [more tokens…] [--match india]
node examples/ats-public-apis/lever.mjs <company-site> [more sites…] [--match india] [--eu]
```

The board token or site name is the last part of a company's job-board address, for example
`https://boards.greenhouse.io/<board-token>` or `https://jobs.lever.co/<company-site>`. Each script prints one JSON
object per job (company, title, location, link, date) and, with `--match`, keeps only jobs whose location contains
that word.

## Fetch responsibly

These rules matter more than the code:

1. **Use documented public endpoints only.** Both APIs are published by the ATS for public job listings. Don't scrape
   pages behind a login, don't reuse cookies or sessions, and never try to get around a CAPTCHA, a rate limit or a
   block.
2. **Go slowly.** The scripts make one request at a time with a pause between requests and a timeout. Keep it that
   way, and fetch at most a few times a day; job boards don't change by the minute.
3. **Say who you are.** Set a real `User-Agent` with a way to contact you (edit `USER_AGENT` in the script).
4. **Respect the source.** Check the provider's terms and the company's wishes. If a company asks you to stop, stop.
5. **Link, don't copy.** Job descriptions belong to the employer. Show the title, company, location and a link to
   the official posting; don't republish full descriptions.
6. **Leave people out.** Don't collect or publish recruiters' or hiring managers' names, e-mail addresses or
   profiles, even when an API returns them.
7. **Cache and expire.** Store what you fetched with the date, and drop roles that disappear from the board.

## Licence

The code in this folder is released under the [MIT licence](LICENSE). The rest of the repository is CC BY-NC 4.0
(see [`../LICENSE`](../LICENSE)).
