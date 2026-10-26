# Contributing

Thanks for helping Indian students find real opportunities. Every contribution is treated as a **lead**: it is checked
against the official page before anything is listed.

## Three ways to contribute

1. **Issue forms (easiest).** [Open an issue](../../issues/new/choose) and pick one:

   | Form | Use it for |
   |---|---|
   | **New opportunity** | A programme, fellowship, research internship, tech job, hackathon or event |
   | **Correction** | A wrong deadline, eligibility rule, name or link on an existing listing |
   | **Caution report** | A suspicious domain or a scheme that charges students |
   | **Removal request** | A listing that is closed, outdated, wrong or contains your personal data |

2. **Pull request.** Add **one row per opportunity** to [`submissions/submissions.csv`](submissions/submissions.csv):

   ```
   url,category,notes,submitted_on
   https://example.org/fellowship-2027,program,"Open to Indian undergraduates; closes 2027-01-15",2026-10-25
   ```

   - `category`: `program`, `swe_job`, `phd_postdoc`, `hackathon`, `event` or `caution`
   - `submitted_on`: the date, as `YYYY-MM-DD`
   - Please don't edit `README.md` or `listings/`: those files are regenerated from the catalog and hand edits are
     overwritten.

3. **The live app.** Use **Submit Opportunity** in [Roziqair](https://roziqair.vercel.app).

## What we accept

- An **official page**: a university, research institute, government body, fellowship organisation, or the
  employer's own careers page or job board (Greenhouse, Lever, Ashby, Workday, SmartRecruiters, Workable…).
- **Not accepted as the source:** aggregator articles, WhatsApp or Telegram forwards, screenshots, or listings that
  ask applicants to pay to apply or to work.

## Privacy

Never post e-mail addresses, phone numbers or links to a person's profile (for example `linkedin.com/in/…`).
Submissions containing personal data are removed without review.

## Caution reports

Write suspicious domains defanged, like `example[.]com`, and never paste a clickable link to them. Reports are reviewed
by hand and worded as caution, never as an accusation.

## What happens next

1. We check the link against the official page.
2. Accepted entries appear in the app and in these listings at the next refresh.
3. If we can't verify it, we reply on the issue or pull request.

## Code of conduct

Be kind. Submissions that harass, dox or defame anyone are removed and the author is blocked.
