---
question: Do I need a data processing agreement with my cloud and SaaS vendors under the DPDP Act?
date: 2026-11-24
asked: https://github.com/Sharmistha-622/pnc-elc-platform/issues/186
---
Yes. A Data Fiduciary may use a Data Processor for any activity related to offering goods or services "only under a valid contract" (s.8(2)), and the business stays responsible for everything the vendor does on its behalf, whatever the contract says (s.8(1)). Unlike the GDPR, the Act does not list mandatory clauses. The Rules add one: the contract must provide for reasonable security safeguards (Rule 6(1)(f)). These duties apply from **14 May 2027**.

## Which vendors count

A Data Processor is "any person who processes personal data on behalf of a Data Fiduciary" (s.2(k)). Your cloud host, database, email sender, analytics tool and payroll software usually fit: you decide why the data is processed and they run it for you.

Some vendors are not processors. If a vendor decides its own purpose and means for the data, it is a Data Fiduciary in its own right (s.2(i)). A background-check agency that keeps candidate data to build its own records may sit there. Sharing with another Data Fiduciary is not a s.8(2) arrangement, and the accuracy duty in s.8(3)(b) applies to what you send it. Map each vendor before you collect contracts.

## What the contract has to do

The Act says "valid contract" and stops there. It does not require a signed paper agreement, so a vendor's standard online addendum that you accept is the normal route for large providers. Whether a click-accepted addendum is enough has not been tested before the Board.

What matters is whether the contract lets you meet duties the Act puts on you:

- **Security.** You must protect data processed on your behalf by a processor with reasonable security safeguards (s.8(5)). Rule 6(1)(f) requires a contract provision on safeguards, and Rule 6(1)(b) covers access control on the processor's computer resources too.
- **Stop on withdrawal.** When a person withdraws consent, you must cease and "cause its Data Processors to cease" processing within a reasonable time (s.6(6)).
- **Erasure.** When the purpose ends, you must cause the processor to erase the data you gave it (s.8(7)(b)), unless a law requires you to keep it.
- **Breach notice to you.** You must tell the Board and every affected person about a breach (s.8(6)). Under Rule 7 the Board gets a first intimation without delay and a detailed report within 72 hours of you becoming aware. A vendor that tells you a week later breaks your clock, so the contract should require prompt notice.
- **Who has the data.** A person can ask you for the identities of all Data Fiduciaries and Data Processors you shared her data with (s.11(1)(b)). Keep a vendor list with sub-processors so you can answer.

Rule-based points above: verify against the notified Gazette text.

## A worked example

A Pune HR platform runs on Supabase, Vercel and Google Workspace, uses a payroll vendor, and sends candidate details to a background-check agency.

Supabase, Vercel and Google publish data processing addenda written for the GDPR. These usually cover security, deletion and breach notice, which maps onto s.8(5), s.8(7)(b) and s.8(6). The founder accepts each one, records the date, and checks the breach-notice period is short enough for Rule 7.

The payroll vendor works on the HR platform's instructions, so it needs a contract under s.8(2) with a security clause (Rule 6(1)(f)). If its standard terms say nothing about deletion or breach notice, the founder adds a short schedule covering s.6(6), s.8(7)(b) and prompt breach notice.

The background-check agency gets a closer look. If it uses the data only for the HR platform's checks and deletes it after, treat it as a processor. If it keeps its own database, it is probably a separate Data Fiduciary, and the HR platform needs its own lawful basis under s.4(1) for sharing the candidate's data with it.

Hosting in Mumbai is a choice, not a DPDP requirement. The Act only lets the Centre notify countries where transfers are restricted (s.16(1)), and none has been notified. Sector rules can still require local storage (s.16(2)).

## What it costs to get wrong

No contract at all is a breach of s.8(2), which falls under the Schedule's residual item: a ceiling of Rs 50 crore. A vendor's security failure is treated as yours under s.8(1) and s.8(5), with a ceiling of Rs 250 crore. Both are maximums. The Board can impose a penalty only if it finds the breach "significant" (s.33(1)).

## What a GDPR-style DPA may miss

Most vendor DPAs are written for the GDPR's Article 28 list, so they usually cover more than DPDP asks. Check them for India-specific gaps: a breach-notice period fast enough for Rule 7, deletion that also reaches backups, and a sub-processor list you can actually produce for s.11(1)(b).

> Not legal advice. Verify statutory text against the Gazette of India and consult qualified
> Indian legal counsel before acting.
