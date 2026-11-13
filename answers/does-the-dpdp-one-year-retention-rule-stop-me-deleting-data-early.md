---
question: Does the DPDP one-year retention rule stop me deleting personal data before a year is up?
date: 2026-11-13
asked: https://github.com/Sharmistha-622/pnc-elc-platform/issues/107
---
Probably yes, for the data and logs of the processing you actually did. Rule 8(3) of the DPDP Rules, 2025 requires a Data Fiduciary to keep personal data, the associated traffic data and other logs of the processing for at least one year from the date of that processing, and the Act itself lets rules require processing to continue after consent is withdrawn (s.6(6)). So a "delete at 90 days" policy now has a one-year floor under it. None of this binds before **14 May 2027**, and the interaction with the erasure duty in s.8(7) is untested.

## The two rules that pull in opposite directions

The Act tells you to delete. Under s.8(7)(a) a Data Fiduciary must erase personal data when the person withdraws consent, or as soon as it is reasonable to assume the specified purpose is no longer served, whichever is earlier. Under s.12(3) it must erase on request. Both duties carry an exception: retention that is "necessary for compliance with any law for the time being in force".

The Rules tell you to keep. Rule 8(3) sets a minimum one-year retention for personal data, traffic data and logs of the processing. Rule 6(1)(e), the security-safeguards rule, separately requires you to keep logs and personal data for one year so you can detect, investigate and remediate unauthorised access, unless another law requires otherwise. Verify both against the notified Gazette text before relying on the exact wording.

## Why the floor most likely wins

Three points in the Act's own text support keeping the data:

- s.6(6) says that after withdrawal you must stop processing "unless such processing without her consent is required or authorised under the provisions of this Act or the rules made thereunder". The Act expressly expects rules to override withdrawal.
- s.8(7) and s.12(3) both yield to "any law for the time being in force". Whether a Rule made under s.40 counts as "law" for that phrase has not been decided, but it is the natural reading.
- s.40(1) allows only rules "not inconsistent with the provisions of this Act". Because s.6(6) itself contemplates rules requiring retention, a one-year floor is hard to call inconsistent.

The narrower reading is that the floor covers only what security work needs: access logs and the records tied to them. That fits Rule 6(1)(e), which states its purpose. Rule 8(3) as summarised in our references carries no such limit. Both readings are arguable. No Board decision exists yet on either.

## What "keep" should mean in practice

Keeping data for a year is not the same as keeping it in use. Once the purpose ends or consent is withdrawn, s.6(6) still requires you to stop processing it for that purpose. The defensible pattern is retain-and-restrict:

1. On withdrawal or end of purpose, pull the record out of every live workflow, search and report.
2. Move it to a restricted store that only security or legal staff can open, with access itself logged.
3. Delete it, and cause your processors to delete it under s.8(7)(b), on the later of the one-year date and any longer statutory period.
4. Your s.8(5) security duty does not pause while the data sits there. A breach of the archive is still a breach under s.8(6), notifiable to the Board and to each affected person.

## A worked example: a candidate who withdraws

An HR platform collects a joining candidate's PAN, bank details and address documents on 1 June 2027. On 1 July the candidate withdraws. The company's own policy says documents go 90 days after withdrawal, which would be 29 September.

Under the conservative reading, Rule 8(3) runs one year from the date of processing, so the documents stay until at least 1 June 2028. From 1 July they leave the onboarding queue and every recruiter's view, move to a locked archive, and get no further use. If the candidate asks for erasure under s.12(3), the reply states that retention is required by law until 1 June 2028, after which the data will be erased. If any record also falls under a longer rule, such as payroll or tax records for someone who did join, that longer period applies, because s.8(7) defers to it.

Under the narrow reading, only the access and activity logs about that candidate stay for a year, and the documents go on 29 September. If you choose this, write down why, and keep that note with your retention policy.

## What to decide now

Pick a reading, record it with reasons, and build the one-year floor as a configurable check rather than hard-coded logic, so you can change it if the Board or the Centre clarifies. The Third Schedule's three-year deemed-expiry periods under Rule 8(1) apply only to large e-commerce, online gaming and social media platforms. They do not change the answer for most businesses.

> Not legal advice. Verify statutory text against the Gazette of India and consult qualified
> Indian legal counsel before acting.
