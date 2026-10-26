# Contributing

Thanks for helping Indian students find real opportunities. You don't need to be a programmer: most contributions are
a link and two sentences. Every contribution is treated as a **lead**: it is checked against the official page before
anything is listed.

**Contents:** [What we list](#what-we-list) · [Add an opportunity](#add-an-opportunity) ·
[Fix or remove a listing](#fix-or-remove-a-listing) · [How listings are checked](#how-listings-are-checked) ·
[Privacy and caution reports](#privacy-and-caution-reports) · [Try the command-line tool](#try-the-command-line-tool) ·
[What happens next](#what-happens-next)

## What we list

| Category | Listing page | What qualifies | `category` in the CSV |
|---|---|---|---|
| **Fellowships** | [`listings/programmes/fellowships.md`](listings/programmes/fellowships.md) | Research, PhD and early-career fellowships run by a university, institute, foundation or government body | `program` |
| **Funded Master's & study scholarships** | [`listings/programmes/funded-masters.md`](listings/programmes/funded-masters.md) | Scholarships or funded places for degree study that Indian students can apply to | `program` |
| **Research internships** | [`listings/programmes/research-internships.md`](listings/programmes/research-internships.md) | Summer, visiting or remote research internships with a named host institution | `program` |
| **Graduate programmes** | [`listings/programmes/graduate-programmes.md`](listings/programmes/graduate-programmes.md) | Structured graduate or early-career programmes run by an employer | `program` |
| **Tech jobs & internships** | [`listings/jobs/tech-jobs-india.md`](listings/jobs/tech-jobs-india.md) | Roles open to candidates in India, posted on the employer's own careers page or job board | `swe_job` |
| **PhD, postdoc & faculty** | [`listings/academic/phd-postdoc-faculty.md`](listings/academic/phd-postdoc-faculty.md) | Academic positions with a public posting by the hiring institution | `phd_postdoc` |
| **Hackathons & events** | [`listings/hackathons-and-events.md`](listings/hackathons-and-events.md) | Hackathons, summer schools and summits open to Indian students | `hackathon` or `event` |

**Every listing needs an official source:** the organiser's own page, or the employer's own careers page or job board
(Greenhouse, Lever, Ashby, Workday, SmartRecruiters, Workable…).

**We don't list:**
- aggregator articles, reposts, WhatsApp or Telegram forwards, or screenshots as the source;
- anything that charges applicants to apply, to be selected, or for a certificate;
- agencies or consultancies selling admission or placement packages.

## Add an opportunity

Pick whichever is easiest for you. All three end up in the same review.

### 1. Issue form (easiest, no Git needed)

1. Open [**New issue**](../../issues/new/choose) and choose **New opportunity**.
2. Paste the **official link**, pick the category, and add a short note (who can apply, the deadline if you know it).
3. Submit. That's it.

### 2. Pull request (one row)

1. Open [`submissions/submissions.csv`](submissions/submissions.csv) and click the pencil icon to edit it (GitHub forks
   the repository for you).
2. Add **one row per opportunity** at the end:

   ```
   url,category,notes,submitted_on
   https://example.org/fellowship-2027,program,"Open to Indian undergraduates; closes 2027-01-15",2026-10-25
   ```

   - `category`: `program`, `swe_job`, `phd_postdoc`, `hackathon`, `event` or `caution`;
   - `notes`: in quotes if it contains a comma;
   - `submitted_on`: today's date, as `YYYY-MM-DD`.
3. Choose **Propose changes**, then **Create pull request**.

Please change only `submissions/submissions.csv`. `README.md` and everything in `listings/` are regenerated from the
catalog, so hand edits there are overwritten.

### 3. The live app

Use **Submit Opportunity** in [Roziqair](https://roziqair.vercel.app). No GitHub account needed.

## Fix or remove a listing

- **Something is wrong** (deadline, eligibility, name or link): open a [**Correction**](../../issues/new/choose) issue
  with the listing's name and a link to the official page that shows the right information.
- **It should come down** (closed for good, a duplicate, or it contains your personal data): open a
  [**Removal request**](../../issues/new/choose). Requests about personal data are handled first.

## How listings are checked

Each listing page says which kind of check its rows have had:

| Tier | Used for | What it means |
|---|---|---|
| **Verified official** | Programmes, hackathons, events | Every value is quoted from the organiser's official page, with the date it was checked. |
| **Employer board** | Tech jobs | Read from the employer's own job board; "Seen" is the last date the posting was there. |
| **Community-sourced** | PhD, postdoc & faculty | Shared by the academic community and **not verified** by Roziqair. Check the posting itself. |

**Reading the tables:**
- **Official ↗ / Apply ↗ / Posting ↗** go to the source. Always confirm details there before applying.
- **Details** opens the listing in the Roziqair app, with eligibility notes and calendar export.
- **Next deadline** is the date published by the organiser. Check the time zone on the official page.
- **Status** is the organiser's state when last checked: for example Open, Announced (the next cycle is announced but
  not open) or Closed (awaiting the next cycle).
- **—** means not stated by the source.

## Privacy and caution reports

- **Never post personal contact details:** e-mail addresses, phone numbers, or links to a person's profile (for
  example `linkedin.com/in/…`), whether yours or someone else's. Submissions containing them are removed without
  review.
- **Report schemes, not people.** A caution report is about a domain, an organisation or a scheme, never a private
  individual.
- **Defang suspicious links.** Write domains like `example[.]com` and never paste a clickable link to a suspicious
  site.
- Caution reports are reviewed by hand and published only as cautious, generic warnings. The common patterns are in
  [`safety/scam-patterns.md`](safety/scam-patterns.md).

## Try the command-line tool

[`app.py`](app.py) reads this repository's listings in your terminal and shows how public job-board APIs work. It
uses only the Python standard library, so there is nothing to install apart from **Python 3.10 or newer**.

```sh
git clone https://github.com/kasimali67/Not-awesome-Indian-opportunities.git
cd Not-awesome-Indian-opportunities
python app.py --help
python app.py stats                     # how many listings in each category, and the nearest deadlines
python app.py closing --days 14         # everything closing in the next 14 days
python app.py greenhouse <board-token> --india   # live roles from a company's public Greenhouse board
```

On some systems the command is `python3` instead of `python`. For more on reading job boards responsibly, see
[`examples/`](examples/).

## What happens next

1. We check the link against the official page.
2. Accepted entries appear in the app and in these listings at the next refresh.
3. If we can't verify it, we reply on the issue or pull request.

## Code of conduct

Be kind. See the [code of conduct](CODE_OF_CONDUCT.md): submissions that harass, dox or defame anyone are removed and
the author is blocked.
