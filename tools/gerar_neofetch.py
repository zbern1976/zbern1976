# -*- coding: utf-8 -*-
"""
Gera a arte do perfil no estilo neofetch: uma imagem qualquer virando ASCII
colorida do lado esquerdo, e a ficha técnica do lado direito.

Uso:
    python tools/gerar_neofetch.py minha_imagem.png
    python tools/gerar_neofetch.py meme.jpg assets/neofetch.svg

Trocar o desenho = rodar de novo com outra imagem e dar commit.
"""
import sys
import os
import html
import io
import base64
from collections import Counter

from PIL import Image, ImageOps

# ------------------------------------------------------------------ ajustes
LINHAS = 46          # altura da arte, em linhas (manda na proporção)
COLS_MAX = 92        # teto de largura, pra imagem muito deitada não estourar
CHAR_W = 8.4         # largura de um caractere, em px
LINE_H = 16.8        # altura de uma linha, em px
FONT_SIZE = 14
RAMPA = " .:-=+*#%@"  # do mais vazio pro mais cheio
FUNDO_TOL = 0.055    # 0..1 — o quanto um pixel pode parecer com o fundo e sumir
GANHO = 2.0          # empurra o contraste da arte; suba se ficar apagada
PALETA_N = 22        # teto de cores no modo caractere (menos cor = SVG menor)
PALETA_RICA = 160    # teto de cores no modo bloco, onde a cor faz o desenho
IMG_ALTURA = 430     # altura da imagem quando ela entra inteira, em px
IMG_LARGURA_MAX = 520  # teto de largura pra imagem deitada nao engolir a ficha

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
C_FRACO = "#8b949e"


def cor_de_fundo(img):
    """A cor mais repetida na moldura provavelmente é o fundo."""
    largura, altura = img.size
    moldura = []
    for x in range(largura):
        moldura.append(img.getpixel((x, 0)))
        moldura.append(img.getpixel((x, altura - 1)))
    for y in range(altura):
        moldura.append(img.getpixel((0, y)))
        moldura.append(img.getpixel((largura - 1, y)))
    return Counter(moldura).most_common(1)[0][0]


def quantizar(rgb, n=PALETA_N):
    """Arredonda a cor pra reduzir a paleta e agrupar caracteres vizinhos."""
    passo = max(1, 256 // max(2, int(n ** (1 / 3)) + 1))
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
    normalizadas = [d / teto for d in distancias]

    # Se quase nada encostou no fundo, a imagem nao tem fundo solido (cena
    # inteira preenchida). Ai a distancia nao separa nada e tudo satura — nesse
    # caso quem manda na densidade e o brilho, que ainda desenha a forma.
    fatia_fundo = sum(1 for d in normalizadas if d < FUNDO_TOL) / len(normalizadas)
    por_brilho = fatia_fundo < 0.12

    # Cena cheia e colorida (ilustracao, foto): caractere de densidade vira
    # mancha e bloco colorido vira mosaico. Nesses casos a imagem entra inteira,
    # do jeito que o neofetch moderno mostra — quem decide isso e montar_arte().
    if por_brilho:
        return None

    grade, i = [], 0
    for _ in range(img.height):
        linha = []
        for _ in range(img.width):
            rgb = pixels[i]
            d = normalizadas[i]
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


def imagem_embutida(caminho, altura_alvo):
    """Devolve a imagem como data URI, pronta pra entrar no SVG."""
    img = Image.open(caminho).convert("RGB")
    escala = altura_alvo / img.height
    largura = max(1, round(img.width * escala))
    img = img.resize((largura, round(altura_alvo)), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=84, optimize=True)
    dado = base64.b64encode(buf.getvalue()).decode("ascii")
    return "data:image/jpeg;base64," + dado, largura


def montar_arte(caminho, x0, y0):
    """ASCII se a imagem for de traço simples; a própria imagem se for cena."""
    grade = imagem_para_ascii(caminho)
    if grade is not None:
        largura = max(len(l) for l in grade) * CHAR_W
        altura = len(grade) * LINE_H
        return arte_para_svg(grade, x0, y0), largura, altura, "ascii"

    # a imagem fica do tamanho da ficha, senão engole a composição
    altura = IMG_ALTURA
    proporcao = Image.open(caminho).size
    if proporcao[0] / proporcao[1] * altura > IMG_LARGURA_MAX:
        altura = IMG_LARGURA_MAX * proporcao[1] / proporcao[0]
    uri, largura = imagem_embutida(caminho, altura)
    svg = (
        '<image x="%.1f" y="%.1f" width="%d" height="%.1f" '
        'preserveAspectRatio="xMidYMid meet" href="%s"/>'
        % (x0, y0 - LINE_H, largura, altura, uri)
    )
    return svg, largura, altura, "imagem"


def ficha():
    """A ficha técnica. Mexa aqui pra atualizar os dados."""
    return [
        ("__TITULO__", "berna@zbern1976", None),
        ("__REGUA__", "", None),
        ("Foco", "segurança ofensiva · dados · desenvolvimento", C_VALOR),
        ("Base", "Rio de Janeiro · Ciência da Computação", C_VALOR),
        ("__VAZIO__", "", None),
        ("CVE", "CVE-2026-48726 · Apache Airflow · CWE-613", C_DESTAQUE),
        ("__CONT__", "a sessão JWT sobrevive ao logout · MITRE/NVD", C_FRACO),
        ("§PROTON", "formato compacto entre modelos de IA", C_DESTAQUE),
        ("__CONT__", "−40% tokens · −43% latência · juiz cego", C_FRACO),
        ("Sherlock", "auditoria do XRP Ledger em C++", C_VALOR),
        ("__CONT__", "7 relatórios submetidos · abril/2026", C_FRACO),
        ("SKYNET", "bot de trading com backtest walk-forward", C_VALOR),
        ("__VAZIO__", "", None),
        ("Stack", "Python · C · TypeScript · SQL · Linux", C_VALOR),
        ("Caça", "auth/session · IDOR · lógica de negócio", C_VALOR),
        ("__CONT__", "segurança de agentes LLM", C_FRACO),
        ("Idiomas", "Português · English (leitura técnica)", C_VALOR),
        ("__VAZIO__", "", None),
        ("Status", "procurando estágio", C_OK),
    ]


def ficha_para_svg(x0, y0):
    itens = ficha()
    larg_label = max(len(k) for k, _, _ in itens if not k.startswith("__"))
    recuo = (larg_label + 5) * CHAR_W   # onde comeca a coluna do valor
    larg_total = max(
        larg_label + 5 + len(v) for k, v, _ in itens if not k.startswith("__")
    )

    saida = []
    y = y0
    for chave, valor, cor in itens:
        if chave == "__VAZIO__":
            y += LINE_H * 0.6
            continue
        if chave == "__CONT__":
            # segunda linha de um item, alinhada na coluna do valor
            saida.append(
                '<text x="%.1f" y="%.1f" fill="%s">%s</text>'
                % (x0 + recuo, y, cor, html.escape(valor))
            )
            y += LINE_H
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
                % (x0, y, C_PONTOS, "─" * larg_total)
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
    pad_x = 22
    barra_h = 34
    arte_x = pad_x + 8
    arte_y = barra_h + 48

    arte_svg, largura_arte, altura_arte, modo = montar_arte(
        caminho_img, arte_x, arte_y
    )
    ficha_x = arte_x + largura_arte + 34
    ficha_svg, ficha_fim, larg_ficha = ficha_para_svg(ficha_x, arte_y + LINE_H)

    fim_arte = arte_y + altura_arte
    altura = max(fim_arte, ficha_fim) + 40
    largura = ficha_x + larg_ficha * CHAR_W + pad_x

    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="%(w).0f" height="%(h).0f" viewBox="0 0 %(w).0f %(h).0f" role="img" aria-labelledby="tt dd">
  <title id="tt">berna@zbern1976 — ficha do perfil em estilo neofetch</title>
  <desc id="dd">Janela de terminal com uma arte em ASCII colorida à esquerda e a ficha técnica à direita.</desc>
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
