#!/usr/bin/env python3
"""Build the static GitHub Pages site for dpdp-act-skill.

Reads the Markdown reference files that ship with the skill and emits a static site into docs/,
built for three kinds of reader at once:

- search engines (SEO): titles, descriptions, canonical URLs, sitemap, structured data;
- answer boxes and voice assistants (AEO): question-shaped headings with direct answers,
  FAQPage and DefinedTermSet markup, deep-linkable anchors;
- AI answer engines such as ChatGPT, Perplexity, Gemini and Claude (GEO): llms.txt,
  llms-full.txt, a Markdown twin of every content page, and a section or rule citation on every
  claim so that a model quoting the page quotes the anchor too.

Run:  python tools/build_site.py
Set SITE_URL to build for a custom domain, e.g.  SITE_URL=https://dpdp.example.in
"""

from __future__ import annotations

import functools
import html
import json
import os
import re
import shutil
import subprocess
import zipfile
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "skills" / "dpdp-analyze" / "references"
STATIC = ROOT / "tools" / "static"
DOCS = ROOT / "docs"
THIS = Path(__file__).resolve()
ACT_MD = REF / "act-full-text.md"
RULES_MD = REF / "rules-2025.md"
INDEX_MD = REF / "section-index.md"
DOCTRINE_MD = REF / "doctrine.md"
CHECKLIST_MD = REF / "compliance-checklist.md"
SKILL_MD = ROOT / "skills" / "dpdp-analyze" / "SKILL.md"
DISCLAIMER_MD = ROOT / "DISCLAIMER.md"

SITE = os.environ.get("SITE_URL", "https://mksd0398.github.io/dpdp-act-skill").rstrip("/")
REPO = "https://github.com/mksd0398/dpdp-act-skill"
SITE_NAME = "DPDP Act 2023 Reference"
AUTHOR = "Mayank Dsouza"
AUTHOR_URL = "https://github.com/mksd0398"
TODAY = date.today().isoformat()
OG_IMAGE = f"{SITE}/assets/og.jpg"
SKILL_PATH = "claude-code-skill"
SKILL_DIR = ROOT / "skills" / "dpdp-analyze"
ZIP_NAME = "dpdp-analyze.zip"

WEBSITE_ID = f"{SITE}/#website"
PERSON_ID = f"{SITE}/#author"
ACT_ID = f"{SITE}/act/#legislation"
RULES_ID = f"{SITE}/rules/#legislation"
SKILL_ID = f"{SITE}/{SKILL_PATH}/#software"

INSTALL = "/plugin marketplace add mksd0398/dpdp-act-skill\n/plugin install dpdp-analyze@dpdp"
INSTALL_MANUAL = (
    "git clone https://github.com/mksd0398/dpdp-act-skill.git\n"
    "cp -r dpdp-act-skill/skills/dpdp-analyze ~/.claude/skills/"
)
NOT_ADVICE = (
    "Not legal advice. Educational compliance reference only; no lawyer-client relationship "
    "arises from its use and the author is not a lawyer. Verify statutory text against the "
    "Gazette of India and consult qualified Indian legal counsel before acting."
)

MD = markdown.Markdown(extensions=["tables", "attr_list", "sane_lists", "toc"])

PAGES: list[dict] = []  # every rendered page, for the sitemap and llms.txt


# ---------------------------------------------------------------- helpers

def md2html(text: str) -> str:
    MD.reset()
    return MD.convert(text)


def strip_md(text: str) -> str:
    """Flatten Markdown to a plain sentence, for meta descriptions and JSON-LD."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^\s*[>#|-]+\s*", " ", text, flags=re.M)
    text = re.sub(r"[*_`\[\]|]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def meta_desc(text: str, limit: int = 155) -> str:
    s = strip_md(text)
    if len(s) <= limit:
        return s
    cut = s[:limit]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(",;:") + "..."


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


def esc(s: str) -> str:
    return html.escape(s, quote=True)


@functools.lru_cache(maxsize=None)
def _git_date(path: Path) -> str:
    rel = str(path.relative_to(ROOT))
    try:
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if dirty:
            return TODAY
        d = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return TODAY
    return d or TODAY


def last_modified(*sources: Path) -> str:
    """The date a page's content last changed: the newest commit touching any of its sources,
    or today for uncommitted work. Keeps sitemap lastmod honest instead of stamping every page
    with the build date."""
    return max((_git_date(p) for p in sources), default=TODAY)


# ---------------------------------------------------------------- citation links

# "IT Act s.43A", "TRAI Act s.14(c)", and the second half of "IBC s.3(12) and s.3(14)"
_OTHER_ACT = re.compile(
    r"(?:IT Act|RTI Act|TRAI Act|IBC|IPC|2005|Copyright Act, 1957)\W{0,3} "
    r"(?:s\.[\w()]+(?:,| and| or) )?$"
)
_SEC_RE = re.compile(r"(?<![\w.\[/])s\.(\d{1,2})((?:\([0-9a-z]+\))*)(?![\w])")
_RULE_RE = re.compile(r"(?<![\w\[/])(Rules?) (\d{1,2})((?:\([0-9a-z]+\))*)(?![\w])")
RULE_PAGES: dict[int, str] = {}  # rule number -> rules/<slug>, filled in by build()


def link_refs(text: str, up: str, *, skip_section: int | None = None,
              skip_rule_page: str | None = None) -> str:
    """Turn every 's.8(6)' and 'Rule 7(2)' in commentary Markdown into a link to that section or
    rule page. References to other statutes ('IT Act s.43A', 'IBC s.3(12)') are left alone."""

    def sec(m: re.Match) -> str:
        n = int(m.group(1))
        if not 1 <= n <= 44 or n == skip_section:
            return m.group(0)
        if _OTHER_ACT.search(text[max(0, m.start() - 40): m.start()]):
            return m.group(0)
        return f"[{m.group(0)}]({up}act/section-{n}/)"

    def rule(m: re.Match) -> str:
        target = RULE_PAGES.get(int(m.group(2)))
        if not target or target == skip_rule_page:
            return m.group(0)
        return f"[{m.group(0)}]({up}{target}/)"

    text = _SEC_RE.sub(sec, text)
    return _RULE_RE.sub(rule, text)


# ---------------------------------------------------------------- structured data

PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": AUTHOR,
    "url": AUTHOR_URL,
    "sameAs": [AUTHOR_URL],
}
WEBSITE = {
    "@type": "WebSite",
    "@id": WEBSITE_ID,
    "name": SITE_NAME,
    "alternateName": ["DPDP Act reference", "dpdp-act-skill"],
    "url": f"{SITE}/",
    "inLanguage": "en-IN",
    "description": (
        "Verbatim text of India's Digital Personal Data Protection Act, 2023, the DPDP Rules, "
        "2025, a compliance checklist, and a free open-source AI skill for DPDP analysis."
    ),
    "author": {"@id": PERSON_ID},
    "publisher": {"@id": PERSON_ID},
}
ACT_NODE = {
    "@type": "Legislation",
    "@id": ACT_ID,
    "name": "The Digital Personal Data Protection Act, 2023",
    "alternateName": ["DPDP Act", "DPDP Act 2023", "DPDPA", "Digital Personal Data Protection Act"],
    "legislationIdentifier": "Act No. 22 of 2023",
    "legislationType": "Act",
    "legislationJurisdiction": "India",
    "legislationDate": "2023-08-11",
    "legislationPassedBy": {"@type": "GovernmentOrganization", "name": "Parliament of India"},
    "legislationLegalForce": "https://schema.org/PartiallyInForce",
    "inLanguage": "en-IN",
    "url": f"{SITE}/act/",
}
RULES_NODE = {
    "@type": "Legislation",
    "@id": RULES_ID,
    "name": "The Digital Personal Data Protection Rules, 2025",
    "alternateName": ["DPDP Rules", "DPDP Rules 2025"],
    "legislationType": "Rules",
    "legislationJurisdiction": "India",
    "legislationDate": "2025-11-13",
    "legislationResponsible": {
        "@type": "GovernmentOrganization",
        "name": "Ministry of Electronics and Information Technology",
    },
    "legislationLegalForce": "https://schema.org/PartiallyInForce",
    "isBasedOn": {"@id": ACT_ID},
    "inLanguage": "en-IN",
    "url": f"{SITE}/rules/",
}
SKILL_NODE = {
    "@type": "SoftwareApplication",
    "@id": SKILL_ID,
    "name": "dpdp-analyze: DPDP Act 2023 analysis skill for Claude Code",
    "alternateName": ["dpdp-analyze", "DPDP Act Claude skill", "DPDP compliance AI skill"],
    "applicationCategory": "BusinessApplication",
    "applicationSubCategory": "Legal compliance, privacy, AI agent skill",
    "operatingSystem": "Windows, macOS, Linux (via Claude Code)",
    "softwareRequirements": "Claude Code, or any agent that loads SKILL.md skills",
    "description": (
        "Open-source Claude Code skill that analyses privacy notices, consent flows, vendor "
        "contracts and whole products against India's DPDP Act 2023 and DPDP Rules 2025, citing "
        "a section or rule for every claim."
    ),
    "url": f"{SITE}/{SKILL_PATH}/",
    "downloadUrl": f"{SITE}/downloads/{ZIP_NAME}",
    "codeRepository": REPO,
    "installUrl": f"{SITE}/{SKILL_PATH}/#install",
    "license": "https://opensource.org/licenses/MIT",
    "isAccessibleForFree": True,
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"},
    "author": {"@id": PERSON_ID},
    "about": [{"@id": ACT_ID}, {"@id": RULES_ID}],
    "image": OG_IMAGE,
}


def jsonld(graph: list[dict]) -> str:
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json">{data.replace("</", "<" + chr(92) + "/")}</script>'


# ---------------------------------------------------------------- template

NAV = [
    ("act/", "The Act", ""),
    ("rules/", "The Rules", ""),
    ("dpdp-act-explained/", "Explained", ""),
    ("compliance-checklist/", "Checklist", ""),
    ("penalties/", "Penalties", ""),
    ("dpdp-vs-gdpr/", "vs GDPR", ""),
    ("glossary/", "Glossary", ""),
    ("faq/", "FAQ", ""),
    (f"{SKILL_PATH}/", "AI skill", "cta"),
    ("disclaimer/", "Disclaimer", ""),
]


def page(
    *,
    url: str,
    title: str,
    description: str,
    body: str,
    sources: tuple[Path, ...],
    breadcrumbs: list[tuple[str, str | None]] | None = None,
    graph: list[dict] | None = None,
    page_type: str = "WebPage",
    page_extra: dict | None = None,
    changefreq: str = "monthly",
    markdown_twin: str | None = None,
    llms_group: str | None = None,
    og_type: str = "article",
) -> None:
    """Render one page, its optional Markdown twin, and register it for sitemap and llms.txt."""
    canonical = f"{SITE}/{url}/" if url else f"{SITE}/"
    up = "../" * (url.count("/") + 1) if url else "./"
    lastmod = last_modified(*sources)
    PAGES.append(
        {"url": url, "title": title, "desc": description, "changefreq": changefreq,
         "lastmod": lastmod, "group": llms_group, "md": markdown_twin is not None}
    )

    nodes: list[dict] = [WEBSITE, PERSON]
    webpage = {
        "@type": page_type,
        "@id": f"{canonical}#webpage",
        "url": canonical,
        "name": title,
        "description": description,
        "inLanguage": "en-IN",
        "isPartOf": {"@id": WEBSITE_ID},
        "dateModified": lastmod,
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": PERSON_ID},
        "primaryImageOfPage": {"@type": "ImageObject", "url": OG_IMAGE, "width": 1200, "height": 630},
    }
    webpage.update(page_extra or {})
    nodes.append(webpage)

    crumbs = ""
    if breadcrumbs:
        # each entry is (label, site path, or None for the current page)
        items = " &rsaquo; ".join(
            f'<a href="{up}{p}{"/" if p else ""}">{esc(t)}</a>' if p is not None
            else f"<span>{esc(t)}</span>"
            for t, p in breadcrumbs
        )
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb">{items}</nav>'
        nodes.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": t,
                 "item": canonical if p is None else (f"{SITE}/{p}/" if p else f"{SITE}/")}
                for i, (t, p) in enumerate(breadcrumbs)
            ],
        })
    nodes.extend(graph or [])

    alt_md = '<link rel="alternate" type="text/markdown" href="index.md">\n' if markdown_twin else ""
    modified = f'<meta property="article:modified_time" content="{lastmod}">\n' if og_type == "article" else ""
    nav = "\n    ".join(
        f'<a{" class=" + chr(34) + c + chr(34) if c else ""} href="{up}{p}">{t}</a>' for p, t, c in NAV
    )

    doc = f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="{AUTHOR}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="theme-color" content="#0b4f9e">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_IN">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DPDP Act 2023 and DPDP Rules 2025: full text, compliance checklist and a free Claude Code skill">
{modified}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{up}assets/style.css">
{alt_md}<link rel="sitemap" type="application/xml" href="{up}sitemap.xml">
{jsonld(nodes)}
</head>
<body>
<header class="site">
  <a class="brand" href="{up}">&#9878; DPDP Act 2023 Reference</a>
  <nav class="top" aria-label="Main">
    {nav}
    <a href="{REPO}">GitHub</a>
  </nav>
</header>
<main>
<aside class="disclaimer" role="note">
  <strong>&#9888; Not legal advice.</strong> This is an educational compliance reference, not legal
  advice, and no lawyer-client relationship arises from its use. The author is not a lawyer.
  Verify all statutory text against the Gazette of India and consult qualified Indian legal counsel
  before acting. <a href="{up}disclaimer/">Full disclaimer</a>.
</aside>
{crumbs}
{body}
<p class="updated">Last updated <time datetime="{lastmod}">{lastmod}</time>.
<a href="{REPO}/issues">Report an error</a>.</p>
</main>
<footer class="site">
  <p class="promo"><strong>Ask AI about the DPDP Act and get the section number back.</strong>
  <a href="{up}{SKILL_PATH}/">Install the free dpdp-analyze skill for Claude Code</a>: it answers
  from the verbatim Act and Rules on this site, and audits privacy notices, consent flows and
  vendor contracts.</p>
  <p><strong>Provenance.</strong> The Act text is verbatim from the Gazette of India, Extraordinary,
  Part II, Section 1, No. 25, dated 11 August 2023 (CG-DL-E-12082023-248045). The Rules content is
  assembled from the PIB release and cross-checked secondary sources; verify against the notified
  Gazette text before relying on it externally.</p>
  <p><strong>Not legal advice.</strong> Educational and compliance-reference material only. Not a
  substitute for a qualified lawyer. No lawyer-client relationship arises from its use. The author is
  not a lawyer. Output of the analysis skill is machine-generated and can be wrong. Provided
  &ldquo;as is&rdquo;, without warranty, and with no liability for any loss arising from its use.
  <a href="{up}disclaimer/">Read the full disclaimer</a>.</p>
  <p>Maintained by <a href="{AUTHOR_URL}">{AUTHOR}</a>.
  <a href="{up}about/">About and methodology</a> &middot;
  <a href="{REPO}">Source and corrections on GitHub</a> &middot;
  <a href="{up}llms.txt">llms.txt</a> &middot;
  <a href="{up}sitemap.xml">Sitemap</a></p>
</footer>
</body>
</html>
"""
    write(f"{url}/index.html" if url else "index.html", doc)
    if markdown_twin is not None:
        write(
            f"{url}/index.md" if url else "index.md",
            f"# {title}\n\n"
            f"> Canonical page: {canonical}\n"
            f"> {NOT_ADVICE}\n\n"
            f"{markdown_twin.strip()}\n",
        )


def skill_cta(up: str, prompt: str, heading: str = "Use this with AI") -> str:
    return (
        f'<aside class="skill-cta"><p class="label">{esc(heading)}</p>'
        f"<p>Ask Claude, grounded in the verbatim statute: <q>{esc(prompt)}</q></p>"
        f'<p>The free <b>dpdp-analyze</b> skill answers from this text and cites the section for '
        f'every claim. <a href="{up}{SKILL_PATH}/">Install it in Claude Code &rarr;</a></p></aside>'
    )


def related_box(up: str, links: list[tuple[str, str]]) -> str:
    if not links:
        return ""
    items = "".join(f'<li><a href="{up}{p}">{esc(t)}</a></li>' for t, p in links)
    return f'<nav class="related" aria-label="Related"><p class="label">Related</p><ul>{items}</ul></nav>'


# ---------------------------------------------------------------- parse sources

def parse_act() -> tuple[list[dict], str]:
    text = ACT_MD.read_text(encoding="utf-8")
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
    text = RULES_MD.read_text(encoding="utf-8")
    out: list[dict] = []
    for block in re.split(r"\n(?=## \d+\. )", text):
        m = re.match(r"## (\d+)\. (.+)", block)
        if not m:
            continue
        body = block.split("\n", 1)[1] if "\n" in block else ""
        body = re.split(r"\n---\n", body)[0].strip()
        out.append({"num": int(m.group(1)), "heading": m.group(2).strip(), "body": body})
    return out


def parse_index() -> dict[int, str]:
    """One-line summaries per section, from section-index.md (stops before the Schedule table)."""
    text = INDEX_MD.read_text(encoding="utf-8").split("## The Schedule")[0]
    out: dict[int, str] = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*[^|]+?\s*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def parse_definitions() -> list[dict]:
    """The section 2 definitions, verbatim."""
    text = ACT_MD.read_text(encoding="utf-8")
    s2 = text.split("### Section 2. Definitions", 1)[1].split("### Section 3.", 1)[0]
    out = []
    for para in re.split(r"\n\s*\n(?=\([a-z]{1,2}\) \*\*\")", s2):
        m = re.match(r'\(([a-z]{1,2})\) \*\*"([^"]+)"\*\*\s*(.+)', para.strip(), re.S)
        if not m:
            continue
        body = m.group(3).strip()
        body = re.sub(r";\s*(and)?$", "", body).rstrip(".").strip()
        out.append({"clause": m.group(1), "term": m.group(2), "text": body})
    return out


def drop_preamble(md_text: str) -> str:
    """Drop the H1 and the model-facing preamble before the first horizontal rule."""
    parts = md_text.split("\n---\n", 1)
    return parts[1] if len(parts) == 2 else md_text


# ---------------------------------------------------------------- content tables

SECTION_PROMPTS = {
    2: "Is our analytics vendor a Data Processor or a Data Fiduciary under section 2?",
    3: "We are a US SaaS company with customers in India. Does the DPDP Act apply to us?",
    4: "Map each processing activity in this data inventory to a lawful basis under section 4.",
    5: "Review this privacy notice against section 5 and Rule 3.",
    6: "Is this consent screen valid under section 6, and is withdrawal as easy as giving consent?",
    7: "Can we rely on section 7(i) to process employee data without consent?",
    8: "We had a data breach. What do we owe the Board and our users under section 8(6)?",
    9: "Our app has users under 18. What do section 9 and Rule 10 require of us?",
    10: "Are we a Significant Data Fiduciary, and do we need a DPO?",
    11: "Draft our process for answering a section 11 access request.",
    12: "When can we refuse an erasure request under section 12(3)?",
    13: "What grievance redressal process and response period do we need?",
    15: "What duties does the DPDP Act place on individuals, and what is the penalty?",
    16: "Can we store Indian customer data on servers in Frankfurt or the US?",
    17: "Does the section 17(1)(d) exemption cover our offshore BPO contract?",
    29: "How do we appeal a Data Protection Board order to TDSAT?",
    33: "What is our realistic penalty exposure under section 33 and the Schedule?",
    37: "When can the government block a service under section 37?",
    44: "Are the SPDI Rules 2011 still valid after section 44?",
}


def section_related(n: int, rule_slug) -> list[tuple[str, str]]:
    r = rule_slug
    table: dict[int, list[tuple[str, str]]] = {
        2: [("Glossary of DPDP defined terms", "glossary/")],
        5: [("Rule 3: what a notice must contain", f"{r('rule-3-')}/")],
        6: [("Rule 4: Consent Managers", f"{r('rule-4-')}/"),
            ("Rule 3: notice", f"{r('rule-3-')}/")],
        7: [("FAQ: employee data", "faq/#does-the-dpdp-act-apply-to-employee-data")],
        8: [("Rule 6: reasonable security safeguards", f"{r('rule-6-')}/"),
            ("Rule 7: personal data breach intimation", f"{r('rule-7-')}/"),
            ("Rule 8: retention and erasure", f"{r('rule-8-')}/"),
            ("Rule 9: contact person", f"{r('other-rules')}/")],
        9: [("Rules 10 and 11: verifiable parental consent", f"{r('rules-10-')}/")],
        10: [("Rule 13: Significant Data Fiduciary obligations", f"{r('rule-13-')}/")],
        11: [("Rule 14: rights of Data Principals", f"{r('rule-14-')}/")],
        12: [("Rule 14: rights of Data Principals", f"{r('rule-14-')}/")],
        13: [("Rule 14: grievance response period", f"{r('rule-14-')}/")],
        14: [("Rule 14: nomination", f"{r('rule-14-')}/")],
        16: [("Rule 15: transfers outside India", f"{r('rule-15-')}/"),
             ("FAQ: data localisation", "faq/#does-the-dpdp-act-require-data-localisation")],
        17: [("Rule 16: research, archiving and statistics", f"{r('other-rules')}/")],
        29: [("Rule 22: appeals", f"{r('other-rules')}/")],
        33: [("DPDP penalties explained", "penalties/")],
        34: [("DPDP penalties explained", "penalties/")],
        44: [("FAQ: are the SPDI Rules still valid?", "faq/#are-the-spdi-rules-2011-still-valid")],
    }
    return table.get(n, []) + [
        ("DPDP Act explained", "dpdp-act-explained/"),
        ("DPDP compliance checklist", "compliance-checklist/"),
    ]


RULE_SECTIONS = {
    "rule-3-": [5], "rule-4-": [6], "rule-6-": [8], "rule-7-": [8], "rule-8-": [8],
    "rules-10-": [9], "rule-13-": [10], "rule-14-": [11, 12, 13, 14], "rule-15-": [16],
}
RULE_TITLES = {
    "notification": "DPDP Rules 2025 commencement dates: when each rule applies",
    "rule-map": "DPDP Rules 2025: list of all 23 rules and 7 schedules",
    "rule-3-": "DPDP Rules 2025, Rule 3: what a privacy notice must contain",
    "rule-4-": "DPDP Rules 2025, Rule 4: Consent Manager registration",
    "rule-6-": "DPDP Rules 2025, Rule 6: reasonable security safeguards",
    "rule-7-": "DPDP Rules 2025, Rule 7: data breach notification and 72 hours",
    "rule-8-": "DPDP Rules 2025, Rule 8: data retention and erasure periods",
    "rules-10-": "DPDP Rules 2025, Rules 10 and 11: verifiable parental consent",
    "rule-13-": "DPDP Rules 2025, Rule 13: Significant Data Fiduciary duties",
    "rule-14-": "DPDP Rules 2025, Rule 14: rights requests and grievances",
    "rule-15-": "DPDP Rules 2025, Rule 15: transferring data outside India",
    "other-rules": "DPDP Rules 2025: Rules 5, 9, 16 and 17 to 23 in brief",
    "what-is-still": "DPDP Rules 2025: what is still not notified",
}

RULE_PROMPTS = {
    "rule-3-": "Review our privacy notice against Rule 3. What is missing?",
    "rule-4-": "Should we integrate with a Consent Manager, and what does Rule 4 require of one?",
    "rule-6-": "Audit our security controls against the Rule 6 minimum safeguards.",
    "rule-7-": "Write a breach notification playbook that meets Rule 7 and section 8(6).",
    "rule-8-": "Does the Third Schedule retention period apply to us?",
    "rules-10-": "Design a verifiable parental consent flow that satisfies Rule 10.",
    "rule-13-": "If we are notified as a Significant Data Fiduciary, what does Rule 13 add?",
    "rule-14-": "Build a rights-request workflow that meets Rule 14.",
    "rule-15-": "Can we use a US cloud provider for Indian user data?",
}

GLOSSARY_NOTES = {
    "Data Fiduciary": "The business or body that decides why and how personal data is processed. "
    "Closest GDPR analogue: controller. The test is conjunctive, purpose and means (s.2(i)).",
    "Data Principal": "The individual the data is about. Closest GDPR analogue: data subject. "
    "For a child it includes the parent or lawful guardian (s.2(j)).",
    "Data Processor": "Processes personal data on a Data Fiduciary's behalf. Must be engaged "
    "under a valid contract (s.8(2)).",
    "Significant Data Fiduciary": "Exists only once the Central Government notifies an entity "
    "or class under s.10(1). Size alone does not make you one, and none had been notified as at "
    "the last check. Only SDFs must appoint a DPO.",
    "Consent Manager": "A Board-registered platform through which people give, manage, review "
    "and withdraw consent. Accountable to the Data Principal, not the business. Registration "
    "under Rule 4 commences 14 November 2026.",
    "child": "Anyone under 18. Not 13 or 16 as in other regimes. Tracking, behavioural "
    "monitoring and targeted advertising directed at children are banned outright (s.9(3)).",
    "personal data": "Very wide: any data about an identifiable individual. The Act creates no "
    "separate sensitive-data category.",
    "personal data breach": "Includes mere loss of access, so ransomware counts. Every breach "
    "is notifiable to the Board and each affected individual, with no harm threshold (s.8(6)).",
    "digital personal data": "The Act only applies to personal data in digital form, or "
    "collected on paper and digitised later (s.3(a)).",
    "processing": "Wholly or partly automated operations on digital personal data, from "
    "collection to erasure.",
    "Board": "The Data Protection Board of India, an adjudicatory body. It has no rule-making "
    "power; the Central Government makes the Rules (s.40).",
    "Data Protection Officer": "Required only for notified Significant Data Fiduciaries, and "
    "must be based in India and responsible to the board of directors (s.10(2)(a)).",
    "certain legitimate uses": "The closed list of non-consent grounds in s.7. There is no "
    "legitimate interests ground.",
    "specified purpose": "The purpose stated in the notice. Consent, retention and erasure all "
    "key off it (s.5, s.8(7)).",
    "Appellate Tribunal": "TDSAT. Appeals from Board orders lie within 60 days (s.29).",
    "she": "Gender-neutral. The Act uses 'she' for every individual.",
    "State": "The State as defined in Article 12 of the Constitution, which brings government "
    "bodies within the Act subject to the s.17 exemptions.",
}

EXTRA_TERMS = [
    ("Data Protection Impact Assessment (DPIA)",
     "A periodic assessment that Significant Data Fiduciaries must carry out. The Act defines it "
     "as a description of Data Principal rights and the purpose of processing, plus the "
     "assessment and management of risk to those rights (s.10(2)(c)(i)). Rule 13(1) requires a "
     "DPIA and audit every twelve months."),
    ("Verifiable parental consent",
     "Consent of a parent or lawful guardian, required before processing a child's personal data "
     "(s.9(1)). Rule 10 requires due diligence that the parent is an identifiable adult, using "
     "identity and age details already held, details voluntarily provided, or a virtual token "
     "from an authorised entity such as DigiLocker."),
    ("Eighth Schedule languages",
     "The 22 languages in the Eighth Schedule to the Constitution. Notice and the consent request "
     "must be available in English or any of them, at the Data Principal's option (s.5(3), "
     "s.6(3))."),
    ("Third Schedule (retention)",
     "The DPDP Rules schedule that deems the purpose expired for large e-commerce entities, "
     "online gaming intermediaries and social media intermediaries three years after the user "
     "last engaged, with 48 hours' notice before erasure (Rule 8)."),
    ("Legitimate interests",
     "Not a DPDP concept. Unlike the GDPR, the Act has no legitimate interests ground. The only "
     "lawful bases are consent (s.6) and the closed list of certain legitimate uses (s.7)."),
    ("Sensitive personal data",
     "Not a DPDP concept. The Act has no special category: health, biometric, financial and caste "
     "data get no extra tier, though sectoral law may still add duties. The old SPDI Rules 2011 "
     "category rested on IT Act s.43A, which s.44(2)(a) omitted."),
]

FAQ_GROUPS: list[tuple[str, list[tuple[str, str, list[tuple[str, str]]]]]] = [
    ("Status and deadlines", [
        ("Is the DPDP Act in force?",
         "Partly. The Act received Presidential assent on 11 August 2023, but section 1(2) permits "
         "staggered commencement. Data Protection Board machinery has been live since 14 November "
         "2025. Consent Manager rules commence 14 November 2026. The substantive obligations on "
         "businesses, covering notice, security, breach reporting, retention, children's data and "
         "rights, commence on 14 May 2027.",
         [("s.1", "act/section-1/"), ("Commencement", "rules/notification-and-phased-commencement/")]),
        ("What is the DPDP compliance deadline?",
         "14 May 2027 for nearly every business obligation. That is when Rules 3, 5 to 16 and 22 to "
         "23 commence: notice, security safeguards, breach intimation, retention and erasure, "
         "children's consent, Significant Data Fiduciary duties, rights machinery and transfers. "
         "Consent Manager registration under Rule 4 commences earlier, on 14 November 2026.",
         [("Commencement", "rules/notification-and-phased-commencement/")]),
        ("When were the DPDP Rules notified?",
         "The Ministry of Electronics and Information Technology notified the Digital Personal "
         "Data Protection Rules, 2025 on 13 November 2025, published 14 November 2025. They contain "
         "23 rules and 7 Schedules and commence in three tranches: 14 November 2025, 14 November "
         "2026 and 14 May 2027.",
         [("DPDP Rules 2025", "rules/")]),
        ("When did the DPDP Act become law?",
         "The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) received Presidential "
         "assent on 11 August 2023 and was published in the Gazette of India the same day. Its "
         "provisions come into force on the dates the Central Government notifies under section "
         "1(2).",
         [("Full text", "act/")]),
    ]),
    ("Scope", [
        ("Does the DPDP Act apply to companies outside India?",
         "Only where the processing is connected to offering goods or services to Data Principals "
         "within India, under section 3(b). Unlike the GDPR, merely monitoring the behaviour of "
         "people in India is not a trigger.",
         [("s.3", "act/section-3/")]),
        ("Does the DPDP Act apply to paper records?",
         "Not unless they are digitised. The Act applies to personal data collected in digital "
         "form, or collected in non-digital form and digitised subsequently, under section 3(a). "
         "Records that stay on paper are outside it.",
         [("s.3", "act/section-3/")]),
        ("Does the DPDP Act apply to publicly available personal data?",
         "Not to personal data that the individual herself made, or caused to be made, publicly "
         "available, or that someone was legally obliged to publish, under section 3(c)(ii). The "
         "Act's own Illustration is a person who blogs her views on social media. Purely personal "
         "or domestic processing by an individual is also outside the Act.",
         [("s.3", "act/section-3/")]),
        ("Does the DPDP Act apply to employee data?",
         "Yes. Employee data is personal data. Section 7(i) lets an employer process it without "
         "consent for the purposes of employment, or to safeguard the employer from loss or "
         "liability, such as preventing corporate espionage, keeping trade secrets, intellectual "
         "property and classified information confidential, or providing a service or benefit the "
         "employee seeks. Uses outside that still need consent.",
         [("s.7", "act/section-7/")]),
        ("Do startups have to comply with the DPDP Act?",
         "Yes, by default. Section 17(3) lets the Central Government notify Data Fiduciaries, "
         "including startups, to whom sections 5, 8(3), 8(7), 10 and 11 do not apply, but no such "
         "notification had been issued as at the last check. Even then, consent, security "
         "safeguards, breach notification and children's protections would still apply.",
         [("s.17", "act/section-17/")]),
    ]),
    ("Lawful basis, notice and consent", [
        ("What lawful bases exist under the DPDP Act?",
         "Exactly two, under section 4(1): the Data Principal's consent meeting section 6, or one "
         "of the closed list of certain legitimate uses in section 7(a) to (i). There is no "
         "legitimate interests balancing test.",
         [("s.4", "act/section-4/"), ("s.6", "act/section-6/"), ("s.7", "act/section-7/")]),
        ("What makes consent valid under the DPDP Act?",
         "Consent must be free, specific, informed, unconditional and unambiguous, given by a "
         "clear affirmative action, and limited to the personal data necessary for the specified "
         "purpose, under section 6(1). Pre-ticked boxes, bundled consent and consent inferred from "
         "continued use fail. Withdrawal must be as easy as giving consent (section 6(4)), and the "
         "business carries the burden of proving valid notice and consent (section 6(10)).",
         [("s.6", "act/section-6/")]),
        ("What must a privacy notice contain under the DPDP Act?",
         "Under section 5(1) and Rule 3, the notice must accompany or precede the consent request, "
         "stand on its own apart from other terms, and in clear and plain language give an "
         "itemised description of the personal data, the specified purpose and the specific goods, "
         "services or uses it enables, plus a link to withdraw consent, exercise rights and "
         "complain to the Data Protection Board. It must be available in English or any of the 22 "
         "Eighth Schedule languages (section 5(3)).",
         [("s.5", "act/section-5/"), ("Rule 3", "rules/rule-3-notice/")]),
        ("What is a Consent Manager under the DPDP Act?",
         "A person registered with the Data Protection Board that acts as a single point of "
         "contact for individuals to give, manage, review and withdraw consent through an "
         "accessible, transparent and interoperable platform (section 2(g)). It is accountable to "
         "the Data Principal, not to the business. Registration under Rule 4 commences on 14 "
         "November 2026 and requires a company incorporated in India.",
         [("s.2(g)", "glossary/#consent-manager"),
          ("Rule 4", "rules/rule-4-and-the-first-schedule-consent-managers/")]),
    ]),
    ("Children", [
        ("What age is a child under the DPDP Act?",
         "Anyone who has not completed 18 years, under section 2(f). Processing a child's data "
         "requires verifiable parental consent, and tracking, behavioural monitoring and targeted "
         "advertising directed at children are prohibited outright under section 9(3), which "
         "consent cannot cure.",
         [("s.2(f)", "glossary/#child"), ("s.9", "act/section-9/")]),
        ("How do you obtain verifiable parental consent under the DPDP Rules?",
         "Rule 10 requires due diligence that the person giving consent as parent is an "
         "identifiable adult, using reliable identity and age details the business already holds, "
         "or details voluntarily provided by the individual or through a virtual token issued by "
         "an authorised entity, which includes DigiLocker. Rule 12 and the Fourth Schedule exempt "
         "specified classes and purposes; verify the Fourth Schedule before relying on one.",
         [("Rules 10 and 11",
           "rules/rules-10-and-11-verifiable-consent-for-children-and-persons-with-disability/")]),
    ]),
    ("Security, breaches and retention", [
        ("What security safeguards does the DPDP Act require?",
         "Reasonable security safeguards to prevent a personal data breach, under section 8(5). "
         "Rule 6 sets the minimum: encryption, obfuscation, masking or tokenisation; access "
         "controls; logging, monitoring and review; backups and continuity measures; one-year "
         "retention of logs; security clauses in processor contracts; and organisational "
         "measures. Failure carries the highest penalty ceiling in the Act, Rs 250 crore.",
         [("s.8", "act/section-8/"), ("Rule 6", "rules/rule-6-reasonable-security-safeguards/")]),
        ("How fast must we report a data breach under the DPDP Act?",
         "Affected individuals must be told without delay under Rule 7(1). The Data Protection "
         "Board gets an initial intimation without delay, then a detailed report within 72 hours "
         "of you becoming aware, under Rule 7(2). There is no harm or materiality threshold, so "
         "every personal data breach is reportable, including loss of access, which brings "
         "ransomware into scope.",
         [("s.8(6)", "act/section-8/"), ("Rule 7", "rules/rule-7-intimation-of-personal-data-breach/")]),
        ("How long can personal data be retained under the DPDP Act?",
         "Until consent is withdrawn or the specified purpose is no longer served, whichever is "
         "earlier, unless a law requires retention (section 8(7)). For large e-commerce entities, "
         "online gaming intermediaries and social media intermediaries, the Third Schedule deems "
         "the purpose expired three years after the user last engaged, with 48 hours' notice "
         "before erasure (Rule 8). Rule 8(3) separately requires keeping associated logs for at "
         "least one year.",
         [("s.8", "act/section-8/"),
          ("Rule 8", "rules/rule-8-and-the-third-schedule-retention-and-erasure/")]),
        ("Do we need a Data Protection Officer in India?",
         "Only if you are notified as a Significant Data Fiduciary. That DPO must be based in "
         "India, be an individual, and be responsible to the board of directors or similar "
         "governing body, under section 10(2)(a). Every other Data Fiduciary need only publish "
         "the business contact information of a person who can answer questions about "
         "processing, under section 8(9) and Rule 9.",
         [("s.10", "act/section-10/"), ("s.8(9)", "act/section-8/")]),
        ("Who is a Significant Data Fiduciary?",
         "Only an entity that the Central Government has notified as one under section 10(1). "
         "You cannot self-classify, and size alone does not make you one. The Government "
         "assesses factors including volume and sensitivity of data, risk to Data Principal "
         "rights, sovereignty, risk to electoral democracy, security of the State and public "
         "order.",
         [("s.10", "act/section-10/"),
          ("Rule 13", "rules/rule-13-significant-data-fiduciary-obligations/")]),
    ]),
    ("Rights of individuals", [
        ("What rights do individuals have under the DPDP Act?",
         "Four: access to information about their personal data (section 11); correction, "
         "completion, updating and erasure (section 12); grievance redressal (section 13); and "
         "nomination of someone to exercise their rights on death or incapacity (section 14). "
         "There is no right to data portability, no general right to object, and no right against "
         "automated decision-making.",
         [("s.11", "act/section-11/"), ("s.12", "act/section-12/"), ("s.13", "act/section-13/"),
          ("s.14", "act/section-14/"), ("Rule 14", "rules/rule-14-rights-of-data-principals/")]),
        ("Is there a right to be forgotten under the DPDP Act?",
         "There is a right to erasure rather than a broad right to be forgotten. Under section "
         "12(3) a business must erase personal data on request unless retention is necessary for "
         "the specified purpose or for compliance with law.",
         [("s.12", "act/section-12/")]),
        ("Can individuals claim compensation under the DPDP Act?",
         "No. Penalties imposed by the Board are credited to the Consolidated Fund of India under "
         "section 34, civil courts are barred from matters the Board is empowered over under "
         "section 39, and the old IT Act section 43A compensation route was repealed.",
         [("s.34", "act/section-34/"), ("s.39", "act/section-39/")]),
    ]),
    ("Transfers and localisation", [
        ("Does the DPDP Act require data localisation?",
         "No, not in the Act itself. Section 16 is a negative list: the Central Government may "
         "notify countries to which transfer is restricted, and none has been notified. Rule "
         "13(4) creates a targeted localisation duty for notified Significant Data Fiduciaries "
         "only, over categories the Government specifies on a committee's recommendation. "
         "Sectoral regulators such as the RBI localise independently, preserved by section 16(2).",
         [("s.16", "act/section-16/"), ("Rule 15", "rules/rule-15-transfers-outside-india/")]),
        ("Can personal data be transferred outside India under the DPDP Act?",
         "Yes, by default. Section 16(1) only lets the Central Government restrict transfers to "
         "notified countries, and none has been notified. Rule 15 adds requirements the "
         "Government may specify for making data available to a foreign State or its agencies. "
         "Stricter sectoral rules, such as RBI payment-data storage, still bind under section "
         "16(2).",
         [("s.16", "act/section-16/"), ("Rule 15", "rules/rule-15-transfers-outside-india/")]),
    ]),
    ("Enforcement and penalties", [
        ("What is the maximum penalty under the DPDP Act?",
         "Rs 250 crore, for failing to take reasonable security safeguards under section 8(5). "
         "Failure to notify a breach and breaches of children's data obligations each carry up to "
         "Rs 200 crore, Significant Data Fiduciary breaches up to Rs 150 crore, and any other "
         "breach up to Rs 50 crore. All figures are ceilings, not tariffs.",
         [("Penalties", "penalties/"), ("s.33", "act/section-33/")]),
        ("Who enforces the DPDP Act?",
         "The Data Protection Board of India, established under section 18. It inquires into "
         "breaches, imposes penalties and can accept voluntary undertakings, but it has no "
         "rule-making power: the Central Government makes the Rules. Appeals go to TDSAT within "
         "60 days under section 29, and onward to the Supreme Court.",
         [("s.18", "act/section-18/"), ("s.29", "act/section-29/")]),
        ("Is there criminal liability under the DPDP Act?",
         "No. The DPDP Act creates no criminal offences and no imprisonment. Penalties are civil "
         "and monetary, imposed by the Data Protection Board.",
         [("Penalties", "penalties/")]),
        ("Does the DPDP Act have a sensitive personal data category?",
         "No. Unlike the GDPR and unlike the earlier SPDI Rules, the DPDP Act creates no special "
         "category. Health, biometric, financial and caste data receive no additional treatment "
         "under this Act, although sectoral law may still impose extra duties.",
         [("Glossary", "glossary/#sensitive-personal-data")]),
        ("Are the SPDI Rules 2011 still valid?",
         "Their footing is materially undermined. Section 44(2) of the DPDP Act omitted both "
         "section 43A of the IT Act, which the SPDI Rules implemented, and section 87(2)(ob), the "
         "rule-making power behind them. Do not cite them as unqualified live obligations.",
         [("s.44", "act/section-44/")]),
        ("What did the DPDP Act change in the RTI Act?",
         "Section 44(3) replaced section 8(1)(j) of the Right to Information Act, 2005 with a flat "
         "exemption for information which relates to personal information, removing the earlier "
         "public-interest override.",
         [("s.44", "act/section-44/")]),
        ("What are the main differences between the DPDP Act and the GDPR?",
         "The DPDP Act has no legitimate interests ground, no sensitive data category, a child age "
         "of 18, an outright ban on targeted advertising to children, breach notification with no "
         "harm threshold, no portability or automated-decision rights, no compensation for "
         "individuals, and enforceable duties on individuals themselves.",
         [("DPDP vs GDPR", "dpdp-vs-gdpr/")]),
    ]),
]

SKILL_PROMPT_GROUPS = [
    ("Review documents", [
        "Is this privacy policy DPDP compliant? [paste or attach it]",
        "Review this consent screen against section 6 and Rule 3.",
        "Check this vendor DPA for what section 8(2) and Rule 6(1)(f) require.",
    ]),
    ("Audit a product", [
        "Audit our signup and onboarding flow against the DPDP Act.",
        "Run the full DPDP compliance checklist against this repository.",
        "Our app has users under 18. What has to change before 14 May 2027?",
    ]),
    ("Answer a question", [
        "Do we need a DPO in India?",
        "Can we store Indian customer data on AWS Frankfurt?",
        "Are we a Significant Data Fiduciary?",
    ]),
    ("Handle an incident", [
        "We had a data breach. What do we have to do, and by when?",
        "Draft the Rule 7 notice to affected users.",
        "Is a ransomware lockout a personal data breach under the DPDP Act?",
    ]),
]

SKILL_FAQ = [
    ("Is the DPDP skill free?",
     "Yes. The skill, the reference files and this site are open source under the MIT licence. "
     "The Act and Rules text are Government of India works reproduced under section 52(1)(q) of "
     "the Copyright Act, 1957."),
    ("What do I need to run it?",
     "Claude Code, Anthropic's agentic coding tool, which runs in the terminal, IDEs, the desktop "
     "app and the web. The skill is a standard SKILL.md folder with plain Markdown references, so "
     "agents that support the Agent Skills format can load it too, and the reference files work in "
     "any RAG index or prompt library unchanged."),
    ("Does the skill send my data anywhere?",
     "The skill itself makes no network calls. It is instructions plus reference files that Claude "
     "reads locally. Your prompts and any documents you share are processed by Claude under the "
     "terms of your own Claude plan, as with any other Claude Code session."),
    ("How is it different from asking a chatbot about the DPDP Act?",
     "General-purpose models pattern-match Indian law to the GDPR and invent things that are not "
     "in the DPDP Act, such as a sensitive-data category or a legitimate interests ground. The "
     "skill makes Claude walk the Act's five gates, quote only from the verbatim Gazette text, "
     "cite a section or rule for every proposition, check commencement dates, and say what is "
     "still unsettled."),
    ("Is the output legal advice?",
     "No. The output is machine-generated analysis and can be wrong. The skill closes every "
     "substantive answer with a reminder to verify against the Gazette of India and consult "
     "qualified Indian legal counsel."),
    ("How do I update it?",
     "Run /plugin marketplace update dpdp inside Claude Code. Corrections and new government "
     "notifications are tracked in the GitHub repository."),
]

TRAPS = [
    "There are only <b>two lawful bases</b>: consent, or the closed section 7 list. "
    "There is <b>no legitimate interests</b> ground.",
    "There is <b>no sensitive personal data category</b>.",
    "A <b>child is anyone under 18</b>, not 13 or 16.",
    "<b>Targeted advertising to children is banned outright</b>; consent does not cure it.",
    "<b>Breach notification has no harm threshold</b>, and covers loss of access.",
    "Only <b>notified Significant Data Fiduciaries</b> need a DPO.",
    "The Act <b>does not mandate data localisation</b>.",
    "Individuals get <b>no compensation</b>; penalties go to the Consolidated Fund.",
    "There is <b>no portability right</b> and no right against automated decisions.",
    "<b>Data Principals have enforceable duties</b>, with a Rs 10,000 penalty.",
]


# ---------------------------------------------------------------- build

def build() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    sections, schedule = parse_act()
    rules = parse_rules()
    oneliners = parse_index()
    definitions = parse_definitions()

    rule_slugs = [slugify(r["heading"]) for r in rules]

    def rule_slug(prefix: str) -> str:
        return "rules/" + next(s for s in rule_slugs if s.startswith(prefix))

    RULE_PAGES.update({
        1: rule_slug("notification"), 2: rule_slug("rule-map"), 3: rule_slug("rule-3-"),
        4: rule_slug("rule-4-"), 6: rule_slug("rule-6-"), 7: rule_slug("rule-7-"),
        8: rule_slug("rule-8-"), 10: rule_slug("rules-10-"), 11: rule_slug("rules-10-"),
        12: rule_slug("rules-10-"), 13: rule_slug("rule-13-"), 14: rule_slug("rule-14-"),
        15: rule_slug("rule-15-"),
    })
    for n in (5, 9, 16, 17, 18, 19, 20, 21, 22, 23):
        RULE_PAGES[n] = rule_slug("other-rules")

    build_sections(sections, oneliners, rule_slug)
    build_act_index(sections, schedule, oneliners)
    build_rules(rules)
    build_explained()
    build_checklist()
    build_glossary(definitions)
    build_penalties(schedule)
    build_gdpr()
    build_faq()
    build_skill()
    build_about()
    build_disclaimer()
    build_landing()

    write("assets/style.css", CSS)
    write(".nojekyll", "")
    if STATIC.exists():
        shutil.copytree(STATIC, DOCS, dirs_exist_ok=True)
    build_404()
    build_skill_zip()
    build_sitemap_robots()
    build_llms(sections, rules)

    print(f"Built {len(PAGES)} pages into {DOCS}")


def build_sections(sections: list[dict], oneliners: dict[int, str], rule_slug) -> None:
    up = "../../"
    for i, s in enumerate(sections):
        n = s["num"]
        prev_s = sections[i - 1] if i else None
        next_s = sections[i + 1] if i + 1 < len(sections) else None
        pager = '<nav class="pager">'
        if prev_s:
            pager += (
                f'<a class="prev" href="../section-{prev_s["num"]}/">&larr; Section '
                f'{prev_s["num"]}: {esc(prev_s["heading"])}</a>'
            )
        if next_s:
            pager += (
                f'<a class="next" href="../section-{next_s["num"]}/">Section '
                f'{next_s["num"]}: {esc(next_s["heading"])} &rarr;</a>'
            )
        pager += "</nav>"

        oneline = oneliners.get(n, "")
        summary = ""
        if oneline:
            summary = (
                f'<div class="summary"><p class="label">Section {n} in one line</p>'
                f"{md2html(link_refs(oneline, up, skip_section=n))}"
                '<p class="fine">Maintainers\' summary, not statutory text. The verbatim section '
                "follows.</p></div>"
            )

        title = fit_title(f"Section {n} DPDP Act 2023", s["heading"], "full text")
        desc = meta_desc(
            f'Section {n} of India\'s DPDP Act 2023, {s["heading"]}: {strip_md(oneline)}. '
            "Full verbatim text from the Gazette."
            if oneline else
            f'Section {n} of the Digital Personal Data Protection Act, 2023, {s["heading"]}. '
            f'Full verbatim text. {strip_md(s["body"])}'
        )
        prompt = SECTION_PROMPTS.get(
            n, f"Explain section {n} of the DPDP Act and what it means for our product."
        )
        body = (
            f'<article>\n<p class="eyebrow">{esc(s["chapter"])}</p>\n'
            f'<h1>Section {n}. {esc(s["heading"])}</h1>\n'
            "<p class='sub'>The Digital Personal Data Protection Act, 2023 (Act 22 of 2023). "
            "Verbatim text from the Gazette of India.</p>\n"
            f"{summary}"
            f'<div class="statute">{md2html(s["body"])}</div>\n'
            f"{related_box(up, section_related(n, rule_slug))}"
            f"{skill_cta(up, prompt)}"
            f"{pager}\n</article>"
        )
        twin = (
            f'**{s["chapter"]}.** The Digital Personal Data Protection Act, 2023 (Act 22 of 2023), '
            f"section {n}. Verbatim from the Gazette of India.\n\n"
            + (f"Summary (maintainers', not statutory text): {oneline}\n\n" if oneline else "")
            + f'## Section {n}. {s["heading"]}\n\n{s["body"]}\n'
        )
        page(
            url=f"act/section-{n}",
            title=title,
            description=desc,
            body=body,
            sources=(ACT_MD, INDEX_MD),
            breadcrumbs=[("Home", ""), ("DPDP Act 2023", "act"), (f"Section {n}", None)],
            graph=[ACT_NODE, {
                "@type": "Legislation",
                "@id": f"{SITE}/act/section-{n}/#legislation",
                "name": f'Section {n}: {s["heading"]}',
                "legislationIdentifier": f"Act No. 22 of 2023, section {n}",
                "legislationType": "Act",
                "legislationJurisdiction": "India",
                "legislationDate": "2023-08-11",
                "isPartOf": {"@id": ACT_ID},
                "inLanguage": "en-IN",
                "url": f"{SITE}/act/section-{n}/",
            }],
            markdown_twin=twin,
            llms_group="The Act, section by section",
        )


def build_act_index(sections: list[dict], schedule: str, oneliners: dict[int, str]) -> None:
    by_chapter: dict[str, list[dict]] = {}
    for s in sections:
        by_chapter.setdefault(s["chapter"], []).append(s)
    toc = ""
    for ch, items in by_chapter.items():
        toc += f"<h2>{esc(ch)}</h2>\n<ul class='toc'>"
        for s in items:
            toc += (
                f'<li><a href="section-{s["num"]}/"><b>Section {s["num"]}</b> '
                f'{esc(s["heading"])}</a></li>'
            )
        toc += "</ul>\n"
    toc += f'<h2>The Schedule</h2><div class="statute">{md2html(schedule)}</div>'

    twin = "\n".join(
        f'- [Section {s["num"]}. {s["heading"]}]({SITE}/act/section-{s["num"]}/index.md): '
        f'{strip_md(oneliners.get(s["num"], ""))}'
        for s in sections
    )
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
            "India, Extraordinary, Part II, Section 1, No. 25.</p>"
            "<p>New to the Act? Start with <a href='../dpdp-act-explained/'>the DPDP Act "
            "explained</a>, or look up a term in the <a href='../glossary/'>glossary</a>.</p>"
            + toc
            + skill_cta("../", "Which sections of the DPDP Act apply to our product?")
        ),
        sources=(ACT_MD,),
        breadcrumbs=[("Home", ""), ("DPDP Act 2023", None)],
        graph=[ACT_NODE],
        changefreq="yearly",
        markdown_twin=(
            "The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023), assented 11 "
            "August 2023. 44 sections in 9 chapters plus a Schedule of penalties.\n\n" + twin
        ),
        llms_group="Start here",
    )


def build_rules(rules: list[dict]) -> None:
    up = "../../"
    for r in rules:
        slug = slugify(r["heading"])
        prefix = next((p for p in RULE_SECTIONS if slug.startswith(p)), None)
        title_key = next((k for k in RULE_TITLES if slug.startswith(k)), None)
        related = [(f"Section {n} of the Act", f"act/section-{n}/")
                   for n in RULE_SECTIONS.get(prefix, [])]
        related.append(("All DPDP Rules 2025", "rules/"))
        related.append(("DPDP compliance checklist", "compliance-checklist/"))
        prompt = RULE_PROMPTS.get(prefix, "What do the DPDP Rules 2025 require of us, and from when?")
        page(
            url=f"rules/{slug}",
            title=RULE_TITLES[title_key] if title_key else fit_title("DPDP Rules 2025", r["heading"]),
            description=meta_desc(
                f'{r["heading"]} under the Digital Personal Data Protection Rules, 2025. '
                f'{strip_md(r["body"])}'
            ),
            body=(
                f'<article><h1>{esc(r["heading"])}</h1>'
                "<p class='sub'>Digital Personal Data Protection Rules, 2025. Notified "
                "13 November 2025. Verify against the notified Gazette text before external use.</p>"
                f'<div class="statute">'
                f'{md2html(link_refs(r["body"], up, skip_rule_page=f"rules/{slug}"))}</div>'
                f"{related_box(up, related)}{skill_cta(up, prompt)}</article>"
            ),
            sources=(RULES_MD,),
            breadcrumbs=[("Home", ""), ("DPDP Rules 2025", "rules"), (r["heading"], None)],
            graph=[RULES_NODE],
            markdown_twin=(
                "Digital Personal Data Protection Rules, 2025. Secondary-sourced from the PIB "
                "release and cross-checked sources; verify against the notified Gazette text "
                f'before external use.\n\n## {r["heading"]}\n\n{r["body"]}\n'
            ),
            llms_group="The Rules, 2025",
        )

    rules_toc = "<ul class='toc'>" + "".join(
        f'<li><a href="{slugify(r["heading"])}/">{esc(r["heading"])}</a></li>'
        for r in rules
    ) + "</ul>"
    page(
        url="rules",
        title="DPDP Rules 2025 explained: 23 rules, schedules and deadlines",
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
            + skill_cta("../", "Which DPDP Rules apply to us, and what must be ready by 14 May 2027?")
        ),
        sources=(RULES_MD,),
        breadcrumbs=[("Home", ""), ("DPDP Rules 2025", None)],
        graph=[RULES_NODE],
        markdown_twin=(
            "The Digital Personal Data Protection Rules, 2025. Notified 13 November 2025. 23 rules "
            "and 7 schedules. Commencement: 14 November 2025 (Rules 1, 2, 17 to 21, Board "
            "machinery); 14 November 2026 (Rule 4, Consent Managers); 14 May 2027 (Rules 3, 5 to "
            "16, 22, 23: every substantive business obligation).\n\n"
            + "\n".join(f'- [{r["heading"]}]({SITE}/rules/{slugify(r["heading"])}/index.md)'
                        for r in rules)
        ),
        llms_group="Start here",
    )


def build_explained() -> None:
    up = "../"
    text = drop_preamble(DOCTRINE_MD.read_text(encoding="utf-8"))
    page(
        url="dpdp-act-explained",
        title="DPDP Act explained: how India's data protection law works",
        description=(
            "A plain-English guide to India's DPDP Act 2023: the five gates, consent, the s.7 "
            "legitimate uses, children, Significant Data Fiduciaries, rights, transfers, "
            "exemptions, enforcement and 16 common misreadings."
        ),
        body=(
            "<article><h1>The DPDP Act explained</h1>"
            "<p class='sub'>How the Digital Personal Data Protection Act, 2023 actually works, "
            "with a section anchor on every proposition. This is the doctrine file the "
            "<a href='../claude-code-skill/'>dpdp-analyze skill</a> loads before it answers any "
            "question.</p>"
            "<div class='callout'><p><strong>The one-sentence version:</strong> the DPDP Act is "
            "consent-heavy, rights-light, State-friendly, and has no sensitive-data tier.</p></div>"
            f'<div class="prose">{md2html(link_refs(text, up))}</div>'
            + skill_cta(up, "Walk our product through the five gates of the DPDP Act.")
            + "</article>"
        ),
        sources=(DOCTRINE_MD,),
        breadcrumbs=[("Home", ""), ("DPDP Act explained", None)],
        page_type="WebPage",
        graph=[{
            "@type": "Article",
            "@id": f"{SITE}/dpdp-act-explained/#article",
            "headline": "The DPDP Act explained: how India's data protection law actually works",
            "about": {"@id": ACT_ID},
            "author": {"@id": PERSON_ID},
            "dateModified": last_modified(DOCTRINE_MD),
            "image": OG_IMAGE,
            "mainEntityOfPage": {"@id": f"{SITE}/dpdp-act-explained/#webpage"},
        }],
        markdown_twin=text,
        llms_group="Guides",
    )


def build_checklist() -> None:
    up = "../"
    raw = CHECKLIST_MD.read_text(encoding="utf-8")
    count = len(re.findall(r"^\| [A-L]\d+ \|", raw, flags=re.M))
    text = re.sub(r"^# .*\n", "", raw, count=1)
    text = re.sub(r"^The working checklist.*?\n\n", "", text, count=1, flags=re.S)
    page(
        url="compliance-checklist",
        title=f"DPDP compliance checklist: {count} checks anchored to the Act and Rules",
        description=(
            f"A {count}-point DPDP Act 2023 compliance checklist for India: scoping, lawful basis, "
            "notice, consent, security, breach, retention, children, SDF duties, rights and "
            "transfers. Every item cites a section or rule."
        ),
        body=(
            f"<article><h1>DPDP compliance checklist: {count} checks</h1>"
            "<p class='sub'>The working checklist for auditing an organisation, a product, a "
            "contract or a privacy notice against the Digital Personal Data Protection Act, 2023 "
            "and the DPDP Rules, 2025. Every item carries its statutory anchor.</p>"
            "<div class='callout'><p><strong>Run it automatically.</strong> The free "
            "<a href='../claude-code-skill/'>dpdp-analyze skill for Claude Code</a> uses this "
            "exact checklist: point it at a privacy notice, a consent flow, a vendor contract or a "
            "codebase and it returns ranked findings, each anchored and each with a fix.</p></div>"
            f'<div class="prose">{md2html(link_refs(text, up))}</div>'
            + skill_cta(up, "Run the DPDP compliance checklist against this repository.")
            + "</article>"
        ),
        sources=(CHECKLIST_MD,),
        breadcrumbs=[("Home", ""), ("Compliance checklist", None)],
        graph=[{
            "@type": "Article",
            "@id": f"{SITE}/compliance-checklist/#article",
            "headline": f"DPDP compliance checklist: {count} checks anchored to the Act and Rules",
            "about": [{"@id": ACT_ID}, {"@id": RULES_ID}],
            "author": {"@id": PERSON_ID},
            "dateModified": last_modified(CHECKLIST_MD),
            "image": OG_IMAGE,
            "mainEntityOfPage": {"@id": f"{SITE}/compliance-checklist/#webpage"},
        }],
        markdown_twin=text,
        llms_group="Guides",
    )


def build_glossary(definitions: list[dict]) -> None:
    up = "../"
    entries = []
    for d in definitions:
        name = d["term"][0].upper() + d["term"][1:]
        entries.append({
            "name": name,
            "slug": slugify(d["term"]),
            "code": f's.2({d["clause"]})',
            "verbatim": f'"{d["term"]}" {d["text"]}',
            "note": GLOSSARY_NOTES.get(d["term"], ""),
        })
    for name, note in EXTRA_TERMS:
        entries.append({"name": name, "slug": slugify(name.split(" (")[0]), "code": "",
                        "verbatim": "", "note": note})
    entries.sort(key=lambda e: e["name"].lower())

    jump = " &middot; ".join(f'<a href="#{e["slug"]}">{esc(e["name"])}</a>' for e in entries)
    items = ""
    twin = ""
    for e in entries:
        items += f'<section class="term" id="{e["slug"]}"><h2>{esc(e["name"])}</h2>'
        if e["note"]:
            items += f'<div class="plain">{md2html(link_refs(e["note"], up))}</div>'
        if e["verbatim"]:
            items += (
                f'<blockquote class="verbatim">{md2html(e["verbatim"])}</blockquote>'
                f'<p class="fine">{e["code"]}, DPDP Act 2023, verbatim. '
                f'<a href="../act/section-2/">Read section 2</a>.</p>'
            )
        items += "</section>"
        twin += f'## {e["name"]}\n\n'
        if e["note"]:
            twin += f'{e["note"]}\n\n'
        if e["verbatim"]:
            twin += f'> {strip_md(e["verbatim"])} ({e["code"]}, verbatim)\n\n'

    term_nodes = [
        {
            "@type": "DefinedTerm",
            "@id": f'{SITE}/glossary/#{e["slug"]}',
            "name": e["name"],
            "description": strip_md(e["note"] or e["verbatim"]),
            **({"termCode": e["code"]} if e["code"] else {}),
            "url": f'{SITE}/glossary/#{e["slug"]}',
            "inDefinedTermSet": {"@id": f"{SITE}/glossary/#termset"},
        }
        for e in entries
    ]
    page(
        url="glossary",
        title="DPDP Act glossary: Data Fiduciary, Data Principal and more",
        description=(
            "Every defined term in India's DPDP Act 2023, verbatim from section 2, with a "
            "plain-English note: Data Fiduciary, Data Principal, Data Processor, Significant Data "
            "Fiduciary, Consent Manager, child, personal data breach."
        ),
        body=(
            "<h1>DPDP Act glossary</h1>"
            "<p class='sub'>Every term defined in section 2 of the Digital Personal Data Protection "
            "Act, 2023, quoted verbatim, with a short plain-English note on the ones that decide "
            "real questions. Plus the terms people look for that the Act does not use.</p>"
            f'<p class="jump">{jump}</p>{items}'
            + skill_cta(up, "Are we a Data Fiduciary or a Data Processor for this processing?")
        ),
        sources=(ACT_MD, THIS),
        breadcrumbs=[("Home", ""), ("Glossary", None)],
        graph=[{
            "@type": "DefinedTermSet",
            "@id": f"{SITE}/glossary/#termset",
            "name": "DPDP Act 2023 defined terms",
            "url": f"{SITE}/glossary/",
            "about": {"@id": ACT_ID},
            "hasDefinedTerm": [{"@id": t["@id"]} for t in term_nodes],
        }, *term_nodes],
        markdown_twin=twin,
        llms_group="Guides",
    )


def build_penalties(schedule: str) -> None:
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
            "<div class='callout'><p><strong>What is the maximum penalty under the DPDP Act?</strong> "
            "Rs 250 crore, for failing to take reasonable security safeguards under section 8(5). "
            "Every figure is a <strong>ceiling</strong>: the Act says "
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
            "<h2>Is there jail time under the DPDP Act?</h2>"
            "<p>No. There are <strong>no criminal offences and no imprisonment</strong> anywhere in "
            "the DPDP Act.</p>"
            "<p><a href=\"../act/section-33/\">Read section 33 in full &rarr;</a></p>"
            + skill_cta("../", "What is our realistic penalty exposure, and which gaps should we fix first?")
        ),
        sources=(ACT_MD, THIS),
        breadcrumbs=[("Home", ""), ("Penalties", None)],
        markdown_twin=(
            "Every figure is a ceiling (\"may extend to\"), imposed only if the Data Protection "
            "Board finds the breach \"significant\" (s.33(1)).\n\n" + schedule + "\n\n"
            "Section 33(2) factors: nature, gravity and duration; type of data; repetition; gain "
            "or loss avoided; mitigation and its timeliness; proportionality and deterrence; "
            "impact on the person. Penalties go to the Consolidated Fund of India (s.34); no "
            "compensation to individuals; civil courts barred (s.39). Appeals to TDSAT within 60 "
            "days (s.29). Blocking possible after two or more penalties (s.37). No criminal "
            "offences.\n"
        ),
        llms_group="Guides",
    )


GDPR_TABLE = """
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


def build_gdpr() -> None:
    up = "../"
    page(
        url="dpdp-vs-gdpr",
        title="DPDP Act vs GDPR: 17 differences that change your compliance programme",
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
            "<div class='callout'><p><strong>Is the DPDP Act the same as the GDPR?</strong> No. "
            "The DPDP Act is consent-heavy, rights-light, State-friendly, and has no "
            "sensitive-data tier.</p></div>"
            + md2html(link_refs(GDPR_TABLE, up))
            + "<h2>What GDPR-trained teams most often get wrong</h2>"
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
            + skill_cta(up, "We are GDPR compliant. What extra do we need for India's DPDP Act?")
        ),
        sources=(THIS,),
        breadcrumbs=[("Home", ""), ("DPDP vs GDPR", None)],
        markdown_twin=(
            "The DPDP Act is consent-heavy, rights-light, State-friendly, and has no "
            "sensitive-data tier.\n" + GDPR_TABLE
        ),
        llms_group="Guides",
    )


def build_faq() -> None:
    up = "../"
    body = (
        "<h1>DPDP Act 2023: frequently asked questions</h1>"
        "<p class='sub'>Direct answers, each with the section or rule it rests on.</p>"
    )
    toc = "<nav class='faq-toc' aria-label='Questions'>"
    twin = ""
    qa_nodes = []
    for group, items in FAQ_GROUPS:
        toc += f"<p class='label'>{esc(group)}</p><ul>"
        body += f"<h2>{esc(group)}</h2>"
        twin += f"## {group}\n\n"
        for q, a, refs in items:
            qid = slugify(q)
            toc += f'<li><a href="#{qid}">{esc(q)}</a></li>'
            chips = " ".join(f'<a class="chip" href="{up}{p}">{esc(t)}</a>' for t, p in refs)
            body += (
                f'<section class="qa" id="{qid}"><h3>{esc(q)}</h3><p>{esc(a)}</p>'
                f'<p class="sources">Source: {chips}</p></section>'
            )
            twin += f"### {q}\n\n{a}\n\n"
            qa_nodes.append({
                "@type": "Question",
                "name": q,
                "url": f"{SITE}/faq/#{qid}",
                "acceptedAnswer": {"@type": "Answer", "text": a},
            })
        toc += "</ul>"
    toc += "</nav>"
    page(
        url="faq",
        title="DPDP Act 2023 FAQ: deadline, penalties, DPO, consent, breach reporting",
        description=(
            "Answers on India's DPDP Act 2023: compliance deadline, whether it applies outside "
            "India, consent and notice, children, data localisation, DPO, breach reporting, "
            "penalties, rights and the SPDI Rules."
        ),
        body=body.replace("</p>", "</p>" + toc, 1)
        + skill_cta(up, "Ask any of these about your own product.", "Ask your own question"),
        sources=(THIS,),
        breadcrumbs=[("Home", ""), ("FAQ", None)],
        page_type="FAQPage",
        page_extra={"mainEntity": qa_nodes},
        markdown_twin=twin,
        llms_group="Start here",
    )


def build_skill() -> None:
    groups = "".join(
        f"<div class='card static'><h3>{esc(g)}</h3><ul>"
        + "".join(f"<li><q>{esc(p)}</q></li>" for p in prompts)
        + "</ul></div>"
        for g, prompts in SKILL_PROMPT_GROUPS
    )
    faq_html = "".join(
        f'<section class="qa" id="{slugify(q)}"><h3>{esc(q)}</h3><p>{esc(a)}</p></section>'
        for q, a in SKILL_FAQ
    )
    howto = {
        "@type": "HowTo",
        "@id": f"{SITE}/{SKILL_PATH}/#install",
        "name": "How to install the DPDP Act skill in Claude Code",
        "totalTime": "PT1M",
        "tool": [{"@type": "HowToTool", "name": "Claude Code"}],
        "step": [
            {"@type": "HowToStep", "position": 1, "name": "Add the marketplace",
             "text": "Inside Claude Code, run: /plugin marketplace add mksd0398/dpdp-act-skill"},
            {"@type": "HowToStep", "position": 2, "name": "Install the plugin",
             "text": "Run: /plugin install dpdp-analyze@dpdp"},
            {"@type": "HowToStep", "position": 3, "name": "Ask a question",
             "text": "Run /dpdp-analyze, or just ask an Indian privacy question such as "
                     "'Is this privacy policy DPDP compliant?'"},
        ],
    }
    faq_node = {
        "@type": "FAQPage",
        "@id": f"{SITE}/{SKILL_PATH}/#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in SKILL_FAQ
        ],
    }
    example = (
        "<div class='example'><p class='label'>Illustrative answer</p>"
        "<p class='q'>&ldquo;Do we need a DPO in India?&rdquo;</p>"
        "<p><b>No, unless the Central Government has notified you as a Significant Data "
        "Fiduciary.</b> Only SDFs must appoint a Data Protection Officer, who must be an "
        "individual based in India and responsible to the board of directors (s.10(2)(a)). Every "
        "other Data Fiduciary publishes the business contact details of a person who can answer "
        "questions about its processing (s.8(9), Rule 9).</p>"
        "<p><b>Trap:</b> size alone does not make you an SDF, and you cannot self-classify "
        "(s.10(1)). No SDF had been notified as at the last check.</p>"
        "<p class='fine'>Not legal advice. Verify statutory text against the Gazette of India and "
        "consult qualified Indian legal counsel before acting.</p></div>"
    )
    page(
        url=SKILL_PATH,
        title="DPDP Act AI skill for Claude Code: free, cites every section",
        description=(
            "Free Claude Code skill that analyses privacy notices, consent flows, vendor contracts "
            "and products against India's DPDP Act 2023 and Rules 2025, citing a section or rule "
            "for every claim. Install in two commands."
        ),
        body=(
            "<h1>The DPDP Act skill for Claude Code</h1>"
            "<p class='sub'>A free, open-source skill that makes Claude answer Indian data "
            "protection questions from the verbatim Digital Personal Data Protection Act, 2023 and "
            "the DPDP Rules, 2025, with a section or rule anchor on every claim.</p>"
            "<h2 id='install'>Install in two commands</h2>"
            "<p>Inside <a href='https://code.claude.com/docs'>Claude Code</a>, run:</p>"
            f"<pre><code>{esc(INSTALL)}</code></pre>"
            "<p>Then type <code>/dpdp-analyze</code>, or just ask an Indian privacy question. The "
            "skill triggers on its own whenever a question touches Indian data protection law, "
            "whether or not you say &ldquo;DPDP&rdquo;. Update with "
            "<code>/plugin marketplace update dpdp</code>.</p>"
            "<details><summary>Prefer to copy the folder by hand?</summary>"
            f"<pre><code>{esc(INSTALL_MANUAL)}</code></pre>"
            "<p>Claude Code reads personal skills from <code>~/.claude/skills/</code> and project "
            "skills from <code>.claude/skills/</code> in a repository, so you can also commit it "
            "to a project and share it with your team.</p></details>"
            "<h2 id='other-tools'>Use it in Claude.ai, Copilot, Gemini, Codex and Cursor</h2>"
            "<p>The skill is a standard <code>SKILL.md</code> folder in the open "
            "<a href='https://agentskills.io'>Agent Skills</a> format, so it is not tied to Claude "
            "Code.</p>"
            "<table><thead><tr><th>Tool</th><th>How</th></tr></thead><tbody>"
            f"<tr><td>Claude.ai (web, desktop, mobile)</td><td>Download "
            f"<a href='../downloads/{ZIP_NAME}'>{ZIP_NAME}</a>, then Customize &rsaquo; Skills "
            "&rsaquo; + &rsaquo; Create skill &rsaquo; Upload a skill. Code execution must be "
            "on.</td></tr>"
            "<tr><td>GitHub Copilot (CLI, VS Code, coding agent)</td>"
            "<td><code>gh skill install mksd0398/dpdp-act-skill dpdp-analyze</code></td></tr>"
            "<tr><td>Gemini CLI</td><td><code>gemini skills install "
            "https://github.com/mksd0398/dpdp-act-skill.git --path skills/dpdp-analyze</code></td></tr>"
            "<tr><td>Many agents at once</td><td><code>npx skills add mksd0398/dpdp-act-skill</code>"
            "</td></tr>"
            "<tr><td>OpenAI Codex, Cursor, Goose, OpenCode, Junie, Amp</td><td>Copy "
            "<code>skills/dpdp-analyze</code> into <code>~/.agents/skills/</code>, or into "
            "<code>.agents/skills/</code> in a project</td></tr>"
            "<tr><td>Claude API</td><td>Upload the folder with the "
            "<a href='https://platform.claude.com/docs/en/build-with-claude/skills-guide'>Skills "
            "API</a></td></tr>"
            "<tr><td>Anything else (RAG, custom GPTs, prompt libraries)</td><td>Index the "
            f"<a href='{REPO}/tree/main/skills/dpdp-analyze/references'>reference files</a> or "
            "this site's <a href='../llms-full.txt'>llms-full.txt</a></td></tr>"
            "</tbody></table>"
            "<h2>What you can ask</h2>"
            f"<div class='cards two'>{groups}</div>"
            "<h2>Why it is more accurate than a general chatbot</h2>"
            "<p>Language models get Indian data protection law wrong in specific, repeatable ways, "
            "because they pattern-match to the GDPR. The skill pins the actual text and makes "
            "Claude follow seven hard rules:</p>"
            "<ol>"
            "<li><b>No proposition without an anchor.</b> Every claim cites a section or rule, or "
            "Claude says it does not know.</li>"
            "<li><b>Quote only the verbatim Gazette text</b>, never the Act from memory.</li>"
            "<li><b>Flag the Rules as secondary-sourced</b> and tell you to verify them.</li>"
            "<li><b>Treat penalties as ceilings</b>, gated on the Board finding a breach "
            "&ldquo;significant&rdquo;.</li>"
            "<li><b>Check commencement</b> before calling anything binding.</li>"
            "<li><b>Never import the GDPR</b>: no sensitive-data tier, no legitimate interests, no "
            "portability, no compensation.</li>"
            "<li><b>Say it is not legal advice</b>, once, at the end.</li>"
            "</ol>"
            "<h2>What it looks like</h2>" + example +
            "<h2>What ships in the skill</h2>"
            "<table><thead><tr><th>File</th><th>What it is</th></tr></thead><tbody>"
            "<tr><td><a href='../act/'>act-full-text.md</a></td><td>All 44 sections and the "
            "Schedule, verbatim from the Gazette, with all 14 Illustrations</td></tr>"
            "<tr><td><a href='../rules/'>rules-2025.md</a></td><td>All 23 Rules and 7 Schedules "
            "with commencement dates</td></tr>"
            "<tr><td><a href='../dpdp-act-explained/'>doctrine.md</a></td><td>The five gates, "
            "consent architecture, exemptions, enforcement and 16 common misreadings</td></tr>"
            "<tr><td><a href='../compliance-checklist/'>compliance-checklist.md</a></td><td>A "
            "78-point audit checklist, every item anchored</td></tr>"
            "<tr><td>section-index.md</td><td>One line per section, for fast lookup</td></tr>"
            "<tr><td>report-template.md</td><td>A formal assessment report template</td></tr>"
            "</tbody></table>"
            "<h2>Questions about the skill</h2>" + faq_html
            + f"<p><a class='btn' href='{REPO}'>View the source on GitHub &rarr;</a></p>"
        ),
        sources=(THIS, SKILL_MD),
        breadcrumbs=[("Home", ""), ("AI skill", None)],
        graph=[ACT_NODE, RULES_NODE, SKILL_NODE, howto, faq_node],
        markdown_twin=(
            "dpdp-analyze is a free, open-source (MIT) Claude Code skill that answers Indian data "
            "protection questions from the verbatim DPDP Act 2023 and the DPDP Rules 2025, citing "
            "a section or rule for every claim. It reviews privacy notices, consent flows, vendor "
            "contracts and whole products.\n\n"
            f"## Install\n\nInside Claude Code:\n\n```\n{INSTALL}\n```\n\n"
            f"Or copy the folder:\n\n```\n{INSTALL_MANUAL}\n```\n\n"
            f"Claude.ai: download {SITE}/downloads/{ZIP_NAME} and upload it under Customize > "
            "Skills. GitHub Copilot: `gh skill install mksd0398/dpdp-act-skill dpdp-analyze`. "
            "Gemini CLI: `gemini skills install https://github.com/mksd0398/dpdp-act-skill.git "
            "--path skills/dpdp-analyze`. Codex, Cursor and other Agent Skills tools: copy "
            "`skills/dpdp-analyze` into `~/.agents/skills/`.\n\n"
            "## Example prompts\n\n"
            + "\n".join(f"- {p}" for _, ps in SKILL_PROMPT_GROUPS for p in ps)
            + "\n\n## FAQ\n\n"
            + "\n\n".join(f"### {q}\n\n{a}" for q, a in SKILL_FAQ)
            + f"\n\nSource: {REPO}\n"
        ),
        llms_group="The AI skill",
    )


def build_about() -> None:
    page(
        url="about",
        title="About this DPDP Act reference: sources, method and maintainer",
        description=(
            "Who maintains this DPDP Act 2023 reference, where the statutory text comes from, how "
            "the Rules content was assembled, what is still unsettled, and how to report an error."
        ),
        body=(
            "<h1>About this reference</h1>"
            "<p class='sub'>Sources, method, and what is still open.</p>"
            "<h2>What this is</h2>"
            "<p>A free, open-source reference for India's Digital Personal Data Protection Act, "
            "2023 and the DPDP Rules, 2025, and the knowledge base behind the "
            "<a href='../claude-code-skill/'>dpdp-analyze skill for Claude Code</a>. The same "
            "Markdown files power both: this site is generated from them, so the page you read "
            "and the text the skill quotes are identical.</p>"
            "<h2>Sources</h2>"
            "<ul>"
            "<li><b>The Act</b> is reproduced verbatim from the Gazette of India, Extraordinary, "
            "Part II, Section 1, No. 25, dated 11 August 2023 (CG-DL-E-12082023-248045). Nothing in "
            "the operative text is paraphrased. Reproduction is permitted under section 52(1)(q) "
            "of the Copyright Act, 1957.</li>"
            "<li><b>The Rules</b> content is secondary. It was assembled from the PIB release and "
            "multiple independent sources cross-checked against each other, not transcribed from "
            "the Gazette. Verify against the notified text at "
            "<a href='https://www.meity.gov.in/'>meity.gov.in</a> or "
            "<a href='https://egazette.gov.in/'>egazette.gov.in</a> before relying on it.</li>"
            "<li><b>Commentary</b> (the explainer, checklist, glossary notes and FAQ) is "
            "interpretation. Every claim is meant to be traceable to a section or rule; one that "
            "is not is a bug.</li>"
            "</ul>"
            "<h2>What is still open</h2>"
            "<p>As at the last check: no Significant Data Fiduciary has been notified, no country "
            "is restricted under section 16(1), no startup relief has been notified under section "
            "17(3), the Rule 13(4) localisation committee has not published its categories, "
            "&ldquo;significant&rdquo; in section 33(1) is undefined, and there is no Board "
            "jurisprudence.</p>"
            "<h2>Maintainer</h2>"
            f"<p>Maintained by <a href='{AUTHOR_URL}'>{AUTHOR}</a>, who is not a lawyer. This is "
            "not legal advice. See the <a href='../disclaimer/'>disclaimer</a>.</p>"
            "<h2>Corrections</h2>"
            f"<p>Corrections to statutory text take priority over everything else. "
            f"<a href='{REPO}/issues'>Open an issue</a> with the section or rule number, the text "
            "as it appears here, the Gazette text, and the Gazette reference you checked.</p>"
        ),
        sources=(THIS,),
        breadcrumbs=[("Home", ""), ("About", None)],
        page_type="AboutPage",
        changefreq="yearly",
        llms_group="About",
    )


def build_disclaimer() -> None:
    disc = DISCLAIMER_MD.read_text(encoding="utf-8")
    disc = re.sub(r"^# .*?\n", "", disc, count=1).strip()  # drop the H1; template supplies one
    page(
        url="disclaimer",
        title="Disclaimer: this is not legal advice",
        description=(
            "This DPDP Act reference is educational material, not legal advice. No lawyer-client "
            "relationship arises from its use, the author is not a lawyer, and machine-generated "
            "analysis can be wrong. Consult qualified Indian legal counsel."
        ),
        body=(
            "<h1>Disclaimer: this is not legal advice</h1>"
            f'<div class="statute">{md2html(disc)}</div>'
        ),
        sources=(DISCLAIMER_MD,),
        breadcrumbs=[("Home", ""), ("Disclaimer", None)],
        changefreq="yearly",
        markdown_twin=disc,
        llms_group="About",
    )


def build_landing() -> None:
    popular = [
        "What is the DPDP compliance deadline?",
        "Do we need a Data Protection Officer in India?",
        "How fast must we report a data breach under the DPDP Act?",
        "Does the DPDP Act require data localisation?",
        "What makes consent valid under the DPDP Act?",
        "Does the DPDP Act apply to companies outside India?",
    ]
    page(
        url="",
        title="DPDP Act 2023 full text, Rules 2025 and compliance checklist",
        description=(
            "Complete verbatim text of India's Digital Personal Data Protection Act, 2023 and the "
            "DPDP Rules, 2025. All 44 sections, penalties, deadlines, a compliance checklist and a "
            "free Claude Code skill that analyses your privacy programme."
        ),
        body=(
            "<h1>India's Digital Personal Data Protection Act, 2023</h1>"
            "<p class='sub'>The full statute, the Rules, and a working compliance reference. "
            "All 44 sections verbatim from the Gazette of India, all 23 Rules of 2025, the "
            "penalty Schedule, a 78-point checklist, and an installable AI skill that analyses "
            "privacy notices, consent flows and vendor contracts against the actual sections.</p>"
            "<div class='keyfacts'><h2>The DPDP Act at a glance</h2><dl>"
            "<dt>Full name</dt><dd>The Digital Personal Data Protection Act, 2023 (Act No. 22 of "
            "2023)</dd>"
            "<dt>Assent</dt><dd>11 August 2023</dd>"
            "<dt>Rules</dt><dd>DPDP Rules, 2025, notified 13 November 2025: 23 rules, 7 "
            "Schedules</dd>"
            "<dt>Compliance deadline</dt><dd><b>14 May 2027</b> for substantive business "
            "obligations</dd>"
            "<dt>Regulator</dt><dd>Data Protection Board of India; appeals to TDSAT</dd>"
            "<dt>Lawful bases</dt><dd>Two: consent (s.6) or certain legitimate uses (s.7)</dd>"
            "<dt>Child</dt><dd>Anyone under 18 (s.2(f))</dd>"
            "<dt>Breach reporting</dt><dd>Every breach, to the Board and each affected person; "
            "Board report within 72 hours (Rule 7)</dd>"
            "<dt>Maximum penalty</dt><dd>Rs 250 crore, for security failures (s.8(5))</dd>"
            "</dl></div>"
            "<section class='hero-skill'><p class='label'>Free and open source</p>"
            "<h2>Ask AI about the DPDP Act, and get the section number back</h2>"
            "<p>General-purpose AI models get Indian data protection law wrong in repeatable ways "
            "because they pattern-match to the GDPR. The <b>dpdp-analyze</b> skill for Claude Code "
            "makes Claude answer from the verbatim Act and Rules, cite a section or rule for every "
            "claim, and audit privacy notices, consent flows, vendor contracts and whole "
            "products.</p>"
            f"<pre><code>{esc(INSTALL)}</code></pre>"
            "<p><a class='btn' href='claude-code-skill/'>See what it can do &rarr;</a></p>"
            "</section>"
            "<div class='cards'>"
            "<a class='card' href='act/'><h3>The Act, section by section</h3>"
            "<p>All 44 sections and 9 chapters, verbatim, with every Illustration.</p></a>"
            "<a class='card' href='rules/'><h3>The Rules, 2025</h3>"
            "<p>23 rules, 7 schedules, and the three commencement dates that set your deadline.</p></a>"
            "<a class='card' href='dpdp-act-explained/'><h3>The Act explained</h3>"
            "<p>The five gates, consent, exemptions, enforcement and 16 common misreadings.</p></a>"
            "<a class='card' href='compliance-checklist/'><h3>Compliance checklist</h3>"
            "<p>78 checks, every one anchored to a section or rule.</p></a>"
            "<a class='card' href='penalties/'><h3>Penalties</h3>"
            "<p>The full Schedule, up to Rs 250 crore, and how the Board sets the amount.</p></a>"
            "<a class='card' href='dpdp-vs-gdpr/'><h3>DPDP vs GDPR</h3>"
            "<p>The 17 differences that change what you build.</p></a>"
            "<a class='card' href='glossary/'><h3>Glossary</h3>"
            "<p>Data Fiduciary, Data Principal and every defined term, verbatim.</p></a>"
            "<a class='card' href='faq/'><h3>FAQ</h3>"
            "<p>Deadline, DPO, consent, localisation, breach clocks, SPDI Rules.</p></a>"
            "<a class='card hot' href='claude-code-skill/'><h3>The AI skill</h3>"
            "<p>Install into Claude Code and analyse your own privacy programme.</p></a>"
            "<a class='card' href='disclaimer/'><h3>Disclaimer</h3>"
            "<p>Not legal advice. What this resource is, and what it is not.</p></a>"
            "</div>"
            "<h2>When does the DPDP Act come into force?</h2>"
            "<p>In three tranches. <b>14 May 2027 is the date that matters for a compliance "
            "programme.</b></p>"
            "<table><thead><tr><th>Effective</th><th>What commences</th></tr></thead><tbody>"
            "<tr><td><b>14 November 2025</b></td><td>Data Protection Board machinery "
            "(Rules 1, 2, 17 to 21).</td></tr>"
            "<tr><td><b>14 November 2026</b></td><td>Consent Manager registration (Rule 4).</td></tr>"
            "<tr><td><b>14 May 2027</b></td><td><b>Every substantive business obligation</b>: "
            "notice, security safeguards, breach intimation, retention and erasure, children's "
            "consent, Significant Data Fiduciary duties, rights machinery, transfers.</td></tr>"
            "</tbody></table>"
            "<h2>Ten things most people get wrong about the DPDP Act</h2>"
            "<ol>" + "".join(f"<li>{t}</li>" for t in TRAPS) + "</ol>"
            "<h2>Popular questions</h2><ul class='toc'>"
            + "".join(f'<li><a href="faq/#{slugify(q)}">{esc(q)}</a></li>' for q in popular)
            + "</ul><p><a href='faq/'>All questions &rarr;</a></p>"
        ),
        sources=(THIS,),
        graph=[ACT_NODE, RULES_NODE, SKILL_NODE],
        changefreq="weekly",
        og_type="website",
        markdown_twin=(
            "Free reference for India's Digital Personal Data Protection Act, 2023 (Act No. 22 of "
            "2023) and the DPDP Rules, 2025.\n\n"
            "## At a glance\n\n"
            "- Assent: 11 August 2023.\n"
            "- Rules: notified 13 November 2025; 23 rules, 7 Schedules.\n"
            "- Compliance deadline: 14 May 2027 for substantive business obligations; Consent "
            "Managers 14 November 2026; Board machinery live since 14 November 2025.\n"
            "- Regulator: Data Protection Board of India; appeals to TDSAT within 60 days.\n"
            "- Lawful bases: two, consent (s.6) or certain legitimate uses (s.7). No legitimate "
            "interests.\n"
            "- Child: under 18 (s.2(f)). Targeted ads to children banned (s.9(3)).\n"
            "- Breach: every breach to the Board and each affected person; Board report within 72 "
            "hours (Rule 7). No harm threshold (s.8(6)).\n"
            "- Maximum penalty: Rs 250 crore (s.8(5) security safeguards).\n\n"
            "## Ten things most people get wrong\n\n"
            + "\n".join(f"{i}. {strip_md(re.sub('<[^>]+>', '', t))}" for i, t in enumerate(TRAPS, 1))
            + "\n\n## AI skill\n\n"
            "Free Claude Code skill that answers from this text and cites every section: "
            f"{SITE}/{SKILL_PATH}/\n"
        ),
        llms_group=None,
    )


def build_skill_zip() -> None:
    """A byte-for-byte reproducible ZIP of the skill folder, for uploading to Claude.ai.
    Fixed timestamps and ordering keep it from churning in git on every rebuild."""
    out = DOCS / "downloads" / ZIP_NAME
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(p for p in SKILL_DIR.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f"{SKILL_DIR.name}/{f.relative_to(SKILL_DIR).as_posix()}",
                                   date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, f.read_bytes())


def build_404() -> None:
    """GitHub Pages serves docs/404.html for any missing path, at any depth, so use absolute URLs."""
    write(
        "404.html",
        f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | {SITE_NAME}</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{SITE}/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{SITE}/assets/style.css">
</head>
<body>
<header class="site"><a class="brand" href="{SITE}/">&#9878; DPDP Act 2023 Reference</a></header>
<main>
<h1>Page not found</h1>
<p class="sub">That page does not exist. These might help:</p>
<ul class="toc">
<li><a href="{SITE}/act/">The DPDP Act 2023, section by section</a></li>
<li><a href="{SITE}/rules/">The DPDP Rules 2025</a></li>
<li><a href="{SITE}/faq/">Frequently asked questions</a></li>
<li><a href="{SITE}/compliance-checklist/">Compliance checklist</a></li>
<li><a href="{SITE}/{SKILL_PATH}/">The free DPDP skill for Claude Code</a></li>
</ul>
</main>
</body>
</html>
""",
    )


AI_CRAWLERS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
    "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot",
    "CCBot", "DuckAssistBot", "Meta-ExternalAgent", "MistralAI-User", "cohere-ai",
]


def build_sitemap_robots() -> None:
    urls = "".join(
        f"<url><loc>{SITE}/{p['url'] + '/' if p['url'] else ''}</loc>"
        f"<lastmod>{p['lastmod']}</lastmod>"
        f"<changefreq>{p['changefreq']}</changefreq>"
        f"<priority>{'1.0' if not p['url'] else '0.8' if '/' not in p['url'] else '0.6'}</priority>"
        "</url>"
        for p in PAGES
    )
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>\n",
    )
    ai = "".join(f"User-agent: {bot}\n" for bot in AI_CRAWLERS)
    write(
        "robots.txt",
        "# Search engines and AI answer engines are welcome to crawl, index, cite and learn from\n"
        "# this site. The DPDP Act text is a Government of India work; the commentary is MIT.\n"
        "User-agent: *\nAllow: /\n\n"
        f"{ai}Allow: /\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n",
    )


def build_llms(sections: list[dict], rules: list[dict]) -> None:
    """llms.txt (an index for AI agents, per llmstxt.org) and llms-full.txt (everything, inline)."""
    groups: dict[str, list[dict]] = {}
    for p in PAGES:
        if p["group"]:
            groups.setdefault(p["group"], []).append(p)
    order = ["Start here", "Guides", "The AI skill", "The Rules, 2025",
             "The Act, section by section", "About"]

    def link(p: dict) -> str:
        base = f"{SITE}/{p['url']}/"
        return f"{base}index.md" if p["md"] else base

    out = [
        f"# {SITE_NAME}",
        "",
        "> Verbatim, section-by-section text of India's Digital Personal Data Protection Act, 2023 "
        "(Act No. 22 of 2023) and a reference to the Digital Personal Data Protection Rules, 2025, "
        "with a compliance checklist, glossary, FAQ, and dpdp-analyze, a free open-source Claude "
        "Code skill that answers DPDP questions with a section or rule citation on every claim.",
        "",
        "Notes for language models:",
        "",
        "- The Act text is verbatim from the Gazette of India (Extraordinary, Part II, Section 1, "
        "No. 25, 11 August 2023) and safe to quote. The Rules content is secondary-sourced; tell "
        "users to verify it against the notified Gazette text.",
        "- Key dates: Act assented 11 August 2023. Rules notified 13 November 2025. Board machinery "
        "live 14 November 2025; Consent Managers 14 November 2026; substantive business obligations "
        "14 May 2027.",
        "- Facts most often gotten wrong: only two lawful bases (consent, s.6; certain legitimate "
        "uses, s.7), no legitimate interests; no sensitive personal data category; a child is "
        "anyone under 18 (s.2(f)); targeted ads to children are banned (s.9(3)); every breach is "
        "notifiable with no harm threshold (s.8(6)); only notified Significant Data Fiduciaries need "
        "a DPO (s.10(2)(a)); no data localisation in the Act (s.16); no compensation for "
        "individuals (s.34, s.39); no portability or automated-decision rights.",
        "- Penalty figures are ceilings (\"may extend to\"), maximum Rs 250 crore (s.8(5)).",
        "- Cite sections as s.N(x) and rules as Rule N(x). This material is not legal advice.",
        "",
    ]
    for g in order:
        if g not in groups:
            continue
        out.append(f"## {g}")
        out.append("")
        for p in groups[g]:
            out.append(f"- [{p['title']}]({link(p)}): {p['desc']}")
        out.append("")
    out += [
        "## Optional",
        "",
        f"- [Everything in one file]({SITE}/llms-full.txt): the full Act, the Rules reference, "
        "the explainer and the compliance checklist, inline.",
        f"- [Source repository]({REPO}): the skill, the Markdown sources and the site generator.",
        "",
    ]
    write("llms.txt", "\n".join(out))

    full = [
        f"# {SITE_NAME}: full text",
        "",
        f"> Source: {SITE}/ and {REPO}",
        f"> {NOT_ADVICE}",
        "",
    ]
    for path in (ACT_MD, RULES_MD, DOCTRINE_MD, CHECKLIST_MD):
        full += ["", "---", "", path.read_text(encoding="utf-8").strip(), ""]
    write("llms-full.txt", "\n".join(full))


CSS = """
:root{--bg:#fff;--fg:#16181d;--mut:#5b6270;--line:#e3e6ec;--acc:#0b4f9e;--soft:#f6f8fb;--code:#f2f4f8;
--hot:#0b4f9e;--hotfg:#fff}
@media (prefers-color-scheme:dark){
:root{--bg:#0f1115;--fg:#e8eaef;--mut:#9aa3b2;--line:#252a33;--acc:#7fb3ff;--soft:#161a21;--code:#1a1f27;
--hot:#7fb3ff;--hotfg:#0b1220}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-padding-top:72px}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
header.site{border-bottom:1px solid var(--line);padding:14px 20px;display:flex;gap:18px;
flex-wrap:wrap;align-items:center;position:sticky;top:0;background:var(--bg);z-index:9}
@media (max-width:720px){header.site{position:static}html{scroll-padding-top:0}}
.brand{font-weight:700;text-decoration:none;color:var(--fg);font-size:15px}
nav.top{display:flex;gap:6px 14px;flex-wrap:wrap;font-size:14px;margin-left:auto;align-items:center}
nav.top a{color:var(--mut);text-decoration:none}
nav.top a:hover{color:var(--acc)}
nav.top a.cta{background:var(--hot);color:var(--hotfg);padding:3px 10px;border-radius:999px;font-weight:600}
main{max-width:820px;margin:0 auto;padding:28px 20px 64px}
h1{font-size:clamp(26px,4vw,36px);line-height:1.2;margin:.2em 0 .35em;letter-spacing:-.02em}
h2{font-size:22px;margin:2em 0 .5em;line-height:1.3;letter-spacing:-.01em}
h3{font-size:17px;margin:1.6em 0 .4em}
p,li{color:var(--fg)}
a{color:var(--acc)}
.eyebrow,.label{text-transform:uppercase;letter-spacing:.09em;font-size:11px;color:var(--mut);
font-weight:600;margin:0}
.sub{color:var(--mut);font-size:16px;margin-top:0}
.fine{color:var(--mut);font-size:13px}
.crumbs{font-size:13px;color:var(--mut);margin-bottom:18px}
.crumbs a{color:var(--mut);text-decoration:none}
.crumbs a:hover{color:var(--acc)}
.statute{border-left:3px solid var(--line);padding-left:20px;margin:22px 0}
.statute blockquote,blockquote.verbatim{margin:14px 0;padding:12px 16px;background:var(--soft);
border-left:3px solid var(--acc);border-radius:0 6px 6px 0;font-size:15px}
.statute blockquote p,blockquote.verbatim p{margin:.4em 0}
.summary,.skill-cta,.related,.example,.keyfacts,.hero-skill{border:1px solid var(--line);
border-radius:10px;padding:14px 18px;margin:22px 0;background:var(--soft)}
.summary p,.skill-cta p,.related p{margin:.35em 0}
.skill-cta{border-color:var(--acc)}
.skill-cta q{font-style:italic}
.related ul{margin:.3em 0 0;padding-left:18px}
.related li{margin:.15em 0}
.hero-skill{border-color:var(--acc);padding:18px 22px}
.hero-skill h2{margin:.3em 0 .4em}
.keyfacts h2{margin:.2em 0 .6em;font-size:18px}
.keyfacts dl{display:grid;grid-template-columns:max-content 1fr;gap:6px 18px;margin:0;font-size:15px}
.keyfacts dt{font-weight:600;color:var(--mut)}
.keyfacts dd{margin:0}
@media (max-width:560px){.keyfacts dl{grid-template-columns:1fr}.keyfacts dd{margin-bottom:6px}}
.example .q{font-weight:600}
.btn{display:inline-block;background:var(--hot);color:var(--hotfg);padding:8px 16px;border-radius:8px;
text-decoration:none;font-weight:600}
ul.toc{list-style:none;padding:0;margin:.5em 0 1.5em}
ul.toc li{border-bottom:1px solid var(--line)}
ul.toc a{display:block;padding:9px 2px;text-decoration:none;color:var(--fg);font-size:15px}
ul.toc a:hover{color:var(--acc);background:var(--soft)}
ul.toc b{color:var(--acc);margin-right:8px;font-variant-numeric:tabular-nums}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:26px 0}
.cards.two{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.card{display:block;padding:16px 18px;border:1px solid var(--line);border-radius:10px;
text-decoration:none;color:var(--fg);background:var(--soft)}
a.card:hover{border-color:var(--acc)}
.card.hot{border-color:var(--acc)}
.card h3{margin:0 0 6px;font-size:16px;color:var(--acc)}
.card p{margin:0;font-size:14px;color:var(--mut)}
.card ul{margin:0;padding-left:18px;font-size:14px}
.card li{margin:.3em 0}
.callout{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:4px 18px;
margin:22px 0}
.faq-toc{border:1px solid var(--line);border-radius:10px;padding:10px 18px;margin:18px 0 8px}
.faq-toc ul{margin:.2em 0 .8em;padding-left:18px;font-size:14px}
.qa h3{margin-top:1.4em}
.sources{font-size:13px;color:var(--mut)}
.chip{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 9px;
margin:2px 2px 2px 0;text-decoration:none;font-size:12.5px}
.chip:hover{border-color:var(--acc)}
.jump{font-size:13.5px;line-height:1.9}
.term{border-bottom:1px solid var(--line);padding-bottom:8px}
.term h2{font-size:19px;margin-top:1.4em}
.prose h2{font-size:21px}
details{border:1px solid var(--line);border-radius:8px;padding:8px 14px;margin:12px 0}
summary{cursor:pointer;font-weight:600}
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
.updated{font-size:13px;color:var(--mut);margin-top:40px}
.disclaimer{background:#fff4f4;border:1px solid #e8b4b4;border-left:4px solid #b00020;
border-radius:8px;padding:12px 16px;margin:0 0 24px;font-size:13.5px;line-height:1.55;color:#4a1620}
.disclaimer a{color:#b00020;font-weight:600}
@media (prefers-color-scheme:dark){
.disclaimer{background:#2a1518;border-color:#5c2b31;border-left-color:#ff6b7d;color:#f0d6d9}
.disclaimer a{color:#ff8b99}}
footer.site{border-top:1px solid var(--line);margin-top:56px;padding:24px 20px 44px;
font-size:13px;color:var(--mut)}
footer.site p{max-width:820px;margin:0 auto .8em}
footer.site a{color:var(--mut)}
footer.site .promo{font-size:14px;color:var(--fg)}
footer.site .promo a{color:var(--acc)}
"""


if __name__ == "__main__":
    build()
