# DPDP compliance checklist

The working checklist for auditing an organisation, a product, a contract, or a privacy notice.
Every item carries its statutory anchor. Do not raise a finding without one.

Scoring convention used in reports:
- **GAP** = a specific provision is not met, with the evidence stated.
- **RISK** = arguably met, but the position is weak or undocumented and would not survive s.6(10)
  burden of proof or a Board inquiry.
- **OPEN** = cannot be determined without a Rule, a notification, or a fact the client must supply.
- **OK** = met, with the evidence stated.

---

## A. Scoping (do this before anything else)

| # | Question | Anchor |
|---|---|---|
| A1 | Is any personal data processed in digital form, or collected on paper and digitised later? | s.2(n), s.3(a) |
| A2 | Is the entity outside India? If so, is the processing connected to offering goods or services to Data Principals in India? Mere behaviour monitoring is **not** a trigger. | s.3(b) |
| A3 | Does any carve-out apply: purely personal or domestic processing, or data the individual herself made public? | s.3(c) |
| A4 | For each processing activity, is the entity a Data Fiduciary (determines purpose **and** means) or a Data Processor? Map joint arrangements. | s.2(i), s.2(k) |
| A5 | Has the entity been **notified** as a Significant Data Fiduciary? If not, s.10 does not apply. Do not assume. | s.2(z), s.10(1) |
| A6 | Are any children (under 18) or persons with disability having a lawful guardian in the user base? | s.2(f), s.2(j)(ii), s.9 |
| A7 | Which s.17 exemptions are in play, and does the client understand that s.8(1) and s.8(5) survive all of them? | s.17(1) |
| A8 | Which sectoral regulator also sits over this data: RBI, IRDAI, SEBI, TRAI, CERT-In, NHA, UIDAI? DPDP does not displace them. | s.16(2), s.38(1) |

---

## B. Lawful basis and purpose

| # | Question | Anchor |
|---|---|---|
| B1 | Is there a written **record of processing activities** mapping each purpose to its lawful basis? Not required by name, but without it s.6(10) is unanswerable. | s.4, s.6(10) |
| B2 | For each purpose, is the basis consent or a **named** s.7 clause? Reject any answer of "legitimate interest". | s.4(1), s.7 |
| B3 | Where s.7(a) is claimed, did the Data Principal actually **volunteer** the data for **that** purpose, and has she not indicated non-consent? | s.7(a) |
| B4 | Where s.7(i) employment is claimed, is the use genuinely employment or loss/liability protection, rather than marketing or surveillance dressed up? | s.7(i) |
| B5 | Is each purpose a "lawful purpose", meaning not expressly forbidden by law? | s.4(2) |
| B6 | Is any purpose broader than what the collected data set supports, so consent would be read down? | s.6(1) and Illustration |

---

## C. Notice

| # | Question | Anchor |
|---|---|---|
| C1 | Does a notice accompany or **precede** every consent request? | s.5(1) |
| C2 | Does it state the personal data and the purpose, with an **itemised description** of the data? | s.5(1)(i), Rule 3(b)(i) |
| C3 | Does it describe the **specific goods or services** or uses enabled, rather than a vague category? | Rule 3(b)(ii) |
| C4 | Does it explain how to **withdraw consent** (s.6(4)) and how to raise a **grievance** (s.13)? | s.5(1)(ii) |
| C5 | Does it explain how to **complain to the Board**? Most notices miss this one. | s.5(1)(iii), Rule 3(c)(iii) |
| C6 | Is it **standalone and understandable independently** of the T&C or any other document? | Rule 3(a) |
| C7 | Is it offered in **English or any Eighth Schedule language**, at the user's option? 22 languages. | s.5(3) |
| C8 | Does it give the **particular communication link** to the site or app for exercising each of these? | Rule 3(c) |
| C9 | For consent obtained **before** commencement, has a retrospective notice gone out, or is one planned? | s.5(2) |

---

## D. Consent mechanics

| # | Question | Anchor |
|---|---|---|
| D1 | Free, specific, informed, unconditional, unambiguous, with a **clear affirmative action**? No pre-ticked boxes, no consent by continued use, no bundling. | s.6(1) |
| D2 | Is consent **granular per purpose**, or one blanket tick? | s.6(1) |
| D3 | Is service access **conditioned** on consent to unnecessary processing? That defeats "unconditional" and "free". | s.6(1) |
| D4 | Any waiver, indemnity or limitation clause riding on the consent that would be void? | s.6(2) and Illustration |
| D5 | Is the consent request in **clear and plain language**, with the language option, and with DPO or authorised-person contact details? | s.6(3) |
| D6 | Is **withdrawal as easy as giving**? Compare the click counts honestly: one-tap in, versus an email to support, is a finding. | s.6(4), Rule 3(c)(i) |
| D7 | On withdrawal, does the system **cease processing** and **propagate the stop to every Processor** within a reasonable time? | s.6(6) |
| D8 | Are **consent artefacts logged**: timestamp, purpose string, notice version, language served, method, and withdrawal events? | s.6(10) |
| D9 | If a Consent Manager is used, is it registered with the Board, and is the accountability-to-the-Data-Principal relationship reflected in contracts? | s.6(7)-(9), Rule 4 |

---

## E. Security, breach and vendors

| # | Question | Anchor |
|---|---|---|
| E1 | **Encryption, obfuscation, masking, or virtual tokens** applied to personal data? | Rule 6(1)(a) |
| E2 | **Access controls** on the computer resources used by the Fiduciary and every Processor? | Rule 6(1)(b) |
| E3 | **Logs, monitoring and review** giving visibility on who accessed personal data? | Rule 6(1)(c) |
| E4 | **Backups and continuity** measures for loss of confidentiality, integrity or availability? | Rule 6(1)(d) |
| E5 | Are logs and the associated personal data retained **one year**? Reconcile with s.8(7) erasure and document the reconciliation. | Rule 6(1)(e) |
| E6 | Does **every Processor contract** contain a security-safeguards clause? | s.8(2), Rule 6(1)(f) |
| E7 | Is there a **valid written contract** with every Processor for goods/services activity? Not a PO, not a click-through, if that will not survive scrutiny. | s.8(2) |
| E8 | Does the breach playbook notify **each affected Data Principal without delay**, separately from the Board timeline? | s.8(6), Rule 7(1) |
| E9 | Does it deliver the Board's **initial intimation without delay** and the **detailed 72-hour report**, with cause and responsible-person findings? | Rule 7(2) |
| E10 | Does the playbook treat **loss of access** (ransomware, destructive incidents) as a notifiable personal data breach? | s.2(u) |
| E11 | Has anyone told the client there is **no harm threshold**? Most breach plans imported from GDPR have one. | s.8(6) |
| E12 | Are **onward Processors and sub-processors** in the incident escalation chain? | s.8(1), s.8(5) |

---

## F. Retention and erasure

| # | Question | Anchor |
|---|---|---|
| F1 | Is there a **retention schedule** mapping purpose to trigger to period to disposal method? | s.8(7) |
| F2 | Does erasure fire on **withdrawal of consent**, and on **purpose exhaustion**, whichever is earlier? | s.8(7)(a) |
| F3 | Does erasure **propagate to Processors**, including backups and analytics copies? | s.8(7)(b) |
| F4 | Where retention continues, is the **specific legal obligation** cited, per activity? | s.8(7) opening words |
| F5 | Does the client fall in a **Third Schedule class** (large e-commerce, online gaming, social media)? If so, apply the deemed period and the erasure workflow. | Rule 8(1) |
| F6 | Is the **48-hour pre-erasure notice** implemented for those classes? | Rule 8(2) |
| F7 | Is the **one-year minimum** for personal data, associated traffic data and processing logs honoured? | Rule 8(3) |

---

## G. Children and persons with disability

| # | Question | Anchor |
|---|---|---|
| G1 | Is there **age assurance** at the point of collection? | s.9(1) |
| G2 | Is **verifiable parental consent** obtained, with due-diligence checks that the person is an identifiable adult, via held identity details, voluntarily provided details, or a virtual token from an authorised entity or DigiLocker? | s.9(1), Rule 10 |
| G3 | For a person with disability having a lawful guardian, is **guardian verification** implemented? | s.2(j)(ii), s.9(1), Rule 11 |
| G4 | Is any processing likely to cause **detrimental effect on a child's well-being**? Note this is **never exemptible**. | s.9(2), s.9(4) |
| G5 | Is **tracking, behavioural monitoring, or targeted advertising** switched off for child users, including analytics SDKs, ad pixels, retargeting and lookalike audiences? Consent does not cure this. | s.9(3) |
| G6 | Does the client rely on a **Fourth Schedule** exemption? Verify the class and the specific purpose against the Gazette. | s.9(4), Rule 12 |
| G7 | Has the client wrongly assumed an age of 13 or 16? | s.2(f) |

---

## H. Significant Data Fiduciary (only if notified)

| # | Question | Anchor |
|---|---|---|
| H1 | **DPO** appointed, **based in India**, an individual, **responsible to the board of directors** or similar governing body, and named as the grievance contact? | s.10(2)(a) |
| H2 | **Independent data auditor** appointed? Independent of the compliance function being audited. | s.10(2)(b) |
| H3 | **DPIA and audit every twelve months** from designation? | s.10(2)(c), Rule 13(1) |
| H4 | Is the **report of significant observations furnished to the Board**? | Rule 13(2) |
| H5 | **Algorithmic due diligence**: has the client verified that its technical measures, including algorithmic software used for hosting, display, upload, publishing, transmission, storage or sharing, do not risk Data Principal rights? | Rule 13(3) |
| H6 | Any **localisation** obligation triggered for Government-specified categories, including traffic data on the flow? | Rule 13(4) |

---

## I. Rights machinery

| # | Question | Anchor |
|---|---|---|
| I1 | Are the **means and required particulars** for exercising rights **prominently published** on the website or app? | Rule 14(1) |
| I2 | Can the client actually produce a **s.11 access response**: summary of data, processing activities, and the identities of Fiduciaries and Processors it was shared with plus a description of what was shared? Most cannot produce the sharing list. | s.11(1) |
| I3 | Is the **law-enforcement sharing carve-out** correctly applied and not over-applied? | s.11(2) |
| I4 | Is there a **correction, completion and updating** workflow that actually writes back to downstream systems? | s.12(2) |
| I5 | Is there an **erasure** workflow with the "necessary for the specified purpose or for legal compliance" test applied per record, not per system? | s.12(3) |
| I6 | Is a **grievance mechanism** live, with the response period **published**, and within a reasonable period not exceeding ninety days? | s.8(10), s.13, Rule 14(3) |
| I7 | Is the **nomination** facility available? | s.14, Rule 14(4) |
| I8 | Is the **business contact information** of the DPO or answering person published, and included in every response to a rights communication? | s.8(9), Rule 9 |
| I9 | Has the client been told there is **no portability right** and **no right against automated decisions**, so it should not over-build? | s.11 to s.14 |

---

## J. Cross-border and governance

| # | Question | Anchor |
|---|---|---|
| J1 | Where does the data physically go? Any country on a **s.16(1) notified restriction list**? | s.16(1) |
| J2 | Does a **sectoral localisation rule** bind independently (RBI payment data, insurance, telecom, CERT-In)? | s.16(2) |
| J3 | Any arrangement making data available to a **foreign State** or a State-controlled entity? | Rule 15 |
| J4 | Is accountability documented at board level, given s.8(1) makes contrary agreements irrelevant? | s.8(1) |
| J5 | Where the client is a **Processor for foreign clients under a foreign contract**, has the s.17(1)(d) exemption been properly claimed, with s.8(1) and s.8(5) still honoured? | s.17(1)(d) |

---

## K. Documents to request in any audit

1. Privacy notice and every consent screen, in every language served.
2. Consent log schema and a sample export.
3. Record of processing activities, purpose to lawful basis map.
4. Data inventory and data flow diagrams, including third-country flows.
5. All Data Processor contracts and sub-processor lists.
6. Retention schedule and the erasure runbook.
7. Incident response plan, with the DPDP notification annexes.
8. Security architecture: encryption at rest and in transit, access control model, logging design.
9. Age assurance and parental-consent design, if any child users.
10. Grievance policy, published response period, and the last twelve months of grievance logs.
11. SDF designation notification, DPO appointment letter, auditor engagement, last DPIA and audit report, if applicable.
12. Any sectoral regulatory correspondence on data handling.

---

## L. Remediation priority order

Rank findings by the Schedule ceiling behind them, then by how quickly the Board could see it.

1. **s.8(5) security safeguards**, Rule 6 minimums. Ceiling Rs 250 crore. Highest exposure, and a
   breach makes the gap self-evident.
2. **s.8(6) and Rule 7 breach readiness.** Ceiling Rs 200 crore. Cheap to fix, catastrophic to miss,
   and it is the failure the Board hears about first because the breach itself brings the file.
3. **s.9 children.** Ceiling Rs 200 crore. Often a single ad-SDK configuration.
4. **s.10 and Rule 13 SDF duties**, if notified. Ceiling Rs 150 crore.
5. **Everything else**, Schedule item 7. Ceiling Rs 50 crore. Notice, consent, retention, rights.

Then re-rank by effort. A tracking pixel disabled for under-18 accounts in an afternoon outranks a
six-month consent re-platforming, even though both sit at the same ceiling.
