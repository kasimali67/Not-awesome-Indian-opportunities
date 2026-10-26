#!/usr/bin/env node
// Read open roles from the public Greenhouse Job Board API (https://developers.greenhouse.io/job-board.html).
// Node.js 18+, no dependencies. One request at a time, with a pause and a timeout. MIT licence (see ../LICENSE).
//
//   node greenhouse.mjs <board-token> [more tokens...] [--match india]
//
// Prints one JSON object per job: {company, title, location, url, updated}.

const USER_AGENT = 'job-board-example/0.1 (+https://example.org/contact)'; // put your own contact link here
const PAUSE_MS = 1500;
const TIMEOUT_MS = 15000;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function parseArgs(argv) {
  const tokens = [];
  let match = null;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--match') match = (argv[++i] || '').toLowerCase();
    else tokens.push(argv[i]);
  }
  return { tokens, match };
}

async function fetchBoard(token) {
  if (!/^[a-z0-9_-]+$/i.test(token)) throw new Error(`not a board token: ${token}`);
  const url = `https://boards-api.greenhouse.io/v1/boards/${encodeURIComponent(token)}/jobs`;
  const response = await fetch(url, {
    headers: { 'User-Agent': USER_AGENT, Accept: 'application/json' },
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  if (response.status === 404) throw new Error(`no public board called ${token}`);
  if (!response.ok) throw new Error(`${token}: HTTP ${response.status}`);
  const body = await response.json();
  return (body.jobs || []).map((job) => ({
    company: token,
    title: job.title,
    location: job.location?.name ?? '',
    url: job.absolute_url,
    updated: job.updated_at ?? null,
  }));
}

async function main() {
  const { tokens, match } = parseArgs(process.argv.slice(2));
  if (tokens.length === 0) {
    console.error('usage: node greenhouse.mjs <board-token> [more tokens...] [--match india]');
    process.exit(2);
  }
  for (const [i, token] of tokens.entries()) {
    if (i > 0) await sleep(PAUSE_MS);
    try {
      for (const job of await fetchBoard(token)) {
        if (!match || job.location.toLowerCase().includes(match)) console.log(JSON.stringify(job));
      }
    } catch (error) {
      console.error(`skipped ${token}: ${error.message}`);
    }
  }
}

main();
