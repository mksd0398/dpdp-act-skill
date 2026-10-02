# Contributing

## Corrections to statutory text come first

This repository's value is that the Act text is exact. If you find any deviation from the Gazette
of India, that is the highest priority issue you can file.

When reporting a text error, please include:

1. The section or rule number.
2. The text as it appears here.
3. The text as it appears in the Gazette.
4. A link or citation to the Gazette source you checked.

## Rules content

`skills/dpdp-analyze/references/rules-2025.md` is assembled from the PIB release and cross-checked
secondary sources, not transcribed from the Gazette. Corrections that replace a secondary-sourced
passage with verified Gazette text are very welcome. Please cite the Gazette reference.

## Commentary and analysis

`doctrine.md`, `compliance-checklist.md` and the site's explanatory pages are interpretation. Where
you disagree, open an issue with the section anchor and the reasoning. Every claim in those files
must be traceable to a section or rule; anything that is not is a bug.

## Notifications and subordinate legislation

The Act delegates a great deal to Rules and to government notifications. If a Significant Data
Fiduciary is notified, a country is restricted under s.16(1), startup relief is granted under
s.17(3), or the Rule 13(4) committee publishes its categories, please open an issue with the
notification reference so the "what is still open" sections can be updated.

## Rebuilding the site

```bash
pip install markdown
python tools/build_site.py
```

The site in `docs/` is generated. Edit the Markdown in `skills/dpdp-analyze/references/`, then
rebuild. Do not hand-edit files in `docs/`. Static files (the social card, favicon, IndexNow key)
live in `tools/static/` and are copied into `docs/` on every build. To regenerate the social card
after editing `tools/og-card.html`, run `node tools/render_og.mjs` with Playwright installed. To
build for a custom domain, set `SITE_URL`, for example `SITE_URL=https://dpdp.example.in`.

## Not legal advice

Nothing here is legal advice, and contributions should not be framed as such.
