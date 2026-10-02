# Draft posts

These are drafts. Rewrite them in your own voice before posting. Every one says "not legal advice",
and none asks for upvotes, which is against the rules on Hacker News, Reddit and Product Hunt.

Links used throughout:
- Site: https://mksd0398.github.io/dpdp-act-skill/
- Skill page: https://mksd0398.github.io/dpdp-act-skill/claude-code-skill/
- Repository: https://github.com/mksd0398/dpdp-act-skill
- Checklist: https://mksd0398.github.io/dpdp-act-skill/compliance-checklist/

---

## Hacker News (Show HN)

Show HN is for things people can try, and a GitHub repository qualifies
([rules](https://news.ycombinator.com/showhn.html)). Post on a weekday morning, US time. Put the
text below in the first comment, not the submission.

**Title** (exactly 80 characters, HN's limit):
```
Show HN: India's DPDP Act as a Claude Code skill, with a citation on every claim
```

**URL:** `https://github.com/mksd0398/dpdp-act-skill`

**First comment:**
```
India's data protection law, the DPDP Act 2023, starts to bite on 14 May 2027, when the
substantive obligations in the DPDP Rules 2025 commence. Whenever I asked an LLM about it I got
the GDPR back: a "legitimate interests" basis the Act does not have, a sensitive-data tier it does
not have, a child age of 13 or 16 instead of 18, and a harm threshold on breach notification that
the Act deliberately omits.

So I packaged the Act as a Claude Code skill: all 44 sections verbatim from the Gazette, a Rules
2025 reference, a doctrine file covering the 16 most common misreadings, and a 78-point checklist.
The skill's hard rules are no proposition without a section or rule anchor, quote only the
verbatim text, check commencement before calling anything binding, and never import GDPR
concepts.

The same Markdown builds a static site with the Act section by section:
https://mksd0398.github.io/dpdp-act-skill/

I'm not a lawyer and this is not legal advice. What I would value most is corrections: if you know
the Act or the Rules and spot something wrong, please open an issue.
```

---

## Reddit

Read each subreddit's sidebar before posting. I could not verify the current rules for any of
them.

### r/ClaudeAI (use the "Built with Claude" flair)

**Title:**
```
I built a skill that stops Claude answering questions about India's privacy law with GDPR
```

**Body:**
```
**What it is:** dpdp-analyze, a free, open-source skill and plugin for Claude Code. It
covers India's Digital Personal Data Protection Act 2023 and the DPDP Rules 2025.

**Why:** general models pattern-match Indian law to the GDPR. They invent a "legitimate
interests" basis (DPDP has only consent or a closed list in s.7). They invent a sensitive-data
category (there isn't one). They use 13 or 16 as the child age (it's 18, s.2(f)). And they add
a harm threshold to breach notification (there's none, s.8(6)).

**How it works:** the skill ships the full Act verbatim from the Gazette, plus a Rules
reference, a "doctrine" file of the common misreadings and a 78-point checklist. SKILL.md gives
Claude hard rules: no claim without a section or rule anchor, quote only the verbatim file, check
commencement dates, flag Rules text as secondary-sourced. It triggers on Indian privacy questions
even if you never say "DPDP".

**Try it:**
    /plugin marketplace add mksd0398/dpdp-act-skill
    /plugin install dpdp-analyze@dpdp

Then ask: "Is this privacy policy DPDP compliant?" or "We had a breach, what do we owe the
Board and users, and by when?"

It also works in Claude.ai: upload the ZIP from the site.

Site with the Act section by section: https://mksd0398.github.io/dpdp-act-skill/
Repo: https://github.com/mksd0398/dpdp-act-skill

Not legal advice, and I'm not a lawyer. Corrections are very welcome.
```

### r/ClaudeCode

**Title:**
```
Packaging a statute as a Claude Code plugin: verbatim references, hard rules, and a site built from the same Markdown
```

**Body:**
```
I built a plugin marketplace for one skill: an analyst for India's DPDP Act 2023. A few things
that worked and might be useful to anyone building reference-heavy skills:

- Verbatim source in references/ and a rule in SKILL.md that quotes may only come from that file.
  This cut "recalled" law to nothing.
- A small doctrine.md that encodes the traps, loaded on every question, while the 64 KB full
  text is only opened when Claude is about to quote. This keeps context lean.
- A description field written as a list of real user questions, so it triggers without the user
  naming the law.
- The same Markdown builds a static site (Python, about 70 pages) with llms.txt, a Markdown twin
  per page, and an auto-link from every "s.8(6)" to its section page.

    /plugin marketplace add mksd0398/dpdp-act-skill
    /plugin install dpdp-analyze@dpdp

Repo: https://github.com/mksd0398/dpdp-act-skill
```

### r/developersIndia, and similar Indian tech communities

Check whether the subreddit wants projects in a weekly showcase thread rather than as a post.

**Title:**
```
DPDP Act deadline is 14 May 2027: free section-by-section reference, a 78-point checklist, and an AI skill to audit your app
```

**Body:**
```
If your app has Indian users, the DPDP Rules' substantive obligations commence on
14 May 2027. They cover notice, consent, security safeguards, the 72-hour breach report,
retention and erasure, and children's data.

I put together a free reference with the full Act verbatim, section by section. It also has the
Rules, a 78-point compliance checklist with every item tied to a section, a glossary and an FAQ:
https://mksd0398.github.io/dpdp-act-skill/

There's also an open-source Claude Code skill that audits a privacy notice, consent flow or
codebase against the Act and cites the section for every finding. It also installs into
Claude.ai, Copilot and Gemini CLI.

Three things that surprise most devs:
1. Every breach is reportable, with no harm threshold, including ransomware lockouts (s.8(6)).
2. Under 18 is a child, and tracking or targeted ads to children are banned outright (s.9(3)).
3. Notice and consent must be available in English or any of the 22 Eighth Schedule languages
   (s.5(3)).

Not legal advice; I'm not a lawyer. Corrections welcome.
```

---

## LinkedIn

Post from your personal profile. Put the links in the post itself; LinkedIn may reduce reach for
posts with links, but moving them to a comment is optional.

```
14 May 2027.

That's when the substantive obligations in India's DPDP Rules 2025 commence for every
business processing personal data: notice, consent, security safeguards, breach reporting,
retention, children's data.

Ask most AI tools about the DPDP Act, though, and you get the GDPR back. Here are 10 things
the Act actually says:

1. Only two lawful bases: consent (s.6) or the closed list in s.7. No "legitimate interests".
2. No sensitive personal data category.
3. A child is anyone under 18 (s.2(f)).
4. Targeted advertising to children is banned outright; consent does not cure it (s.9(3)).
5. Every breach is notifiable to the Board and to each affected person, with no harm
   threshold (s.8(6)).
6. Only notified Significant Data Fiduciaries must appoint a DPO (s.10(2)(a)).
7. The Act does not mandate data localisation (s.16).
8. Individuals get no compensation; penalties go to the Consolidated Fund (s.34).
9. No right to data portability, and no right against automated decisions.
10. Individuals have enforceable duties too, with a penalty of up to Rs 10,000 (s.15).

I've published the full Act, verbatim and section by section, with the Rules, a 78-point
compliance checklist, a glossary and an FAQ, free:
https://mksd0398.github.io/dpdp-act-skill/

And because general AI keeps importing GDPR into Indian law, I packaged it as an open-source
skill for Claude Code. It reviews privacy notices, consent flows and vendor contracts, and
cites the section for every claim:
https://mksd0398.github.io/dpdp-act-skill/claude-code-skill/

Not legal advice. I'm not a lawyer, and I'd genuinely welcome corrections from privacy
practitioners.

#DPDP #DPDPAct #DataProtection #Privacy #India #Compliance #LegalTech #AI #ClaudeCode
```

---

## X / Twitter thread

```
1/ India's DPDP Act deadline is 14 May 2027, and most AI tools still answer DPDP questions with the GDPR.

I built a free Claude Code skill that answers from the verbatim Act and cites the section every time. 🧵

2/ What models get wrong, part 1: "legitimate interests". It doesn't exist under DPDP. There are only two lawful bases: consent (s.6) or the closed list in s.7.

3/ No sensitive personal data category. A child is anyone under 18 (s.2(f)). Targeted ads to children are banned outright, and consent doesn't cure it (s.9(3)).

4/ Breach notification has no harm threshold (s.8(6)). Every breach goes to the Board and to each affected person. The Board's detailed report is due within 72 hours (Rule 7).

5/ Only notified Significant Data Fiduciaries need a DPO (s.10(2)(a)). No localisation in the Act (s.16). No compensation for individuals (s.34, s.39).

6/ Install in Claude Code:
/plugin marketplace add mksd0398/dpdp-act-skill
/plugin install dpdp-analyze@dpdp

Also works in Claude.ai, Copilot, Gemini CLI and Codex.

7/ The full Act section by section, the Rules, a 78-point checklist and an FAQ:
https://mksd0398.github.io/dpdp-act-skill/

Not legal advice. Corrections welcome.
```

---

## Product Hunt

Launch once you have a few stars and some early feedback to quote. Makers may post their own
products; ask for feedback, never upvotes.

- **Name:** DPDP Act Skill
- **Tagline** (60-character limit): `Ask AI about India's privacy law, get the section back`
- **Link:** https://mksd0398.github.io/dpdp-act-skill/claude-code-skill/
- **Topics:** Legal, Privacy, Developer Tools, Artificial Intelligence, Open Source
- **Gallery:** `tools/static/assets/og.jpg`, plus screenshots of the home page, a section page,
  the checklist and a real Claude Code answer.
- **Description:**
  ```
  Free, open-source Claude Code skill and website for India's DPDP Act 2023 and Rules 2025:
  the verbatim Act, a 78-point compliance checklist, and an AI analyst that reviews privacy
  notices, consent flows and contracts, citing the section for every claim. Not legal advice.
  ```
- **Maker's first comment:**
  ```
  Hi PH! India's DPDP Rules start to bite on 14 May 2027. I kept getting GDPR answers from AI
  tools when I asked about Indian law, so I pinned the verbatim Act and Rules into a Claude
  Code skill with one rule: no claim without a section number. It installs in two commands,
  and also works in Claude.ai, Copilot and Gemini CLI. I'm not a lawyer, so I'd especially love
  feedback from anyone who works with the DPDP Act.
  ```

---

## Blog article (dev.to, Hashnode, Medium or a LinkedIn article)

Some platforms require you to disclose AI assistance. Disclose it if this draft is the basis of
your post.

**Title:** What AI gets wrong about India's DPDP Act, and the Claude Code skill I built to fix it

**Tags:** `ai` `privacy` `india` `claude`

```markdown
India's Digital Personal Data Protection Act, 2023 is the country's first comprehensive data
protection law. Its Rules were notified on 13 November 2025, and the obligations most businesses
care about (notice, consent, security safeguards, breach reporting, retention, children's data)
commence on **14 May 2027**.

When I started asking AI assistants about it, I kept getting confident answers that were
really about the GDPR.

## Six things models get wrong

1. **"You can rely on legitimate interests."** You can't. The DPDP Act has exactly two lawful
   bases: consent under section 6, or one of the closed list of "certain legitimate uses" in
   section 7.
2. **"Health and biometric data are sensitive personal data."** Not under this Act. There is
   no special category at all.
3. **"Children are under 13 (or 16)."** Under the DPDP Act a child is anyone under 18 (s.2(f)),
   and tracking, behavioural monitoring and targeted advertising directed at children are banned
   outright (s.9(3)).
4. **"Notify the regulator if the breach is likely to cause harm."** There is no harm threshold.
   Every personal data breach is notified to the Data Protection Board and to each affected
   individual (s.8(6)), and loss of access counts, so ransomware is in scope.
5. **"Appoint a DPO."** Only entities notified as Significant Data Fiduciaries must (s.10(2)(a)).
   Everyone else publishes a contact person (s.8(9)).
6. **"Indian data must stay in India."** The Act doesn't say that. Section 16 is a negative list
   of restricted countries, and none has been notified. Sectoral rules such as the RBI's are a
   separate matter.

## Why this happens

Models have seen far more GDPR commentary than DPDP text, so they fill gaps with the familiar
regime. The fix is not a cleverer prompt; it's grounding. Give the model the actual statute and
forbid it to assert anything it can't anchor.

## The skill

`dpdp-analyze` is an open-source skill for Claude Code. It ships:

- all 44 sections of the Act, verbatim from the Gazette of India;
- a reference to all 23 Rules and 7 Schedules, flagged as secondary-sourced;
- a doctrine file covering the 16 most common misreadings;
- a 78-point compliance checklist, every item anchored to a section or rule;
- an assessment report template.

Its SKILL.md sets hard rules: no proposition without a section or rule anchor; quotes only from
the verbatim file; check commencement before calling anything binding; never import GDPR
concepts; close with a single not-legal-advice line.

Install it in Claude Code:

    /plugin marketplace add mksd0398/dpdp-act-skill
    /plugin install dpdp-analyze@dpdp

Then ask "Is this privacy policy DPDP compliant?" or point it at your signup flow. It also loads
in Claude.ai, GitHub Copilot, Gemini CLI and Codex, because it uses the open Agent Skills format.

The same Markdown builds a free reference site with the Act section by section, the Rules, the
checklist, a glossary and an FAQ: https://mksd0398.github.io/dpdp-act-skill/

*This is not legal advice, and I'm not a lawyer. If you find an error, please open an issue on
[GitHub](https://github.com/mksd0398/dpdp-act-skill).*
```

---

## Press pitch (MediaNama, Inc42, YourStory)

- Inc42: [startup submission form](https://inc42.com/startup-submission/)
- YourStory: [editorial coverage request](https://www.contacts.yourstory.com/editorial-coverage-request)
- MediaNama and IAPP: no submission route verified. Reach a reporter who covers the DPDP Act.

**Subject:** Free, open-source DPDP Act reference and AI skill ahead of the May 2027 deadline

```
Hi <name>,

With the DPDP Rules' substantive obligations commencing on 14 May 2027, I've released a free,
open-source reference for the DPDP Act 2023: the full Act verbatim and section by section, the
Rules 2025, a 78-point compliance checklist, a glossary and an FAQ.

It also ships as an AI skill for Claude Code (and Claude.ai, Copilot and Gemini CLI). The skill
reviews privacy notices, consent flows and vendor contracts against the Act and must cite a
section or rule for every claim. It's built because general AI models routinely answer Indian
privacy questions with GDPR concepts the DPDP Act doesn't contain.

Site: https://mksd0398.github.io/dpdp-act-skill/
Code: https://github.com/mksd0398/dpdp-act-skill

Happy to share examples or talk through what AI tools get wrong about the Act. It is an
educational resource, not legal advice.

<your name>
```

---

## LiveLaw column

LiveLaw rejects AI-generated or AI-rewritten text ([guidelines](https://www.livelaw.in/share-content):
1,200 to 1,500 words, Word file, to columns@livelaw.in). Write it yourself. A possible angle is
"Six ways AI tools misstate the DPDP Act, and why practitioners should care", using the
misreadings in `doctrine.md` section 13. Mention the resource in your author bio, not the body.

---

## WhatsApp, Slack and community groups

```
Free, open-source DPDP Act 2023 reference: the full Act section by section, Rules 2025, a 78-point
compliance checklist, FAQ. There's also an AI skill for Claude that cites the section for every
answer. https://mksd0398.github.io/dpdp-act-skill/ (not legal advice)
```
