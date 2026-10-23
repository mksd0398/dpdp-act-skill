# Daily answer routine

Run once a day, by Claude Code or any other agent that can search the web, read files, run Python
and use `git`/`gh`. Output: one new page under `answers/`, opened as a pull request. Merging the PR
publishes it (the `Build site` workflow rebuilds `docs/`).

Work from the repository root. The skill's hard rules in `skills/dpdp-analyze/SKILL.md` apply to
every sentence you write. Read that file first, then `references/doctrine.md`.

## 1. Find real questions (picking the question is the whole game)

Collect 10 questions real people asked in the last 90 days, each with its source URL:

- Reddit: r/developersIndia, r/StartUpIndia, r/LegalAdviceIndia, r/india, r/IndiaTech, r/privacy,
  r/SaaS, r/shopify (search "DPDP", "data protection India", "privacy policy India", "consent India")
- Google "People also ask" and autocomplete for "DPDP Act ...", "DPDP ... startup", "DPDP ... app"
- Quora, Stack Exchange, LinkedIn posts, GitHub issues that mention DPDP

Keep the asker's own wording. A question is a good pick when **all** of these hold:

1. Someone with a real product or job would search it (a founder, developer, marketer, HR, CA).
2. It is specific: a tool, data type, business model or situation, not "what is DPDP".
3. The honest answer needs the statute, and a general chatbot would likely get it wrong by
   importing GDPR (legitimate interests, sensitive data, cookie law, DPO for everyone, 13 or 16 as
   the child age).
4. It is **not already covered**: check every file in `answers/` and the `FAQ_GROUPS` list in
   `tools/build_site.py` for the same intent, not just the same words.

Pick one. Note in the PR body why it beat the other nine.

## 2. Write `answers/<slug>.md`

Slug: the question, lower case, hyphens, at most 70 characters. Format:

```
---
question: Does the DPDP Act require a cookie consent banner?
date: YYYY-MM-DD
asked: https://www.reddit.com/r/... (the URL the question came from; omit the line if none)
---
First paragraph: the direct answer in two or three sentences. Search engines and AI answer engines
use it as the snippet, so it must stand alone and carry its main section citation.

## Short headed sections that work through the asker's situation
...

> Not legal advice. Verify statutory text against the Gazette of India and consult qualified
> Indian legal counsel before acting.
```

Rules for the body:

- 400 to 900 words. Answer the asker's situation, with one concrete worked example.
- Every DPDP proposition carries `s.N(x)` or `Rule N(x)`. If you cannot anchor it, cut it.
  Write citations exactly in that form; the builder turns them into links.
- Quote only from `references/act-full-text.md`, verbatim. Never quote the Act from memory.
- Anything resting on a Rule says once: verify against the notified Gazette text.
- Commencement: substantive Rules (3, 5 to 16, 22, 23) apply from **14 May 2027**. Never call them
  binding today.
- Penalties are ceilings ("may extend to"), never predicted fines.
- No invented cases, Board decisions, statistics or quotes. There is no Board jurisprudence yet; say
  "untested" where an answer is a reading, not a holding.
- Do not copy text from the source thread beyond the question itself. Do not name the asker.

## 3. Edit pass (fresh eyes; a second model is fine)

Reread as an Indian founder skimming on a phone. Cut filler and throat-clearing ("In today's
digital landscape", "It's important to note", "delve", "navigate", "robust"). Short sentences.
Plain verbs. No bullet soup: use bullets only for real lists. Rs and crore, not USD. The page should
read like a careful practitioner wrote it, because the content is checked, not because it was
disguised.

## 4. Citation check (do not skip)

List every `s.` and `Rule` citation in the answer. Open each one in `references/` and confirm it
says what the answer claims. Fix or delete anything that does not match. Put the table
(citation, claim, confirmed yes/no) in the PR body.

## 5. Build and publish

```bash
pip install markdown        # once
python tools/build_site.py  # must finish with "Built N pages"
git checkout -- docs && git clean -fdq docs   # CI rebuilds docs on merge; keep the PR to one file
git switch -c answer/<slug>
git add answers/<slug>.md
git commit -m "answer: <question>"
git push -u origin answer/<slug>
gh pr create --title "answer: <question>" --body "<source URL, why this question, citation table>"
```

Never post to Reddit or any forum, never reply to the asker, never touch other files.
