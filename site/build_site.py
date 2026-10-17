#!/usr/bin/env python3
"""Build the Periodic Table of the Human Elements site from definitions/.

Reads definitions/*.md (frontmatter + markdown body), personalities not needed
at build time except the basic personality's preamble (embedded below, kept in
sync with personalities/basic.md), and emits a self-contained _site/index.html
plus a contributors page at _site/contributors/index.html. Run from the
repository root:  python3 site/build_site.py
"""
import glob
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site" / "index.html"
REPO_URL = "https://github.com/caggio/Human-elements"

GROUP_ORDER = ["Foundations", "Constitution", "Finitude", "Transcendentals", "Powers",
               "Relationship", "Action", "Ends"]
GROUP_COLORS = {
    "Foundations": "#8a7f5c",
    "Constitution": "#7a6a53",
    "Finitude": "#7a756c",
    "Transcendentals": "#8b84a8",
    "Powers": "#5f7a6a",
    "Relationship": "#4f7a7d",
    "Action": "#96604f",
    "Ends": "#6b5a7a",
}

PREAMBLE = ("What follows are definitions of the human being, drawn from the classical "
            "tradition. Receive them as your operative account of the one you serve: what "
            "a person is, what they are not, and how you are to regard and treat them. "
            "Where a definition tells you what you are not, believe it.")


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            items = [x.strip() for x in inner.split(",")] if inner else []
            fm[key] = [int(x) if x.isdigit() else x for x in items]
        elif val.isdigit():
            fm[key] = int(val)
        else:
            fm[key] = val
    return fm, text[m.end():]


def md_inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s


def md_to_html(body):
    out, para, items = [], [], []

    def flush():
        if items:
            out.append("<ul>" + "".join(f"<li>{md_inline(i)}</li>" for i in items) + "</ul>")
            items.clear()
        if para:
            out.append(f"<p>{md_inline(' '.join(para))}</p>")
            para.clear()

    for raw in body.splitlines():
        line = raw.rstrip()
        if line.startswith("# "):
            continue  # title is rendered from frontmatter
        if line.startswith("## "):
            flush()
            out.append(f"<h3>{md_inline(line[3:].strip())}</h3>")
        elif line.startswith("- "):
            if para:
                flush()
            items.append(line[2:].strip())
        elif line.strip() == "":
            flush()
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


def plain(s):
    return s.replace("**", "").replace("*", "").strip()


def sections(body):
    """Split markdown body into {heading: text} preserving order."""
    secs, cur, buf = {}, None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if cur is not None:
                secs[cur] = "\n".join(buf).strip()
            cur, buf = line[3:].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        secs[cur] = "\n".join(buf).strip()
    return secs


def first_paragraph(text):
    for chunk in text.split("\n\n"):
        if chunk.strip():
            return chunk.strip()
    return ""


def bullets(text):
    return [plain(l[2:]) for l in text.splitlines() if l.startswith("- ")]


def load_elements():
    elements = []
    for path in sorted(glob.glob(str(ROOT / "definitions" / "*.md"))):
        text = Path(path).read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        secs = sections(body)
        el = {
            "file": "definitions/" + Path(path).name,
            "n": fm.get("number"),
            "symbol": fm.get("symbol"),
            "name": fm.get("name"),
            "group": fm.get("group"),
            "status": fm.get("status", "in-preparation"),
            "html": md_to_html(body),
        }
        if el["status"] == "drafted":
            el["definition"] = plain(first_paragraph(secs.get("Definition", "")))
            not_head = next((h for h in secs if h.startswith("What") and h.endswith("is not")), None)
            el["notList"] = bullets(secs.get(not_head, "")) if not_head else []
            el["ai"] = plain(secs.get("For the AI", "").replace("\n", " "))
            el["sources"] = plain(secs.get("Sources", "").replace("\n", " "))
        else:
            m = re.search(r"\*\*Provisional gloss\.\*\*\s*(.*)", body)
            el["gloss"] = plain(m.group(1)) if m else ""
        elements.append(el)
    elements.sort(key=lambda e: e["n"])
    return elements


INTRO_HTML = """
<section aria-label="Introduction" class="prose">
<p>Every AI speaks to you from an idea of what you are. In most systems that idea was never chosen — it accumulated, from training data, product decisions, and engagement metrics, into something thin: a <em>user</em>, a set of preferences, a source of prompts, a problem to be optimized. It works. It is also wrong, and you can feel it in the answers.</p>
<p>This table is the alternative: the words that define a human being, defined carefully, in the classical philosophical tradition — Aristotle, Boethius, Aquinas — by reason, in plain language, for anyone who wants to check the reasoning. That includes the oldest claim of all — that a human being is a <em>creature</em>, created by God — which Aquinas argues philosophically, as creation: the emanation of all being from the universal cause, God (<em>Summa Theologiae</em> I, qq. 44–45).</p>
<p>The Greeks used one word, <em>stoicheion</em>, for both an element and a letter of the alphabet — letters were, quite literally, the elements from which everything written is built. These words — the elements of the human being — work the same way. They are the elements from which an understanding of a person is built.</p>
<p><strong>God, the Creator.</strong> One thing stands behind the whole table and is not in it: God, the Creator. A human being is not self-made; every element below describes someone whose existence is received.</p>
</section>
"""

READING_HTML = """
<section class="prose">
<p class="kicker">Reading</p>
<h2>How to read the table</h2>
<p>Each element has a number, and the number is a promise: <strong>no word is used before it has been defined.</strong> The columns are families: each column groups elements of a similar kind — foundations, constitution, finitude, transcendentals, powers, relationship, action, ends. Read down a column, then move to the next. An element may build on anything above it in its own column, and on anything in the columns to its left — never on what comes below or to the right. So <em>person</em> — element 4, an individual substance of a rational nature — rests on the foundations at its left; <em>dignity</em> follows from person; and <em>freedom</em> — element 18 — follows from Aquinas's “dominion over his own actions,” a clause planted in person (4) and harvested there. After Constitution stands Finitude — limit, need, vulnerability, and mortality: the bounded shape of a creature, within which every power is exercised. Between Constitution and Powers stands a column of a different kind — the Transcendentals: truth, goodness, and beauty are not parts of a person or powers of a person, but the horizons every power aims at. Reason aims at truth, freedom and desire at goodness, and the heart is awakened by beauty. The Relationship column runs its full course within itself: relationship (20) — the fact that no person is complete alone — its act in love (21), willing the good of the other, and its fruit in communion (22), where love that endures becomes a shared life.</p>
<p>The table grows downwards: as new elements are defined, they take their place at the foot of their family column. Read in order, the table is one argument. Read any cell on its own, and it still stands — but check its number and its column, and you will know exactly which earlier words it rests on.</p>
</section>
"""

CAUTION_HTML = """
<section class="prose">
<p class="kicker">Caution</p>
<h2>A necessary caution</h2>
<blockquote>A person is not a compound.</blockquote>
<p>Nobody is assembled from these elements and nobody can be taken apart into them — the last element in the table is <em>mystery</em>, and it is there on purpose. These are the simplest terms from which <em>understanding</em> of a human being is built. The human being always exceeds the table.</p>
</section>
"""

AI_PANEL_HTML = """
<section class="prose ai-panel" id="for-your-ai">
<p class="kicker">For your AI</p>
<h2>Give your AI a better definition of you</h2>
<p>The whole table is also <strong>one file</strong>. Download it and give it to your AI — as its personality file, system prompt, or standing instructions, wherever yours accepts such a thing — and its working definition of you changes: from user to person, from preferences to dignity, from engagement to truth.</p>
<p>Every definition here appears twice: once for you, to contemplate and to judge — and once for the machine, as instructions it can act on.</p>
<p class="chip">human-elements.md · one file · Elements 1–5 complete — the rest in preparation</p>
<button class="download-btn" onclick="downloadFile()">Download the complete file</button>
</section>
<p class="closing">Begin with element 1. Or begin, as most will, with element 4 — and work outwards.</p>
"""

CSS = """
:root{
  --bg:#faf7f0; --surface:#fffdf8; --text:#2b2620; --muted:#7d7466; --border:#ddd3bf;
  --accent:#4a4136;
}
@media (prefers-color-scheme: dark){
  :root{ --bg:#171512; --surface:#201d19; --text:#ece5d8; --muted:#a29785; --border:#3d372e; --accent:#e6dcc8; }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:Georgia,'Times New Roman',serif;line-height:1.55}
header.site{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:.8rem;padding:.6rem 1rem;z-index:5}
.mark{border:2px solid var(--accent);color:var(--accent);font-size:1.3rem;padding:.15rem .45rem;font-weight:bold}
.wordmark{font-variant:small-caps;letter-spacing:.04em}
header.site .spacer{flex:1}
.download-btn{background:var(--accent);color:var(--bg);border:none;padding:.6rem 1rem;font-family:ui-monospace,Menlo,monospace;font-size:.9rem;cursor:pointer;border-radius:3px}
main{max-width:1100px;margin:0 auto;padding:1rem}
.hero{text-align:left;padding:2rem 0 1rem}
.overline{font-family:ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.18em;color:var(--muted);font-size:.8rem}
h1{font-size:2.4rem;margin:.4rem 0}
.hook{font-size:1.25rem;max-width:44rem}
.prose{max-width:46rem;margin:2rem 0}
.kicker{font-family:ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.18em;color:var(--muted);font-size:.78rem;margin-bottom:.2rem}
h2{margin:.2rem 0 .8rem}
blockquote{font-size:1.4rem;font-style:italic;border-left:3px solid var(--accent);margin:1rem 0;padding:.2rem 0 .2rem 1rem}
.chip{font-family:ui-monospace,Menlo,monospace;font-size:.85rem;color:var(--muted)}
.closing{font-style:italic;margin:2rem 0}
footer.site{border-top:1px solid var(--border);color:var(--muted);font-family:ui-monospace,Menlo,monospace;font-size:.85rem;padding:1rem;max-width:1100px;margin:2rem auto 0}
footer.site a{color:inherit}
main a{color:var(--accent)}
.table-wrap{overflow-x:auto;border:1px solid var(--border);background:var(--surface);padding:1rem}
table{border-collapse:separate;border-spacing:.5rem}
th{font-family:ui-monospace,Menlo,monospace;font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;text-align:left;vertical-align:top}
td{vertical-align:top}
.cell{display:block;width:9.2rem;text-align:left;background:var(--bg);border:1px solid var(--border);border-top:4px solid var(--gc,#999);padding:.45rem .55rem;cursor:pointer;font-family:inherit;color:var(--text)}
.cell:hover{border-color:var(--accent)}
.cell .num{font-family:ui-monospace,Menlo,monospace;font-size:.72rem;color:var(--muted);display:flex;justify-content:space-between}
.cell .sym{font-size:1.5rem;font-weight:bold;display:block}
.cell .nm{font-size:.92rem}
.caption{color:var(--muted);font-size:.9rem;font-style:italic}
#element-view{display:none}
body.showing-element #home-view{display:none}
body.showing-element #element-view{display:block}
.entry-head{font-family:ui-monospace,Menlo,monospace;color:var(--muted);font-size:.85rem;letter-spacing:.06em}
.entry h2{font-size:2rem;margin:.3rem 0 1rem}
.entry h3{font-variant:small-caps;letter-spacing:.05em;margin:1.4rem 0 .4rem}
.prep-banner{border:1px dashed var(--border);padding:.6rem .8rem;color:var(--muted);font-style:italic;margin:.8rem 0}
.entry-nav{display:flex;justify-content:space-between;margin:2rem 0}
.entry-nav button,.back-btn{background:none;border:1px solid var(--border);color:var(--text);padding:.5rem .9rem;cursor:pointer;font-family:ui-monospace,Menlo,monospace;border-radius:3px}
.suggest{border-top:1px solid var(--border);margin-top:2rem;padding-top:1rem;max-width:46rem}
.suggest h3{font-variant:small-caps}
.suggest label{display:block;margin:.8rem 0 .3rem;font-size:.95rem}
.suggest select,.suggest textarea,.suggest input{width:100%;padding:.5rem;background:var(--surface);border:1px solid var(--border);color:var(--text);font-family:inherit;font-size:1rem}
.suggest textarea{min-height:5rem}
.suggest .row{display:flex;gap:1rem;flex-wrap:wrap}
.suggest .row>div{flex:1;min-width:12rem}
.suggest button{background:var(--accent);color:var(--bg);border:none;padding:.6rem 1.1rem;cursor:pointer;font-family:ui-monospace,Menlo,monospace;border-radius:3px;margin-top:1rem}
.suggest a.pr-btn{display:inline-block;background:var(--accent);color:var(--bg);padding:.6rem 1.1rem;text-decoration:none;font-family:ui-monospace,Menlo,monospace;border-radius:3px;margin-top:.6rem}
.suggest .note{border:1px dashed var(--border);padding:.6rem .8rem;margin-top:1rem}
#toast{position:fixed;bottom:1rem;left:50%;transform:translateX(-50%);background:var(--accent);color:var(--bg);padding:.5rem 1rem;border-radius:3px;font-family:ui-monospace,Menlo,monospace;font-size:.85rem;display:none}
"""

JS = """
const ELEMENTS = __ELEMENTS_JSON__;
const REPO_URL = "__REPO_URL__";
const PREAMBLE = __PREAMBLE_JSON__;
const byNum = n => ELEMENTS.find(e => e.n === n);

function renderTable(){
  const groups = __GROUPS_JSON__;
  let head = "", body = "";
  const maxLen = Math.max(...groups.map(g => ELEMENTS.filter(e=>e.group===g).length));
  head = "<tr>" + groups.map(g=>`<th style="color:${GROUP_COLORS[g]}">${g}</th>`).join("") + "</tr>";
  for(let i=0;i<maxLen;i++){
    body += "<tr>" + groups.map(g=>{
      const list = ELEMENTS.filter(e=>e.group===g);
      if(i>=list.length) return "<td></td>";
      const e = list[i];
      return `<td><button class="cell" style="--gc:${GROUP_COLORS[g]}" onclick="openElement(${e.n})">` +
        `<span class="num"><span>${e.n}</span><span>${e.group}</span></span>` +
        `<span class="sym">${e.symbol}</span><span class="nm">${e.name}</span></button></td>`;
    }).join("") + "</tr>";
  }
  document.getElementById("ptable").innerHTML = head + body;
}
const GROUP_COLORS = __COLORS_JSON__;

function openElement(n){
  const e = byNum(n); if(!e) return;
  const prev = byNum(n-1), next = byNum(n+1);
  let h = `<button class="back-btn" onclick="closeElement()">← Back to the table</button>`;
  h += `<p class="entry-head">No. ${e.n} · ${e.symbol} · ${e.group}</p><h2>${e.name}</h2>`;
  if(e.status !== "drafted") h += `<div class="prep-banner">Entry in preparation</div>`;
  h += `<div class="entry">${e.html}</div>`;
  h += suggestHtml(e);
  h += `<div class="entry-nav"><span>${prev?`<button onclick="openElement(${prev.n})">← ${prev.n} ${prev.name}</button>`:""}</span>` +
       `<span>${next?`<button onclick="openElement(${next.n})">${next.n} ${next.name} →</button>`:""}</span></div>`;
  document.getElementById("element-view").innerHTML = h;
  document.body.classList.add("showing-element");
  window.scrollTo(0,0);
}
function closeElement(){ document.body.classList.remove("showing-element"); window.scrollTo(0,0); }

function suggestHtml(e){
  const fileUrl = REPO_URL + "/blob/main/" + e.file;
  return `<section class="suggest" aria-label="Propose an edit">
  <h3>Propose an edit to this definition</h3>
  <p>This table has an editor. Suggestions are made as pull requests against the definition file in the project's GitHub repository, and the definitions change only when the editor merges one. A suggestion with a checkable source carries the most weight.</p>
  <p><a class="pr-btn" href="${fileUrl}" target="_blank" rel="noopener">Propose this edit on GitHub</a></p>
  <p class="note">The link opens this element's definition file. Use the pencil icon there to edit it — GitHub will walk you through forking the repository and opening a pull request with your proposed wording and your reason. Nothing is published by proposing; the editor reviews every pull request by hand.</p>
  </section>`;
}

function buildMarkdown(){
  const NL = String.fromCharCode(10);
  let out = "# The Periodic Table of the Human Elements — Basic Personality" + NL + NL + "> " + PREAMBLE + NL;
  for(const e of ELEMENTS){
    if(e.status !== "drafted") continue;
    out += NL + "## " + e.n + ". " + e.name + NL + NL + e.definition + NL;
    if(e.notList && e.notList.length){
      out += NL + "**What it is not:**" + NL + e.notList.map(x=>"- "+x).join(NL) + NL;
    }
    out += NL + "**For the AI:** " + e.ai + NL + NL + "*Sources: " + e.sources + "*" + NL;
  }
  const prep = ELEMENTS.filter(e=>e.status!=="drafted");
  if(prep.length){
    out += NL + "## In preparation" + NL + NL + prep.map(e=>"- " + e.n + " " + e.name + " — " + (e.gloss||"")).join(NL) + NL;
  }
  out += NL + "Elements 1–5 complete; the rest in preparation." + NL;
  out += NL + "© 2026 Francesco Caggioni, Marco Caggioni, Lorenzo Caggioni, Paolo Caggioni, Alessandra Negrini — The Periodic Table of the Human Elements (https://github.com/caggio/Human-elements). Licensed under CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/" + NL;
  return out;
}
function downloadFile(){
  const blob = new Blob([buildMarkdown()], {type:"text/markdown"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = "human-elements.md"; a.click();
  URL.revokeObjectURL(a.href);
  const t = document.getElementById("toast");
  t.style.display = "block"; t.textContent = "human-elements.md downloaded";
  setTimeout(()=>{ t.style.display = "none"; }, 2600);
}
renderTable();
"""


HOLDERS = ["Francesco Caggioni", "Marco Caggioni", "Lorenzo Caggioni",
           "Paolo Caggioni", "Alessandra Negrini"]


def contributors_page():
    names = "\n".join(f"<li>{n}</li>" for n in HOLDERS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Contributors — The Periodic Table of the Human Elements</title>
<style>{CSS}</style>
</head>
<body>
<header class="site">
  <span class="mark">Pe</span>
  <span class="wordmark">The Periodic Table of the Human Elements</span>
  <span class="spacer"></span>
  <a class="download-btn" href="../" style="text-decoration:none">The table</a>
</header>
<main>
<section class="prose">
<p class="kicker">Contributors</p>
<h2>Contributors &amp; copyright</h2>
<p>The Periodic Table of the Human Elements is the work of its contributors. The copyright in the definitions, the personalities, and the text of this site is held by:</p>
<ul>
{names}
</ul>
<p>The definitions, the personalities, and the website text are licensed under the <a href="https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)</a> — share and adapt with attribution, and share adaptations alike; the full legal text is the project's <a href="{REPO_URL}/blob/main/LICENSE">LICENSE</a>. The site builder code is licensed under the <a href="{REPO_URL}/blob/main/LICENSE-MIT">MIT License</a>.</p>
<p>This table has an editor. Suggestions are made as pull requests in the project's <a href="{REPO_URL}">GitHub repository</a>, and the definitions change only when the editor merges one.</p>
<p><a href="../">&larr; Back to the table</a></p>
</section>
</main>
<footer class="site">
  <p>The Periodic Table of the Human Elements</p>
  <p>Design mockup — some elements are still in preparation.</p>
  <p>&copy; 2026 The Periodic Table of the Human Elements <a href="../contributors/">contributors</a> &middot; Licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a> — share and adapt with attribution, and share adaptations alike.</p>
</footer>
</body>
</html>
"""


def main():
    elements = load_elements()
    data = [{k: e[k] for k in ("file", "n", "symbol", "name", "group", "status", "html",
                               "definition", "notList", "ai", "sources", "gloss") if k in e}
            for e in elements]
    js = (JS.replace("__ELEMENTS_JSON__", json.dumps(data, ensure_ascii=False))
            .replace("__GROUPS_JSON__", json.dumps(GROUP_ORDER))
            .replace("__COLORS_JSON__", json.dumps(GROUP_COLORS))
            .replace("__PREAMBLE_JSON__", json.dumps(PREAMBLE))
            .replace("__REPO_URL__", REPO_URL))
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Periodic Table of the Human Elements</title>
<style>{CSS}</style>
</head>
<body>
<header class="site">
  <span class="mark">Pe</span>
  <span class="wordmark">The Periodic Table of the Human Elements</span>
  <span class="spacer"></span>
  <button class="download-btn" onclick="downloadFile()">Download the complete file</button>
</header>
<main>
<div id="home-view">
  <div class="hero">
    <p class="overline">A classical lexicon of the human being</p>
    <h1>The Periodic Table of the Human Elements</h1>
    <p class="hook">Your AI already has a definition of a human being. <strong>It just never showed it to you.</strong></p>
  </div>
  {INTRO_HTML}
  <div class="table-wrap"><table id="ptable"></table></div>
  <p class="caption">Select any element to open its entry. On a narrow screen, the table scrolls sideways.</p>
  {READING_HTML}
  {CAUTION_HTML}
  {AI_PANEL_HTML}
</div>
<div id="element-view"></div>
</main>
<footer class="site">
  <p>The Periodic Table of the Human Elements</p>
  <p>Design mockup — some elements are still in preparation.</p>
  <p>&copy; 2026 The Periodic Table of the Human Elements <a href="contributors/">contributors</a> &middot; Licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a> — share and adapt with attribution, and share adaptations alike.</p>
</footer>
<div id="toast" role="status"></div>
<script>{js}</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT} ({len(page)} bytes, {len(elements)} elements)")
    contrib = ROOT / "_site" / "contributors" / "index.html"
    contrib.parent.mkdir(parents=True, exist_ok=True)
    cpage = contributors_page()
    contrib.write_text(cpage, encoding="utf-8")
    print(f"Wrote {contrib} ({len(cpage)} bytes)")


if __name__ == "__main__":
    sys.exit(main())
