#!/usr/bin/env python3
"""The checks of submission-templates.

  python3 verification/check.py            offline: templates, examples, and the DOIs against the cached registry records
  python3 verification/check.py --online   the same, but every DOI is resolved again at Crossref (then DataCite), and the
                                           example copied from a repository is fetched again from GitHub
  python3 verification/check.py --record   --online, and write the registry records into verification/cache/
  python3 verification/check.py --break    every check fails when the thing it watches is broken (offline)
"""
import datetime
import hashlib
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rules  # noqa: E402
from rules import add, jload, sub  # noqa: E402

PROSE = ["README.md", "README.en.md"]
VENUES = ("figshare", "sophaxis", "ssrn", "philarchive", "zenodo")
MARKS = ("場の頁で確かめた", "運営者の記録による", "記憶による")
# A field marked 運営者の記録による names, in brackets, the repository and the file of the record.
RECORD_MARK = re.compile(r"^確かめ：運営者の記録による（[^）]*\b[a-z0-9]+(?:-[a-z0-9]+)+ の [\w./-]+\.(?:md|json|toml|yml)")
EMAIL_FIELD = "（本人のものを入力）"
CACHE = "verification/cache/registry.json"
DOI = re.compile(r"10\.\d{4,9}/[^\s)（）、,;`\"]+", re.I)
UA = {"User-Agent": "submission-templates-check/1.0 (+https://github.com/cpsbvbng26-dotcom/submission-templates)"}


def today():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def letters(s):
    s = re.sub(r"\$[^$]*\$", "", str(s or ""))
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", s.casefold())


def family(s):
    s = str(s or "").strip()
    if not re.search(r"[A-Za-z]", s):
        return unicodedata.normalize("NFKC", s)
    if "," in s:
        s = s.split(",")[0]
    return letters(s.split()[-1])


def dois_in(text):
    return sorted({d.rstrip(".:").lower() for d in DOI.findall(text)})


def body(text):
    i = text.find("\n---\n\n")
    return text[i + 6:] if i >= 0 else None


def sections(text):
    out = []
    for chunk in re.split(r"\n(?=## )", text)[1:]:
        head, _, rest = chunk.partition("\n")
        out.append((head[3:].strip(), rest))
    return out


def block(F):
    return F.get("blocks/disclosure.md", "").strip("\n")


# ------------------------------------------------------------------ checks

def layout(F):
    bad = []
    have = sorted({f.split("/")[1] for f in F if f.startswith("venues/")})
    if have != sorted(VENUES):
        bad.append("the venues are " + ", ".join(have))
    for v in VENUES:
        for f in ("fields.md", "steps.md"):
            if "venues/%s/%s" % (v, f) not in F:
                bad.append(v + ": no " + f)
        if not any(re.fullmatch(r"venues/%s/examples/[a-z0-9.-]+\.md" % v, f) for f in F):
            bad.append(v + ": no example")
    return bad


def templates(F):
    bad = []
    b = block(F)
    if not b.startswith("<!-- 開示の段：ここから") or "Claude is not an author." not in b or not b.endswith("<!-- 開示の段：ここまで -->"):
        bad.append("blocks/disclosure.md is not the fixed block")
    for v in VENUES:
        f = "venues/%s/fields.md" % v
        t = F.get(f, "")
        if b not in t:
            bad.append(f + ": the disclosure block is missing or changed")
        for name, rest in sections(t):
            marks = [line for line in rest.split("\n") if line.startswith("確かめ：")]
            if len(marks) != 1 or not marks[0][4:].startswith(MARKS):
                bad.append("%s %s: one mark, 場の頁で確かめた, 運営者の記録による or 記憶による" % (f, name))
            elif marks[0][4:].startswith("運営者の記録による") and not RECORD_MARK.match(marks[0]):
                bad.append("%s %s: 運営者の記録による without the repository and the file of the record" % (f, name))
            if "Email" in name and EMAIL_FIELD not in rest:
                bad.append("%s %s: an e-mail field without %s" % (f, name, EMAIL_FIELD))
        for m in re.finditer(r"\{\{[^}]*\}\}|\{\{|\}\}", t):
            if not re.fullmatch(r"\{\{[A-Z][A-Z_]*\}\}", m.group(0)):
                bad.append(f + ": a malformed placeholder " + m.group(0)[:30])
        for g in ("fields.md", "steps.md"):
            for m in rules.KANJI_COUNT.finditer(F.get("venues/%s/%s" % (v, g), "")):
                bad.append("venues/%s/%s: a number in kanji「%s」" % (v, g, m.group(0)))
        if not any(re.search(r"\(\./examples/[a-z0-9.-]+\.md\)", t) for _ in [0]):
            bad.append(f + ": does not link its example")
    return bad


def examples(F):
    E = jload(F, "verification/examples.json")
    if not E:
        return ["verification/examples.json cannot be read"]
    bad = []
    listed = {e["file"] for e in E["examples"]}
    on_disk = {f for f in F if re.fullmatch(r"venues/[a-z]+/examples/[a-z0-9.-]+\.md", f)}
    if listed != on_disk:
        bad.append("the examples listed and on disk differ")
    seen = set()
    for e in E["examples"]:
        f = e["file"]
        t = F.get(f, "")
        if e["status"] not in ("deposited", "prepared"):
            bad.append(f + ": the status")
        if e["status"] == "deposited" and not e.get("doi"):
            bad.append(f + ": deposited without a DOI")
        if e.get("doi") and e["doi"] not in t:
            bad.append(f + ": does not name its DOI")
        b = body(t)
        if b is None or hashlib.sha256(b.encode("utf-8")).hexdigest() != e["body_sha256"]:
            bad.append(f + ": the copied part differs from the copy that was made")
        if "Claude" not in t or not re.search(r"not an author", t):
            bad.append(f + ": no disclosure of the language model")
        for d in dois_in(t):
            seen.add(d)
            if d not in E["dois"]:
                bad.append("%s: %s is not in the list of DOIs" % (f, d))
    for d, x in E["dois"].items():
        if d not in seen:
            bad.append(d + ": listed, and in no example")
        if not x.get("source") or x.get("match") not in ("exact", "prefix"):
            bad.append(d + ": source or match")
    return bad


def against(F, records):
    E = jload(F, "verification/examples.json") or {"dois": {}}
    bad = []
    for d, x in E["dois"].items():
        r = records.get(d)
        if r is None or "error" in r:
            bad.append(d + ": no registry record" + (" (" + r["error"] + ")" if r else ""))
            continue
        a, b = letters(r["title"]), letters(x["title"])
        if not (a == b if x["match"] == "exact" else a.startswith(b) and b):
            bad.append("%s: title: list %r, %s %r" % (d, x["title"], r["registry"], r["title"]))
        if family(r["first_author"]) != family(x["first_author"]):
            bad.append("%s: first author: list %r, %s %r" % (d, x["first_author"], r["registry"], r["first_author"]))
    return bad


def registry_cached(F):
    C = jload(F, CACHE)
    if C is None:
        return [CACHE + " cannot be read"]
    bad = against(F, C["records"])
    E = jload(F, "verification/examples.json") or {"dois": {}}
    for k in sorted(set(C["records"]) - set(E["dois"])):
        bad.append(k + ": a cached record that no example uses")
    for k, r in C["records"].items():
        if r.get("fetched", "") > today() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r.get("fetched", "")):
            bad.append(k + ": the date fetched")
    return bad


def readme_venues(F):
    """Each README has a table of the venues whose links are, venue by venue, the fields, the steps and every example
    on disk, and nothing else."""
    bad = []
    want = {f for f in F if re.fullmatch(r"venues/[a-z]+/(fields\.md|steps\.md|examples/[a-z0-9.-]+\.md)", f)}
    for f in ("README.md", "README.en.md"):
        rows = [line for line in F.get(f, "").split("\n") if line.startswith("| ") and "](./venues/" in line]
        got = set()
        for row in rows:
            links = re.findall(r"\]\(\./(venues/[^)]+)\)", row)
            if len({x.split("/")[1] for x in links}) != 1:
                bad.append(f + ": a row of the venue table links more than one venue")
            got |= set(links)
        if len(rows) != len(VENUES) or got != want:
            bad.append(f + ": the venue table does not link every template, steps and example, and nothing else")
    return bad


COUNTERS = {
    "venues": lambda F: len({f.split("/")[1] for f in F if f.startswith("venues/")}),
    "examples": lambda F: len((jload(F, "verification/examples.json") or {"examples": []})["examples"]),
    "deposited": lambda F: sum(1 for e in (jload(F, "verification/examples.json") or {"examples": []})["examples"] if e["status"] == "deposited"),
}

CHECKS = [
    ("One folder per venue, each with fields, steps and at least one example", layout),
    ("Every template field is marked 場の頁で確かめた, 運営者の記録による (naming the record) or 記憶による, has the fixed disclosure block, asks for an e-mail only as （本人のものを入力）, and uses well-formed placeholders", templates),
    ("Every filled example is listed, is the copy that was made, discloses the language model, and lists every DOI it names with its source", examples),
    ("Every DOI in a filled example resolves at Crossref or DataCite with the title and first author listed (cached; --online fetches again)", registry_cached),
    ("Copies of the canonical files and the licences are byte-identical (sha256)", rules.copies),
    ("No name of the operator's own university in any spelling, other place of creative work, self-title, item of rule 10 or single relative", rules.words_not_written),
    ("No e-mail address in any file", rules.no_email),
    ("Workflows: actions pinned to commits, permissions, timeouts; Dependabot", rules.workflows),
    ("labels.yml makes the labels of the canonical workflows", lambda F: rules.labels(F)),
    ("CLAUDE.md carries rules 16, 17 and 18 (10 times)", rules.claude_md),
    ("The writing rules: です/ます, no second person, no bold, one dash per paragraph, short sentences", lambda F: rules.prose(F, PROSE)),
    ("Every number in prose is in the ledger of numbers, and every count matches the files", lambda F: rules.numbers(F, PROSE, COUNTERS)),
    ("README.md and README.en.md link each other, disclose the language model and name the licences", rules.readme_pair),
    ("Both READMEs have the venue table, linking every template, steps and example", readme_venues),
]


def http(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8")


def fetch_doi(doi):
    q = urllib.parse.quote(doi)
    try:
        m = json.loads(http("https://api.crossref.org/works/" + q))["message"]
        a = (m.get("author") or [{}])[0]
        return {"registry": "crossref", "title": (m.get("title") or [""])[0], "first_author": a.get("family") or a.get("name")}
    except Exception:
        a = json.loads(http("https://api.datacite.org/dois/" + q))["data"]["attributes"]
        c = (a.get("creators") or [{}])[0]
        return {"registry": "datacite", "title": a["titles"][0]["title"], "first_author": c.get("familyName") or c.get("name")}


def online(F, record):
    E = jload(F, "verification/examples.json")
    records, bad = {}, []
    for d in E["dois"]:
        try:
            records[d] = fetch_doi(d)
        except Exception as e:
            records[d] = {"error": str(e)}
        records[d]["fetched"] = today()
    bad += against(F, records)
    for e in E["examples"]:
        if e.get("source_raw"):
            try:
                got = http(e["source_raw"])
                if "```json\n" + got + "```\n" != body(F[e["file"]]):
                    bad.append(e["file"] + ": differs from " + e["source_raw"])
            except Exception as x:
                bad.append(e["file"] + ": " + str(x))
    if record:
        with open(os.path.join(rules.ROOT, CACHE), "w", encoding="utf-8") as fh:
            json.dump({"_": ["Records fetched by verification/check.py --record: Crossref first, DataCite when Crossref has no record."],
                       "records": dict(sorted(records.items()))}, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    for b in bad:
        print("  FAIL  " + b)
    print("\nonline: %d records, %d problems." % (len(records), len(bad)))
    return 1 if bad else 0


C = [c[0] for c in CHECKS]
FIG = "venues/figshare/fields.md"
BREAKS = [
    (C[0], "a venue without steps", lambda G: G.pop("venues/zenodo/steps.md")),
    (C[0], "a sixth venue", add("venues/osf/fields.md", "# OSF\n")),
    (C[1], "a field without a mark", sub(FIG, "## Keywords\n\n確かめ：記憶による（必須）\n", "## Keywords\n\n")),
    (C[1], "a mark outside the three", sub(FIG, "## Funding\n\n確かめ：記憶による", "## Funding\n\n確かめ：たぶん")),
    (C[1], "運営者の記録による without the record it names", sub("venues/ssrn/fields.md", "確かめ：運営者の記録による（Philosophy Research Network の Continental Philosophy だけ。原論文の区分として、cpsbvbng26-dotcom の docs/external-evaluations.md の「出した分野」にある。", "確かめ：運営者の記録による（Philosophy Research Network の Continental Philosophy だけ。原論文の区分として、記録にある。")),
    (C[1], "the disclosure block changed in one template", sub("venues/ssrn/fields.md", "The author is responsible for the content. Claude is not an author.", "The author is responsible for the content.")),
    (C[1], "an e-mail field with something else in it", sub("venues/ssrn/fields.md", "（本人のものを入力）", "（あとで書く）")),
    (C[1], "a malformed placeholder", sub(FIG, "{{TITLE}}", "{{title}}")),
    (C[1], "a number in kanji in the steps", add("venues/figshare/steps.md", "\n語は十語までにする。\n")),
    (C[2], "one character changed in a copied example", sub("venues/ssrn/examples/celibacy-follow-up.md", "Affiliation: none.", "Affiliation: none")),
    (C[2], "an example names a DOI that is not listed", add("venues/philarchive/examples/celibacy-follow-up.md", "\nSee also 10.1234/abcd.\n")),
    (C[2], "a deposited example without a DOI", sub("verification/examples.json", '"doi": "10.5281/zenodo.24033372"', '"doi": null')),
    (C[3], "a listed title that differs from the registry", sub("verification/examples.json", '"title": "Sophaxis: An Independent Overlay Preprint Server"', '"title": "Sophaxis: A Dependent Overlay Preprint Server"')),
    (C[3], "a listed first author that differs", sub("verification/examples.json", '"title": "The Hausdorff dimension of the survivor set", "first_author": "Kuang"', '"title": "The Hausdorff dimension of the survivor set", "first_author": "Xiao"')),
    (C[3], "a prefix match turned exact on a longer title", sub("verification/examples.json", '"match": "prefix"', '"match": "exact"')),
    (C[4], "one character of error-report.yml", sub(".github/ISSUE_TEMPLATE/error-report.yml", "誤りの知らせ", "誤りのお知らせ")),
    (C[4], "the note on the copies says the cross-repository check compares them", sub("verification/copies.json", "いま正本と写しを突き合わせるのは、このリポジトリの検査（verification/rules.py の copies）だけです。cpsbvbng26-dotcom の横断の検査（verification/check_ecosystem.js）は、まだこのリポジトリを見ていません。", "cpsbvbng26-dotcom の verification/check_ecosystem.js も、正本と写しを突き合わせます。")),
    (C[5], "the university's name in katakana", add("venues/zenodo/fields.md", "\n" + rules.dec("44K844Oz") + rules.dec("5aSn5a2m") + "\n")),
    (C[5], "the university's name, romanised", add("venues/zenodo/fields.md", "\n" + rules.dec("emVu") + " " + rules.dec("ZGFpZ2FrdQ==") + "\n")),
    (C[5], "the university's name in hiragana", add("venues/zenodo/fields.md", "\n" + rules.dec("44Gc44KT") + rules.dec("44Gg44GE44GM44GP") + "\n")),
    (C[5], "the university's name in katakana, spelt out", add("venues/zenodo/fields.md", "\n" + rules.dec("44K844Oz") + rules.dec("44OA44Kk44Ks44Kv") + "\n")),
    (C[6], "an e-mail address in a template", sub("venues/ssrn/fields.md", "（本人のものを入力）", "author" + "@" + "example.org")),
    (C[7], "an action named by its version", sub(".github/workflows/check.yml", "actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7", "actions/setup-python@v7")),
    (C[8], "labels.yml drops a label", sub(".github/workflows/labels.yml", 'gh label create "needs a person"', 'gh label create "person"')),
    (C[9], "CLAUDE.md loses rule 16", sub("CLAUDE.md", "**Claude は利用者に命令しない。**", "**Claude は利用者に頼む。**")),
    (C[10], "a sentence not in です/ます", add("README.md", "\n雛形は預け先ごとに置く。\n")),
    (C[10], "bold", sub("README.md", "預け先ごとに残すリポジトリです。", "**預け先ごとに残すリポジトリです。**")),
    (C[11], "a count that differs from the files", sub("README.md", "預け先は 5 か所です。", "預け先は 6 か所です。")),
    (C[11], "a number not in the ledger of numbers", add("README.en.md", "\nIt took 3 days.\n")),
    (C[12], "README.en.md loses the licences", sub("README.en.md", "(./LICENSE-CODE)", "(./LICENCE-CODE)")),
    (C[13], "README.en.md drops a venue from the table", sub("README.en.md", "| SSRN | [fields.md](./venues/ssrn/fields.md) | [steps.md](./venues/ssrn/steps.md) | [The follow-up to the celibacy paper](./venues/ssrn/examples/celibacy-follow-up.md) |\n", "")),
    (C[13], "README.en.md links the wrong example", sub("README.en.md", "(./venues/zenodo/examples/sophaxis-v1.0.0.md)", "(./venues/zenodo/examples/sophaxis-v1.0.1.md)")),
    (C[13], "an example on disk that README.md does not link", add("venues/figshare/examples/another.md", "x")),
]

if __name__ == "__main__":
    F = rules.load()
    if "--online" in sys.argv or "--record" in sys.argv:
        sys.exit(online(F, "--record" in sys.argv))
    sys.exit(rules.run(CHECKS, BREAKS, F, sys.argv))
