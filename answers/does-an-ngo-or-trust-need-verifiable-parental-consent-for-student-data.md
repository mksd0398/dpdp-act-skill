---
question: Does an NGO or charitable trust need verifiable parental consent to collect student data?
date: 2026-10-26
asked: https://github.com/digipants/educatia/issues/27
---
Yes, by default. The DPDP Act has no exemption for charities, NGOs or trusts, and anyone under 18 is a child (s.2(f)). Before processing a child's personal data, the trust must obtain "verifiable consent of the parent" (s.9(1)), in the manner Rule 10 sets. A required "my parent agrees" checkbox on a sign-up form is unlikely to be enough. Some educational and childcare bodies may fall in a narrow, purpose-limited Rule 12 carve-out, but that has to be checked against the Fourth Schedule, not assumed.

## A trust is a Data Fiduciary like any company

The Act applies to any "person" who decides why and how personal data is processed (s.2(i)). "Person" includes an association of persons and "every artificial juristic person" (s.2(s)), which covers registered trusts and societies. Non-profit status changes nothing. s.17 exempts legal claims, courts and crime prevention (s.17(1)), and research, archiving or statistics (s.17(2)(b)). A scholarship, tuition or mentoring programme is none of these. The s.17(3) relief for startups and others applies only once the Central Government notifies a class, and none has been notified.

## What "verifiable" means

The Act leaves the method to the Rules (s.9(1)). Rule 10(1) requires the trust to observe due diligence to check that the person consenting as parent is an identifiable adult, using either:

- reliable identity and age details the trust already holds, or
- details the parent provides, either directly or through a virtual token from an authorised entity such as DigiLocker.

A checkbox the child can tick, with nothing behind it, does neither. Whether a parent typing their own name, age and phone number counts as "voluntarily provided" details under Rule 10(1) is a reading, not a holding. It is **untested**, and there are no Board decisions yet. A safer pattern is a separate parent step, such as an OTP to the parent's phone plus a declaration, logged with a timestamp.

The trust carries the burden of proving consent was valid (s.6(10)). No log, no defence.

Rule 10 is taken here from secondary sources: verify against the notified Gazette text.

## The Rule 12 exemption is narrow

s.9(4) lets the Rules exempt some classes of Data Fiduciary, for some purposes, from s.9(1) and s.9(3). Rule 12 and the Fourth Schedule use that power. Secondary sources place educational institutions and childcare providers among those classes, each limited to set purposes. A trust running a school may be covered for its school work. A trust running a weekend programme should not assume it is an "educational institution" in that sense. Read the Fourth Schedule entry and its conditions first.

Two limits hold even where the carve-out applies:

- s.9(2) bars any processing "likely to cause any detrimental effect on the well-being of a child". No Rule can exempt this.
- The rest of the Act still applies: a lawful basis (s.4(1)), a notice with the consent request (s.5(1)), security (s.8(5)), breach reporting (s.8(6)) and erasure (s.8(7)).

## The form is only half the problem

Form data usually lands in several places: a database, an inbox, exports, backups. Each copy is processing.

- **Email providers and hosting are Data Processors.** Using one needs a valid contract (s.8(2)), and the trust stays responsible for what they do (s.8(1)).
- **Collect only what the purpose needs.** Consent is limited to "such personal data as is necessary" for the purpose (s.6(1)). If you do not need gender or full date of birth to run the programme, do not ask.
- **Delete when done.** Erase once the purpose is served, unless a law requires you to keep it (s.8(7)). That includes the copies sitting in a mailbox.
- **No tracking.** s.9(3) bars "tracking or behavioural monitoring of children". Ad pixels and behavioural analytics on the student form page are a problem even with parental consent.

## Worked example: a tuition programme run by a trust

A trust runs free weekend classes. Its website form asks for the child's name, date of birth, gender, school, and a parent's phone number. Submissions are emailed to a shared inbox and saved to a database. The form has a required box: "My parent or guardian consents".

What changes before 14 May 2027:

1. The child fills in the class details. The parent then gets an OTP on their own phone and confirms, with a short notice in English or a language they choose from the Eighth Schedule (s.5(3), s.6(3)).
2. The notice says what is collected, why, how to withdraw, and how to complain to the Board (s.5(1)). Withdrawal is as easy as consenting (s.6(4)).
3. Gender is dropped. Date of birth becomes an age band, unless the programme truly needs the date.
4. Email notifications carry a reference number, not the child's details.
5. Records are deleted a fixed time after the child leaves the programme, inbox included.
6. The form page loads no ad pixels.

## When this bites

Rule 10 and the other substantive Rules apply from **14 May 2027**. Nothing here is a fine today. For a breach of the children's obligations, the penalty may extend to Rs 200 crore under the Schedule, and only if the Board finds the breach "significant" (s.33(1)). That is a ceiling, not a predicted fine.

> Not legal advice. Verify statutory text against the Gazette of India and consult qualified
> Indian legal counsel before acting.
