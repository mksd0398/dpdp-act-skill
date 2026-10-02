# Launch kit: getting dpdp-act-skill found

This folder is the promotion plan for the skill and the site. It is not part of the skill or
the site, and nothing in it is published by the build.

| File | What it is |
|---|---|
| [`README.md`](README.md) | This plan: what is already done, what you need to do, in order |
| [`directories.md`](directories.md) | Every skill directory, marketplace and awesome list worth submitting to, with entry text and each list's rules |
| [`posts.md`](posts.md) | Draft posts for Hacker News, Reddit, LinkedIn, X, Product Hunt, a blog article and press pitches |
| [`github-social-preview.png`](github-social-preview.png) | 1280×640 image for the repository's social preview |

**Where things stand:** the repository has **0 stars** (checked 2 October 2026). Several awesome
lists refuse projects under 10 or 100 stars, so order matters. Use the channels that have no star
gate first, collect stars, then submit to the gated lists.

---

## Already done in this repository

**Search engines (SEO)**
- Every page has a unique title and description, a canonical URL, Open Graph and Twitter cards,
  and a 1200×630 social image (`tools/static/assets/og.jpg`).
- Every page has schema.org JSON-LD as a single `@graph`: `WebSite`, `Person`, `WebPage`,
  `BreadcrumbList`. Pages add `Legislation` for the Act and Rules, `FAQPage`, `DefinedTermSet`,
  `SoftwareApplication` and `HowTo` for the skill, and `Article` where they fit.
- New high-intent pages: [compliance checklist](https://mksd0398.github.io/dpdp-act-skill/compliance-checklist/),
  [DPDP Act explained](https://mksd0398.github.io/dpdp-act-skill/dpdp-act-explained/),
  [glossary](https://mksd0398.github.io/dpdp-act-skill/glossary/),
  [AI skill](https://mksd0398.github.io/dpdp-act-skill/claude-code-skill/) and
  [about](https://mksd0398.github.io/dpdp-act-skill/about/).
- Every `s.8(6)` and `Rule 7(2)` in the commentary links to that section or rule page. That is
  several hundred internal links, with references to other Acts (IT Act, RTI Act, IBC) left
  alone.
- Each sitemap `lastmod` is the source file's real commit date, not the build date, so Google
  keeps trusting it.
- A 404 page.

**Answer boxes and voice assistants (AEO)**
- The FAQ grew from 12 to 32 questions in 8 groups. Each answer leads with the direct answer and
  links its source section. Every question has its own deep link (`/faq/#question-slug`).
- Every section page opens with a one-line summary before the verbatim text.
- The home page has a "DPDP Act at a glance" fact box with the exact answers people search for:
  the deadline, the regulator, the maximum penalty, the child age, the breach clock.

**AI answer engines (GEO)**
- [`llms.txt`](https://mksd0398.github.io/dpdp-act-skill/llms.txt) indexes every page for AI
  agents and carries notes on the facts models most often get wrong.
- [`llms-full.txt`](https://mksd0398.github.io/dpdp-act-skill/llms-full.txt) holds the whole corpus
  in one file.
- Every content page has a Markdown twin at `index.md`, linked with `rel="alternate"`.
- `robots.txt` explicitly welcomes GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot,
  Google-Extended and other AI crawlers.
- IndexNow: CI pings Bing on every change, and Bing feeds ChatGPT search and Copilot. The key file
  is in `tools/static/`.
- Every claim carries a citation. Citation-dense, quotable pages are what generative engines pick
  up.

**Interactive readiness self-check**
- On the home page and at [`/dpdp-compliance-checker/`](https://mksd0398.github.io/dpdp-act-skill/dpdp-compliance-checker/),
  which targets searches like "DPDP compliance checker".
- Up to 22 questions. It returns a readiness score, a score per area, and gaps ranked by the
  penalty ceiling behind each one, each with its section or rule.
- "Copy results as a prompt for Claude" hands the gaps straight to the skill, which turns
  every visitor who finishes the check into a skill user.
- It runs entirely in the browser: no cookies, no analytics, nothing sent. That's worth
  saying in posts, given the audience.

**Promoting the skill everywhere on the site**
- "AI skill" is highlighted in the navigation on every page.
- Every section and rule page ends with a "Use this with AI" box holding a prompt written for that
  provision.
- The site footer promotes the skill on all 69 pages.
- A one-click [`dpdp-analyze.zip`](https://mksd0398.github.io/dpdp-act-skill/downloads/dpdp-analyze.zip)
  for uploading to Claude.ai.
- Install instructions for Claude.ai, GitHub Copilot, Gemini CLI, Codex, Cursor and the
  `npx skills` installer.

**Repository**
- The README has a search-friendly opening line, install steps for other tools, links to the site
  and a "help others find it" section.
- A `CITATION.cff` file, which turns on GitHub's "Cite this repository" button.
- More plugin keywords in `.claude-plugin/`.

---

## Your to-do list, in order

These steps need your accounts, so I could not do them from here.

### Day 0: settings (about 20 minutes)

1. **GitHub repository settings.** Open <https://github.com/mksd0398/dpdp-act-skill> and click the
   gear next to **About**.
   - **Description** (paste it as is):
     `Free DPDP Act skill for Claude Code + verbatim text of India's Digital Personal Data Protection Act 2023 and DPDP Rules 2025. 78-point compliance checklist, FAQ, glossary. Cites the section for every claim. Not legal advice.`
   - **Website:** `https://mksd0398.github.io/dpdp-act-skill/`
   - **Topics** (20, the maximum):
     `dpdp` `dpdp-act` `dpdp-act-2023` `dpdp-rules` `india` `data-protection` `data-privacy`
     `privacy-law` `gdpr` `compliance` `regtech` `legaltech` `claude` `claude-code`
     `claude-code-plugin` `claude-skills` `agent-skills` `anthropic` `llms-txt` `privacy`
2. **Social preview.** Settings › General › Social preview › upload
   [`github-social-preview.png`](github-social-preview.png).
3. **Merge this branch to `main`.** The site only rebuilds from `main`. Check that GitHub Pages is
   serving from `main` › `/docs`.
4. **Cut a release.** Go to Releases › Draft a new release, tag `v1.1.0`, and attach
   `docs/downloads/dpdp-analyze.zip`. Releases show up in GitHub search, in watchers' feeds and in
   some directories' crawlers.
5. **Google Search Console.** Add a URL-prefix property for
   `https://mksd0398.github.io/dpdp-act-skill/`. Choose the **HTML file** method, put the file
   Google gives you into `tools/static/`, push, then verify. Submit `sitemap.xml`. Use URL
   Inspection › Request indexing on the home page, `/faq/`, `/compliance-checklist/` and
   `/claude-code-skill/`.
6. **Bing Webmaster Tools.** Use "Import from Google Search Console", which takes one click.
   Bing's index powers ChatGPT search, Copilot and DuckDuckGo.

### Week 1: launch on channels that need no stars

Copy for all of these is in [`posts.md`](posts.md). The submission details are in
[`directories.md`](directories.md).

1. **Anthropic's plugin directory**, the single highest-value listing. It reaches claude.ai, the
   desktop and mobile apps, Cowork and Claude Code. It needs a paid Claude plan.
2. **LinkedIn post.** The Indian privacy, legal and product audience lives there.
3. **Show HN**, on a weekday morning US time.
4. **r/ClaudeAI** (with the "Built with Claude" flair) and **r/ClaudeCode**.
5. **lawve.ai**. Its form also feeds `lawve-ai/awesome-legal-skills`, which has India and Data
   Protection sections.
6. **hesreallyhim/awesome-claude-code.** This uses an issue form, not a PR, and you must submit it
   yourself.
7. **ComposioHQ/awesome-claude-skills, BehiSecc/awesome-claude-skills, getprobo/awesome-compliance.**
   All three take PRs.
8. **Product Hunt**, once you have a few stars and some feedback to quote.

### Later: gated lists

- Once you have **10 or more stars**: `travisvn/awesome-claude-skills` (PR; AI-written PRs are
  rejected).
- Once you have **real usage** to point to: `VoltAgent/awesome-agent-skills`.
- Once you have **100 or more stars**: `jeswinsimon/awesome-made-by-indians`.
- **Press:** pitch MediaNama, Inc42 and YourStory using the drafts in `posts.md`. LiveLaw only
  accepts columns you wrote yourself.

### Strongly recommended: a custom domain

`mksd0398.github.io/dpdp-act-skill` is a project path on a shared host. That costs you three
things:

- crawlers only read `robots.txt` and `llms.txt` at a host's root, so the ones in `docs/` are
  ignored for now;
- Google shows a host-level favicon, so you get GitHub's;
- a short branded domain (something like `dpdp<something>.in`) is easier to cite, remember and
  link.

Switching is quick once you have the domain:

1. Buy the domain and point it at GitHub Pages (Settings › Pages › Custom domain).
2. Add a `CNAME` file containing the domain to `tools/static/`.
3. In `tools/build_site.py`, change the default `SITE` (or set `SITE_URL` in the workflow).
4. Rebuild and push. Every canonical URL, sitemap entry and `llms.txt` link moves over, and GitHub
   Pages redirects the old URLs.

---

## Measuring it

- **Search Console:** impressions and clicks per query. Watch for `dpdp act`, `dpdp rules 2025`,
  `dpdp compliance checklist`, `dpdp penalty` and `data fiduciary meaning`.
- **GitHub › Insights › Traffic:** referrers and views. Stars are the gate for half the
  directories.
- **AI answer engines:** once a month, ask ChatGPT (with search), Perplexity, Gemini, Copilot and
  Claude the questions below, and note whether the site or the repository is cited. If you use
  Ahrefs, Brand Radar can track this for you.
  - What is the DPDP Act compliance deadline?
  - Do I need a DPO under India's DPDP Act?
  - DPDP Act breach notification timeline
  - Is there a DPDP Act compliance checklist?
  - DPDP Act vs GDPR differences
  - What is a Data Fiduciary under the DPDP Act?
  - Is there a Claude skill for the DPDP Act?
  - What AI tool can review a privacy policy for DPDP compliance?

---

## Ground rules

- Every post and listing must say **not legal advice**. The skill and the site already do.
- **Never ask for upvotes** on HN, Reddit or Product Hunt; it gets posts killed. Ask for
  feedback, especially from Indian privacy lawyers, since corrections are the most valuable thing
  this project can get.
- The drafts in `posts.md` were written with AI help. Rewrite them in your own voice. Some venues
  (LiveLaw, `travisvn/awesome-claude-skills`) reject AI-written submissions outright, and
  `hesreallyhim/awesome-claude-code` must be submitted by a person, not an agent.
- **One date to check before you promote hard.** Some trackers give the later commencement dates as
  **13** November 2026 and **13** May 2027, while this repository says **14**. Check against the
  Gazette notification (G.S.R. 846(E), 13 November 2025) and correct `rules-2025.md` if needed,
  before a lawyer points it out publicly.
