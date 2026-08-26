# DPDP doctrine: how this statute actually works

Read this before answering any DPDP question. It encodes the structural moves that decide most
answers, and the misreadings that produce wrong advice. Every claim here is anchored to a section
in `act-full-text.md`. If a claim is not anchored, do not assert it.

---

## 1. The five gates

Almost every DPDP question resolves by walking these in order. Do not skip a gate.

**Gate 1: Is it digital personal data?**
- "Personal data" = any data **about an individual who is identifiable by or in relation to such
  data** (s.2(t)). Wide. No "identifiability threshold" test in the Act.
- The Act only bites on **digital** personal data (s.2(n), s.3(a)). Paper records collected and kept
  on paper are outside it. Paper **digitised subsequently** is inside it (s.3(a)(ii)).
- Truly anonymised data has no identifiable individual, so it falls out at this gate. The Act does
  not define "anonymisation", so this is an evidentiary argument, not a safe harbour.

**Gate 2: Does the Act apply at all?**
- Inside India: yes, if collected digitally or digitised later (s.3(a)).
- Outside India: only if the processing is **in connection with any activity related to offering of
  goods or services to Data Principals within the territory of India** (s.3(b)).
- Carve-outs (s.3(c)): purely personal or domestic processing by an individual; and personal data
  made publicly available by the Data Principal herself, or by someone under a legal obligation to
  publish it.

**Gate 3: Who is who?**
- **Data Fiduciary** = determines purpose *and* means (s.2(i)). Note the conjunctive "and".
- **Data Processor** = processes on behalf of a Data Fiduciary (s.2(k)).
- **Data Principal** = the individual; for a child, includes the parent or lawful guardian; for a
  person with disability, includes her lawful guardian acting on her behalf (s.2(j)).
- **Significant Data Fiduciary** = only exists once the Central Government **notifies** you or your
  class (s.2(z), s.10(1)). You cannot self-classify into it and you cannot be one by size alone.

**Gate 4: What is the lawful basis?**
There are exactly **two** (s.4(1)):
- (a) **consent** meeting s.6(1); or
- (b) **certain legitimate uses**, meaning only the closed list in s.7(a) to s.7(i).

And the purpose must be a "lawful purpose", defined as any purpose **not expressly forbidden by
law** (s.4(2)).

**Gate 5: Which obligations attach, and is anything exempted?**
- Baseline Data Fiduciary duties: s.5 notice, s.6 consent mechanics, s.8 general obligations.
- Child-specific: s.9.
- SDF-only: s.10.
- Then check s.17 exemptions, which is where a lot of real-world answers land.

---

## 2. The consent architecture

**s.6(1) five adjectives, all mandatory:** consent must be *free, specific, informed, unconditional
and unambiguous*, with a **clear affirmative action**. That kills pre-ticked boxes, bundled
"I agree to everything" checkboxes, and consent inferred from continued use.

**Automatic narrowing (s.6(1) + its Illustration).** Consent is "limited to such personal data as is
necessary for such specified purpose". The telemedicine Illustration is the point: even where the
user ticks yes to contact-list access, the consent is *legally read down* to only what the service
needs. So over-collection is not cured by a tick.

**Severability (s.6(2)).** An offending part of a consent is invalid **to the extent of the
infringement**, not the whole consent. The insurance Illustration: a waiver-of-complaint clause is
struck; the policy-issuance consent survives.

**Withdrawal (s.6(4)-(6)).**
- Withdrawal must be **as easy as giving** it. A one-click opt-in with an email-us-to-opt-out is a
  s.6(4) breach on its face.
- Withdrawal is **prospective only**; prior processing stays legal (s.6(5)).
- Consequences of withdrawal are borne by the Data Principal (s.6(5)). The e-commerce Illustration:
  you may cut off future ordering, but you must still fulfil goods already ordered and paid for.
- On withdrawal the Data Fiduciary must, within a reasonable time, **cease and cause its Processors
  to cease** (s.6(6)). Processor pass-through is your contractual obligation, not optional.

**Notice pairs with consent (s.5(1)).** Notice must accompany or precede every consent request, and
must itemise: (i) the personal data and the purpose, (ii) how to exercise s.6(4) withdrawal and
s.13 grievance rights, (iii) how to complain to the Board.

**Legacy consent (s.5(2)).** Consent obtained before commencement stays valid, but you owe a
retrospective notice "as soon as reasonably practicable", and processing continues until withdrawal.
This is the migration path for every existing Indian database.

**Language (s.5(3), s.6(3)).** The Data Principal must be given the **option** to access the notice
and the consent request in English **or any Eighth Schedule language**. That is 22 languages. This is
a build requirement, not a nicety.

**Burden of proof (s.6(10)).** In a proceeding, the **Data Fiduciary must prove** notice was given
and consent was validly obtained. Practical consequence: consent logs with timestamp, notice version,
language served, and the exact purpose string are the compliance artefact. No log, no defence.

**Consent Managers (s.2(g), s.6(7)-(9)).** An optional intermediary layer. Must be registered with
the Board, is accountable **to the Data Principal** (not to the Data Fiduciary), and the Board can
inquire into and penalise its breaches directly (s.27(1)(c), s.27(1)(d)).

---

## 3. Section 7 legitimate uses, read narrowly

s.7 is a **closed list**. There is no residual "legitimate interests" balancing test. If a use is not
in s.7(a)-(i), the only remaining basis is consent.

| s.7 | Ground | The trap |
|---|---|---|
| (a) | Voluntarily provided for a specified purpose, and she has not indicated non-consent | This is the workhorse for walk-in and inbound scenarios. It dies the moment she says stop (see Illustration II). It does **not** license secondary use, and it does **not** cover data you collected rather than she volunteered. |
| (b) | State issuing a prescribed subsidy, benefit, service, certificate, licence or permit | Needs either prior consent to the State, or the data to sit in a **notified** State database. Also needs the prescribed list to exist. |
| (c) | State function under law, or sovereignty/integrity/security of State | Broad. State-only. |
| (d) | Legal obligation on any person to disclose information to the State | Private bodies can use this, but only for the disclosure obligation itself. |
| (e) | Compliance with a judgment, decree or order (Indian, or foreign contractual/civil claims) | |
| (f) | Medical emergency, threat to life or immediate threat to health | Of the Data Principal **or any other individual**. |
| (g) | Medical treatment or health services during epidemic, outbreak, or threat to public health | |
| (h) | Safety, assistance or services during disaster or breakdown of public order | "disaster" takes the Disaster Management Act, 2005 s.2(d) meaning. |
| (i) | Employment purposes, or safeguarding the employer from loss or liability | Named examples: corporate espionage prevention, trade secret confidentiality, IP, classified information, or a service or benefit sought by an employee. This is the HR basis. It does **not** obviously cover employee wellness marketing, or monitoring dressed up as "safety". |

**s.7(a) vs consent, the practical distinction.** s.7(a) requires that *she volunteered the data for
that purpose*. If your app collected it in the background, or you inferred it, or you are using it for
a purpose beyond the one she volunteered it for, s.7(a) is not available.

---

## 4. Section 8, the operating obligations

| s.8 | Obligation | What it means in practice |
|---|---|---|
| (1) | Fiduciary is responsible regardless of contrary agreement, and regardless of Data Principal's own failure of duties | You cannot contract accountability away to a vendor. You cannot excuse yourself because the user lied. |
| (2) | Processors only under a **valid contract** | For goods/services activity. A DPA is a statutory precondition, not best practice. |
| (3) | Completeness, accuracy and consistency | Only triggered where data is likely to be used for a decision affecting her, **or** disclosed to another Data Fiduciary. Not a general data-quality duty. |
| (4) | Appropriate technical and organisational measures | For observance of the Act generally (governance), distinct from (5). |
| (5) | **Reasonable security safeguards** to prevent breach | Covers data in possession or control, including at the Processor. Highest penalty in the Schedule: up to Rs 250 crore. |
| (6) | Breach intimation to **the Board AND each affected Data Principal** | No harm threshold. No materiality threshold. No "risk of harm" filter. This is stricter than GDPR Art 33/34. Up to Rs 200 crore. |
| (7) | Erase on withdrawal, or when the specified purpose is no longer served, whichever is earlier, and cause the Processor to erase | Unless retention is necessary for compliance with law (bank KYC Illustration). |
| (8) + (11) | Deemed purpose-expiry after a prescribed period of no contact and no rights exercised | The period is set by Rules and may differ by class of Fiduciary and by purpose. |
| (9) | Publish DPO business contact info, or a person who can answer questions | Non-SDFs still need a published contact point. |
| (10) | Effective grievance redressal mechanism | Pairs with s.13. |

**The s.8(6) point deserves repeating because people get it wrong constantly:** the Act sets no
threshold. Every personal data breach as defined in s.2(u) is notifiable, to the Board and to each
affected individual, in the form and manner the Rules prescribe. s.2(u) includes mere **loss of
access** (so ransomware and even a botched availability incident can be a "personal data breach").

---

## 5. Children (s.9)

- **Child = under 18** (s.2(f)). India uses 18, not 13 or 16. There is no general teen-consent tier.
- s.9(1): **verifiable** parental or lawful-guardian consent before processing a child's data, in the
  prescribed manner. Same rule extends to a person with disability who has a lawful guardian.
- s.9(2): no processing likely to cause **detrimental effect on the well-being of a child**. This is a
  substantive prohibition that stands even with perfect parental consent.
- s.9(3): **absolute bar** on (i) tracking, (ii) behavioural monitoring of children, (iii) targeted
  advertising directed at children. Consent does not cure it.
- s.9(4): the Rules may exempt classes of Fiduciaries or purposes from (1) and (3). Note: **not from
  (2)**. The well-being prohibition is never exemptible under s.9(4).
- s.9(5): a Fiduciary that proves "verifiably safe" processing can be notified an **age above which**
  s.9(1) and s.9(3) do not apply to it. Company-specific, government-granted, not self-declared.
- Penalty: up to Rs 200 crore (Schedule item 3).

Any product with under-18 users in India: age assurance, verifiable parental consent, and a hard kill
on behavioural ad targeting and tracking for those users. Analytics that profiles child users is
squarely inside s.9(3).

---

## 6. Significant Data Fiduciaries (s.10)

Trigger is **notification by the Central Government**, based on factors it may determine, including:
volume and sensitivity of data, risk to Data Principal rights, sovereignty and integrity of India,
**risk to electoral democracy**, security of the State, public order (s.10(1)(a)-(f)).

Once notified, four hard duties:
1. **DPO** who represents the SDF, is **based in India**, is an individual **responsible to the board
   of directors or similar governing body**, and is the grievance point of contact (s.10(2)(a)).
2. **Independent data auditor** to carry out a data audit evaluating compliance (s.10(2)(b)).
3. **Periodic DPIA**, defined in the Act itself as a process comprising a description of Data
   Principal rights and the purpose of processing, plus assessment and management of risk to those
   rights (s.10(2)(c)(i)).
4. **Periodic audit**, plus any other prescribed measures (s.10(2)(c)(ii)-(iii)).

Penalty: up to Rs 150 crore (Schedule item 4).

Note the asymmetry: **only SDFs must appoint a DPO.** Everyone else only needs to publish a contact
person under s.8(9). Do not tell a non-notified company it must appoint a DPO under the Act.

---

## 7. Rights, and the rights that are NOT there

**Present:**
- s.11 access: summary of personal data + processing activities; identities of other Fiduciaries and
  Processors it was shared with + description of what was shared; plus prescribed extras. Blocked for
  law-enforcement sharing under s.11(2).
- s.12 correction, completion, updating, erasure. On a correction request the Fiduciary **shall**
  correct, complete and update (s.12(2)). On an erasure request it **shall** erase unless retention is
  necessary for the specified purpose or for legal compliance (s.12(3)).
- s.13 grievance redressal, with a **mandatory exhaustion rule**: she must exhaust the Fiduciary's
  grievance mechanism **before** approaching the Board (s.13(3)).
- s.14 nomination, so a nominee can exercise her rights on death or incapacity (unsoundness of mind or
  infirmity of body).

**Conspicuously absent. Do not invent these:**
- No right to **data portability**.
- No right to **object** to processing generally.
- No right against **automated decision-making** or profiling, and no explanation right.
- No **compensation** to the Data Principal. Penalties go to the Consolidated Fund of India (s.34).
  DPDP gives the individual no monetary remedy. And s.44(2)(a) **omitted IT Act s.43A**, deleting the
  old compensation route for negligent handling of sensitive personal data.
- No private cause of action, and s.39 **bars civil courts** from matters the Board is empowered over.

**Rights attach to consent-based (and s.7(a)-based) processing.** s.11(1) and s.12(1) are both worded
"to whom she has previously given consent, including consent as referred to in clause (a) of section
7". Processing under s.7(b) to s.7(i) does not carry these access and correction rights in the same
way. That is a real and often-missed limitation.

**Duties of the Data Principal (s.15)** are enforceable against her, penalty up to Rs 10,000
(Schedule item 5). Frivolous complaints can also draw a warning or costs from the Board (s.28(12)).
This is unusual internationally and is worth flagging in any comparison.

---

## 8. Cross-border transfers (s.16)

- Default is **permitted**. s.16(1) is a **blacklist / negative-list** model: the Central Government
  may notify countries or territories to which transfer is **restricted**.
- s.16(2) preserves any **higher** standard in other Indian law. So sectoral localisation still binds:
  RBI payment-data storage directions, insurance and telecom rules, CERT-In directions, and so on.
  DPDP does not relax them.
- Practical answer: for most transfers, DPDP itself is not the blocker. The sectoral regulator is.
  Always ask which regulator sits over the client before saying "transfers are fine".

---

## 9. Exemptions (s.17), the most litigable part

**s.17(1): partial exemption.** Chapter II is disapplied **except s.8(1) and s.8(5)**, and Chapter III
and s.16 are disapplied, in six cases: (a) enforcing a legal right or claim; (b) judicial,
quasi-judicial, regulatory or supervisory bodies performing their function; (c) prevention, detection,
investigation or prosecution of offences; (d) processing of non-India Data Principals under a contract
with a person outside India by a person based in India; (e) court-approved M&A, demerger and similar;
(f) ascertaining the assets and liabilities of a **loan defaulter** (IBC s.3(12) and s.3(14) meanings).

Two things survive every s.17(1) exemption: **s.8(1) accountability** and **s.8(5) security
safeguards**. So even an exempt processor still owes reasonable security. Say this out loud in advice.

**s.17(1)(d) is the outsourcing / GCC / BPO clause.** Indian entities processing foreign data under a
foreign contract get a broad exemption. This is deliberate industrial policy and is the single most
commercially significant exemption in the Act.

**s.17(2): total exemption.** (a) notified **State instrumentalities** on sovereignty, security,
friendly relations, public order, or incitement grounds, plus the Centre's processing of what they
furnish; (b) **research, archiving or statistical** purposes, provided the data is not used to take a
decision specific to a Data Principal, and prescribed standards are followed.

**s.17(3): startup relief.** The Centre may notify Fiduciaries, including startups, to whom **s.5,
s.8(3), s.8(7), s.10 and s.11** do not apply. It is a notification-based relief, not automatic. And it
does **not** exempt s.6 consent, s.8(5) security, s.8(6) breach notice, s.9 children, s.12 or s.13.

**s.17(4): the State's retention and correction carve-out.** For State processing, s.8(7) erasure and
s.12(3) erasure do not apply; and s.12(2) correction does not apply where the processing does not
involve a decision affecting her.

**s.17(5): five-year sunset power.** For five years from commencement, the Centre may declare any
provision inapplicable to any Fiduciary or class, for a specified period.

---

## 10. Enforcement mechanics

- **Data Protection Board of India** (s.18). Body corporate. Chairperson plus notified Members, all
  Centre-appointed (s.19(2)), **two-year terms**, re-appointable (s.20(2)). At least one Member must
  be a legal expert (s.19(3)).
- The Board is an **adjudicatory** body only. It has **no rule-making or standard-setting power**.
  Rules are made by the Central Government under s.40. This is a major structural difference from the
  ICO, the EDPB, or a typical independent DPA.
- **Digital by design** (s.28(1)), civil-court powers under CPC 1908 for summons, evidence, discovery
  and inspection (s.28(7)). But it **cannot** prevent access to premises or seize equipment (s.28(8)).
- Board triggers (s.27(1)): breach intimation, Data Principal complaint, Centre or State reference,
  court direction, Consent Manager complaint or registration breach, or s.37(2) intermediary reference.
- **Mediation** may be directed (s.31). **Voluntary undertakings** may be accepted (s.32); accepting
  one **bars** proceedings on its contents (s.32(4)), but breaching it is itself a breach of the Act
  and reopens s.33 (s.32(5)).
- **Penalty only if the breach is "significant"** (s.33(1)). "Significant" is undefined. The s.33(2)
  factors (a) to (g) are the mitigation playbook, and (e) explicitly rewards prompt, effective
  mitigation. Argue (e), (f) and (g) hard in any real matter.
- **Appeal to TDSAT** within **60 days**, extendable for sufficient cause (s.29(2)-(3)). Endeavour to
  dispose within six months (s.29(6)). Onward appeal follows TRAI Act s.18, meaning the Supreme Court.
- **s.37 blocking:** after the Board has imposed a monetary penalty on a Data Fiduciary in **two or
  more instances**, and advises blocking in the interests of the general public, the Centre may order
  intermediaries to block public access. Effectively a market-exclusion power. Hearing required first.
- **No criminal offences and no imprisonment anywhere in this Act.** Purely civil monetary penalties.

---

## 11. Knock-on amendments (s.44), commonly missed

- **TRAI Act s.14(c)** amended so TDSAT is expressly the DPDP appellate tribunal.
- **IT Act s.43A omitted.** The old statutory compensation route for a body corporate's negligent
  handling of sensitive personal data is gone. The SPDI Rules 2011 rested on s.43A, so their footing is
  materially undermined. Do not cite SPDI Rules as live obligations without flagging this.
- **IT Act s.87(2)(ob) omitted**, removing the rule-making power that supported the SPDI Rules.
- **IT Act s.81 proviso** amended so the IT Act does not override DPDP.
- **RTI Act s.8(1)(j) replaced** with a flat exemption for "information which relates to personal
  information". The old text's public-interest and public-activity carve-ins were deleted. This is the
  most politically contested amendment in the Act and should be flagged in any public-sector work.

---

## 12. DPDP vs GDPR, the differences that change advice

| Topic | DPDP 2023 | GDPR |
|---|---|---|
| Lawful bases | 2: consent, or s.7 closed list | 6, including legitimate interests balancing |
| Legitimate interests | **None** | Art 6(1)(f) |
| Sensitive data category | **None**. No special category at all | Art 9 special categories |
| Scope trigger abroad | Only offering goods/services to India (s.3(b)) | Offering **or monitoring behaviour** |
| Child age | **Under 18**, flat | 16, states may lower to 13 |
| Ad targeting at children | **Prohibited outright** (s.9(3)) | Restricted, not banned |
| Breach notice threshold | **None**, always notify Board + each individual | Risk-based; 72h to DPA; high risk to individuals |
| DPO | Only for notified SDFs | Art 37 triggers, wider |
| Portability | **Absent** | Art 20 |
| Object / automated decisions | **Absent** | Arts 21, 22 |
| Compensation to individual | **Absent**; penalties to Consolidated Fund | Art 82 |
| Transfers | Negative list, default permitted | Adequacy / SCCs / BCRs, default restricted |
| Regulator | Adjudicatory Board, **no rule-making** | Independent DPAs with guidance powers |
| Individual duties + fines on individuals | **Yes**, s.15, up to Rs 10,000 | No |
| Criminal liability | **None** | Member-State dependent |
| Max penalty | Rs 250 crore per Schedule item | 4% global turnover / EUR 20m |

**The single sentence to remember:** DPDP is consent-heavy, rights-light, State-friendly, and has no
sensitive-data tier. Advice imported wholesale from a GDPR programme will over-build rights machinery
and under-build consent-and-notice machinery, breach readiness, and Eighth Schedule language support.

---

## 13. Traps that produce wrong answers

1. **Inventing "sensitive personal data".** The Act has no such category. Health, biometric, financial
   and caste data get **no** extra treatment under DPDP. (Sectoral law may still add duties. Say that
   instead.)
2. **Asserting "legitimate interest" as a basis.** It does not exist. s.7 is closed.
3. **Assuming a large company is automatically an SDF.** It is not, until notified (s.10(1)).
4. **Telling every company to appoint a DPO.** Only notified SDFs (s.10(2)(a)). Others need only a
   published contact under s.8(9).
5. **Applying a breach-notification harm threshold.** There isn't one (s.8(6)).
6. **Reading DPDP as mandating data localisation.** It does not (s.16 is a negative list). Sectoral
   rules do, preserved by s.16(2).
7. **Promising the individual compensation or damages.** No such remedy; s.39 bars civil courts; s.43A
   was omitted.
8. **Citing the SPDI Rules 2011 as unqualified live law** after s.44(2)(a) and (c).
9. **Using 13 or 16 as the child age.** It is 18 (s.2(f)).
10. **Saying "consent covers it" for children's behavioural ads.** s.9(3) is an outright bar.
11. **Forgetting s.8(1) and s.8(5) survive every s.17(1) exemption.**
12. **Treating rights under s.11 and s.12 as universal.** They are worded against consent-based and
    s.7(a)-based processing.
13. **Stating obligations are "in force" without checking commencement.** s.1(2) allows staggered
    commencement, and most operative duties depend on Rules that were still phasing in.
14. **Quoting a penalty as a fine that will be imposed.** Every Schedule figure is a **ceiling**
    ("may extend to"), gated on the Board finding the breach "significant" (s.33(1)) and weighing the
    s.33(2) factors.
15. **Forgetting the Eighth Schedule language option** in notice and consent UX (s.5(3), s.6(3)).
16. **Ignoring s.6(10)**: the burden of proving valid notice and consent sits on the business.

---

## 14. Open items that depend on subordinate legislation

The Act delegates roughly 26 matters to Rules under s.40(2)(a) to (z). When any of these come up, the
answer is "the Rules govern; check the current notified Rules", not a guess:

manner of notice (s.5(1), s.5(2)); Consent Manager obligations and registration conditions (s.6(8),
s.6(9)); the prescribed subsidy/benefit list (s.7(b)); form and manner of breach intimation (s.8(6));
the no-contact period that deems purpose expiry (s.8(8)); manner of publishing DPO contact (s.8(9));
manner of obtaining verifiable parental consent (s.9(1)); child-processing exemptions (s.9(4)); DPIA
contents and other SDF measures (s.10(2)(c)); manner of access and erasure requests (s.11(1), s.12(3));
grievance response period (s.13(2)); manner of nomination (s.14(1)); research/archiving/statistical
standards (s.17(2)(b)); Board appointment, salary, procedure, techno-legal measures (s.19 to s.28);
appeal form, fee and procedure (s.29).

Plus government **notifications** rather than Rules: restricted countries (s.16(1)), SDF designation
(s.10(1)), State-instrumentality exemptions (s.17(2)(a)), startup relief (s.17(3)), the s.9(5)
verifiably-safe age, s.17(5) sunset declarations, and Schedule amendments (s.42, capped at doubling).
