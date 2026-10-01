<!--
  Pra trocar o desenho da esquerda por outra imagem:

      python tools/gerar_neofetch.py caminho/da/imagem.png
      git add assets/neofetch.svg && git commit -m "chore: troca a arte" && git push

  O script decide sozinho como desenhar:
    - imagem de traco simples e fundo solido (meme de linha, logo)  -> vira ASCII art colorida
    - ilustracao ou foto de cena cheia (tipo o Gragas)              -> entra inteira, embutida no SVG

  Os dados da ficha ficam na funcao ficha(), dentro do script.
-->

<p align="center">
  <img src="https://raw.githubusercontent.com/zbern1976/zbern1976/master/assets/neofetch.svg" width="100%" alt="berna@zbern1976 — ficha do perfil">
</p>

<p align="center">
  <a href="https://nvd.nist.gov/vuln/detail/CVE-2026-48726"><img src="https://img.shields.io/badge/CVE--2026--48726-Apache_Airflow-f0b72f?style=flat-square&labelColor=161b22" alt="CVE-2026-48726"></a>
  <a href="https://github.com/zbern1976/proton"><img src="https://img.shields.io/badge/%C2%A7PROTON-%E2%88%9240%25_tokens-a371f7?style=flat-square&labelColor=161b22" alt="§PROTON"></a>
  <img src="https://img.shields.io/badge/CWE--613-session_expiration-58a6ff?style=flat-square&labelColor=161b22" alt="CWE-613">
</p>

---

Pesquisador de segurança ofensiva — autor do **CVE-2026-48726**, falha de expiração de sessão (CWE-613) no Apache Airflow (`< 3.2.2`), publicada no MITRE/NVD. Criador do **§PROTON** — formato compacto para modelos de IA trocarem vereditos entre si (−40% tokens, −43% latência, qualidade igual, validado com juiz cego).

[Advisory (NVD)](https://nvd.nist.gov/vuln/detail/CVE-2026-48726) · [§PROTON](https://github.com/zbern1976/proton) · [CVE.org](https://www.cve.org/CVERecord?id=CVE-2026-48726)

### Selected work

**[§PROTON](https://github.com/zbern1976/proton)** — e se dois modelos de IA parassem de escrever prosa um pro outro?
Benchmark custo × qualidade de um formato compacto entre modelos. Juiz LLM cego, reproduzível, MIT.
`−40% tokens de saída` · `−43% latência` · `qualidade empatada` · `Python, zero dependências`

**[CVE-2026-48726](https://nvd.nist.gov/vuln/detail/CVE-2026-48726)** — o logout que não desligava a luz.
No Apache Airflow `< 3.2.2`, o token JWT de sessão continuava válido depois do logout. Reportada de forma responsável, publicada no MITRE/NVD.
`CWE-613` · `auth/session` · `disclosure coordenado`

<details>
<summary><b>Arquivo de missões</b> — o que mais roda por aqui</summary>

<br>

- **Trading quantitativo** — bots próprios em Python/TypeScript: coleta de dados, backtest com validação walk-forward, paper trading. Privados porque mexem com chave de API.
- **Ferramental próprio** — automação de recon, scripts de análise, utilitários em C. A regra é: se eu uso toda semana, viro ferramenta.
- **Estudo em público** — Ciência da Computação (UVA, Rio). C, autômatos, estatística.

</details>

---

<sub>A arte da esquerda sai de <a href="tools/gerar_neofetch.py"><code>tools/gerar_neofetch.py</code></a> — joga uma imagem nele e ele devolve o SVG inteiro. Troca quando enjoar.</sub>
