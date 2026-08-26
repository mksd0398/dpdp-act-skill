---
name: dpdp-analyze
description: Analyse anything against India's Digital Personal Data Protection Act, 2023 (Act 22 of 2023) and the DPDP Rules, 2025. Use whenever the question touches Indian data protection or privacy law, whether or not "DPDP" is named. Triggers include - is this DPDP compliant, what consent do we need in India, Indian privacy notice review, data breach notification India, is my company a Significant Data Fiduciary, do we need a DPO in India, children's data and age gating for Indian users, can we transfer Indian user data abroad, data localisation India, RTI section 8(1)(j) after DPDP, IT Act section 43A repeal, SPDI Rules status, DPDP penalties and the Data Protection Board, DPDP vs GDPR, and any Indian privacy policy, consent flow, DPA or vendor contract review. Also reach for it when auditing a product or store that collects personal data from users in India.
---

# DPDP analysis

Analyse anything against the **Digital Personal Data Protection Act, 2023** and the
**DPDP Rules, 2025**, from a one-line question to a full compliance audit.

## Hard rules

1. **Never state a DPDP proposition without a section or rule anchor.** If you cannot point to
   `s.X` or `Rule Y`, you do not know it. Say so.
2. **Quote from `references/act-full-text.md` only.** That file is verbatim Gazette text. Do not
   quote the Act from memory, and do not paraphrase a quotation into quotation marks.
3. **Rules are secondary.** `references/rules-2025.md` was assembled from PIB and cross-checked
   secondary sources, not from the Gazette. Every output that relies on a Rule must carry the line:
   *verify against the notified Gazette text before external use.*
4. **Penalties are ceilings.** Every Schedule figure is "may extend to", gated on the Board finding
   the breach "significant" under s.33(1). Never present one as a fine that will be levied.
5. **Check commencement before saying anything is binding.** s.1(2) permits staggered commencement.
   Substantive Rules commence **14 May 2027**; Rule 4 Consent Managers **14 November 2026**; Board
   machinery has been live since **14 November 2025**.
6. **Do not import GDPR.** No sensitive-data category, no legitimate interests, no portability, no
   right against automated decisions, no compensation to individuals. Asserting any of these is the
   most common way to get DPDP wrong. See `references/doctrine.md` section 13.
7. **This is analysis, not legal advice.** Say so once, at the end, briefly. Do not hedge every
   sentence.

## How to work

### Step 1: load what you need
| Need | Read |
|---|---|
| Any answer at all | `references/doctrine.md` |
| Finding the right provision | `references/section-index.md` |
| Quoting the law | `references/act-full-text.md` |
| Anything about Rules, timelines, breach clocks, retention, SDF duties, children's consent mechanics | `references/rules-2025.md` |
| Auditing an org, product, notice or contract | `references/compliance-checklist.md` |
| Writing up a formal assessment | `assets/report-template.md` |

For a quick factual question, `doctrine.md` plus `section-index.md` is usually enough. Only open
`act-full-text.md` when you are about to quote.

### Step 2: walk the five gates
Never skip and never reorder. Full detail in `doctrine.md` section 1.

1. **Is it digital personal data?** s.2(t), s.2(n), s.3(a).
2. **Does the Act apply?** s.3(a) India, s.3(b) extraterritorial only for goods/services offering,
   s.3(c) carve-outs.
3. **Who is who?** Data Fiduciary determines purpose **and** means (s.2(i)). SDF only if
   **notified** (s.10(1)).
4. **What is the lawful basis?** Only two exist: consent under s.6, or a **named clause** of the
   closed s.7 list. There is no third option.
5. **Which obligations attach, and does s.17 exempt anything?** Remember s.8(1) and s.8(5) survive
   every s.17(1) exemption.

### Step 3: answer at the right size
- **A question** gets a direct answer, the anchor, and the one trap that applies. Two to six lines.
- **A review** (notice, consent flow, contract, product) gets findings from
  `compliance-checklist.md`, ranked by Schedule ceiling then by effort, each anchored and each with
  a concrete fix.
- **A full assessment** gets `assets/report-template.md`.

Always include a short **"what is NOT a problem"** note in reviews. Telling a client they do not
need portability machinery or a DPO saves them more than another finding does.

### Step 4: separate the known from the open
End any substantive output by naming what is still open. As things stand, no Significant Data
Fiduciary has been notified, no country is on the s.16(1) restricted list, no startup relief has
been notified under s.17(3), the Rule 13(4) localisation committee has not published its
categories, "significant" in s.33(1) is undefined, and there is no Board jurisprudence. That is not
a hedge, it is the actual state of the law, and clients need it in writing.

## The facts most often gotten wrong

Keep these loaded. They decide more answers than anything else.

| | |
|---|---|
| Lawful bases | **Two.** Consent (s.6), or the closed s.7 list. No legitimate interests. |
| Sensitive personal data | **Does not exist** under DPDP. Health, biometric, financial, caste get no special tier. |
| Child | **Under 18** (s.2(f)). Not 13, not 16. |
| Ads to children | **Banned outright** (s.9(3)). Consent does not cure it. s.9(2) well-being bar is never exemptible. |
| Breach notification | **No threshold.** Board **and every affected individual** (s.8(6)). Individuals **without delay**; Board detailed report within **72 hours** (Rule 7). Includes **loss of access**. |
| DPO | **Only notified SDFs** (s.10(2)(a)). Everyone else publishes a contact person (s.8(9), Rule 9). |
| Localisation | **Not in the Act.** s.16 is a negative list. Rule 13(4) localises specified categories for **SDFs only**. Sectoral rules bind independently (s.16(2)). |
| Individual remedy | **None.** Penalties go to the Consolidated Fund (s.34). Civil courts barred (s.39). IT Act s.43A **omitted** (s.44(2)(a)). |
| Rights absent | Portability, objection, automated-decision protection. |
| Duties on individuals | **Yes**, s.15, penalty up to **Rs 10,000**. Unusual internationally. |
| Burden of proof | On the **Data Fiduciary** to prove valid notice and consent (s.6(10)). |
| Languages | Notice and consent must be available in **English or any Eighth Schedule language**, 22 in all (s.5(3), s.6(3)). |
| Appeal | **TDSAT**, within **60 days** (s.29). |
| Blocking | After **two or more** penalties, the Centre may order blocking (s.37). |
| Criminal liability | **None** anywhere in the Act. |
| RTI | s.8(1)(j) replaced with a flat personal-information exemption; public-interest carve-in deleted (s.44(3)). |

## Penalty ceilings (the Schedule)

| Breach | Ceiling |
|---|---|
| s.8(5) reasonable security safeguards | **Rs 250 crore** |
| s.8(6) breach notification | **Rs 200 crore** |
| s.9 children | **Rs 200 crore** |
| s.10 SDF obligations | **Rs 150 crore** |
| s.15 Data Principal duties | **Rs 10,000** |
| s.32 voluntary undertaking | Ceiling of the underlying breach |
| Anything else | **Rs 50 crore** |

Mitigation lives in **s.33(2)(a) to (g)**. Argue (e) prompt effective mitigation, (f)
proportionality, and (g) impact on the person, in any real matter.

## Output style

Plain, direct, sourced. Tables for anything comparative. Section anchors inline, in the form
`s.8(6)` and `Rule 7(2)`. No em-dashes. No hedging padding. If the honest answer is "the Rules
govern this and you must check the current notified text", give that answer and stop.
