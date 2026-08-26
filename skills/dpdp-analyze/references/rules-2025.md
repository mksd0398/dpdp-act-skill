# The Digital Personal Data Protection Rules, 2025

## Provenance and confidence warning, read this first

`act-full-text.md` is **verbatim from the Gazette** and can be quoted directly.

**This file is not.** It was assembled from the PIB release and multiple secondary sources
cross-checked against each other. Rule numbering, headings, the phased dates, and the
substance below were corroborated across independent sources, and quoted sub-rule text is
reproduced as those sources give it. Treat it as **reliable working knowledge, not as a citable
primary source**.

**Before quoting any Rule to a client, in a legal opinion, or in anything that leaves the
building, verify against the notified Gazette text at meity.gov.in / egazette.gov.in.** Say so
in the output. Where this file and a client's own copy of the Rules disagree, the Gazette wins.

Where a specific point below is contested between sources, it is flagged inline.

---

## 1. Notification and phased commencement

- Notified by the **Ministry of Electronics and Information Technology (MeitY)** on
  **13 November 2025**, published **14 November 2025**.
- **23 Rules and 7 Schedules.**
- MeitY simultaneously notified commencement of the Act's provisions in three tranches, keyed to
  **14 November 2025**, **14 November 2026**, and **14 May 2027**.

| Tranche | Effective | What comes into force |
|---|---|---|
| Immediate | **14 November 2025** | Rules 1, 2, and 17 to 21. Definitions, plus the machinery to constitute and run the Data Protection Board (appointment of Chairperson and Members, salary and service terms, Board meetings, digital-office functioning, Board staff). |
| 12 months | **14 November 2026** | **Rule 4**, registration and obligations of Consent Managers. |
| 18 months | **14 May 2027** | **Rules 3, 5 to 16, and 22 to 23.** This is the tranche that carries essentially every substantive business obligation: notice, security safeguards, breach intimation, retention and erasure, contact-person publication, children's consent, SDF duties, Data Principal rights machinery, transfers, research exemption, appeals, and calling for information. |

**The practical consequence, and the thing to tell every client:** as of the 2026 tranche, the
operative compliance duties for ordinary Data Fiduciaries are **not yet enforceable**. The date
that matters for a build plan is **14 May 2027**. Do not describe Rules 3 or 5 to 16 as currently
binding. Do describe them as the fixed target the programme must hit.

Note the sequencing problem worth flagging in advice: Consent Manager registration bites at
14 November 2026, though the Board that registers them has to be constituted first.

---

## 2. Rule map

| Rule | Heading |
|---|---|
| 1 | Short title and commencement |
| 2 | Definitions |
| 3 | Notice given by Data Fiduciary to Data Principal |
| 4 | Registration and obligations of Consent Manager |
| 5 | Processing of personal data for provision or issue of subsidy, benefit, service, certificate, licence or permit by State and its instrumentalities |
| 6 | Reasonable security safeguards |
| 7 | Intimation of personal data breach |
| 8 | Time period for specified purpose to be deemed as no longer being served |
| 9 | Contact information of person to answer questions about processing |
| 10 | Verifiable consent for processing of personal data of child |
| 11 | Verifiable consent for processing of personal data of person with disability who has lawful guardian |
| 12 | Exemptions from certain obligations applicable to processing of personal data of child |
| 13 | Additional obligations of Significant Data Fiduciary |
| 14 | Rights of Data Principals |
| 15 | Transfer of personal data outside the territory of India |
| 16 | Exemption from Act for research, archiving or statistical purposes |
| 17 | Appointment of Chairperson and other Members |
| 18 | Salary, allowances and other terms and conditions of service |
| 19 | Procedure for meetings of Board |
| 20 | Functioning of Board as digital office |
| 21 | Terms and conditions of appointment and service of officers and employees |
| 22 | Appeal to Appellate Tribunal |
| 23 | Calling for information from Data Fiduciary or intermediary |

| Schedule | Subject |
|---|---|
| First | Conditions of registration and obligations of Consent Manager |
| Second | Standards for processing personal data by the State |
| Third | Class of Data Fiduciaries, purposes, and time period (the retention table) |
| Fourth | Classes of Data Fiduciaries with exemptions (children's-data exemptions) |
| Fifth | Terms and conditions of service of Chairperson and Members |
| Sixth | Terms and conditions of appointment of Board officers and employees |
| Seventh | Purpose and authorised person (for calling for information) |

---

## 3. Rule 3, notice

The notice must—

(a) **be presented and be understandable independently** of any other information the Data
Fiduciary has made or may make available. This kills the practice of burying privacy terms inside
a general T&C document.

(b) give, **in clear and plain language**, a fair account of the details needed for specific and
informed consent, including at minimum:
  (i) an **itemised description** of the personal data; and
  (ii) the specified purpose or purposes, and a **specific description of the goods or services**
  to be provided or the uses to be enabled by the processing.

(c) give the **particular communication link** for the website or app, and a description of other
means, by which the Data Principal may:
  (i) **withdraw consent, with ease comparable to giving it**;
  (ii) exercise her rights under the Act; and
  (iii) **make a complaint to the Board**.

**Build implications.** A standalone consent notice screen. A machine-readable itemised data
inventory per consent purpose. Purpose strings tied to concrete goods or services, not to
categories like "improving our services". A one-click withdrawal link, live at the URL you
declared. Plus the Eighth Schedule language option, which comes from s.5(3) and s.6(3) of the Act.

---

## 4. Rule 4 and the First Schedule, Consent Managers

- Must be **incorporated as a company in India**.
- Must have **minimum net worth of Rs 2 crore**. *(Corroborated across sources; verify the figure
  in the First Schedule, Part A before quoting it.)*
- Must have sufficient **technical, operational and financial capacity**, and sound financial
  condition and general character of management.
- Registers with the **Board**. Obligations run **to the Data Principal**, per s.6(8) of the Act.
- Effective **14 November 2026**.

---

## 5. Rule 6, reasonable security safeguards

This is the rule that turns Act s.8(5) from an abstraction into an audit checklist. A Data
Fiduciary must protect personal data in its possession or control, including processing done on
its behalf by a Data Processor, by taking reasonable security safeguards **which shall include, at
the minimum**:

(a) **appropriate data security measures**, such as securing personal data through **encryption,
obfuscation, masking, or the use of virtual tokens** mapped to that personal data;

(b) **appropriate measures to control access** to the computer resources used by the Data
Fiduciary or Data Processor, wherever applicable;

(c) **visibility on access**, through appropriate **logs, monitoring and review**, enabling
detection of unauthorised access, its investigation, and remediation to prevent recurrence;

(d) **reasonable measures for continued processing** where confidentiality, integrity or
availability is compromised by destruction or loss of access, **such as data backups**;

(e) **retain such logs and personal data for a period of one year**, to enable detection,
investigation, remediation and continued processing, unless another law in force requires
otherwise;

(f) **appropriate provision in the contract** between the Data Fiduciary and the Data Processor,
wherever applicable, for taking reasonable security safeguards;

(g) **appropriate technical and organisational measures** to ensure effective observance of
security safeguards.

Rule 6(2): "computer resource" takes its Information Technology Act, 2000 meaning.

**This is a floor, not a ceiling.** "At the minimum" means an incident where you did all seven can
still be a s.8(5) breach. But missing any one of the seven is close to a self-proving breach, with
a Rs 250 crore ceiling behind it.

**Note the tension in (e):** a mandatory **one-year log retention** sits against the s.8(7) erasure
duty. Reconcile them by scoping (e) to access logs and the associated personal data needed for
security forensics, and document that reasoning.

---

## 6. Rule 7, intimation of personal data breach

**Two audiences, two clocks.**

**To each affected Data Principal, Rule 7(1): without delay**, through her registered contact or
user account, describing:
- the **nature, extent and timing** of the breach;
- the **likely consequences** relevant to her;
- **mitigation measures** implemented or being implemented;
- **safety measures she can take** to protect her interests;
- **contact details** of a person able to answer queries.

**To the Board, Rule 7(2): two stages.**
1. **Without delay**, on becoming aware: a description of the breach, including its nature, extent,
   timing and location of occurrence, and the likely impact.
2. **Within 72 hours** of becoming aware (or a longer period the Board allows on written request),
   an updated and detailed report covering:
   - broad facts, and the events, circumstances and reasons leading to the breach;
   - measures implemented or proposed to mitigate risk;
   - findings regarding the person who caused the breach;
   - remedial measures taken to prevent recurrence;
   - a report on the intimations given to affected Data Principals.

**Points to hammer in advice:**
- **No harm or materiality threshold**, from Act s.8(6). Every breach as defined in s.2(u) is in
  scope, including **loss of access**, so ransomware and serious availability incidents qualify.
- The **individual notice is "without delay"**, not 72 hours. Do not let a client build a process
  that batches user notification behind the regulator report.
- The 72-hour clock runs from **becoming aware**, and the Board's report requires you to have
  already identified the cause and the person responsible, which is a demanding forensic ask.

---

## 7. Rule 8 and the Third Schedule, retention and erasure

- **Rule 8(1):** a Data Fiduciary of a class, processing for the corresponding purposes specified
  in the **Third Schedule**, shall **erase** the personal data once the specified period has
  elapsed since the Data Principal last approached it or exercised her rights, **unless retention
  is necessary for compliance with any law in force**.
- **Rule 8(2):** give the Data Principal notice **at least forty-eight hours before** completion of
  that period, so she can prevent erasure by approaching the Fiduciary or exercising a right.
- **Rule 8(3):** retain personal data, **associated traffic data and other logs** of the processing
  for a **minimum of one year** from the date of such processing.

**Third Schedule classes and periods** *(corroborated across sources; verify exact wording and
thresholds against the Gazette before quoting):*

| Class of Data Fiduciary | Period |
|---|---|
| **E-commerce entity** with not less than **two crore** registered users in India | **3 years** |
| **Online gaming intermediary** with not less than **fifty lakh** registered users in India | **3 years** |
| **Social media intermediary** with not less than **two crore** registered users in India | **3 years** |

The three-year clock runs from the Data Principal's **last approach** to the Fiduciary for the
specified purpose, or her last exercise of a right, whichever is later.

**Scope note:** the Third Schedule fixes a **deemed** expiry only for these classes and purposes.
For everyone else, s.8(7) still applies on its own terms: erase on withdrawal, or when it is
reasonable to assume the specified purpose is no longer served.

---

## 8. Rules 10 and 11, verifiable consent for children and persons with disability

**Rule 10(1):** the Data Fiduciary must adopt appropriate technical and organisational measures to
ensure **verifiable consent of the parent** is obtained before processing a child's personal data,
and must **observe due diligence** to check that the person identifying herself as the parent is an
**adult who is identifiable if required** in connection with any law in force in India, by
reference to:
- (a) **reliable details of identity and age already held** by the Data Fiduciary; or
- (b) details of identity and age **voluntarily provided**, either
  - (i) by the individual, or
  - (ii) through a **virtual token mapped to such details, issued by an authorised entity**.

**Rule 10(2)** definitions: "adult" is a person who has completed eighteen years. "Authorised
entity" is an entity entrusted by law or by the Central or a State Government with issuing identity
and age details or a virtual token mapped to them, or a person appointed or permitted by such an
entity, and includes details made available and verified by a **Digital Locker service provider**
(DigiLocker), an intermediary notified by the Central Government under the IT Act, 2000.

**Rule 11** applies the equivalent mechanism to a **person with disability who has a lawful
guardian**, with the guardian verified as duly appointed under the relevant disability or
guardianship law.

**Rule 12** and the **Fourth Schedule** carve out classes of Data Fiduciaries and purposes exempt
from s.9(1) and s.9(3), under the Act's s.9(4) power. This is where healthcare providers,
educational institutions, childcare providers and certain State functions typically sit, in each
case limited to specified purposes such as health services, education, transport safety tracking,
or issuing a subsidy or benefit. **Verify the Fourth Schedule directly before relying on any
exemption for a client.**

**Remember what Rule 12 cannot do:** s.9(4) permits exemption only from s.9(1) and s.9(3). The
s.9(2) prohibition on processing likely to cause **detrimental effect on a child's well-being** is
never exemptible.

---

## 9. Rule 13, Significant Data Fiduciary obligations

*(One secondary source numbers these obligations Rule 12; the corroborated numbering is Rule 13.
Verify before citing the rule number.)*

**(1)** Once in every period of **twelve months** from the date it is notified as an SDF, or
included in a notified class, undertake a **Data Protection Impact Assessment and an audit** to
ensure effective observance of the Act and Rules.

**(2)** Cause the person carrying out the DPIA and audit to **furnish a report to the Board**
containing significant observations.

**(3)** Observe **due diligence to verify that technical measures, including algorithmic
software**, adopted for hosting, display, uploading, modification, publishing, transmission,
storage, updating or sharing of personal data are **not likely to pose a risk to the rights of Data
Principals**. This is India's algorithmic accountability hook, and it is unusual: the Act itself
contains no automated-decision provision, so this duty exists only for SDFs and only via the Rules.

**(4)** Undertake measures to ensure that personal data **specified by the Central Government**, on
the recommendations of a **committee constituted by it**, is processed subject to the restriction
that **the personal data and the traffic data pertaining to its flow are not transferred outside
the territory of India**.

**(5)** Defines "committee" for the purposes of the rule.

**This is where localisation actually lives.** The Act's s.16 is a negative list and imposes no
localisation. Rule 13(4) creates a **targeted, committee-driven localisation mandate that applies
only to notified SDFs and only to categories of data the Government specifies**. Correct advice:
"DPDP does not mandate localisation generally; if your client is notified an SDF, Rule 13(4) may
localise specified categories once the committee acts; and sectoral regulators such as the RBI
already localise independently under Act s.16(2)."

---

## 10. Rule 14, rights of Data Principals

**(1)** The Data Fiduciary and Consent Manager must **prominently publish on its website or app**:
  (a) the **means** by which a Data Principal may make a request to exercise her rights; and
  (b) the **particulars**, if any, such as a username or other identifier, needed to identify her.

**(2)** She exercises rights by making a request to the Data Fiduciary **to whom she has previously
given consent**, using the published means and particulars.

**(3)** The Data Fiduciary and Consent Manager must **publish the period within which they will
respond to grievances**, being a **reasonable period not exceeding ninety days**, and must
implement appropriate technical and organisational measures to meet it. *(Verify the ninety-day
figure against the Gazette; some commentary reports different numbers.)*

**(4)** She may **nominate one or more individuals** under Act s.14, in accordance with the terms of
service and applicable law.

**(5)** "Identifier" means any sequence of characters issued by the Data Fiduciary to identify her,
such as a customer ID, enrolment ID, email address, mobile number or licence number.

**Read Rule 14(2) against Act s.11(1) and s.12(1).** Both are worded around processing where she
has previously given consent, including s.7(a) consent. Rights machinery under DPDP is narrower
than a GDPR DSAR programme, and advice should not over-build it.

---

## 11. Rule 15, transfers outside India

Personal data processed by a Data Fiduciary under the Act **may be transferred outside the
territory of India**, subject to the restriction that the Data Fiduciary shall meet such
requirements as the **Central Government may, by general or special order, specify** in respect of
making that personal data available to **any foreign State**, or to any person or entity **under
the control of, or any agency of, such a State**.

Reading:
- Confirms the **permissive default**. There is no adequacy regime, no SCCs, no transfer impact
  assessment under DPDP.
- The specific concern addressed is **onward availability to foreign governments**, not commercial
  transfer as such.
- **Act s.16(1)** negative-list notifications remain the mechanism for restricting named countries,
  and **s.16(2)** preserves stricter sectoral law.

---

## 12. Other rules in brief

- **Rule 5 and the Second Schedule:** standards for State processing under Act s.7(b), covering
  lawful and transparent use, purpose limitation, accuracy, security, retention, accountability and
  a grievance mechanism.
- **Rule 9:** publish the **business contact information** of the DPO where applicable, or of the
  person who can answer questions about processing, **on the website or app and in every response**
  to a communication from a Data Principal exercising her rights. This is the Act s.8(9) duty made
  concrete, and it applies to **non-SDFs too**.
- **Rule 16:** the Act does not apply to processing **necessary for research, archiving or
  statistical purposes** if carried on in accordance with the **standards in the Second Schedule**.
- **Rules 17 to 21:** Board constitution, search-cum-selection process, service terms, meetings, and
  digital-office functioning. Live since 14 November 2025.
- **Rule 22:** appeals to TDSAT, filed **digitally**, with the Tribunal regulating its own procedure.
- **Rule 23 and the Seventh Schedule:** the Central Government may require a Data Fiduciary or
  intermediary to furnish information for a specified purpose, through an authorised person, with a
  confidentiality restriction where disclosure would prejudice India's sovereignty and integrity or
  security of the State.

---

## 13. What is still missing even with the Rules

- **No SDF has been notified** by class or by name under Act s.10(1) as at the last verification.
  Until that notification exists, no company is legally an SDF, and Rule 13 binds nobody.
- **No country has been notified** as restricted under Act s.16(1).
- **No startup relief** notified under Act s.17(3).
- **No State instrumentality** exempted under Act s.17(2)(a) by public notification.
- **No s.9(5) verifiably-safe age** notified for any Data Fiduciary.
- The **Rule 13(4) committee** and its list of localised data categories.
- **"Significant" in s.33(1) remains undefined**, and there is no Board jurisprudence, so penalty
  exposure cannot be modelled from precedent.

Always state which of these are still open when giving a client a risk picture. The honest answer
to "what is my exposure" in the current posture is that the ceilings are known, the triggers are
known, and the enforcement practice is entirely unknown.
