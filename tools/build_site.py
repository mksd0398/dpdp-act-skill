#!/usr/bin/env python3
"""Build the static GitHub Pages site for dpdp-act-skill.

Reads the Markdown reference files that ship with the skill and emits an SEO-oriented
static site into docs/. Run:  python tools/build_site.py
"""

from __future__ import annotations

import html
import re
import shutil
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "skills" / "dpdp-analyze" / "references"
DOCS = ROOT / "docs"

SITE = "https://mksd0398.github.io/dpdp-act-skill"
SITE_NAME = "DPDP Act 2023 Reference"
AUTHOR = "Mayank Dsouza"
TODAY = date.today().isoformat()

MD = markdown.Markdown(extensions=["tables", "attr_list", "sane_lists"])

PAGES: list[tuple[str, str, str]] = []  # (url_path, title, changefreq)


# ---------------------------------------------------------------- helpers

def md2html(text: str) -> str:
    MD.reset()
    return MD.convert(text)


def strip_md(text: str) -> str:
    """Flatten Markdown to a plain sentence, for meta descriptions."""
    text = re.sub(r"^\s*[>#|-]+\s*", " ", text, flags=re.M)
    text = re.sub(r"[*_`\[\]]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def meta_desc(text: str, limit: int = 155) -> str:
    s = strip_md(text)
    if len(s) <= limit:
        return s
    cut = s[:limit]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut + "..."


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return s.strip("-")


def fit_title(prefix: str, heading: str, suffix: str = "", limit: int = 62) -> str:
    """Build 'prefix: heading (suffix)' trimmed to fit a search result."""
    full = f"{prefix}: {heading}" + (f" ({suffix})" if suffix else "")
    if len(full) <= limit:
        return full
    full = f"{prefix}: {heading}"
    if len(full) <= limit:
        return full
    room = limit - len(prefix) - 2
    trimmed = heading[:room]
    if " " in trimmed:
        trimmed = trimmed[: trimmed.rfind(" ")]
    return f"{prefix}: {trimmed}"


def write(path: str, content: str) -> None:
    p = DOCS / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------- template

def page(
    *,
    url: str,
    title: str,
    description: str,
    body: str,
    breadcrumbs: list[tuple[str, str | None]] | None = None,
    jsonld: str = "",
    changefreq: str = "monthly",
) -> None:
    """Render one page and register it in the sitemap."""
    PAGES.append((url, title, changefreq))
    canonical = f"{SITE}/{url}/" if url else f"{SITE}/"
    up = "../" * (url.count("/") + 1) if url else "./"

    crumbs = ""
    if breadcrumbs:
        # each entry is (label, absolute site path, or None for the current page)
        items = " &rsaquo; ".join(
            f'<a href="{up}{p}{"/" if p else ""}">{html.escape(t)}</a>' if p is not None
            else f"<span>{html.escape(t)}</span>"
            for t, p in breadcrumbs
        )
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb">{items}</nav>'
        ld_parts = []
        for i, (t, p) in enumerate(breadcrumbs):
            item = canonical if p is None else (f"{SITE}/{p}/" if p else f"{SITE}/")
            ld_parts.append(
                f'{{"@type":"ListItem","position":{i + 1},'
                f'"name":"{html.escape(t)}","item":"{item}"}}'
            )
        ld_items = ",".join(ld_parts)
        jsonld += (
            '<script type="application/ld+json">'
            f'{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{ld_items}]}}'
            "</script>"
        )

    doc = f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="{AUTHOR}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(description)}">
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='26'>&#9878;</text></svg>">
{jsonld}
</head>
<body>
<header class="site">
  <a class="brand" href="{up}">&#9878; DPDP Act 2023 Reference</a>
  <nav class="top">
    <a href="{up}act/">The Act</a>
    <a href="{up}rules/">The Rules</a>
    <a href="{up}penalties/">Penalties</a>
    <a href="{up}dpdp-vs-gdpr/">vs GDPR</a>
    <a href="{up}faq/">FAQ</a>
    <a href="https://github.com/mksd0398/dpdp-act-skill">GitHub</a>
  </nav>
</header>
<main>
{crumbs}
{body}
</main>
<footer class="site">
  <p><strong>Provenance.</strong> The Act text is verbatim from the Gazette of India, Extraordinary,
  Part II, Section 1, No. 25, dated 11 August 2023 (CG-DL-E-12082023-248045). The Rules content is
  assembled from the PIB release and cross-checked secondary sources; verify against the notified
  Gazette text before relying on it externally.</p>
  <p><strong>Not legal advice.</strong> This is a compliance reference. No lawyer-client relationship
  arises from its use.</p>
  <p>Maintained by <a href="https://github.com/mksd0398">{AUTHOR}</a>.
  <a href="https://github.com/mksd0398/dpdp-act-skill">Source and corrections on GitHub</a>.
  Last built {TODAY}.</p>
</footer>
</body>
</html>
"""
    write(f"{url}/index.html" if url else "index.html", doc)


# ---------------------------------------------------------------- parse the Act

def parse_act() -> tuple[list[dict], str]:
    text = (REF / "act-full-text.md").read_text(encoding="utf-8")
    chapter = ""
    sections: list[dict] = []
    schedule = ""

    blocks = re.split(r"\n(?=## |### Section )", text)
    for block in blocks:
        if block.startswith("## CHAPTER"):
            chapter = block.split("\n", 1)[0].removeprefix("## ").strip()
        if block.startswith("## THE SCHEDULE"):
            schedule = block.split("\n---\n")[0]
        m = re.match(r"### Section (\d+)\. (.+)", block)
        if m:
            num, heading = int(m.group(1)), m.group(2).strip()
            body = block.split("\n", 1)[1] if "\n" in block else ""
            body = re.split(r"\n---\n", body)[0].strip()
            sections.append(
                {"num": num, "heading": heading, "chapter": chapter, "body": body}
            )
    sections.sort(key=lambda s: s["num"])
    return sections, schedule


def parse_rules() -> list[dict]:
    text = (REF / "rules-2025.md").read_text(encoding="utf-8")
    out: list[dict] = []
    for block in re.split(r"\n(?=## \d+\. )", text):
        m = re.match(r"## (\d+)\. (.+)", block)
        if not m:
            continue
        body = block.split("\n", 1)[1] if "\n" in block else ""
        body = re.split(r"\n---\n", body)[0].strip()
        out.append({"num": int(m.group(1)), "heading": m.group(2).strip(), "body": body})
    return out


# ---------------------------------------------------------------- build

def build() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    sections, schedule = parse_act()
    rules = parse_rules()

    # ---- per-section pages -------------------------------------------------
    for i, s in enumerate(sections):
        prev_s = sections[i - 1] if i else None
        next_s = sections[i + 1] if i + 1 < len(sections) else None
        nav = '<nav class="pager">'
        if prev_s:
            nav += (
                f'<a class="prev" href="../section-{prev_s["num"]}/">&larr; Section '
                f'{prev_s["num"]}: {html.escape(prev_s["heading"])}</a>'
            )
        if next_s:
            nav += (
                f'<a class="next" href="../section-{next_s["num"]}/">Section '
                f'{next_s["num"]}: {html.escape(next_s["heading"])} &rarr;</a>'
            )
        nav += "</nav>"

        title = fit_title(f'Section {s["num"]} DPDP Act 2023', s["heading"], "full text")
        desc = meta_desc(
            f'Section {s["num"]} of the Digital Personal Data Protection Act, 2023, '
            f'{s["heading"]}. Full verbatim text. {strip_md(s["body"])}'
        )
        ld = (
            '<script type="application/ld+json">'
            f'{{"@context":"https://schema.org","@type":"Legislation",'
            f'"name":"Section {s["num"]}: {html.escape(s["heading"])}",'
            '"legislationType":"Act","legislationJurisdiction":"India",'
            '"legislationIdentifier":"Act 22 of 2023",'
            '"legislationDate":"2023-08-11",'
            '"isPartOf":{"@type":"Legislation","name":"The Digital Personal Data Protection Act, 2023"},'
            f'"inLanguage":"en-IN","url":"{SITE}/act/section-{s["num"]}/"}}'
            "</script>"
        )
        body = (
            f'<article>\n<p class="eyebrow">{html.escape(s["chapter"])}</p>\n'
            f'<h1>Section {s["num"]}. {html.escape(s["heading"])}</h1>\n'
            f'<p class="sub">The Digital Personal Data Protection Act, 2023 (Act 22 of 2023). '
            f"Verbatim text from the Gazette of India.</p>\n"
            f'<div class="statute">{md2html(s["body"])}</div>\n{nav}\n</article>'
        )
        page(
            url=f'act/section-{s["num"]}',
            title=title,
            description=desc,
            body=body,
            breadcrumbs=[("Home", ""), ("DPDP Act 2023", "act"), (f'Section {s["num"]}', None)],
            jsonld=ld,
        )

    # ---- Act index ---------------------------------------------------------
    by_chapter: dict[str, list[dict]] = {}
    for s in sections:
        by_chapter.setdefault(s["chapter"], []).append(s)
    toc = ""
    for ch, items in by_chapter.items():
        toc += f"<h2>{html.escape(ch)}</h2>\n<ul class='toc'>"
        for s in items:
            toc += (
                f'<li><a href="section-{s["num"]}/"><b>Section {s["num"]}</b> '
                f'{html.escape(s["heading"])}</a></li>'
            )
        toc += "</ul>\n"
    toc += f'<h2>The Schedule</h2><div class="statute">{md2html(schedule)}</div>'

    page(
        url="act",
        title="DPDP Act 2023 full text: all 44 sections, section by section",
        description=(
            "Complete verbatim text of India's Digital Personal Data Protection Act, 2023 "
            "(Act 22 of 2023). All 44 sections, 9 chapters and the penalties Schedule, "
            "reproduced from the Gazette of India."
        ),
        body=(
            "<h1>The Digital Personal Data Protection Act, 2023: full text</h1>"
            "<p class='sub'>Act 22 of 2023. Assented 11 August 2023. All 44 sections across 9 "
            "chapters, plus the Schedule of penalties, reproduced verbatim from the Gazette of "
            "India, Extraordinary, Part II, Section 1, No. 25.</p>" + toc
        ),
        breadcrumbs=[("Home", ""), ("DPDP Act 2023", None)],
        changefreq="yearly",
    )

    # ---- Rules -------------------------------------------------------------
    for r in rules:
        page(
            url=f'rules/{slugify(r["heading"])}',
            title=fit_title("DPDP Rules 2025", r["heading"]),
            description=meta_desc(
                f'{r["heading"]} under the Digital Personal Data Protection Rules, 2025. '
                f'{strip_md(r["body"])}'
            ),
            body=(
                f'<article><h1>{html.escape(r["heading"])}</h1>'
                "<p class='sub'>Digital Personal Data Protection Rules, 2025. Notified "
                "13 November 2025. Verify against the notified Gazette text before external use.</p>"
                f'<div class="statute">{md2html(r["body"])}</div></article>'
            ),
            breadcrumbs=[("Home", ""), ("DPDP Rules 2025", "rules"), (r["heading"], None)],
        )

    rules_toc = "<ul class='toc'>" + "".join(
        f'<li><a href="{slugify(r["heading"])}/">{html.escape(r["heading"])}</a></li>'
        for r in rules
    ) + "</ul>"
    page(
        url="rules",
        title="DPDP Rules 2025 explained: all 23 rules, 7 schedules and the commencement dates",
        description=(
            "The Digital Personal Data Protection Rules, 2025, notified 13 November 2025. "
            "All 23 rules and 7 schedules, the phased commencement dates, the 72-hour breach "
            "report, retention periods and Significant Data Fiduciary duties."
        ),
        body=(
            "<h1>The Digital Personal Data Protection Rules, 2025</h1>"
            "<p class='sub'>Notified by MeitY on 13 November 2025. 23 rules and 7 schedules, "
            "commencing in three tranches.</p>"
            "<div class='callout'><p><strong>When do the DPDP Rules come into force?</strong></p>"
            "<table><thead><tr><th>Effective</th><th>What commences</th></tr></thead><tbody>"
            "<tr><td><b>14 November 2025</b></td><td>Rules 1, 2 and 17 to 21. Data Protection "
            "Board machinery.</td></tr>"
            "<tr><td><b>14 November 2026</b></td><td>Rule 4. Consent Manager registration and "
            "obligations.</td></tr>"
            "<tr><td><b>14 May 2027</b></td><td>Rules 3, 5 to 16 and 22 to 23. Every substantive "
            "business obligation.</td></tr>"
            "</tbody></table></div>" + rules_toc
        ),
        breadcrumbs=[("Home", ""), ("DPDP Rules 2025", None)],
    )

    # ---- Penalties ---------------------------------------------------------
    page(
        url="penalties",
        title="DPDP Act penalties: the full Schedule, up to Rs 250 crore",
        description=(
            "Every penalty under India's DPDP Act 2023: Rs 250 crore for security failures, "
            "Rs 200 crore for breach notification and children's data, Rs 150 crore for "
            "Significant Data Fiduciaries. How the Data Protection Board decides the amount."
        ),
        body=(
            "<h1>DPDP Act penalties in full</h1>"
            "<p class='sub'>The Schedule to the Digital Personal Data Protection Act, 2023, "
            "read with section 33.</p>"
            "<div class='callout'><p>Every figure is a <strong>ceiling</strong>. The Act says "
            "&ldquo;may extend to&rdquo;. A penalty may only be imposed if the Data Protection "
            "Board finds, on conclusion of an inquiry, that the breach is "
            "<strong>&ldquo;significant&rdquo;</strong> under section 33(1). That word is "
            "undefined and there is no Board jurisprudence yet.</p></div>"
            f'<div class="statute">{md2html(schedule)}</div>'
            "<h2>How the Board sets the amount</h2>"
            "<p>Section 33(2) lists seven factors the Board must weigh:</p>"
            "<ol><li>the nature, gravity and duration of the breach;</li>"
            "<li>the type and nature of the personal data affected;</li>"
            "<li>the repetitive nature of the breach;</li>"
            "<li>whether the person realised a gain or avoided a loss;</li>"
            "<li>whether the person acted to mitigate, and how timely and effective that was;</li>"
            "<li>whether the penalty is proportionate and effective as a deterrent;</li>"
            "<li>the likely impact of the penalty on the person.</li></ol>"
            "<p>Factors 5, 6 and 7 are where mitigation arguments live.</p>"
            "<h2>Where the money goes</h2>"
            "<p>All penalties are credited to the <strong>Consolidated Fund of India</strong> "
            "(section 34). The DPDP Act gives affected individuals <strong>no right to "
            "compensation</strong>, civil courts are barred from these matters (section 39), and "
            "section 43A of the IT Act, which used to provide a compensation route, was repealed "
            "by section 44(2)(a).</p>"
            "<h2>Appeals</h2>"
            "<p>An appeal lies to the <strong>Telecom Disputes Settlement and Appellate Tribunal "
            "(TDSAT)</strong> within <strong>60 days</strong> of receiving the order, extendable "
            "for sufficient cause (section 29). TDSAT endeavours to dispose of appeals within six "
            "months.</p>"
            "<h2>Blocking orders</h2>"
            "<p>After the Board has penalised a Data Fiduciary in <strong>two or more "
            "instances</strong>, it may advise the Central Government to block public access to "
            "the service in the interests of the general public (section 37). Intermediaries are "
            "bound to comply.</p>"
            "<p>There are <strong>no criminal offences and no imprisonment</strong> anywhere in "
            "the DPDP Act.</p>"
            "<p><a href=\"../act/section-33/\">Read section 33 in full &rarr;</a></p>"
        ),
        breadcrumbs=[("Home", ""), ("Penalties", None)],
    )

    # ---- DPDP vs GDPR ------------------------------------------------------
    page(
        url="dpdp-vs-gdpr",
        title="DPDP Act vs GDPR: 15 differences that change your compliance programme",
        description=(
            "India's DPDP Act 2023 compared with the GDPR. No sensitive data category, no "
            "legitimate interests, no portability, no compensation, child age 18, and breach "
            "notification with no harm threshold."
        ),
        body=(
            "<h1>DPDP Act 2023 vs GDPR</h1>"
            "<p class='sub'>The differences that actually change what you build. Importing a GDPR "
            "programme wholesale over-builds rights machinery and under-builds consent, notice, "
            "breach readiness and Indian-language support.</p>"
            + md2html(
                """
| Topic | DPDP Act 2023 | GDPR |
|---|---|---|
| Lawful bases | **2**: consent (s.6) or the closed s.7 list | 6, including legitimate interests |
| Legitimate interests | **None** | Art 6(1)(f) |
| Sensitive data category | **None**. Health, biometric, financial and caste get no special tier | Art 9 special categories |
| Extraterritorial trigger | Offering goods or services to India (s.3(b)) | Offering **or monitoring behaviour** |
| Child age | **Under 18** (s.2(f)) | 16, states may lower to 13 |
| Targeted ads at children | **Prohibited outright** (s.9(3)) | Restricted, not banned |
| Breach notification threshold | **None**. Board and every affected individual (s.8(6)) | Risk-based |
| Breach clock | Individuals without delay; Board detailed report in 72 hours (Rule 7) | 72 hours to the DPA |
| DPO | Notified Significant Data Fiduciaries only (s.10(2)(a)) | Wider Art 37 triggers |
| Data portability | **Absent** | Art 20 |
| Right to object / automated decisions | **Absent** | Arts 21, 22 |
| Compensation to individuals | **Absent**. Penalties go to the Consolidated Fund (s.34) | Art 82 |
| Cross-border transfers | Negative list, permitted by default (s.16) | Adequacy, SCCs, BCRs |
| Regulator | Adjudicatory Board with **no rule-making power** | Independent DPAs that issue guidance |
| Duties on individuals | **Yes** (s.15), penalty up to Rs 10,000 | No |
| Criminal liability | **None** | Member-State dependent |
| Maximum penalty | Rs 250 crore | 4% of global turnover or EUR 20m |
"""
            )
            + "<h2>The one sentence version</h2>"
            "<p>The DPDP Act is <strong>consent-heavy, rights-light, State-friendly, and has no "
            "sensitive-data tier</strong>.</p>"
            "<h2>What GDPR-trained teams most often get wrong</h2>"
            "<ol>"
            "<li>Reaching for <b>legitimate interests</b>. It does not exist in the DPDP Act.</li>"
            "<li>Applying a <b>harm threshold</b> to breach notification. There isn't one.</li>"
            "<li>Building <b>portability</b> and <b>automated-decision</b> machinery nobody needs.</li>"
            "<li>Assuming a large company is automatically a <b>Significant Data Fiduciary</b>. "
            "It is not, until the Central Government notifies it.</li>"
            "<li>Using <b>13 or 16</b> as the child age instead of 18.</li>"
            "<li>Forgetting the <b>Eighth Schedule language</b> requirement: notice and consent "
            "must be available in English or any of the 22 scheduled languages "
            "(ss.5(3), 6(3)).</li>"
            "<li>Missing that the <b>burden of proving valid notice and consent sits on the "
            "business</b> (s.6(10)).</li>"
            "</ol>"
        ),
        breadcrumbs=[("Home", ""), ("DPDP vs GDPR", None)],
    )

    # ---- FAQ ---------------------------------------------------------------
    faqs = [
        (
            "Is the DPDP Act in force?",
            "Partly. The Act received Presidential assent on 11 August 2023, but section 1(2) "
            "permits staggered commencement. Data Protection Board machinery has been live since "
            "14 November 2025. Consent Manager rules commence 14 November 2026. The substantive "
            "obligations on businesses, covering notice, security, breach reporting, retention, "
            "children's data and rights, commence on 14 May 2027.",
        ),
        (
            "Does the DPDP Act apply to companies outside India?",
            "Only where the processing is connected to offering goods or services to Data "
            "Principals within India, under section 3(b). Unlike the GDPR, merely monitoring the "
            "behaviour of people in India is not a trigger.",
        ),
        (
            "Does the DPDP Act require data localisation?",
            "No, not in the Act itself. Section 16 is a negative list: the Central Government may "
            "notify countries to which transfer is restricted, and none has been notified. Rule "
            "13(4) creates a targeted localisation duty for notified Significant Data Fiduciaries "
            "only, over categories the Government specifies on a committee's recommendation. "
            "Sectoral regulators such as the RBI localise independently, preserved by section 16(2).",
        ),
        (
            "Who is a Significant Data Fiduciary?",
            "Only an entity that the Central Government has notified as one under section 10(1). "
            "You cannot self-classify, and size alone does not make you one. The Government "
            "assesses factors including volume and sensitivity of data, risk to Data Principal "
            "rights, sovereignty, risk to electoral democracy, security of the State and public "
            "order.",
        ),
        (
            "Do we need a Data Protection Officer in India?",
            "Only if you are notified as a Significant Data Fiduciary. That DPO must be based in "
            "India, be an individual, and be responsible to the board of directors or similar "
            "governing body, under section 10(2)(a). Every other Data Fiduciary need only publish "
            "the business contact information of a person who can answer questions about "
            "processing, under section 8(9) and Rule 9.",
        ),
        (
            "How fast must we report a data breach under the DPDP Act?",
            "Affected individuals must be told without delay under Rule 7(1). The Data Protection "
            "Board gets an initial intimation without delay, then a detailed report within 72 "
            "hours of you becoming aware, under Rule 7(2). There is no harm or materiality "
            "threshold, so every personal data breach is reportable, including loss of access, "
            "which brings ransomware into scope.",
        ),
        (
            "What is the maximum penalty under the DPDP Act?",
            "Rs 250 crore, for failing to take reasonable security safeguards under section 8(5). "
            "Failure to notify a breach and breaches of children's data obligations each carry up "
            "to Rs 200 crore, Significant Data Fiduciary breaches up to Rs 150 crore, and any "
            "other breach up to Rs 50 crore. All figures are ceilings, not tariffs.",
        ),
        (
            "What lawful bases exist under the DPDP Act?",
            "Exactly two, under section 4(1): the Data Principal's consent meeting section 6, or "
            "one of the closed list of certain legitimate uses in section 7(a) to (i). There is no "
            "legitimate interests balancing test.",
        ),
        (
            "Does the DPDP Act have a sensitive personal data category?",
            "No. Unlike the GDPR and unlike the earlier SPDI Rules, the DPDP Act creates no "
            "special category. Health, biometric, financial and caste data receive no additional "
            "treatment under this Act, although sectoral law may still impose extra duties.",
        ),
        (
            "What age is a child under the DPDP Act?",
            "Anyone who has not completed 18 years, under section 2(f). Processing a child's data "
            "requires verifiable parental consent, and tracking, behavioural monitoring and "
            "targeted advertising directed at children are prohibited outright under section 9(3), "
            "which consent cannot cure.",
        ),
        (
            "Are the SPDI Rules 2011 still valid?",
            "Their footing is materially undermined. Section 44(2) of the DPDP Act omitted both "
            "section 43A of the IT Act, which the SPDI Rules implemented, and section 87(2)(ob), "
            "the rule-making power behind them. Do not cite them as unqualified live obligations.",
        ),
        (
            "Can individuals claim compensation under the DPDP Act?",
            "No. Penalties imposed by the Board are credited to the Consolidated Fund of India "
            "under section 34, civil courts are barred from matters the Board is empowered over "
            "under section 39, and the old IT Act section 43A compensation route was repealed.",
        ),
    ]
    faq_ld_items = ",".join(
        f'{{"@type":"Question","name":{_json(q)},"acceptedAnswer":{{"@type":"Answer","text":{_json(a)}}}}}'
        for q, a in faqs
    )
    faq_body = "<h1>DPDP Act 2023: frequently asked questions</h1>" + "".join(
        f"<h2>{html.escape(q)}</h2><p>{html.escape(a)}</p>" for q, a in faqs
    )
    page(
        url="faq",
        title="DPDP Act 2023 FAQ: in force date, penalties, DPO, localisation, breach reporting",
        description=(
            "Answers on India's DPDP Act 2023: when it comes into force, whether it applies "
            "outside India, data localisation, who needs a DPO, breach reporting timelines, "
            "penalties and the status of the SPDI Rules."
        ),
        body=faq_body,
        breadcrumbs=[("Home", ""), ("FAQ", None)],
        jsonld=(
            '<script type="application/ld+json">'
            f'{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_ld_items}]}}'
            "</script>"
        ),
    )

    # ---- Landing -----------------------------------------------------------
    page(
        url="",
        title="DPDP Act 2023: full text, Rules 2025, penalties and a compliance checklist",
        description=(
            "Complete verbatim text of India's Digital Personal Data Protection Act, 2023 and the "
            "DPDP Rules, 2025. All 44 sections, penalties, commencement dates, a compliance "
            "checklist and a free Claude Code skill that analyses your privacy programme."
        ),
        body=(
            "<h1>India's Digital Personal Data Protection Act, 2023</h1>"
            "<p class='sub'>The full statute, the Rules, and a working compliance reference. "
            "All 44 sections verbatim from the Gazette of India, all 23 Rules of 2025, the "
            "penalty Schedule, and an installable AI skill that analyses privacy notices, consent "
            "flows and vendor contracts against the actual sections.</p>"
            "<div class='cards'>"
            "<a class='card' href='act/'><h3>The Act, section by section</h3>"
            "<p>All 44 sections and 9 chapters, verbatim, with every Illustration.</p></a>"
            "<a class='card' href='rules/'><h3>The Rules, 2025</h3>"
            "<p>23 rules, 7 schedules, and the three commencement dates that set your deadline.</p></a>"
            "<a class='card' href='penalties/'><h3>Penalties</h3>"
            "<p>The full Schedule, up to Rs 250 crore, and how the Board sets the amount.</p></a>"
            "<a class='card' href='dpdp-vs-gdpr/'><h3>DPDP vs GDPR</h3>"
            "<p>The 15 differences that change what you build.</p></a>"
            "<a class='card' href='faq/'><h3>FAQ</h3>"
            "<p>In force date, DPO, localisation, breach clocks, SPDI Rules.</p></a>"
            "<a class='card' href='https://github.com/mksd0398/dpdp-act-skill'><h3>The skill</h3>"
            "<p>Install into Claude Code and analyse your own privacy programme.</p></a>"
            "</div>"
            "<h2>When does the DPDP Act come into force?</h2>"
            "<table><thead><tr><th>Effective</th><th>What commences</th></tr></thead><tbody>"
            "<tr><td><b>14 November 2025</b></td><td>Data Protection Board machinery "
            "(Rules 1, 2, 17 to 21).</td></tr>"
            "<tr><td><b>14 November 2026</b></td><td>Consent Manager registration (Rule 4).</td></tr>"
            "<tr><td><b>14 May 2027</b></td><td><b>Every substantive business obligation</b>: "
            "notice, security safeguards, breach intimation, retention and erasure, children's "
            "consent, Significant Data Fiduciary duties, rights machinery, transfers.</td></tr>"
            "</tbody></table>"
            "<p><b>14 May 2027 is the date that matters for a compliance programme.</b></p>"
            "<h2>Ten things most people get wrong about the DPDP Act</h2>"
            "<ol>"
            "<li>There are only <b>two lawful bases</b>: consent, or the closed section 7 list. "
            "There is <b>no legitimate interests</b> ground.</li>"
            "<li>There is <b>no sensitive personal data category</b>.</li>"
            "<li>A <b>child is anyone under 18</b>, not 13 or 16.</li>"
            "<li><b>Targeted advertising to children is banned outright</b>; consent does not cure it.</li>"
            "<li><b>Breach notification has no harm threshold</b>, and covers loss of access.</li>"
            "<li>Only <b>notified Significant Data Fiduciaries</b> need a DPO.</li>"
            "<li>The Act <b>does not mandate data localisation</b>.</li>"
            "<li>Individuals get <b>no compensation</b>; penalties go to the Consolidated Fund.</li>"
            "<li>There is <b>no portability right</b> and no right against automated decisions.</li>"
            "<li><b>Data Principals have enforceable duties</b>, with a Rs 10,000 penalty.</li>"
            "</ol>"
            "<h2>Install the analysis skill</h2>"
            "<pre><code>git clone https://github.com/mksd0398/dpdp-act-skill.git\n"
            "cp -r dpdp-act-skill/skills/dpdp-analyze ~/.claude/skills/</code></pre>"
            "<p>Then ask: <i>&ldquo;Is this privacy policy DPDP compliant?&rdquo;</i>, "
            "<i>&ldquo;Do we need a DPO in India?&rdquo;</i>, or "
            "<i>&ldquo;We had a breach, what do we have to do?&rdquo;</i></p>"
        ),
        jsonld=(
            '<script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"WebSite",'
            f'"name":"{SITE_NAME}","url":"{SITE}/",'
            f'"author":{{"@type":"Person","name":"{AUTHOR}"}},'
            '"about":{"@type":"Legislation","name":"The Digital Personal Data Protection Act, 2023",'
            '"legislationIdentifier":"Act 22 of 2023","legislationJurisdiction":"India",'
            '"legislationDate":"2023-08-11"}}'
            "</script>"
        ),
        changefreq="weekly",
    )

    # ---- assets, sitemap, robots ------------------------------------------
    write("assets/style.css", CSS)
    write(".nojekyll", "")

    urls = "".join(
        f"<url><loc>{SITE}/{u}/</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>{cf}</changefreq>"
        f"<priority>{'1.0' if not u else '0.8' if u.count('/') == 0 else '0.6'}</priority></url>"
        for u, _t, cf in PAGES
    ).replace(f"{SITE}//", f"{SITE}/")
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>\n",
    )
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

    print(f"Built {len(PAGES)} pages into {DOCS}")


def _json(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


CSS = """
:root{--bg:#fff;--fg:#16181d;--mut:#5b6270;--line:#e3e6ec;--acc:#0b4f9e;--soft:#f6f8fb;--code:#f2f4f8}
@media (prefers-color-scheme:dark){
:root{--bg:#0f1115;--fg:#e8eaef;--mut:#9aa3b2;--line:#252a33;--acc:#7fb3ff;--soft:#161a21;--code:#1a1f27}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
header.site{border-bottom:1px solid var(--line);padding:14px 20px;display:flex;gap:18px;
flex-wrap:wrap;align-items:center;position:sticky;top:0;background:var(--bg);z-index:9}
.brand{font-weight:700;text-decoration:none;color:var(--fg);font-size:15px}
nav.top{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;margin-left:auto}
nav.top a{color:var(--mut);text-decoration:none}
nav.top a:hover{color:var(--acc)}
main{max-width:820px;margin:0 auto;padding:28px 20px 64px}
h1{font-size:clamp(26px,4vw,36px);line-height:1.2;margin:.2em 0 .35em;letter-spacing:-.02em}
h2{font-size:22px;margin:2em 0 .5em;line-height:1.3;letter-spacing:-.01em}
h3{font-size:17px;margin:1.6em 0 .4em}
p,li{color:var(--fg)}
a{color:var(--acc)}
.eyebrow{text-transform:uppercase;letter-spacing:.09em;font-size:11px;color:var(--mut);
font-weight:600;margin:0}
.sub{color:var(--mut);font-size:16px;margin-top:0}
.crumbs{font-size:13px;color:var(--mut);margin-bottom:18px}
.crumbs a{color:var(--mut);text-decoration:none}
.crumbs a:hover{color:var(--acc)}
.statute{border-left:3px solid var(--line);padding-left:20px;margin:22px 0}
.statute blockquote{margin:14px 0;padding:12px 16px;background:var(--soft);
border-left:3px solid var(--acc);border-radius:0 6px 6px 0;font-size:15px}
.statute blockquote p{margin:.4em 0}
ul.toc{list-style:none;padding:0;margin:.5em 0 1.5em}
ul.toc li{border-bottom:1px solid var(--line)}
ul.toc a{display:block;padding:9px 2px;text-decoration:none;color:var(--fg);font-size:15px}
ul.toc a:hover{color:var(--acc);background:var(--soft)}
ul.toc b{color:var(--acc);margin-right:8px;font-variant-numeric:tabular-nums}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:26px 0}
.card{display:block;padding:16px 18px;border:1px solid var(--line);border-radius:10px;
text-decoration:none;color:var(--fg);background:var(--soft)}
.card:hover{border-color:var(--acc)}
.card h3{margin:0 0 6px;font-size:16px;color:var(--acc)}
.card p{margin:0;font-size:14px;color:var(--mut)}
.callout{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:4px 18px;
margin:22px 0}
table{border-collapse:collapse;width:100%;margin:18px 0;font-size:15px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
th{background:var(--soft);font-weight:600}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13.5px}
pre{background:var(--code);padding:14px 16px;border-radius:8px;overflow-x:auto;
border:1px solid var(--line)}
code{background:var(--code);padding:2px 5px;border-radius:4px}
pre code{background:none;padding:0}
.pager{display:flex;justify-content:space-between;gap:16px;margin:36px 0 0;padding-top:20px;
border-top:1px solid var(--line);font-size:14px;flex-wrap:wrap}
.pager a{text-decoration:none;max-width:46%}
.pager .next{margin-left:auto;text-align:right}
footer.site{border-top:1px solid var(--line);margin-top:56px;padding:24px 20px 44px;
font-size:13px;color:var(--mut)}
footer.site p{max-width:820px;margin:0 auto .8em}
footer.site a{color:var(--mut)}
"""


if __name__ == "__main__":
    build()
