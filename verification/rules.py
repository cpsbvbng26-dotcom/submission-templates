"""Checks shared by omscs-preparation, reading-ledger and submission-templates.

The same file is in all three repositories. Each repository's verification/check.py imports it,
adds the checks of its own subject, and runs them. A check is a pure function: it takes the map of
files (path -> text) and returns a list of problems. --break copies the map, breaks one thing,
and confirms that the matching check returns at least one problem.

Words that these repositories do not write (the university, the operator's other place of
creative work, self-titles, the items of rule 10, words for a single living relative) are kept
in base64 below, so that this file does not itself contain them.
"""
import base64
import hashlib
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
BINARY_EXT = {".pdf", ".png", ".jpg", ".ico"}


def load(root=ROOT):
    files = {}
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            if os.path.splitext(fn)[1] in BINARY_EXT:
                continue
            with open(p, encoding="utf-8") as f:
                files[rel] = f.read()
    return files


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def jload(F, p):
    try:
        return json.loads(F[p])
    except Exception:
        return None


def dec(b):
    return base64.b64decode(b).decode("utf-8")


def norm(text):
    return unicodedata.normalize("NFKC", text).casefold()


# ------------------------------------------------------------------ words not written

SCHOOL = [re.compile(dec("emVu") + r"[\s\-_.・]*(" + dec("5aSn5a2m") + "|univ)"),
          re.compile(dec("44K844Oz") + r"[\s・]*" + dec("5aSn5a2m")),
          re.compile(dec("emVu") + r"\s*\.\s*ac\s*\.\s*jp")]
OTHER_PLACE = [dec(x) for x in ("bnVzcXVhbWE=", "44OM44K544Kv44Kh44Oe", "54Sh5L2V5pyJ6aiO5aOr546L5Zu9")]
TITLES = [re.compile(x) for x in (dec("54us56uL56CU56m26ICF"), dec("aW5kZXBlbmRlbnQ=") + r"\s+" + dec("cmVzZWFyY2hlcg=="),
                                  dec("Y29uc3VsdGFudA=="), dec("44Kz44Oz44K144Or44K/44Oz44OI"),
                                  "(" + dec("44Op44Kk44OW6YWN5L+h") + "|live)" + r"[\s-]*" + "stream",
                                  dec("c2VhbGFuZA=="), dec("44K344O844Op44Oz44OJ"))]
RELATIVES = [dec(x) for x in ("54i26Kaq", "5q+N6Kaq", "44GK54i244GV44KT", "44GK5q+N44GV44KT", "56WW54i2", "56WW5q+N",
                              "5YWE5byf", "5aeJ5aa5")]
RELATIVES_EN = [re.compile(r"\b" + dec(x) + r"\b") for x in ("ZmF0aGVy", "bW90aGVy", "YnJvdGhlcg==", "c2lzdGVy")]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
MAILTO = re.compile("mail" + "to:", re.I)
SELF = {"verification/rules.py"}


def words_not_written(F):
    bad = []
    for f, t in F.items():
        if f in SELF:
            continue
        n = norm(t)
        if any(r.search(n) for r in SCHOOL):
            bad.append(f + ": the name of a university")
        if any(w.casefold() in n for w in OTHER_PLACE):
            bad.append(f + ": the name of the operator's other place of creative work")
        if any(r.search(n) for r in TITLES):
            bad.append(f + ": a self-title or an item of rule 10")
        if any(w in t for w in RELATIVES) or any(r.search(n) for r in RELATIVES_EN):
            bad.append(f + ": a word for a single relative")
    return bad


def no_email(F):
    return [f for f, t in F.items() if EMAIL.search(t) or MAILTO.search(t)]


# ------------------------------------------------------------------ copies of the canonical files

def copies(F):
    C = jload(F, "verification/copies.json")
    if not C:
        return ["verification/copies.json cannot be read"]
    bad = [f for f, h in C["copies"].items() if f not in F or sha(F[f]) != h]
    want = {"SECURITY.md", ".github/ISSUE_TEMPLATE/error-report.yml", ".github/checked-intake/verify.js",
            ".github/workflows/checked-intake.yml", ".github/workflows/empty-issue.yml", "LICENSE", "LICENSE-CODE"}
    if set(C["copies"]) != want:
        bad.append("the list of copies is not the seven files")
    if not re.fullmatch(r"[0-9a-f]{40}", C.get("canonical_commit", "")):
        bad.append("the canonical commit")
    return bad


# ------------------------------------------------------------------ workflows

def workflows(F):
    bad = []
    wf = sorted(f for f in F if re.match(r"^\.github/workflows/.+\.ya?ml$", f))
    if not wf:
        bad.append("no workflow")
    for f in wf:
        t = F[f]
        for m in re.finditer(r"uses:\s*(\S+)(.*)$", t, re.M):
            if not re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", m.group(1)) or not re.search(r"# v\d", m.group(2)):
                bad.append(f + ": " + m.group(1))
        if not re.search(r"^permissions:", t, re.M):
            bad.append(f + ": permissions")
        perm = re.search(r"^permissions:\n((?:  .*\n)+)", t, re.M)
        writes = re.findall(r"(\w[\w-]*): write", perm.group(1)) if perm else []
        if any(w != "issues" for w in writes):
            bad.append(f + ": a write permission other than issues")
        jobs = len(re.findall(r"^  [\w-]+:\n(?:    .*\n)*?    runs-on:", t, re.M))
        if jobs == 0 or len(re.findall(r"^    timeout-minutes: \d+", t, re.M)) != jobs:
            bad.append(f + ": a job without timeout-minutes")
    own = [f for f in wf if f not in (".github/workflows/checked-intake.yml", ".github/workflows/empty-issue.yml",
                                      ".github/workflows/labels.yml")]
    for f in own:
        if re.search(r": write", F[f]):
            bad.append(f + ": the check workflows read only")
    D = F.get(".github/dependabot.yml", "")
    if "package-ecosystem: github-actions" not in D:
        bad.append("Dependabot")
    if "package.json" in F:
        bad.append("package.json")
    return bad


def labels(F, extra=()):
    L = F.get(".github/workflows/labels.yml", "")
    made = set(re.findall(r'gh label create "([^"]+)"', L))
    want = {"erratum", "quote verified", "not verified", "not checked", "needs a person"} | set(extra)
    return sorted(want - made)


# ------------------------------------------------------------------ CLAUDE.md: rules 16, 17 and 18

RULE_LINES = [
    "**Claude は利用者に命令しない。** Claude には、利用者に作業を割り当てる権限が無い。",
    "**issue の中身を言語モデルに渡すのは、本人の同意がある題と本文だけにする。**",
    "（\"I consent to the operator giving the title and text of this issue to Claude\"）",
    "`list_issues` で一覧を取らない（本文も返る）。コメントは読まない。メールの中身は扱わない。",
    "**合っているかを、最低 10 回確かめる。** 報告・返答・コミット・PR・マージの前に、",
    "(9) 他の言語版・写し・生成元と突き合わせる (10) 結論を渡さずに別の担当に確かめさせる。",
    "確かめた回数とやり方は、報告に一行で書く。2026-11-18 に利用者が 3 回と決め、2026-11-19 に 10 回へ引き上げた。",
]


def claude_md(F):
    t = F.get("CLAUDE.md", "")
    return [s[:30] for s in RULE_LINES if s not in t]


# ------------------------------------------------------------------ prose: the six writing rules, ですます

def strip_code(s):
    s = re.sub(r"```[\s\S]*?```", "", s)
    s = re.sub(r"`[^`\n]*`", "``", s)
    s = re.sub(r"\]\([^)]*\)", "]", s)
    s = re.sub(r"https?://\S+", "", s)
    return s


def strip_quotes(s):
    out, depth = [], 0
    for ch in s:
        if ch == "「":
            depth += 1
            if depth == 1:
                out.append("「」")
            continue
        if ch == "」" and depth:
            depth -= 1
            continue
        if not depth:
            out.append(ch)
    return "".join(out)


def bare(s):
    return strip_quotes(strip_code(s))


ENDS = re.compile(r"(です|ます|ません|でした|ました|ましょう)$")


def ja_lines(text):
    inside = False
    out = []
    for line in text.split("\n"):
        if line.startswith("```"):
            inside = not inside
            continue
        if inside or not line.strip() or re.match(r"^(#|\||>|<!--)", line):
            continue
        out.append(line)
    return out


def prose(F, files, allow=()):
    """allow: names (such as the title of a page) that are left out before the checks."""
    bad = []
    for f in files:
        raw = F.get(f)
        if raw is None:
            bad.append(f + ": missing")
            continue
        for a in allow:
            raw = raw.replace(a, "")
        plain = bare(raw)
        en = f.endswith(".en.md")
        if "**" in plain:
            bad.append(f + ": bold")
        if re.search("あなた|ください|下さい", plain):
            bad.append(f + ": second person or an instruction")
        if re.search(r"\b(?:you|your|yours|yourself)\b", plain, re.I):
            bad.append(f + ": you")
        for para in re.split(r"\n\s*\n", raw):
            if len(re.findall("[—―–]", bare(para))) > 1:
                bad.append(f + ": two dashes in one paragraph")
        if en:
            for line in plain.split("\n"):
                if line.startswith("|"):
                    continue
                for s in re.split(r"(?<=\.)\s+", line):
                    if len(s) > 200:
                        bad.append(f + ": a long sentence " + s[:30])
            continue
        for line in ja_lines(raw):
            b = bare(line).strip()
            b = re.sub(r"^(- |\* |\d+\. )", "", b)
            if b.startswith("[English]") or b.startswith("[日本語]") or "。" not in b:
                continue
            parts = b.split("。")
            if parts[-1].strip():
                bad.append(f + ": text after the last 。「" + parts[-1][:16] + "」")
            for s in parts[:-1]:
                x = re.sub(r"[（(][^（）()]*[）)]$", "", s).rstrip("」』").strip()
                if not ENDS.search(x):
                    bad.append(f + ": not です/ます「…" + x[-14:] + "」")
                if len(x) > 110:
                    bad.append(f + ": a long sentence「" + x[:16] + "…」")
    return bad


# ------------------------------------------------------------------ prose: every number is in the ledger of numbers

KANJI_COUNT = re.compile("[一二三四五六七八九十百千]+(?:つ|件|項目|通り|本|か所|人|条|行|回|段|欄|語|頁|篇)")
DIGITS = re.compile(r"(?<![A-Za-z0-9_\-./])\d+(?:[.,\-]\d+)*(?![A-Za-z0-9_])")


def numbers(F, files, counters, table_copies=()):
    """counters: name -> function(F) returning the true value of a count named in numbers.json.
    table_copies: files whose table rows are copies of data that another check compares; their rows are skipped."""
    N = jload(F, "verification/numbers.json")
    if not N:
        return ["verification/numbers.json cannot be read"]
    bad = []
    seen_dates = set()
    for f in files:
        t = bare(F.get(f, ""))
        for n, line in enumerate(t.split("\n"), 1):
            if line.startswith("|") and f in table_copies:
                continue  # a table row that is a copy of data, which its own check compares
            spans = []
            for x in N.get("fixed", []):
                for m in re.finditer(x["re"], line):
                    spans.append((m.start(), m.end()))
            for c in N.get("counts", []):
                for m in re.finditer(c["re"], line):
                    spans.append((m.start(), m.end()))
                    want = counters[c["count"]](F) if c["count"] in counters else None
                    if want is None or int(m.group(1)) != want:
                        bad.append("%s %d: the count %s says %s, the files give %s" % (f, n, c["count"], m.group(1), want))
            for m in re.finditer(r"\d{4}-\d{2}-\d{2}", line):
                spans.append((m.start(), m.end()))
                if m.group(0) in N["dates"]:
                    seen_dates.add(m.group(0))
                else:
                    bad.append("%s %d: a date not in the ledger %s" % (f, n, m.group(0)))
            for m in DIGITS.finditer(line):
                if any(a <= m.start() < b for a, b in spans):
                    continue
                bad.append("%s %d: a number not in the ledger %s" % (f, n, m.group(0)))
            for m in KANJI_COUNT.finditer(line):
                bad.append("%s %d: a number in kanji「%s」" % (f, n, m.group(0)))
    for d in N["dates"]:
        if d not in seen_dates:
            bad.append("the date %s of the ledger appears nowhere" % d)
    for c in N.get("counts", []):
        if c["count"] not in counters:
            bad.append("no counter for " + c["count"])
    return bad


# ------------------------------------------------------------------ the two README pages

def readme_pair(F):
    bad = []
    a, b = F.get("README.md", ""), F.get("README.en.md", "")
    if "(./README.en.md)" not in a:
        bad.append("README.md does not link README.en.md")
    if "(./README.md)" not in b:
        bad.append("README.en.md does not link README.md")
    for t, f in ((a, "README.md"), (b, "README.en.md")):
        if "Claude" not in t or ("Claude は著者ではありません。" not in t and "Claude is not an author." not in t):
            bad.append(f + ": the disclosure of the use of a language model")
        if "(./LICENSE)" not in t or "(./LICENSE-CODE)" not in t:
            bad.append(f + ": the licences")
    return bad


# ------------------------------------------------------------------ running

def run(checks, breaks, F, argv):
    if "--break" in argv:
        missed = 0
        for name, desc, mut in breaks:
            G = dict(F)
            err = None
            try:
                mut(G)
                caught = len(dict(checks)[name](G)) > 0
            except Exception as e:  # a break that does not apply is a failure too
                caught, err = False, str(e)
            print(("  caught  " if caught else "  MISSED  ") + desc + (" -- " + err if err else ""))
            missed += 0 if caught else 1
        without = [n for n, _ in checks if not any(b[0] == n for b in breaks)]
        for n in without:
            print("  no break for  " + n)
        print("\n%d breaks, %d caught. Checks without a break: %d." % (len(breaks), len(breaks) - missed, len(without)))
        return 1 if missed or without else 0
    fail = 0
    for name, fn in checks:
        bad = fn(F)
        print(("  FAIL  " if bad else "  ok    ") + name)
        for b in bad[:20]:
            print("          " + b)
        fail += 1 if bad else 0
    print("\n%d checks, %d passed." % (len(checks), len(checks) - fail))
    return 1 if fail else 0


def sub(f, a, b):
    def mut(G):
        if f not in G or a not in G[f]:
            raise ValueError("the break does not apply: %s %s" % (f, a[:30]))
        G[f] = G[f].replace(a, b, 1)
    return mut


def add(f, s):
    def mut(G):
        G[f] = G.get(f, "") + s
    return mut
