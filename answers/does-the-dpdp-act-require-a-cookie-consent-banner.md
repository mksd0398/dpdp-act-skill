---
question: Does the DPDP Act require a cookie consent banner?
date: 2026-10-23
---
The DPDP Act never mentions cookies, so there is no "cookie law" in India. But a cookie or device ID that lets you single out a visitor is personal data under s.2(t), and the Act allows only two lawful bases for processing it: consent or a listed legitimate use (s.4(1)). For analytics, ad pixels and retargeting, that leaves consent. So in practice most Indian sites will need a real opt-in banner by **14 May 2027**, the date the notice and consent machinery becomes enforceable.

## Why a cookie counts as personal data

s.2(t) defines personal data as "any data about an individual who is identifiable by or in relation to such data". There is no separate identifiability threshold test. A first-party analytics ID, a Meta pixel event tied to a browser, or a logged-in session all relate to an individual you can tell apart from others. Anything digital is in scope under s.3(a). A cookie that holds no identifier at all, such as a site-wide language preference, is a weaker case.

## There is no "legitimate interests" escape route

This is where GDPR habits mislead. Under s.4(1) you process personal data only:

- with consent that meets s.6(1), or
- for one of the "certain legitimate uses" in the closed list in s.7.

There is no legitimate-interests ground. Analytics, A/B testing, ad attribution and retargeting fit none of the s.7 uses, so they need consent.

Strictly necessary cookies are different. A cart or login cookie serves the purpose the visitor asked for. s.7(a) covers data the person "voluntarily provided" for a specified purpose, and its pharmacy illustration (sending a receipt the buyer asked for) is the closest analogy. Reading s.7(a) to cover a session cookie is plausible but **untested**: there are no Board decisions yet. A defensible position is to treat strictly necessary cookies as s.7(a) and put everything else behind consent.

## What a valid banner has to look like

s.6(1) requires consent to be "free, specific, informed, unconditional and unambiguous with a clear affirmative action". That rules out the common Indian banner patterns:

- **"By continuing to browse you accept cookies."** Continued use is not a clear affirmative action.
- **Pre-ticked boxes** for analytics or marketing.
- **One "Accept all" with no per-purpose choice.** Consent must be specific to a purpose, and s.6(1) reads it down to what that purpose needs.
- **A cookie wall** that blocks the site unless the visitor accepts ad tracking. Making the service conditional on unnecessary processing undermines "free" and "unconditional".

Withdrawal must be as easy as giving consent (s.6(4)). If accepting took one click on a banner, a "Cookie settings" link that reopens the same choice on every page is the natural way to meet that. "Email us to opt out" is not.

The consent request must come with or after a notice (s.5(1)) that says what personal data is processed and why, how to withdraw, and how to complain to the Board. Rule 3 adds an itemised description of the data and a standalone, plain-language notice. Rule 3 is secondary-sourced in this reference, so verify against the notified Gazette text. In practice the banner links to a short cookie notice that lists each tool, what it collects, and the purpose.

The visitor must also be able to read the notice and the consent request in English or any Eighth Schedule language (s.5(3), s.6(3)).

## Your vendors do not carry this for you

If you add Google Analytics, Meta or a heatmap tool, you choose that processing. s.8(1) makes you responsible for compliance "in respect of any processing undertaken by it or on its behalf by a Data Processor", whatever the vendor contract says. The banner has to stop those scripts loading until the visitor opts in, not just record a choice.

## Children: consent does not fix tracking

If under-18s use your site, s.9(3) bars "tracking or behavioural monitoring of children or targeted advertising directed at children". This is an outright prohibition. A parent's consent does not cure it. A youth-facing site needs ad pixels and behavioural analytics switched off for child users, not a banner.

## Worked example: a Shopify store selling to India

A D2C store runs Shopify's session cookies, Google Analytics 4, a Meta pixel and a review widget.

- **Cart and checkout cookies:** treat as strictly necessary under s.7(a). No opt-in needed. List them in the notice.
- **GA4 and the Meta pixel:** consent only. Load them after the visitor clicks "Accept analytics" or "Accept marketing" as separate toggles. A "Reject" button sits next to "Accept".
- **Review widget:** if it sets tracking cookies of its own, it goes in the analytics or marketing bucket.
- **A "Cookie settings" link in the footer** reopens the choice at any time (s.6(4)).

## When this bites

Enforcement of the notice and consent duties starts on 14 May 2027, the commencement date for Rules 3 and 5 to 16. Nothing here is a fine today. The penalty for most breaches of these duties is a ceiling of up to Rs 50 crore under the Schedule's residual item, and only if the Board finds the breach "significant" (s.33(1)). Consent collected before commencement stays valid, but you owe those people a notice as soon as reasonably practicable (s.5(2)).

> Not legal advice. Verify statutory text against the Gazette of India and consult qualified
> Indian legal counsel before acting.
