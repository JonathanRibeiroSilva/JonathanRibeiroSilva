#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera assets/stats-terminal.svg -- commits por repositorio, no mesmo
visual de terminal da secao 04.

Uso:  python scripts/gen_stats_svg.py

Por que existe: os cards de terceiro (github-readme-stats, streak-stats)
so enxergam repositorio PUBLICO. Como a maior parte do trabalho esta em
repositorio privado, eles mostravam 25 commits onde havia 518 -- 20x
menos. Este script consulta a API com o token do proprio dono, que ve
os privados, e renderiza o numero real.

Privacidade: repositorio privado nao tem o nome exposto, com uma excecao
-- RunasERP, que ja e descrito na secao 03 do README. Os demais entram
agregados em "outros".

Dependencias: stdlib + gh CLI autenticado (ou GH_TOKEN no ambiente).
"""

import datetime
import io
import json
import math
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------- config

LOGIN = "JonathanRibeiroSilva"
YEAR = 2026
SINCE = "%d-01-01T00:00:00Z" % YEAR

# Privados que podem ser nomeados (ja aparecem no README).
NAMEABLE_PRIVATE = {"JonathanRibeiroSilva/RunasERP"}
TOP_N = 5

# ---------------------------------------------------------------- paleta

T = {
    "bg":     "#000000",
    "chrome": "#0A0C0E",
    "edge":   "#1F2328",
    "fg":     "#E6E8EC",
    "dim":    "#6E7581",
    "dir":    "#00D4FF",
    "accent": "#39FF5E",
    "arg":    "#8B919C",
    "year":   "#FF2EC4",
    "dots":   ["#FF2EC4", "#00D4FF", "#39FF5E"],
}

# ---------------------------------------------------------------- layout

FS   = 12.5
CH   = FS * 0.6
LH   = 21.0
PADX = 22.0
BAR  = 34.0
TOP  = BAR + 24.0
COLS = 62
W    = PADX * 2 + COLS * CH

NUM_END, NAME_COL, DOTS_END, TAG_COL = 6, 9, 46, 48

FONT = ("ui-monospace, SFMono-Regular, Menlo, Consolas, "
        "&quot;DejaVu Sans Mono&quot;, &quot;Liberation Mono&quot;, monospace")

USER, HOST, CWD = "jonathan", "kali", "~"
COMMAND, ARGS = "git", "shortlog -sn --all --since=%d-01-01" % YEAR

# ---------------------------------------------------------------- coleta


def gh(*args):
    try:
        p = subprocess.run(["gh"] + list(args), capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
    except OSError:
        sys.exit("erro: gh CLI nao encontrado no PATH")
    return p.stdout if p.returncode == 0 else None


def count_commits(full_name, branch):
    """Total de commits do autor sem baixar a lista: le o header Link."""
    out = gh("api", "-i", "repos/%s/commits?author=%s&since=%s&sha=%s&per_page=1"
             % (full_name, LOGIN, SINCE, branch))
    if not out:
        return 0
    m = re.search(r'[?&]page=(\d+)>;\s*rel="last"', out)
    if m:
        return int(m.group(1))
    try:
        return len(json.loads(out.split("\n\n", 1)[-1]))
    except ValueError:
        return 0


def collect():
    raw = gh("api", "--paginate",
             "user/repos?affiliation=owner,collaborator,organization_member"
             "&per_page=100")
    if not raw:
        sys.exit("erro: gh nao autenticado (rode `gh auth login`)")
    repos = json.loads(raw)

    rows = []
    for r in repos:
        n = count_commits(r["full_name"], r.get("default_branch") or "main")
        if n:
            rows.append({"full": r["full_name"], "private": r["private"],
                         "commits": n})
    rows.sort(key=lambda x: -x["commits"])

    prs = gh("api", "graphql", "-f", "query={viewer{pullRequests{totalCount}}}",
             "--jq", ".data.viewer.pullRequests.totalCount")
    return {
        "rows": rows,
        "total": sum(r["commits"] for r in rows),
        "repos": len(rows),
        "prs": int((prs or "0").strip() or 0),
    }


def display_rows(data):
    """Top N nomeaveis + o resto agregado, sem vazar nome de repo privado."""
    shown, hidden, hidden_n = [], 0, 0
    for r in data["rows"]:
        nameable = (not r["private"]) or r["full"] in NAMEABLE_PRIVATE
        if nameable and len(shown) < TOP_N:
            name = r["full"].split("/")[-1] if r["full"].startswith(LOGIN + "/") \
                else r["full"]
            shown.append((r["commits"], name,
                          "privado" if r["private"] else "público"))
        else:
            hidden += r["commits"]
            hidden_n += 1
    if hidden:
        shown.append((hidden, "outros",
                      "%d repositório%s" % (hidden_n, "s" if hidden_n > 1 else "")))
    return shown

# ---------------------------------------------------------------- desenho


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cx(col):
    return PADX + col * CH


def cy(row):
    return TOP + row * LH


def mid(row):
    return cy(row) - FS * 0.34


def text(col, row, s, fill, weight=None):
    return ('<text x="%.2f" y="%.2f" fill="%s"%s textLength="%.2f" '
            'lengthAdjust="spacingAndGlyphs" xml:space="preserve">%s</text>'
            % (cx(col), cy(row), fill,
               ' font-weight="%s"' % weight if weight else "",
               len(s) * CH, esc(s)))


def rule(x1, y1, x2, y2, stroke, dashed=False):
    return ('<path d="M%.2f %.2fL%.2f %.2f" stroke="%s" stroke-width="1"%s/>'
            % (x1, y1, x2, y2, stroke,
               ' stroke-dasharray="1 4" stroke-linecap="round"' if dashed else ""))


def kali_mark(col, row):
    x, y = cx(col) + CH * 0.5, mid(row)
    return ('<circle cx="%.2f" cy="%.2f" r="4.4" fill="none" stroke="%s" '
            'stroke-width="1"/><text x="%.2f" y="%.2f" fill="%s" font-size="7" '
            'text-anchor="middle" font-weight="600">K</text>'
            % (x, y, T["dim"], x, y + 2.5, T["dim"]))


def prompt(row, trailing=False):
    o, px = [], cx(0) + 3
    o.append(rule(px, mid(row), px, mid(row + 1), T["dim"]))
    o.append(rule(px, mid(row), px + CH * 2, mid(row), T["dim"]))
    o.append(rule(px, mid(row + 1), px + CH * 1.4, mid(row + 1), T["dim"]))
    o.append(text(2, row, "(", T["dim"]))
    o.append(text(3, row, USER, T["accent"], 600))
    o.append(kali_mark(3 + len(USER), row))
    o.append(text(4 + len(USER), row, HOST, T["accent"], 600))
    o.append(text(4 + len(USER) + len(HOST), row, ")-[", T["dim"]))
    o.append(text(7 + len(USER) + len(HOST), row, CWD, T["dir"]))
    o.append(text(7 + len(USER) + len(HOST) + len(CWD), row, "]", T["dim"]))
    o.append(text(2, row + 1, "$", T["accent"], 600))
    if trailing:
        o.append('<rect class="blink" x="%.2f" y="%.2f" width="%.2f" '
                 'height="%.2f" fill="%s"/>'
                 % (cx(4), cy(row + 1) - FS * 0.82, CH * 0.85, FS * 0.98, T["fg"]))
    else:
        o.append(text(4, row + 1, COMMAND, T["fg"], 500))
        o.append(text(5 + len(COMMAND), row + 1, ARGS, T["arg"]))
    return o

# ---------------------------------------------------------------- animacao

CYCLE = 11.0
T_TYPE = (4, 20)
T_OUT = (25, 40)
ROOT_ROW = 3


def anim(h):
    cmd_len = len(COMMAND) + 1 + len(ARGS)
    out_top = cy(ROOT_ROW) - 15
    steps = int(math.ceil((h - out_top) / LH))
    return cmd_len, cmd_len * CH, out_top, steps, steps * LH


def style(h):
    cl, ctrav, otop, ost, otrav = anim(h)
    return ('<style>\n'
            '.t-cmd{transform:translateX(%.2fpx);animation:cmd %gs steps(%d) infinite}\n'
            '.t-out{transform:translateY(%.2fpx);animation:out %gs steps(%d) infinite}\n'
            '.caret{opacity:.9;animation:caret %gs steps(1) infinite}\n'
            '.blink{opacity:.85;animation:blink 1.05s steps(1) infinite}\n'
            '@keyframes cmd{0%%,%d%%{transform:translateX(0)}'
            '%d%%,100%%{transform:translateX(%.2fpx)}}\n'
            '@keyframes out{0%%,%d%%{transform:translateY(0)}'
            '%d%%,100%%{transform:translateY(%.2fpx)}}\n'
            '@keyframes caret{0%%,%d%%{opacity:.9}%d%%,100%%{opacity:0}}\n'
            '@keyframes blink{0%%,49%%{opacity:.85}50%%,100%%{opacity:0}}\n'
            '@media (prefers-reduced-motion:reduce){'
            '.t-cmd,.t-out,.blink{animation:none}.caret{animation:none;opacity:0}}\n'
            '</style>'
            % (ctrav, CYCLE, cl, otrav, CYCLE, ost, CYCLE,
               T_TYPE[0], T_TYPE[1], ctrav, T_OUT[0], T_OUT[1], otrav,
               T_TYPE[1], T_TYPE[1] + 1))


def curtains(h):
    cl, ctrav, otop, ost, otrav = anim(h)
    return ('<g class="t-out"><rect x="1" y="%.2f" width="%.2f" height="%.2f" '
            'fill="%s"/></g>\n<g class="t-cmd">'
            '<rect x="%.2f" y="%.2f" width="%.2f" height="15" fill="%s"/>'
            '<rect class="caret" x="%.2f" y="%.2f" width="%.2f" height="%.2f" '
            'fill="%s"/></g>'
            % (otop, W - 2, h - otop, T["bg"],
               cx(4), cy(1) - 11, W - cx(4), T["bg"],
               cx(4), cy(1) - FS * 0.82, CH * 0.85, FS * 0.98, T["fg"]))

# ---------------------------------------------------------------- build


def build(data, stamp):
    o = list(prompt(0))
    rows = display_rows(data)

    r = ROOT_ROW
    for n, name, tag in rows:
        num = str(n)
        o.append(text(NUM_END - len(num), r, num, T["accent"], 600))
        o.append(text(NAME_COL, r, name, T["fg"]))
        o.append(rule(cx(NAME_COL) + len(name) * CH + CH * 0.8, mid(r),
                      cx(DOTS_END), mid(r), T["dim"], dashed=True))
        o.append(text(TAG_COL, r, tag, T["year"] if tag == "privado" else T["dim"]))
        r += 1

    r += 1
    head = "%d commits · %d pull requests · %d repositórios" % (
        data["total"], data["prs"], data["repos"])
    o.append(text(0, r, head, T["dim"]))
    r += 1
    o.append(text(0, r, "atualizado em %s" % stamp, T["dim"]))

    prow = r + 2
    o += prompt(prow, trailing=True)
    h = cy(prow + 1) + 22

    title = "j4yz0n@%s: %s" % (HOST, CWD)
    back = ['<rect x="0" y="0" width="%.2f" height="%.2f" rx="9" fill="%s"/>'
            % (W, h, T["bg"]),
            '<path d="M.5 9.5A9 9 0 0 1 9.5.5H%.2fA9 9 0 0 1 %.2f 9.5V%.1fH.5Z" '
            'fill="%s"/>' % (W - 9.5, W - 0.5, BAR, T["chrome"]),
            '<path d="M0 %.1fH%.2f" stroke="%s" stroke-width="1"/>'
            % (BAR, W, T["edge"])]
    for i, c in enumerate(T["dots"]):
        back.append('<circle cx="%d" cy="%.1f" r="4.5" fill="%s"/>'
                    % (18 + i * 15, BAR / 2, c))
    back.append('<text x="%.2f" y="%.1f" fill="%s" text-anchor="middle" '
                'font-size="11">%s</text>'
                % (W / 2, BAR / 2 + 4, T["dim"], esc(title)))
    front = ['<rect x=".5" y=".5" width="%.2f" height="%.2f" rx="9" fill="none" '
             'stroke="%s"/>' % (W - 1, h - 1, T["edge"])]

    alt = ("Terminal: %d commits em %d distribuídos por %d repositórios"
           % (data["total"], YEAR, data["repos"]))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
            'width="%.2f" height="%.2f" role="img" aria-label="%s" '
            'font-family="%s" font-size="%s">\n%s\n%s\n%s\n%s\n%s\n</svg>\n'
            % (W, h, W, h, alt, FONT, FS, style(h), "\n".join(back),
               "\n".join(o), curtains(h), "\n".join(front)))


if __name__ == "__main__":
    data = collect()
    stamp = os.environ.get("STATS_DATE") or datetime.date.today().isoformat()
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(repo, "assets", "stats-terminal.svg")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build(data, stamp))
    print("escrito: %s (%d commits, %d repos, %d bytes)"
          % (out, data["total"], data["repos"], os.path.getsize(out)))
