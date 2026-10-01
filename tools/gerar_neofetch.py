# -*- coding: utf-8 -*-
"""
Gera a arte do perfil no estilo neofetch: uma imagem qualquer virando ASCII
colorida do lado esquerdo, e a ficha tecnica do lado direito.

Uso:
    python tools/gerar_neofetch.py minha_imagem.png
    python tools/gerar_neofetch.py meme.jpg assets/neofetch.svg

Trocar o desenho = rodar de novo com outra imagem e dar commit.
"""
import sys
import os
import html
from collections import Counter

from PIL import Image, ImageOps

# ------------------------------------------------------------------ ajustes
LINHAS = 40          # altura da arte, em linhas (manda na proporcao)
COLS_MAX = 84        # teto de largura, pra imagem muito deitada nao estourar
CHAR_W = 8.4         # largura de um caractere, em px
LINE_H = 16.8        # altura de uma linha, em px
FONT_SIZE = 14
RAMPA = " .:-=+*#%@"  # do mais vazio pro mais cheio
FUNDO_TOL = 0.055    # 0..1 — o quanto um pixel pode parecer com o fundo e sumir
GANHO = 2.0          # empurra o contraste da arte; suba se ficar apagada
PALETA_N = 22        # teto de cores (menos cor = SVG menor)

FONTE = "'Cascadia Code','JetBrains Mono',Consolas,'DejaVu Sans Mono','Courier New',monospace"

BG_JANELA = "#0d1117"
BG_BARRA = "#161b22"
BORDA = "#30363d"
C_LABEL = "#a371f7"
C_PONTOS = "#30363d"
C_VALOR = "#c9d1d9"
C_DESTAQUE = "#f0b72f"
C_OK = "#3fb950"
C_USER = "#58a6ff"


def cor_de_fundo(img):
    """A cor mais repetida na moldura provavelmente e o fundo."""
    largura, altura = img.size
    moldura = []
    for x in range(largura):
        moldura.append(img.getpixel((x, 0)))
        moldura.append(img.getpixel((x, altura - 1)))
    for y in range(altura):
        moldura.append(img.getpixel((0, y)))
        moldura.append(img.getpixel((largura - 1, y)))
    return Counter(moldura).most_common(1)[0][0]


def quantizar(rgb):
    """Arredonda a cor pra reduzir a paleta e agrupar caracteres vizinhos."""
    passo = max(1, 256 // max(2, int(PALETA_N ** (1 / 3)) + 1))
    return tuple(min(255, (c // passo) * passo + passo // 2) for c in rgb)


def imagem_para_ascii(caminho):
    img = Image.open(caminho).convert("RGB")
    img = ImageOps.autocontrast(img, cutoff=2)
    fundo = cor_de_fundo(img)

    # a altura manda: a largura sai da proporcao da imagem, corrigida pelo
    # fato de um caractere ser mais alto que largo
    cols = max(8, round(LINHAS * (img.width / img.height) * (LINE_H / CHAR_W)))
    cols = min(cols, COLS_MAX)
    img = img.resize((cols, LINHAS), Image.LANCZOS)

    # 1a passada: o quanto cada pixel se afasta do fundo (0..1)
    MAX_DIST = (3 * 255 ** 2) ** 0.5
    pixels, distancias = [], []
    for y in range(img.height):
        for x in range(img.width):
            rgb = img.getpixel((x, y))
            d = sum((c - f) ** 2 for c, f in zip(rgb, fundo)) ** 0.5 / MAX_DIST
            pixels.append(rgb)
            distancias.append(d)

    # normaliza pelo pixel que mais se afasta, senao foto de pouco contraste some
    teto = max(distancias) or 1.0

    grade, i = [], 0
    for _ in range(img.height):
        linha = []
        for _ in range(img.width):
            rgb, d = pixels[i], distancias[i] / teto
            i += 1
            if d < FUNDO_TOL:
                linha.append((" ", None))
                continue
            peso = min(1.0, d * GANHO)
            idx = min(len(RAMPA) - 1, int(peso * len(RAMPA)))
            linha.append((RAMPA[idx], quantizar(rgb)))
        grade.append(linha)
    return grade


def arte_para_svg(grade, x0, y0):
    """Junta caracteres vizinhos de mesma cor num tspan, com x absoluto."""
    saida = []
    for i, linha in enumerate(grade):
        y = y0 + i * LINE_H
        spans = []
        col = 0
        atual = None
        buf = ""
        for j, (ch, cor) in enumerate(list(linha) + [(" ", "FIM")]):
            if cor != atual:
                if buf.strip() and atual is not None and atual != "FIM":
                    r, g, b = atual
                    spans.append(
                        '<tspan x="%.1f" fill="rgb(%d,%d,%d)">%s</tspan>'
                        % (x0 + col * CHAR_W, r, g, b, html.escape(buf))
                    )
                atual = cor
                buf = ""
                col = j
            buf += ch
        if spans:
            saida.append(
                '<text y="%.1f" xml:space="preserve">%s</text>' % (y, "".join(spans))
            )
    return "\n    ".join(saida)


def ficha():
    """A ficha tecnica. Mexa aqui pra atualizar os dados."""
    return [
        ("__TITULO__", "berna@zbern1976", None),
        ("__REGUA__", "", None),
        ("OS", "Windows 11 Home - build 26200", C_VALOR),
        ("Host", "Dell Inspiron 15 3511", C_VALOR),
        ("CPU", "i5-1135G7 - 4C/8T - Iris Xe", C_VALOR),
        ("Memory", "7.7 GiB (um pente soldado, sofrendo)", C_VALOR),
        ("Shell", "PowerShell - Git Bash", C_VALOR),
        ("Editor", "VS Code - Dev-C++ 5.11", C_VALOR),
        ("__VAZIO__", "", None),
        ("Languages.Code", "Python - C - TypeScript - SQL", C_VALOR),
        ("Languages.Real", "Portugues - English (leitura tecnica)", C_VALOR),
        ("__VAZIO__", "", None),
        ("Security", "CVE-2026-48726 - Airflow - CWE-613", C_DESTAQUE),
        ("Project", "PROTON - menos 40% de tokens entre modelos", C_DESTAQUE),
        ("Contest", "Sherlock x Ripple (XRPL) - 7 relatorios", C_VALOR),
        ("__VAZIO__", "", None),
        ("Repos", "2 publicos - 9 privados", C_VALOR),
        ("Stars.Given", "16", C_VALOR),
        ("Commits.2026", "92", C_VALOR),
        ("Studying", "Ciencia da Computacao - Rio de Janeiro", C_VALOR),
        ("__VAZIO__", "", None),
        ("Status", "procurando estagio", C_OK),
    ]


def ficha_para_svg(x0, y0):
    itens = ficha()
    larg_label = max(len(k) for k, _, _ in itens if not k.startswith("__"))
    larg_total = max(
        larg_label + 5 + len(v) for k, v, _ in itens if not k.startswith("__")
    )

    saida = []
    y = y0
    for chave, valor, cor in itens:
        if chave == "__VAZIO__":
            y += LINE_H * 0.6
            continue
        if chave == "__TITULO__":
            saida.append(
                '<text x="%.1f" y="%.1f" fill="%s" font-weight="700">%s</text>'
                % (x0, y, C_USER, html.escape(valor))
            )
            y += LINE_H
            continue
        if chave == "__REGUA__":
            saida.append(
                '<text x="%.1f" y="%.1f" fill="%s">%s</text>'
                % (x0, y, C_PONTOS, "-" * larg_total)
            )
            y += LINE_H
            continue
        pontos = "." * (larg_label - len(chave) + 3)
        saida.append(
            '<text y="%.1f" xml:space="preserve">'
            '<tspan x="%.1f" fill="%s">%s</tspan>'
            '<tspan fill="%s">%s: </tspan>'
            '<tspan fill="%s">%s</tspan></text>'
            % (
                y,
                x0,
                C_LABEL,
                html.escape(chave),
                C_PONTOS,
                pontos,
                cor,
                html.escape(valor),
            )
        )
        y += LINE_H
    return "\n    ".join(saida), y, larg_total


def gerar(caminho_img, destino):
    grade = imagem_para_ascii(caminho_img)

    pad_x = 22
    barra_h = 34
    arte_x = pad_x + 8
    arte_y = barra_h + 48
    largura_arte = max(len(l) for l in grade) if grade else 0
    ficha_x = arte_x + largura_arte * CHAR_W + 34

    arte_svg = arte_para_svg(grade, arte_x, arte_y)
    ficha_svg, ficha_fim, larg_ficha = ficha_para_svg(ficha_x, arte_y + LINE_H)

    fim_arte = arte_y + len(grade) * LINE_H
    altura = max(fim_arte, ficha_fim) + 40
    largura = ficha_x + larg_ficha * CHAR_W + pad_x

    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="%(w).0f" height="%(h).0f" viewBox="0 0 %(w).0f %(h).0f" role="img" aria-labelledby="tt dd">
  <title id="tt">berna@zbern1976 - ficha do perfil em estilo neofetch</title>
  <desc id="dd">Janela de terminal com uma arte em ASCII colorida a esquerda e a ficha tecnica a direita.</desc>
  <rect width="%(w).0f" height="%(h).0f" rx="10" fill="%(bg)s" stroke="%(borda)s"/>
  <path d="M0 %(barra)d V10 a10 10 0 0 1 10-10 H%(wm10).0f a10 10 0 0 1 10 10 v%(barra10)dZ" fill="%(bgbarra)s"/>
  <circle cx="22" cy="17" r="6" fill="#ff5f56"/>
  <circle cx="42" cy="17" r="6" fill="#ffbd2e"/>
  <circle cx="62" cy="17" r="6" fill="#27c93f"/>
  <text x="%(meio).0f" y="22" text-anchor="middle" font-family="%(fonte)s" font-size="12.5" fill="#8b949e">berna@zbern1976: ~</text>
  <g font-family="%(fonte)s" font-size="%(fs)d">
    <text x="%(artex).1f" y="%(prompty).1f" xml:space="preserve"><tspan fill="%(ok)s">$</tspan><tspan fill="%(valor)s"> neofetch</tspan></text>
    %(arte)s
    %(ficha)s
  </g>
</svg>
""" % {
        "w": largura,
        "h": altura,
        "wm10": largura - 10,
        "meio": largura / 2,
        "barra": barra_h,
        "barra10": barra_h - 10,
        "bg": BG_JANELA,
        "bgbarra": BG_BARRA,
        "borda": BORDA,
        "fonte": FONTE,
        "fs": FONT_SIZE,
        "artex": arte_x,
        "prompty": barra_h + 26,
        "ok": C_OK,
        "valor": C_VALOR,
        "arte": arte_svg,
        "ficha": ficha_svg,
    }

    pasta = os.path.dirname(destino)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(svg)
    return destino, largura, altura


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    alvo = sys.argv[2] if len(sys.argv) > 2 else "assets/neofetch.svg"
    caminho, w, h = gerar(sys.argv[1], alvo)
    print("gerado: %s  (%.0fx%.0f)" % (caminho, w, h))
