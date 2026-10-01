<p align="center">
  <img src="https://raw.githubusercontent.com/zbern1976/zbern1976/master/assets/banner.svg" width="100%" alt="Bernardo Curi — pesquisador de segurança ofensiva">
</p>

<p align="center">
  <a href="https://nvd.nist.gov/vuln/detail/CVE-2026-48726"><img src="https://img.shields.io/badge/CVE--2026--48726-Apache_Airflow-fbbf24?style=flat-square&labelColor=4c1d95" alt="CVE-2026-48726"></a>
  <a href="https://github.com/zbern1976/proton"><img src="https://img.shields.io/badge/%C2%A7PROTON-%E2%88%9240%25_tokens-ec4899?style=flat-square&labelColor=4c1d95" alt="§PROTON"></a>
  <img src="https://img.shields.io/badge/CWE--613-session_expiration-a78bfa?style=flat-square&labelColor=4c1d95" alt="CWE-613">
</p>

<p align="center"><sub>ゴ　ゴ　ゴ　ゴ　ゴ</sub></p>

### Bernardo Curi

Pesquisador de segurança ofensiva — autor do **CVE-2026-48726**, falha de expiração de sessão (CWE-613) no Apache Airflow (`< 3.2.2`), publicada no MITRE/NVD. Criador do **§PROTON** — formato compacto para modelos de IA trocarem vereditos entre si (−40% tokens, −43% latência, qualidade igual, validado com juiz cego).

[Advisory (NVD)](https://nvd.nist.gov/vuln/detail/CVE-2026-48726) · [§PROTON](https://github.com/zbern1976/proton) · [CVE.org](https://www.cve.org/CVERecord?id=CVE-2026-48726)

---

<table>
  <tr>
    <td colspan="2" align="center">
      <b>STAND</b> 「 S E S S I O N &nbsp; E X P I R E D 」<br>
      <sub><i>habilidade: mantém vivo o que já devia ter morrido</i></sub>
    </td>
  </tr>
  <tr>
    <td><b>DESTRUCTIVE POWER</b></td>
    <td><code>▰▰▰▰▱</code>&nbsp; CVE publicado no MITRE/NVD — Apache Airflow</td>
  </tr>
  <tr>
    <td><b>SPEED</b></td>
    <td><code>▰▰▰▰▰</code>&nbsp; §PROTON: −40% tokens, −43% latência, mesma qualidade</td>
  </tr>
  <tr>
    <td><b>RANGE</b></td>
    <td><code>▰▰▰▱▱</code>&nbsp; aplicações web e APIs — auth/session, IDOR, lógica de negócio</td>
  </tr>
  <tr>
    <td><b>PRECISION</b></td>
    <td><code>▰▰▰▰▱</code>&nbsp; CWE-613 — a sessão JWT sobrevive ao logout</td>
  </tr>
  <tr>
    <td><b>PERSISTENCE</b></td>
    <td><code>▰▰▰▰▰</code>&nbsp; 7 relatórios no concurso Sherlock × Ripple (XRP Ledger, C++)</td>
  </tr>
  <tr>
    <td><b>DEVELOPMENT POTENTIAL</b></td>
    <td><code>▰▰▰▰▰</code>&nbsp; Ciência da Computação · Rio de Janeiro · 2026</td>
  </tr>
</table>

**Trabalho em:** aplicações web e APIs (auth/session, IDOR, lógica de negócio) · segurança de agentes LLM e comunicação entre modelos · ferramentas próprias em Python/C.

---

### ▰ Selected Battles

**[§PROTON](https://github.com/zbern1976/proton)** — e se dois modelos de IA parassem de escrever prosa um pro outro?
Benchmark custo × qualidade de um formato compacto entre modelos. Juiz LLM cego, reproduzível, MIT.
`−40% tokens de saída` · `−43% latência` · `qualidade empatada` · `Python, zero dependências`

**[CVE-2026-48726](https://nvd.nist.gov/vuln/detail/CVE-2026-48726)** — o logout que não desligava a luz.
No Apache Airflow `< 3.2.2`, o token JWT de sessão continuava válido depois do logout. Reportada de forma responsável, publicada no MITRE/NVD.
`CWE-613` · `auth/session` · `disclosure coordenado`

<details>
<summary><b>▰ Arquivo de missões</b> — o que mais roda por aqui</summary>

<br>

- **Sherlock × Ripple (XRP Ledger)** — concurso de auditoria de abril/2026. Revisei código C++ de protocolo (Batch, MPT, Confidential Transfer) e submeti 7 relatórios. Nenhum premiado — mas foi onde aprendi a ler protocolo de verdade.
- **Trading quantitativo** — bots próprios em Python/TypeScript: coleta de dados, backtest com validação walk-forward, paper trading. Privados porque mexem com chave de API.
- **Ferramental próprio** — automação de recon, scripts de análise, utilitários em C. A regra é: se eu uso toda semana, viro ferramenta.
- **Estudo em público** — Ciência da Computação (UVA, Rio). C, autômatos, estatística.

</details>

---

### ▰ Stack

`Python` · `C` · `SQLite / SQL` · `Linux` · `Git` · `LLM APIs` · `Burp / recon próprio`

<sub>Procurando **estágio** em segurança, dados ou desenvolvimento — Rio de Janeiro ou remoto.</sub>

<p align="center">
  <img src="https://img.shields.io/github/stars/zbern1976/proton?style=flat-square&label=proton&color=fbbf24&labelColor=4c1d95" alt="stars">
  <img src="https://img.shields.io/github/license/zbern1976/proton?style=flat-square&color=a78bfa&labelColor=4c1d95" alt="license">
</p>

<p align="center"><sub>banner desenhado do zero — nenhum material licenciado de JoJo's Bizarre Adventure foi usado.</sub></p>
