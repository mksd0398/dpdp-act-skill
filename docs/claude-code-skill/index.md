# DPDP Act AI skill for Claude Code: free, cites every section

> Canonical page: https://mksd0398.github.io/dpdp-act-skill/claude-code-skill/
> Not legal advice. Educational compliance reference only; no lawyer-client relationship arises from its use and the author is not a lawyer. Verify statutory text against the Gazette of India and consult qualified Indian legal counsel before acting.

dpdp-analyze is a free, open-source (MIT) Claude Code skill that answers Indian data protection questions from the verbatim DPDP Act 2023 and the DPDP Rules 2025, citing a section or rule for every claim. It reviews privacy notices, consent flows, vendor contracts and whole products.

## Install

Inside Claude Code:

```
/plugin marketplace add mksd0398/dpdp-act-skill
/plugin install dpdp-analyze@dpdp
```

Or copy the folder:

```
git clone https://github.com/mksd0398/dpdp-act-skill.git
cp -r dpdp-act-skill/skills/dpdp-analyze ~/.claude/skills/
```

Claude.ai: download https://mksd0398.github.io/dpdp-act-skill/downloads/dpdp-analyze.zip and upload it under Customize > Skills. GitHub Copilot: `gh skill install mksd0398/dpdp-act-skill dpdp-analyze`. Gemini CLI: `gemini skills install https://github.com/mksd0398/dpdp-act-skill.git --path skills/dpdp-analyze`. Codex, Cursor and other Agent Skills tools: copy `skills/dpdp-analyze` into `~/.agents/skills/`.

## Example prompts

- Is this privacy policy DPDP compliant? [paste or attach it]
- Review this consent screen against section 6 and Rule 3.
- Check this vendor DPA for what section 8(2) and Rule 6(1)(f) require.
- Audit our signup and onboarding flow against the DPDP Act.
- Run the full DPDP compliance checklist against this repository.
- Our app has users under 18. What has to change before 14 May 2027?
- Do we need a DPO in India?
- Can we store Indian customer data on AWS Frankfurt?
- Are we a Significant Data Fiduciary?
- We had a data breach. What do we have to do, and by when?
- Draft the Rule 7 notice to affected users.
- Is a ransomware lockout a personal data breach under the DPDP Act?

## FAQ

### Is the DPDP skill free?

Yes. The skill, the reference files and this site are open source under the MIT licence. The Act and Rules text are Government of India works reproduced under section 52(1)(q) of the Copyright Act, 1957.

### What do I need to run it?

Claude Code, Anthropic's agentic coding tool, which runs in the terminal, IDEs, the desktop app and the web. The skill is a standard SKILL.md folder with plain Markdown references, so agents that support the Agent Skills format can load it too, and the reference files work in any RAG index or prompt library unchanged.

### Does the skill send my data anywhere?

The skill itself makes no network calls. It is instructions plus reference files that Claude reads locally. Your prompts and any documents you share are processed by Claude under the terms of your own Claude plan, as with any other Claude Code session.

### How is it different from asking a chatbot about the DPDP Act?

General-purpose models pattern-match Indian law to the GDPR and invent things that are not in the DPDP Act, such as a sensitive-data category or a legitimate interests ground. The skill makes Claude walk the Act's five gates, quote only from the verbatim Gazette text, cite a section or rule for every proposition, check commencement dates, and say what is still unsettled.

### Is the output legal advice?

No. The output is machine-generated analysis and can be wrong. The skill closes every substantive answer with a reminder to verify against the Gazette of India and consult qualified Indian legal counsel.

### How do I update it?

Run /plugin marketplace update dpdp inside Claude Code. Corrections and new government notifications are tracked in the GitHub repository.

Source: https://github.com/mksd0398/dpdp-act-skill
