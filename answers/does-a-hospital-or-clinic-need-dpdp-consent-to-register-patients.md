---
question: Does a hospital or clinic need DPDP consent to register patients, or is treatment a legitimate use?
date: 2026-11-14
asked: https://github.com/pilgrim-AIEngineer/Artemis-HMIS/issues/39
---
There is no general "healthcare" ground in the DPDP Act. The medical grounds in s.7 cover only emergencies (s.7(f)) and epidemics or other public-health threats (s.7(g)). Routine treatment of a walk-in patient most likely rests on s.7(a), data the patient voluntarily gives for a specified purpose. Anything beyond that purpose, such as WhatsApp offers or linking records to another platform, needs separate consent under s.6(1). These duties apply from **14 May 2027**.

## Health data gets no special tier

Patient records are personal data under s.2(t), like any other. The Act has no "sensitive personal data" category, so diagnoses and lab reports carry no extra DPDP duties because they are medical. Medical-records rules and professional codes may still add duties of their own. That is a matter for those laws, not the DPDP Act.

## Which lawful basis covers treatment?

s.4(1) allows only two bases: consent, or one of the "certain legitimate uses" in s.7. The list is closed. Unlike the GDPR, there is no clause for providing health care.

- **Emergencies.** s.7(f) covers "responding to a medical emergency involving a threat to the life or immediate threat to the health" of the patient "or any other individual". An unconscious patient brought into casualty is covered. A routine OPD visit is not.
- **Epidemics.** s.7(g) covers treatment "during an epidemic, outbreak of disease, or any other threat to public health". It is not an everyday ground.
- **Everyday care.** s.7(a) covers data the patient "has voluntarily provided" for a specified purpose, until she says she does not consent. Its pharmacy illustration is the nearest analogy: a buyer gives her number for a receipt, and the shop may use it for that. A patient who gives her details at registration to be treated fits the same pattern. This is a reading, not a holding. There are no Board decisions yet, so it is untested.

s.7(a) stops at the purpose she gave the data for. Appointment reminders for her own follow-up are arguably inside it. A health-camp promotion, a newsletter or a records-sharing link she did not ask for is not.

## Consent or s.7(a) for the treatment record?

You can also take consent for treatment. If you do, it must meet s.6(1), come with a notice under s.5(1), and be as easy to withdraw as to give (s.6(4)). Withdrawal does not force you to delete records another law requires you to keep. s.6(6) and s.8(7) both carve out processing required by law.

Either way, the patient keeps her access and correction rights. s.11(1) and s.12(1) cover consent "including consent as referred to in clause (a) of section 7".

A short notice at registration costs little even where you rely on s.7(a). In a Board proceeding on a consent-based purpose, the hospital must prove notice and consent (s.6(10)). Rule 3 says the notice must stand on its own, itemise the data, and give a link to withdraw, exercise rights and complain to the Board. Offer it in English or any Eighth Schedule language (s.5(3), s.6(3)). Rule 3 is secondary-sourced here, so verify it against the notified Gazette text.

## Children

A patient under 18 is a child under s.2(f). s.9(1) requires verifiable parental consent, but s.9(4) lets the Rules exempt classes of Fiduciaries and purposes. Rule 12 and the Fourth Schedule reportedly exempt healthcare providers for health services. Check the Fourth Schedule wording before relying on it. No exemption lifts s.9(2), which bars processing "likely to cause any detrimental effect on the well-being of a child".

## Worked example: a 30-bed hospital building an HMIS

The registration desk captures name, age, phone, address and complaint.

- **Treatment, billing and follow-up calls:** s.7(a), with a one-screen notice shown at the desk.
- **Casualty admissions without registration:** s.7(f). Complete the record and give the notice once the patient can take it.
- **WhatsApp health tips and camp invitations:** a separate, unticked opt-in under s.6(1). The outbox checks it before sending.
- **Linking records to an external health platform:** a separate purpose with its own consent and notice.
- **The HMIS vendor and cloud host:** Data Processors, hired only under a valid contract (s.8(2)). The hospital stays responsible for what they do (s.8(1)).
- **Security:** reasonable safeguards under s.8(5). Rule 6 sets the minimum, including encryption or masking, access control, logs and backups.
- **Retention:** erase when the purpose ends, unless a law requires you to keep the record (s.8(7)). Rule 8(3) separately requires keeping processing logs for at least one year.

## Breaches and penalties

Ransomware that locks the HMIS is a breach even if nothing leaks, because s.2(u) includes "loss of access". s.8(6) requires notice to the Board and to each affected patient, with no harm threshold. Rule 7 adds a detailed report to the Board within 72 hours. Rules 6, 7 and 8 are secondary-sourced; verify them against the notified Gazette text.

Under the Schedule, the ceiling is Rs 250 crore for failing to take reasonable security safeguards (s.8(5)) and Rs 200 crore for a missed breach notice (s.8(6)). These are maximums ("may extend to"), and the Board can penalise only a breach it finds "significant" (s.33(1)).

> Not legal advice. Verify statutory text against the Gazette of India and consult qualified
> Indian legal counsel before acting.
