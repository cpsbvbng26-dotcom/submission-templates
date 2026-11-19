# 埋めた例：sophaxis v1.0.0 の .zenodo.json（Zenodo）

- 記録の DOI：10.5281/zenodo.24033372（cpsbvbng26-dotcom の `docs/doi-index.md` の R13。利用者から受け取った番号。2026-11-19 に DataCite の記録で、題・筆頭の著者・版 v1.0.0・種類 Software を確かめた）
- 状態：出した。Zenodo の GitHub の連携が、タグ v1.0.0 の版から記録を作った
- 下の囲みは、sophaxis のタグ v1.0.0（コミット b8f9fe88f782ba35e04bfa0347efb3ab386b74c8）の `.zenodo.json` を一字も変えずに写したものです。いまの sophaxis の `.zenodo.json` は、この後に直してあります

---

```json
{
  "title": "Sophaxis: an overlay preprint server for philosophy and mathematics",
  "description": "<p>Sophaxis is an overlay preprint server for philosophy, mathematics, logic, the philosophy of mathematics and the philosophy of science. It holds no manuscripts of its own: authors submit a preprint they have deposited in a repository (Zenodo, Figshare, arXiv, SSRN and others) by its DOI and their ORCID iD, and after moderation it is listed with a stable record page.</p><p>This record is the code and the records of the site: a static site generator with no dependencies, the submission intake (metadata from DataCite, Crossref and JaLC, an ORCID check that the submitter is an author), the weekly watch of listed works, the policies, and the checks that run on every change. Acceptance is moderation, not peer review.</p><p>Site: https://sophaxis.vercel.app/</p>",
  "upload_type": "software",
  "license": "mit",
  "access_right": "open",
  "language": "eng",
  "creators": [
    {
      "name": "Nemoto, Takuya",
      "orcid": "0009-0000-1406-0547"
    }
  ],
  "keywords": [
    "preprint server",
    "overlay journal",
    "philosophy",
    "mathematics",
    "logic",
    "open access",
    "ORCID",
    "DataCite",
    "static site"
  ],
  "related_identifiers": [
    {
      "identifier": "10.17605/OSF.IO/MQ7ZA",
      "relation": "isPartOf",
      "scheme": "doi"
    },
    {
      "identifier": "https://sophaxis.vercel.app/",
      "relation": "isSupplementTo",
      "scheme": "url"
    }
  ],
  "notes": "Built with Claude Code (Anthropic) at the author's request. The author reviewed the work and is responsible for it. Claude is not an author. The text of the site is CC BY 4.0; the code is MIT."
}
```
