# India DPDP Act 2023 + DPDP Rules 2025: full text and a compliance analysis skill

[![Read the Act online](https://img.shields.io/badge/read-DPDP%20Act%202023-0b6bcb)](https://mksd0398.github.io/dpdp-act-skill/act/)
[![Read the Rules](https://img.shields.io/badge/read-DPDP%20Rules%202025-0b6bcb)](https://mksd0398.github.io/dpdp-act-skill/rules/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Not legal advice](https://img.shields.io/badge/⚠-not%20legal%20advice-b00020)](DISCLAIMER.md)

> ## ⚠️ This is not legal advice
>
> This repository is an **educational and compliance-reference resource**. It is **not legal
> advice**, it is **not a substitute for a qualified lawyer**, and **no lawyer-client relationship
> arises** from using it, reading it, or running the skill.
>
> The author is **not a lawyer** and is **not authorised to practise law**. Nothing here should be
> relied on to determine your legal obligations. The analysis produced by the skill is
> machine-generated and **can be wrong**.
>
> Data protection law is fact-specific, and the DPDP framework is still being brought into force in
> stages, with key notifications yet to be issued. **Before you act on anything here, verify the
> statutory text against the Gazette of India and consult qualified Indian legal counsel.**
>
> Provided "as is", with no warranty and no liability for any loss arising from its use.
> Full terms in [DISCLAIMER.md](DISCLAIMER.md).

A complete, verbatim, section-by-section reference for the **Digital Personal Data Protection Act,
2023** (Act 22 of 2023) and the **Digital Personal Data Protection Rules, 2025**, packaged as an
installable **Claude Code skill** that analyses privacy notices, consent flows, vendor contracts and
whole products against Indian data protection law.

**Read it in your browser:** [mksd0398.github.io/dpdp-act-skill](https://mksd0398.github.io/dpdp-act-skill/)

---

## What is in here

| | |
|---|---|
| **All 44 sections of the DPDP Act, 2023**, verbatim from the Gazette of India | [`act-full-text.md`](skills/dpdp-analyze/references/act-full-text.md) |
| **All 23 DPDP Rules, 2025 and 7 Schedules**, with phased commencement dates | [`rules-2025.md`](skills/dpdp-analyze/references/rules-2025.md) |
| **How the statute actually works**: the five gates, 16 common misreadings, DPDP vs GDPR | [`doctrine.md`](skills/dpdp-analyze/references/doctrine.md) |
| **Section index** for fast lookup | [`section-index.md`](skills/dpdp-analyze/references/section-index.md) |
| **A 12-part compliance checklist**, every item anchored to a section or rule | [`compliance-checklist.md`](skills/dpdp-analyze/references/compliance-checklist.md) |
| **An assessment report template** | [`report-template.md`](skills/dpdp-analyze/assets/report-template.md) |

Every one of the Act's **14 Illustrations** is reproduced, because they are part of the enacted text
and are the strongest interpretive aid the statute gives you.

---

## Install

### Recommended: as a Claude Code plugin

This repository is a Claude Code plugin marketplace. Inside Claude Code, run:

```
/plugin marketplace add mksd0398/dpdp-act-skill
```

```
/plugin install dpdp-analyze@dpdp
```

That is it. You get updates with `/plugin marketplace update dpdp`, and you can remove it cleanly
with `/plugin uninstall dpdp-analyze@dpdp`.

### Alternative: copy the skill directly

If you would rather not use the plugin system, Claude Code also reads skills from `~/.claude/skills/`:

```bash
git clone https://github.com/mksd0398/dpdp-act-skill.git
cp -r dpdp-act-skill/skills/dpdp-analyze ~/.claude/skills/
```

### Using it

```
/dpdp-analyze
```

Or just ask a question. The skill triggers on Indian privacy topics without being named:

- "Is this privacy policy DPDP compliant?"
- "Do we need a DPO in India?"
- "What consent do we need to collect phone numbers from Indian users?"
- "Can we store Indian customer data on AWS Frankfurt?"
- "We had a data breach, what do we have to do?"
- "Are we a Significant Data Fiduciary?"

Works with Claude Code, and the reference files are plain Markdown so they drop into any other
agent, RAG index or prompt library unchanged.

---

## Why this exists

Large language models get Indian data protection law wrong in specific, repeatable ways, because
they pattern-match to GDPR. This repository pins the actual text so the answer is anchored to a
section rather than recalled.

**The ten things most often gotten wrong about the DPDP Act:**

1. **There are only two lawful bases.** Consent (s.6), or the closed list of "certain legitimate
   uses" in s.7. There is **no legitimate interests** ground.
2. **There is no sensitive personal data category.** Health, biometric, financial and caste data get
   no special tier under the DPDP Act.
3. **A child is anyone under 18** (s.2(f)). Not 13, not 16.
4. **Targeted advertising to children is banned outright** (s.9(3)). Parental consent does not cure it.
5. **Breach notification has no harm threshold** (s.8(6)). You notify the Board **and every affected
   individual**, every time. It includes mere **loss of access**, so ransomware counts.
6. **Only notified Significant Data Fiduciaries need a DPO** (s.10(2)(a)). Everyone else publishes a
   contact person under s.8(9).
7. **The Act does not mandate data localisation.** s.16 is a negative list. Rule 13(4) localises
   specified categories for SDFs only. Sectoral rules such as RBI's bind independently.
8. **Individuals get no compensation.** Penalties go to the Consolidated Fund of India (s.34), civil
   courts are barred (s.39), and IT Act s.43A was repealed (s.44(2)(a)).
9. **There is no data portability right and no right against automated decision-making.**
10. **Data Principals have enforceable duties** (s.15), with a penalty up to Rs 10,000. That is
    unusual internationally.

---

## Key dates: when does the DPDP Act come into force?

The Rules were notified **13 November 2025** and commence in three tranches.

| Effective | What comes into force |
|---|---|
| **14 November 2025** | Rules 1, 2 and 17 to 21. Data Protection Board machinery: appointment, service terms, meetings, digital-office functioning. |
| **14 November 2026** | Rule 4, registration and obligations of **Consent Managers**. |
| **14 May 2027** | Rules 3, 5 to 16 and 22 to 23. **Every substantive business obligation**: notice, security safeguards, breach intimation, retention and erasure, children's consent, SDF duties, rights machinery, transfers. |

**14 May 2027 is the date that matters for a compliance programme.**

---

## DPDP Act penalties

Every figure in the Schedule is a ceiling ("may extend to"), gated on the Data Protection Board
finding the breach **"significant"** under s.33(1).

| Breach | Maximum penalty |
|---|---|
| Failure to take reasonable security safeguards, s.8(5) | **Rs 250 crore** |
| Failure to notify a personal data breach, s.8(6) | **Rs 200 crore** |
| Breach of children's data obligations, s.9 | **Rs 200 crore** |
| Breach of Significant Data Fiduciary obligations, s.10 | **Rs 150 crore** |
| Breach of Data Principal duties, s.15 | **Rs 10,000** |
| Breach of a voluntary undertaking, s.32 | Ceiling of the underlying breach |
| Any other provision | **Rs 50 crore** |

Mitigation lives in s.33(2)(a) to (g). Appeals go to **TDSAT** within **60 days** (s.29).

---

## DPDP Act vs GDPR

| Topic | DPDP 2023 | GDPR |
|---|---|---|
| Lawful bases | 2: consent, or the closed s.7 list | 6, including legitimate interests |
| Legitimate interests | **None** | Art 6(1)(f) |
| Sensitive data category | **None** | Art 9 special categories |
| Extraterritorial trigger | Offering goods or services to India only | Offering **or monitoring behaviour** |
| Child age | **Under 18** | 16, states may lower to 13 |
| Ads targeted at children | **Prohibited outright** | Restricted, not banned |
| Breach notification threshold | **None** | Risk-based |
| DPO | Notified SDFs only | Wider Art 37 triggers |
| Data portability | **Absent** | Art 20 |
| Automated decision-making | **Absent** | Art 22 |
| Compensation to individuals | **Absent** | Art 82 |
| Transfers | Negative list, permitted by default | Adequacy, SCCs, BCRs |
| Regulator | Adjudicatory Board, **no rule-making power** | Independent DPAs with guidance powers |
| Duties on individuals | **Yes**, s.15 | No |
| Maximum penalty | Rs 250 crore | 4% global turnover or EUR 20m |

Full comparison in [`doctrine.md`](skills/dpdp-analyze/references/doctrine.md).

---

## What the DPDP Act changed in other laws

Section 44 quietly amended three statutes, and this is routinely missed:

- **IT Act s.43A omitted.** The statutory compensation route for negligent handling of sensitive
  personal data is gone, which materially undermines the footing of the **SPDI Rules, 2011**.
- **IT Act s.87(2)(ob) omitted**, removing the rule-making power those Rules rested on.
- **RTI Act s.8(1)(j) replaced** with a flat exemption for "information which relates to personal
  information", deleting the old public-interest carve-in. The most politically contested amendment
  in the Act.
- **TRAI Act s.14(c)** amended so TDSAT is expressly the DPDP appellate tribunal.

---

## Accuracy and provenance

This matters more than usual, because it is legislation.

- **The Act text is verbatim from the Gazette of India**, Extraordinary, Part II, Section 1, No. 25,
  dated 11 August 2023 (CG-DL-E-12082023-248045). It is reproduced here in full and is safe to quote.
  Reproduction of an Act of Parliament is permitted under s.52(1)(q) of the Copyright Act, 1957.
- **The Rules content is secondary.** It was assembled from the PIB release and multiple independent
  sources cross-checked against each other, not transcribed from the Gazette. It is reliable working
  knowledge. **Verify against the notified Gazette text at
  [meity.gov.in](https://www.meity.gov.in/) before relying on it externally.** The skill enforces
  this warning in its own output.
- **No Board jurisprudence exists.** "Significant" in s.33(1) is undefined. Penalty figures are
  statutory ceilings, not predictions.

Found an error in the Act text? [Open an issue](https://github.com/mksd0398/dpdp-act-skill/issues).
Corrections to legislation are the most valuable contribution you can make here.

---

## Frequently asked questions

**Is the DPDP Act in force?**
Partly. The Act received assent on 11 August 2023 but s.1(2) permits staggered commencement. Board
machinery has been live since 14 November 2025. The substantive obligations on businesses commence
**14 May 2027**.

**Does the DPDP Act apply to companies outside India?**
Only where the processing is connected to **offering goods or services to Data Principals within
India** (s.3(b)). Unlike GDPR, merely monitoring the behaviour of people in India is not a trigger.

**Does the DPDP Act require data localisation?**
No, not in the Act. s.16 lets the Central Government notify countries to which transfer is
*restricted*, and none has been notified. Rule 13(4) creates a targeted localisation duty for
**notified Significant Data Fiduciaries only**, over categories the Government specifies. Sectoral
regulators such as the RBI localise independently, preserved by s.16(2).

**Who is a Significant Data Fiduciary?**
Only an entity the **Central Government has notified** as one under s.10(1). You cannot self-classify,
and size alone does not make you one. As at the last check, none has been notified.

**Do we need a Data Protection Officer in India?**
Only if notified as a Significant Data Fiduciary. The DPO must be **based in India**, be an
individual, and be **responsible to the board of directors** (s.10(2)(a)). Every other Data Fiduciary
need only publish the contact information of a person who can answer questions (s.8(9), Rule 9).

**How fast must we report a data breach under the DPDP Act?**
Affected individuals: **without delay** (Rule 7(1)). The Data Protection Board: an initial
intimation **without delay**, then a detailed report within **72 hours** of becoming aware
(Rule 7(2)). There is no harm threshold, so every breach is reportable.

**What is the maximum penalty under the DPDP Act?**
**Rs 250 crore**, for failure to take reasonable security safeguards under s.8(5). See the table above.

**Are the SPDI Rules, 2011 still valid?**
Their footing is materially undermined. DPDP s.44(2) omitted both IT Act s.43A, which they
implemented, and s.87(2)(ob), the rule-making power behind them. Do not cite them as unqualified
live obligations.

---

## Contributing

Corrections to statutory text take priority over everything else. Please cite the Gazette reference
in your issue or pull request.

## License

[MIT](LICENSE) for the skill, the tooling and the commentary.

The text of the Digital Personal Data Protection Act, 2023 and the Digital Personal Data Protection
Rules, 2025 are Government of India works, reproduced under s.52(1)(q) of the Copyright Act, 1957.

## Disclaimer

**This is not legal advice.** See [DISCLAIMER.md](DISCLAIMER.md) for the full terms. In short:

- This is an educational and compliance-reference resource, not legal advice, and not a substitute
  for a qualified lawyer.
- **No lawyer-client relationship** arises from using this repository or the skill.
- The author is **not a lawyer** and is not authorised to practise law.
- Output from the skill is **machine-generated and can be wrong**. Verify every statutory
  reference against the Gazette of India.
- The DPDP framework is **still being brought into force in stages**, and several key notifications
  have not been issued. Positions stated here can change.
- Consult **qualified Indian legal counsel** before acting on anything here.
- Provided "as is", with no warranty and no liability for any loss arising from its use.

---

**Keywords:** DPDP Act 2023, Digital Personal Data Protection Act India, DPDP Rules 2025, Indian data
protection law, DPDP compliance checklist, Data Protection Board of India, Significant Data
Fiduciary, Data Fiduciary obligations, Data Principal rights, DPDP penalties, DPDP vs GDPR, India
privacy law, personal data breach notification India, verifiable parental consent India, consent
manager DPDP, Claude Code skill, AI legal compliance.
