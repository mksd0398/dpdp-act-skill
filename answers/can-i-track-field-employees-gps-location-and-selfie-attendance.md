---
question: Can I track field employees' GPS location and selfie attendance under the DPDP Act?
date: 2026-11-13
asked: https://github.com/Zeus-pr/ariforce/issues/36
---
Yes, for work. A location ping or an attendance selfie is personal data under s.2(t), and s.7(i) lets an employer process it without consent "for the purposes of employment". Tracking a field rep between check-in and check-out sits inside that. Tracking after logout, on leave days, or around the clock is much harder to fit, and the fallback, consent under s.6(1), is weak when it comes from an employee. None of the Rules' duties are enforceable before **14 May 2027**.

## Two lawful bases, and no third

s.4(1) allows processing only with consent or for a "legitimate use" in the closed s.7 list. There is no legitimate-interests balancing test, so the European habit of "we have a business need, here is our assessment" does not work. You must point to a clause.

For staff, that clause is s.7(i): processing "for the purposes of employment or those related to safeguarding the employer from loss or liability". Marking attendance, proving a doctor or dealer visit happened, paying travel allowance by distance and checking that a selfie matches the person on the payroll are all plausibly employment purposes. That is a reading, not a holding. There is no Board decision on employee tracking yet, so it is untested.

## Where the employment basis runs out

The words "for the purposes of employment" are the limit. Three uses sit badly with them:

- **Off-duty tracking.** A GPS trail at 10 pm on a Sunday is not about the job.
- **Second purposes.** Reusing location history for something other than running the job, such as selling movement data or building a profile of where staff live and shop.
- **Data the job does not need.** A continuous trail when the job only needs check-in and check-out points.

For those you would need consent, and s.6(1) wants it "free, specific, informed, unconditional and unambiguous with a clear affirmative action". A rep who must tap "I agree" to get paid has not given free consent. The cleaner fix is to design those uses out.

## A selfie is not "biometric sensitive data"

The DPDP Act has no sensitive-data tier. A face photo gets the same treatment as a phone number. What raises the stakes is how you handle it: a face-match template stored centrally is valuable to an attacker, so it needs serious security under s.8(5).

## What you owe even without consent

- **Security** (s.8(5)). Rule 6 sets the floor: encryption or masking, access control, access logs, backups and processor contracts. Rule 6 comes from secondary sources here, so verify it against the notified Gazette text.
- **A contract with the tracking-app vendor** (s.8(2)). If a SaaS vendor runs the app for you, it is your Data Processor, and you stay responsible for what it does (s.8(1)).
- **Erasure when the purpose ends** (s.8(7)). Location trails of an employee who left two years ago serve no purpose. Rule 8(3) separately asks you to keep personal data and the logs of processing for at least one year, so plan a one-year floor, not a 30-day purge. Verify Rule 8(3) against the Gazette text too.
- **Breach notice** (s.8(6)). A leaked location database is a personal data breach under s.2(u). The Board and every affected employee must be told, with no harm threshold.
- **A contact person** (s.8(9)) and a grievance route (s.8(10)).

Two things you are, on the text, not strictly obliged to do under s.7(i). The s.5(1) notice attaches to a consent request "under section 6", so it does not apply when you rely on s.7(i). And the access and correction rights in s.11(1) and s.12(1) are worded for consent and s.7(a) processing. Give staff a plain notice and let them see their own trail anyway. It costs nothing, and it is the evidence you will want if a complaint ever reaches the Board.

## Worked example: a 40-person pharma field team

The app records GPS only between the rep's tap on "Start day" and "End day", and only at three points: start, each doctor visit, end. At each visit the rep takes a selfie, matched on the phone against their enrolment photo; only the match result and a timestamp go to the server, not the photo. The written policy names s.7(i), lists what is collected and why (attendance, visit proof, travel allowance), and says who can see it: the rep, their manager and payroll. The vendor contract covers encryption, access logs and deletion on exit. Trails are kept for one year after the month they cover, then deleted. Nothing is tracked after "End day", and leave days switch tracking off.

## What it costs to get wrong

All figures are ceilings, not predictions: up to Rs 250 crore for failing s.8(5) security safeguards, up to Rs 200 crore for missing a s.8(6) breach notice, and up to Rs 50 crore for anything else. The Board can impose them only if it finds the breach "significant" under s.33(1). Penalties go to the Consolidated Fund of India (s.34); the Act gives employees no compensation claim.

> Not legal advice. Verify statutory text against the Gazette of India and consult qualified
> Indian legal counsel before acting.
