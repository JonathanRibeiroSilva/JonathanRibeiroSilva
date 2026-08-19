#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera assets/galaga.svg -- uma nave estilo Galaga varrendo o grafico de
contribuicoes e explodindo cada dia com commit.

Uso:  python scripts/gen_galaga_svg.py

Por que existe: para a cobrinha havia a Platane/snk pronta; para Galaga
nao existe action equivalente, e as de outros jogos nao aceitam a paleta
do perfil. O script le o MESMO calendario PUBLICO que a cobrinha lia
(github.com/users/<login>/contributions) -- sem secret nenhum -- e
escreve um SVG com animacao DECLARATIVA em CSS. Isso importa: o proxy de
imagem do GitHub (camo) serve o arquivo como <img>, onde <script> nunca
roda mas @keyframes roda normalmente.

Regra do calendario: ele so mostra commit privado se a opcao "Include
private contributions on my profile" estiver ligada no perfil -- a mesma
condicao que a cobrinha tinha.

Dependencias: stdlib.
"""

import io
import os
import random
import re
import sys
import time
import urllib.request

# ---------------------------------------------------------------- config

LOGIN = (os.environ.get("GALAGA_LOGIN")
         or os.environ.get("GITHUB_REPOSITORY_OWNER")
         or "JonathanRibeiroSilva")

URL = "https://github.com/users/%s/contributions" % LOGIN
UA = "Mozilla/5.0 (compatible; galaga-readme/1.0; +https://github.com/%s)" % LOGIN

# ---------------------------------------------------------------- paleta

T = {
    "bg":     "#000000",
    "edge":   "#1F2328",
    "fg":     "#E6E8EC",
    "dim":    "#6E7581",
    "star":   "#39414C",
    "hull":   "#E6E8EC",
    "wing":   "#00D4FF",
    "hot":    "#FF2EC4",
    "shot":   "#39FF5E",
    # mesma rampa que a cobrinha usava: do quase-preto ao verde dos badges
    "ramp":   ["#0F1418", "#0B3A1A", "#126B2C", "#22B843", "#39FF5E"],
}

FONT = ("ui-monospace, SFMono-Regular, Menlo, Consolas, "
        "&quot;DejaVu Sans Mono&quot;, &quot;Liberation Mono&quot;, monospace")

# ---------------------------------------------------------------- layout

CELL, GAP = 12.0, 4.0
PITCH = CELL + GAP
COLS, ROWS = 53, 7
PAD = 14.0

HUD_Y = 21.0
MONTH_Y = 40.0
GRID_TOP = 46.0

W = PAD * 2 + COLS * PITCH - GAP
GRID_BOT = GRID_TOP + ROWS * PITCH - GAP
SHIP_Y = GRID_BOT + 32.0
H = SHIP_Y + 18.0

MUZZLE = SHIP_Y - 14.0          # de onde a bala sai
SHIP_X0 = PAD + CELL / 2.0      # nave nasce sobre a coluna 0
TRAVEL = (COLS - 1) * PITCH     # ate a coluna 52

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# ---------------------------------------------------------------- tempo

CYCLE = 18.0          # ciclo completo, igual para TODO elemento animado
SWEEP = 15.3          # varredura da coluna 0 ate a 52
STAGGER = 0.075       # intervalo entre dois tiros na mesma coluna
SPEED = 380.0         # px/s da bala -- velocidade constante, nao duracao
DEAD = 2.9            # quanto tempo a celula fica destruida


def col_x(c):
    return PAD + c * PITCH


def row_y(r):
    return GRID_TOP + r * PITCH


def cell_mid(r):
    return row_y(r) + CELL / 2.0


def pc(t):
    """Segundos -> porcentagem do ciclo, com o sinal ja colado."""
    return "%.3f" % (t / CYCLE * 100.0) + "%"


def delay(t):
    """animation-delay que poe o instante 0 do elemento no tempo t."""
    return "animation-delay:%.3fs" % (t - CYCLE)

# ---------------------------------------------------------------- coleta


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html"})
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:            # rede do runner falha as vezes
            last = exc
            time.sleep(2 + 3 * attempt)
    sys.exit("erro: nao consegui ler %s (%s)" % (url, last))


def collect():
    local = os.environ.get("GALAGA_HTML")   # atalho para testar offline
    if local:
        html = io.open(local, encoding="utf-8").read()
    else:
        html = fetch(URL)

    cells = re.findall(
        r'data-date="(\d{4})-(\d\d)-(\d\d)"\s+'
        r'id="contribution-day-component-(\d+)-(\d+)"\s+'
        r'data-level="(\d+)"', html)
    if not cells:
        sys.exit("erro: o HTML do calendario mudou de formato -- nenhuma "
                 "celula reconhecida em %s" % URL)

    tips = dict(re.findall(
        r'for="contribution-day-component-(\d+-\d+)"[^>]*>([^<]*)</tool-tip>',
        html))

    days, total, best = [], 0, 0
    for year, month, day, row, col, level in cells:
        n = 0
        m = re.match(r"(\d+) contribution", tips.get(row + "-" + col, ""))
        if m:
            n = int(m.group(1))
        total += n
        best = max(best, n)
        days.append({"row": int(row), "col": int(col), "level": int(level),
                     "month": int(month), "year": int(year), "count": n})

    active = sum(1 for d in days if d["level"] > 0)
    return {"days": days, "total": total, "best": best, "active": active}

# ---------------------------------------------------------------- desenho


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, fill, anchor=None, size=None, weight=None, cls=None):
    return ('<text x="%.1f" y="%.1f" fill="%s"%s%s%s%s '
            'xml:space="preserve">%s</text>'
            % (x, y, fill,
               ' text-anchor="%s"' % anchor if anchor else "",
               ' font-size="%s"' % size if size else "",
               ' font-weight="%s"' % weight if weight else "",
               ' class="%s"' % cls if cls else "",
               esc(s)))


def stars():
    """Campo de estrelas do fundo. Semente fixa: sem semente o arquivo
    mudaria a cada execucao e o workflow commitaria diff todo dia."""
    rnd = random.Random(1981)               # ano do Galaga
    out = []
    for i in range(54):
        x = rnd.uniform(6, W - 6)
        y = rnd.uniform(8, H - 6)
        r = rnd.choice([0.7, 0.7, 0.9, 1.2])
        out.append('<circle class="s%d" cx="%.1f" cy="%.1f" r="%.1f" '
                   'fill="%s"/>' % (i % 3, x, y, r, T["star"]))
    return out


def months(days):
    """Rotula a coluna em que o mes vira, com folga para nao empilhar."""
    first = {}
    for d in days:
        first.setdefault(d["col"], d)
    out, last_col, last_month = [], -9, None
    for c in sorted(first):
        m = first[c]["month"]
        if m != last_month and c - last_col >= 3 and c <= COLS - 3:
            out.append(text(col_x(c), MONTH_Y, MONTHS[m - 1], T["dim"],
                            size="9", weight="600"))
            last_col = c
        last_month = m
    return out


def hud(data):
    return [text(PAD, HUD_Y, "1UP", T["hot"], size="11", weight="700",
                 cls="blink"),
            text(PAD + 30, HUD_Y, "%06d" % data["total"], T["fg"], size="11",
                 weight="700"),
            text(W - PAD, HUD_Y,
                 "%d ALIENS  ·  BEST DAY %d" % (data["active"],
                                                     data["best"]),
                 T["dim"], anchor="end", size="10")]


def ship():
    """Nave do Galaga: casco branco, asas ciano, faixa e chama magenta.
    Desenhada em torno de (0,0) para a animacao so precisar de translateX.

    Os dois <g> nao sao enfeite: transform de CSS SUBSTITUI o atributo
    transform, entao a posicao fica no <g> de fora (atributo) e a
    varredura no de dentro (animacao). Junto num so, a nave saltaria
    para y=0 no primeiro frame."""
    return ('<g transform="translate(%.1f %.1f)"><g class="ship">'
            '<path d="M-11 7L-11 0L-3.5 3L-3.5 7Z" fill="%s"/>'
            '<path d="M11 7L11 0L3.5 3L3.5 7Z" fill="%s"/>'
            '<path d="M0 -11L3 -3L3 7L-3 7L-3 -3Z" fill="%s"/>'
            '<path d="M-1.3 -1L1.3 -1L1.3 7L-1.3 7Z" fill="%s"/>'
            '<path class="flame" d="M-2.2 7L2.2 7L0 13Z" fill="%s"/>'
            '</g></g>' % (SHIP_X0, SHIP_Y, T["wing"], T["wing"], T["hull"],
                          T["hot"], T["hot"]))


def schedule(days):
    """Quem morre quando. A nave chega na coluna c em t_c; dentro da
    coluna atira de baixo para cima, o alvo mais perto primeiro."""
    by_col = {}
    for d in days:
        if d["level"] > 0:
            by_col.setdefault(d["col"], []).append(d)

    shots = []
    for c in sorted(by_col):
        t_col = (c / float(COLS - 1)) * SWEEP
        for k, d in enumerate(sorted(by_col[c], key=lambda d: -d["row"])):
            launch = t_col + k * STAGGER
            dist = MUZZLE - cell_mid(d["row"])
            shots.append({"col": c, "row": d["row"], "launch": launch,
                          "impact": launch + dist / SPEED})
    return shots


def grid(days, shots):
    hit = dict(((s["col"], s["row"]), s["impact"]) for s in shots)
    cells, bullets, sparks = [], [], []

    for d in days:
        t = hit.get((d["col"], d["row"]))
        cells.append('<rect%s x="%.1f" y="%.1f" width="%.0f" height="%.0f" '
                     'rx="2.5" fill="%s"%s/>'
                     % (' class="k"' if t is not None else "",
                        col_x(d["col"]), row_y(d["row"]), CELL, CELL,
                        T["ramp"][d["level"]],
                        ' style="%s"' % delay(t) if t is not None else ""))

    for s in shots:
        bullets.append('<rect class="b%d" x="%.1f" y="%.1f" width="2" '
                       'height="8" rx="1" fill="%s" style="%s"/>'
                       % (s["row"], col_x(s["col"]) + CELL / 2.0 - 1.0,
                          MUZZLE, T["shot"], delay(s["launch"])))
        sparks.append('<circle class="x" cx="%.1f" cy="%.1f" r="%.1f" '
                      'fill="none" stroke="%s" stroke-width="2" style="%s"/>'
                      % (col_x(s["col"]) + CELL / 2.0, cell_mid(s["row"]),
                         CELL * 0.62, T["hot"], delay(s["impact"])))

    return cells, bullets, sparks

# ---------------------------------------------------------------- animacao


def kf(name, frames):
    return "@keyframes %s{%s}" % (name, "".join("%s{%s}" % f for f in frames))


def style():
    css = [".k,.x{transform-box:fill-box;transform-origin:50% 50%}",
           ".k{animation:k %gs linear infinite}" % CYCLE,
           ".x{opacity:0;animation:x %gs linear infinite}" % CYCLE,
           ".ship{animation:ship %gs linear infinite}" % CYCLE,
           ".flame{animation:flame .16s steps(1) infinite}",
           ".blink{animation:blink 1.1s steps(1) infinite}",
           ".s0{animation:tw 2.6s steps(1) infinite}",
           ".s1{animation:tw 2.6s steps(1) -.9s infinite}",
           ".s2{animation:tw 2.6s steps(1) -1.7s infinite}"]

    for r in range(ROWS):
        css.append(".b%d{opacity:0;animation:b%d %gs linear infinite}"
                   % (r, r, CYCLE))

    # celula: explode no instante 0 do proprio ciclo e volta DEAD depois
    css.append(kf("k", [
        ("0%", "opacity:1;transform:scale(1)"),
        (pc(0.14), "opacity:1;transform:scale(1.6)"),
        (pc(0.55), "opacity:0;transform:scale(.2)"),
        (pc(DEAD), "opacity:0;transform:scale(.2)"),
        (pc(DEAD + 0.42), "opacity:1;transform:scale(1.18)"),
        (pc(DEAD + 0.7), "opacity:1;transform:scale(1)"),
        ("100%", "opacity:1;transform:scale(1)")]))

    css.append(kf("x", [
        ("0%", "opacity:1;transform:scale(.25)"),
        (pc(0.2), "opacity:.9;transform:scale(1)"),
        (pc(0.8), "opacity:0;transform:scale(2.1)"),
        ("100%", "opacity:0;transform:scale(2.1)")]))

    # uma keyframe por linha: a bala anda sempre a SPEED, entao o tempo de
    # voo depende da distancia -- 7 distancias, 7 animacoes.
    for r in range(ROWS):
        dist = MUZZLE - cell_mid(r)
        flight = dist / SPEED
        css.append(kf("b%d" % r, [
            ("0%", "opacity:1;transform:translateY(0)"),
            (pc(flight), "opacity:1;transform:translateY(%.1fpx)" % -dist),
            (pc(flight + 0.02),
             "opacity:0;transform:translateY(%.1fpx)" % -dist),
            ("100%", "opacity:0;transform:translateY(%.1fpx)" % -dist)]))

    # varredura da esquerda para a direita atirando, pausa curta na ponta
    # e volta rapida ao ponto de partida -- sem teleporte, a nave nunca
    # some da tela.
    css.append(kf("ship", [
        ("0%", "transform:translateX(0)"),
        (pc(SWEEP), "transform:translateX(%.1fpx)" % TRAVEL),
        (pc(SWEEP + 0.45), "transform:translateX(%.1fpx)" % TRAVEL),
        (pc(CYCLE - 0.3), "transform:translateX(0)"),
        ("100%", "transform:translateX(0)")]))

    css.append(kf("flame", [("0%,49%", "opacity:1"),
                            ("50%,100%", "opacity:.15")]))
    css.append(kf("blink", [("0%,54%", "opacity:1"),
                            ("55%,100%", "opacity:.2")]))
    css.append(kf("tw", [("0%,64%", "opacity:1"),
                         ("65%,100%", "opacity:.25")]))

    css.append("@media (prefers-reduced-motion:reduce){"
               ".k,.x,.ship,.flame,.blink,.s0,.s1,.s2,"
               + ",".join(".b%d" % r for r in range(ROWS))
               + "{animation:none}}")

    return "<style>\n" + "\n".join(css) + "\n</style>"

# ---------------------------------------------------------------- build


def build(data):
    shots = schedule(data["days"])
    cells, bullets, sparks = grid(data["days"], shots)

    alt = ("Galaga: the ship clears the contribution graph -- %d "
           "contributions across %d days" % (data["total"], data["active"]))

    parts = ['<rect x="0" y="0" width="%.0f" height="%.0f" rx="9" fill="%s"/>'
             % (W, H, T["bg"])]
    parts += stars()
    parts += months(data["days"])
    parts += hud(data)
    parts += cells
    parts += bullets
    parts += sparks
    parts.append(ship())
    parts.append('<rect x=".5" y=".5" width="%.0f" height="%.0f" rx="9" '
                 'fill="none" stroke="%s"/>' % (W - 1, H - 1, T["edge"]))

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
            'width="%.0f" height="%.0f" role="img" aria-label="%s" '
            'font-family="%s">\n%s\n%s\n</svg>\n'
            % (W, H, W, H, esc(alt), FONT, style(), "\n".join(parts)))


if __name__ == "__main__":
    data = collect()
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(repo, "assets", "galaga.svg")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build(data))
    print("escrito: %s (%d contribuicoes, %d alvos, %d bytes)"
          % (out, data["total"], data["active"], os.path.getsize(out)))
