# Where to list the skill

Checked 2 October 2026. Directories change their rules often, so reread each one's rules before
you submit. "Unverified" means I could not confirm the detail from the directory's own pages.

## Reusable copy

**Name:** DPDP Act Analysis (`dpdp-analyze`)

**One line (under 150 characters):**
> Analyse privacy notices, consent flows and contracts against India's DPDP Act 2023, citing the section for every claim.

**Awesome-list entry:**
```markdown
- [DPDP Act Analysis](https://github.com/mksd0398/dpdp-act-skill) - Analyses privacy notices, consent flows, vendor contracts and products against India's Digital Personal Data Protection Act 2023 and DPDP Rules 2025, from the verbatim Gazette text, citing a section or rule for every claim.
```

**Short description (about 50 words):**
> A Claude Code skill and plugin for India's Digital Personal Data Protection Act, 2023. It ships all
> 44 sections verbatim from the Gazette, a DPDP Rules 2025 reference, a 78-point compliance checklist
> and an assessment template, and makes Claude cite a section or rule for every proposition instead
> of importing GDPR concepts. Open source (MIT). Not legal advice.

**Install line:**
```
/plugin marketplace add mksd0398/dpdp-act-skill
/plugin install dpdp-analyze@dpdp
```

**Category:** Legal / Compliance / Privacy. **Licence:** MIT.
**Homepage:** https://mksd0398.github.io/dpdp-act-skill/

---

## Tier 1: submit now, no star gate

| Where | How | Notes |
|---|---|---|
| **Anthropic plugin directory** ([claude.ai/directory/manage](https://claude.ai/directory/manage)) | Web portal. Guide: [claude.com/docs/directory/publish](https://claude.com/docs/directory/publish) | Needs a paid Claude plan (Pro, Max, Team or Enterprise). A skill must be bundled as a plugin from a public GitHub repository, which this one already is. Every version is scanned automatically, and new listings get a human review. One listing reaches claude.ai, the desktop and mobile apps, Cowork and Claude Code. **Highest value.** |
| **claude-plugins.dev** | Indexed automatically from GitHub | No submission. Search for "dpdp" a few days after merging to check it was picked up. |
| **skillsmp.com** | Indexed automatically from GitHub | No submission form found. |
| **claudemarketplaces.com** | Found automatically via `.claude-plugin/marketplace.json`, then reviewed by an editor | One secondary source says it needs 5 or more stars (unverified). |
| **skills.sh** | Ranked by installs through `npx skills add` | The README now documents `npx skills add mksd0398/dpdp-act-skill`. Whether listing is automatic is unverified. |
| **lawve.ai** ([lawve.ai/new/skill](https://lawve.ai/new/skill)) | Web form, reviewed by hand | Legal-skills directory with India and Data Protection sections. Also feeds [lawve-ai/awesome-legal-skills](https://github.com/lawve-ai/awesome-legal-skills). It already lists other India DPDP skills, so lead with what is different: the verbatim Gazette text and a citation on every claim. |
| **hesreallyhim/awesome-claude-code** (~55k stars) | [Issue form](https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml). **Do not open a PR.** | A person must submit it, not a coding agent. The repository must be at least 14 days old and actively developed, or have 100 or more stars. One resource per submission. [Rules](https://github.com/hesreallyhim/awesome-claude-code/blob/main/CONTRIBUTING.md). |
| **ComposioHQ/awesome-claude-skills** (~76k) | PR titled `Add DPDP Act Analysis skill` | Must be tested and documented. [Rules](https://github.com/ComposioHQ/awesome-claude-skills/blob/master/CONTRIBUTING.md). |
| **BehiSecc/awesome-claude-skills** (~10k) | PR or issue | [Repository](https://github.com/BehiSecc/awesome-claude-skills). |
| **getprobo/awesome-compliance** (~110) | PR into "Security, privacy & data protection" | [Repository](https://github.com/getprobo/awesome-compliance). |
| **theopenlane/awesome-compliance** (~90) | PR | [Repository](https://github.com/theopenlane/awesome-compliance). |
| **Vaquill-AI/awesome-legaltech** (~240) | PR into "Agent Skills" or "Compliance & RegTech" | Its rules exclude "personal projects" and require neutral descriptions, so read them first. [Rules](https://github.com/Vaquill-AI/awesome-legaltech/blob/main/CONTRIBUTING.md). |
| **aitmpl.com** | PR to [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | Exact process unverified. |
| **Smithery** ([smithery.ai/skills](https://smithery.ai/skills)) | "Publish" button | Mechanism unverified. |

## Tier 2: once you have 10 or more stars

| Where | How | Notes |
|---|---|---|
| **travisvn/awesome-claude-skills** (~15k) | PR | PRs from repositories under 10 stars are closed automatically. **AI-generated PRs are not accepted**, so write this one yourself. [Rules](https://github.com/travisvn/awesome-claude-skills/blob/main/CONTRIBUTING.md). |
| **claudemarketplaces.com** | Automatic | Check again once you pass 5 stars. |

## Tier 3: once you have real usage or 100 or more stars

| Where | How | Notes |
|---|---|---|
| **VoltAgent/awesome-agent-skills** (~35k) | PR titled `Add skill: mksd0398/dpdp-analyze` | Wants "real community usage" and refuses brand-new skills. Point to stars, installs or users. [Rules](https://github.com/VoltAgent/awesome-agent-skills/blob/main/CONTRIBUTING.md). |
| **jeswinsimon/awesome-made-by-indians** (~135) | PR | Needs 100 or more stars. |

## Not available

- **anthropics/skills** is Anthropic's own and partners' skills, with no route for third
  parties. Use the plugin directory above.

## Neighbours

[mukul975/Privacy-Data-Protection-Skills](https://github.com/mukul975/Privacy-Data-Protection-Skills)
(~290 stars) also covers the DPDP Act among other regimes. Lists that already include it are
receptive to the topic. If a maintainer asks how this one differs: it is DPDP-only, depth over
breadth, with the verbatim Act, the Rules, a published site and a citation on every claim.
