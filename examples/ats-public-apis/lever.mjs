#!/usr/bin/env node
// Read open roles from the public Lever Postings API (https://github.com/lever/postings-api).
// Node.js 18+, no dependencies. One request at a time, with a pause and a timeout. MIT licence (see ../LICENSE).
//
//   node lever.mjs <company-site> [more sites...] [--match india] [--eu]
//
// --eu reads from api.eu.lever.co, for companies whose board is hosted on Lever's EU instance.
// Prints one JSON object per job: {company, title, location, url, updated}.

const USER_AGENT = 'job-board-example/0.1 (+https://example.org/contact)'; // put your own contact link here
const PAUSE_MS = 1500;
const TIMEOUT_MS = 15000;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function parseArgs(argv) {
  const sites = [];
  let match = null;
  let eu = false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--match') match = (argv[++i] || '').toLowerCase();
    else if (argv[i] === '--eu') eu = true;
    else sites.push(argv[i]);
  }
  return { sites, match, eu };
}

async function fetchSite(site, eu) {
  if (!/^[a-z0-9_-]+$/i.test(site)) throw new Error(`not a Lever site name: ${site}`);
  const host = eu ? 'https://api.eu.lever.co' : 'https://api.lever.co';
  const url = `${host}/v0/postings/${encodeURIComponent(site)}?mode=json`;
  const response = await fetch(url, {
    headers: { 'User-Agent': USER_AGENT, Accept: 'application/json' },
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  if (response.status === 404) throw new Error(`no public Lever board called ${site}${eu ? '' : ' (try --eu)'}`);
  if (!response.ok) throw new Error(`${site}: HTTP ${response.status}`);
  const postings = await response.json();
  return postings.map((posting) => ({
    company: site,
    title: posting.text,
    location: posting.categories?.location ?? '',
    url: posting.hostedUrl,
    updated: posting.createdAt ? new Date(posting.createdAt).toISOString() : null,
  }));
}

async function main() {
  const { sites, match, eu } = parseArgs(process.argv.slice(2));
  if (sites.length === 0) {
    console.error('usage: node lever.mjs <company-site> [more sites...] [--match india] [--eu]');
    process.exit(2);
  }
  for (const [i, site] of sites.entries()) {
    if (i > 0) await sleep(PAUSE_MS);
    try {
      for (const job of await fetchSite(site, eu)) {
        if (!match || job.location.toLowerCase().includes(match)) console.log(JSON.stringify(job));
      }
    } catch (error) {
      console.error(`skipped ${site}: ${error.message}`);
    }
  }
}

main();
