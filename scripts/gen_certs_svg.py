#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera assets/certs-terminal.svg -- a secao 04 do README renderizada como
uma janela de terminal.

Uso:  python scripts/gen_certs_svg.py

Para adicionar um certificado, edite CERTS abaixo e rode de novo.
Sem dependencias: so a stdlib.

Por que SVG em vez de texto: os tracos da arvore e os pontilhados sao
vetor, nao caractere. O alinhamento nao depende da fonte monoespacada
instalada na maquina de quem le o README.
"""

import io
import os

# ---------------------------------------------------------------- dados

# (emissor_slug, [(trilha_slug, ano), ...])  -- a ordem aqui e a ordem exibida
CERTS = [
    ("cisco-academy", [
        ("gerenciamento-de-ameacas-ciberneticas", "2025"),
        ("introducao-a-ciberseguranca",           "2025"),
    ]),
    ("fundacao-bradesco", [
        ("etica-no-desenvolvimento-de-sistemas",  "2023"),
        ("fundamentos-de-logica-de-programacao",  "2023"),
    ]),
    ("pietro-m-oliveira", [
        ("logica-de-programacao-em-linguagem-c",  "2023"),
    ]),
    ("scrumstudy", [
        ("scrum-fundamentals-certified",          "2024"),
    ]),
]

USER, HOST, CWD = "jonathan", "kali", "~/certs"
COMMAND, ARGS = "tree", "-L 2 --dirsfirst"

# ---------------------------------------------------------------- paleta
# As mesmas cores dos badges, do capsule-render e do typing-svg do README.
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

FS   = 12.5              # font-size
CH   = FS * 0.6          # avanco de um caractere monoespacado
LH   = 21.0              # altura de linha
PADX = 22.0
BAR  = 34.0              # altura da titlebar
TOP  = BAR + 24.0        # baseline da primeira linha
COLS = 62                # largura util em caracteres
W    = PADX * 2 + COLS * CH

NAME_COL, DOTS_END_COL, YEAR_COL, OK_COL = 8, 54, 55, 60

FONT = ("ui-monospace, SFMono-Regular, Menlo, Consolas, "
        "&quot;DejaVu Sans Mono&quot;, &quot;Liberation Mono&quot;, monospace")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cx(col):
    return PADX + col * CH


def cy(row):
    return TOP + row * LH


def mid(row):
    """Meio vertical da linha -- onde os tracos horizontais cruzam."""
    return cy(row) - FS * 0.34


def text(col, row, s, fill, weight=None):
    """Texto travado em textLength: o layout nao depende das metricas da fonte."""
    return (
        '<text x="%.2f" y="%.2f" fill="%s"%s textLength="%.2f" '
        'lengthAdjust="spacingAndGlyphs" xml:space="preserve">%s</text>'
        % (cx(col), cy(row), fill,
           ' font-weight="%s"' % weight if weight else "",
           len(s) * CH, esc(s))
    )


def rule(x1, y1, x2, y2, stroke, dashed=False):
    return ('<path d="M%.2f %.2fL%.2f %.2f" stroke="%s" stroke-width="1"%s/>'
            % (x1, y1, x2, y2, stroke,
               ' stroke-dasharray="1 4" stroke-linecap="round"' if dashed else ""))


def kali_mark(col, row):
    """O simbolo do prompt do Kali, desenhado -- nem toda fonte tem esse glifo."""
    x, y = cx(col) + CH * 0.5, mid(row)
    return (
        '<circle cx="%.2f" cy="%.2f" r="4.4" fill="none" stroke="%s" stroke-width="1"/>'
        '<text x="%.2f" y="%.2f" fill="%s" font-size="7" text-anchor="middle" '
        'font-weight="600">K</text>' % (x, y, T["dim"], x, y + 2.5, T["dim"])
    )


def check(col, row, fill):
    """O check de status, desenhado pelo mesmo motivo."""
    x, y, s = cx(col) + CH * 0.5, mid(row), 4.2
    return ('<path d="M%.2f %.2fL%.2f %.2fL%.2f %.2f" fill="none" stroke="%s" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
            % (x - s, y, x - s * 0.25, y + s * 0.7, x + s, y - s * 0.75, fill))


def prompt(row, trailing=False):
    """As duas linhas do prompt do Kali. Os cantos da moldura sao vetor."""
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
        o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" '
                 'opacity=".85"/>'
                 % (cx(4), cy(row + 1) - FS * 0.82, CH * 0.85, FS * 0.98, T["fg"]))
    else:
        o.append(text(4, row + 1, COMMAND, T["fg"], 500))
        o.append(text(5 + len(COMMAND), row + 1, ARGS, T["arg"]))
    return o


def build():
    o = []
    o += prompt(0)

    # ---- arvore ----------------------------------------------------
    root = 3
    rows, r = [], root + 1          # rows[i] = linha de cada emissor
    for _, items in CERTS:
        rows.append((r, [r + 1 + k for k in range(len(items))]))
        r += 1 + len(items)
    last_row = r - 1

    o.append(text(0, root, ".", T["dim"]))

    t1 = cx(1) + CH * 0.5
    o.append(rule(t1, mid(root) + 4, t1, mid(rows[-1][0]), T["dim"]))

    for (issuer, items), (drow, frows) in zip(CERTS, rows):
        o.append(rule(t1, mid(drow), t1 + CH * 1.9, mid(drow), T["dim"]))
        o.append(text(4, drow, issuer + "/", T["dir"], 500))

        t2 = cx(5) + CH * 0.5
        o.append(rule(t2, mid(drow) + 4, t2, mid(frows[-1]), T["dim"]))

        for (name, year), frow in zip(items, frows):
            o.append(rule(t2, mid(frow), t2 + CH * 1.9, mid(frow), T["dim"]))
            o.append(text(NAME_COL, frow, name, T["fg"]))
            o.append(rule(cx(NAME_COL) + len(name) * CH + CH * 0.8, mid(frow),
                          cx(DOTS_END_COL), mid(frow), T["dim"], dashed=True))
            o.append(text(YEAR_COL, frow, year, T["year"]))
            o.append(check(OK_COL, frow, T["accent"]))

    # ---- resumo ----------------------------------------------------
    total = sum(len(i) for _, i in CERTS)
    head = u"%d diretórios · %d certificados · " % (len(CERTS), total)
    srow = last_row + 2
    o.append(text(0, srow, head, T["dim"]))
    o.append(text(len(head), srow, u"%d concluídos" % total, T["accent"]))

    # ---- prompt final ----------------------------------------------
    prow = srow + 2
    o += prompt(prow, trailing=True)
    h = cy(prow + 1) + 22

    # ---- moldura da janela -----------------------------------------
    title = "j4yz0n@%s: %s" % (HOST, CWD)
    chrome = [
        '<rect x=".5" y=".5" width="%.2f" height="%.2f" rx="9" fill="%s" stroke="%s"/>'
        % (W - 1, h - 1, T["bg"], T["edge"]),
        '<path d="M.5 9.5A9 9 0 0 1 9.5.5H%.2fA9 9 0 0 1 %.2f 9.5V%.1fH.5Z" fill="%s"/>'
        % (W - 9.5, W - 0.5, BAR, T["chrome"]),
        '<path d="M0 %.1fH%.2f" stroke="%s" stroke-width="1"/>' % (BAR, W, T["edge"]),
    ]
    for i, c in enumerate(T["dots"]):
        chrome.append('<circle cx="%d" cy="%.1f" r="4.5" fill="%s"/>'
                      % (18 + i * 15, BAR / 2, c))
    chrome.append('<text x="%.2f" y="%.1f" fill="%s" text-anchor="middle" '
                  'font-size="11">%s</text>' % (W / 2, BAR / 2 + 4, T["dim"], esc(title)))

    alt = "Terminal listando %d certificados agrupados por emissor" % total
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.2f %.2f" '
        'width="%.2f" height="%.2f" role="img" aria-label="%s" '
        'font-family="%s" font-size="%s">\n%s\n%s\n</svg>\n'
        % (W, h, W, h, alt, FONT, FS, "\n".join(chrome), "\n".join(o))
    )


if __name__ == "__main__":
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(repo, "assets", "certs-terminal.svg")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build())
    print("escrito: %s (%d bytes)" % (out, os.path.getsize(out)))
