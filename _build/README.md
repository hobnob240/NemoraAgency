# nemora.uk build

`python3 _build/build.py .` rebuilds every page of nemora.uk from this script. Jekyll skips folders starting with `_`, so nothing here is published.

- Guides: add one object to `guides.json` (slug, date YYYY-MM-DD, mins, title, desc, intro, body HTML), run the build, and the guide page, the guides hub, the sitemap and the structured data all update.
- The guides writer agent follows the `guides_playbook` rules in the NEMORA database. It may only add or fix guides: after a build, `git status` must show changes to `_build/guides.json`, `guides/` and `sitemap.xml` only. Anything else means stop and tell Charlie.
