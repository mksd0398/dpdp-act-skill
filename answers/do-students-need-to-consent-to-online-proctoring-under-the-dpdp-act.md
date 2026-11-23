---
question: Do students need to consent before an online proctored test logs their IP address and activity under the DPDP Act?
date: 2026-11-23
asked: https://github.com/yashsrivastava1408/OpsAcademy/issues/181
---
Yes, in most cases. An IP address, a webcam frame or a tab-switch log tied to a named candidate is personal data under s.2(t), and the DPDP Act allows only two lawful bases: consent or a listed legitimate use (s.4(1)). No s.7 ground covers proctoring a student, so the platform needs consent under s.6(1), preceded by a notice under s.5(1). If any test-taker is under 18, s.9(3) bars tracking and behavioural monitoring outright unless a Rule exempts it. These duties apply from **14 May 2027**.

## Why there is no consent-free route

India has no "legitimate interests in exam integrity" ground. s.7 is a closed list. s.7(a) covers data the student "has voluntarily provided" for a specified purpose. Her name, roll number and answers arguably fit. Her IP address, browser events and webcam feed do not: your software collects them, she does not hand them over. s.7(i) covers employment purposes, and a student is not an employee. That leaves consent.

## Who owes the consent: you or the college

The Data Fiduciary is whoever decides the purpose and means of processing (s.2(i)).

- **You run your own certification tests.** You are the Data Fiduciary. The notice, consent and every duty below are yours.
- **A college runs its exam on your platform.** The college likely decides why and how students are proctored, so it is the Data Fiduciary and you are its Data Processor (s.2(k)). It must have a valid contract with you (s.8(2)), and it stays responsible for what you do (s.8(1)). In practice you build the consent screen and the college owns it.

If you also reuse the logs for your own ends, such as training a cheating model, you are probably a Data Fiduciary for that use too. This is a reading of s.2(i), untested before the Board.

## What valid consent looks like here

s.6(1) wants consent that is "free, specific, informed, unconditional and unambiguous with a clear affirmative action", limited to the data "necessary for such specified purpose". Three practical consequences:

- **Show the notice before the test, not in the terms of service.** s.5(1) requires it to list the data and the purpose, how to withdraw consent, how to raise a grievance, and how to complain to the Board. The student must be able to read it in English or any Eighth Schedule language (s.5(3), s.6(3)).
- **Collect only what integrity needs.** Consent is read down to what the purpose needs (s.6(1) and its telemedicine Illustration). Tab switches and one IP check per session are easy to justify. Continuous room video, keystroke timing and contact-list access are not.
- **Withdrawal stops future proctoring, not past results.** The student may withdraw at any time (s.6(4)). The consequences fall on her (s.6(5)), so you may stop her taking further proctored tests, but processing before withdrawal stays lawful.

Is consent "free" when the exam is compulsory? Untested. Offering a supervised in-person sitting as the alternative makes the consent easier to defend.

## Students under 18

A child is anyone under 18 (s.2(f)). s.9(1) needs verifiable parental consent, and Rule 10 sets how the parent is checked. s.9(3) says a Data Fiduciary "shall not undertake tracking or behavioural monitoring of children", and parental consent does not cure that. Live proctoring of a minor looks like behavioural monitoring.

s.9(4) lets the Rules exempt classes of Data Fiduciaries and purposes, and Rule 12 with the Fourth Schedule does that for some educational uses. Check its exact wording against the notified Gazette text before relying on it. No exemption can lift s.9(2), the bar on processing likely to harm a child's well-being.

## Retention: delete integrity logs, keep security logs

Erase personal data once the purpose is served (s.8(7)). For proctoring that is when results are final and any re-evaluation window has closed. Separately, Rule 8(3) asks you to keep logs of processing for at least one year. Rules 8, 10 and 12 here come from secondary sources, so verify them against the notified Gazette text. So keep webcam snapshots only until results are final, and an image-free access log for one year.

## Worked example: a college placement test

A Pune college runs an aptitude test for 600 final-year students on your platform. Before the timer starts, each student sees a one-screen notice in English or Marathi: IP check at login, tab-switch count, one webcam snapshot every five minutes, used only to flag malpractice for the exam cell. She taps "I agree" and the platform logs time, notice version and language, because the college must prove valid consent (s.6(10)). Students who decline sit the test in a supervised lab. Snapshots are deleted 30 days after results; the access log stays for one year. Your contract with the college covers security safeguards (s.8(5)) and deletion on instruction.

## What it costs to get wrong

All figures are ceilings, not predictions: up to Rs 200 crore for a breach of the children's obligations in s.9, up to Rs 250 crore for failing the s.8(5) security safeguards, and up to Rs 50 crore for a defective notice or consent. The Board can impose a penalty only if it finds the breach "significant" (s.33(1)). Penalties go to the Consolidated Fund of India (s.34); students get no compensation under the Act.

> Not legal advice. Verify statutory text against the Gazette of India and consult qualified
> Indian legal counsel before acting.
