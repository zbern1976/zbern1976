<p align="center">
  <a href="https://github.com/zbern1976/proton"><img src="https://raw.githubusercontent.com/zbern1976/proton/main/docs/logo.svg" width="480" alt="§PROTON"></a>
</p>

### Bernardo Curi

Pesquisador de segurança ofensiva. **Creditado como _finder_ do CVE-2026-48726** no registro oficial do MITRE: no Apache Airflow `< 3.2.2`, o logout do `FabAuthManager` e do `KeycloakAuthManager` não chegava ao `revoke_token()`, então o JWT continuava aceito pela API até expirar sozinho (CWE-613). Corrigido na 3.2.2.

[Advisory (NVD)](https://nvd.nist.gov/vuln/detail/CVE-2026-48726) · [Registro no CVE.org](https://www.cve.org/CVERecord?id=CVE-2026-48726) · [Patch — apache/airflow#67289](https://github.com/apache/airflow/pull/67289)

---

**Trabalho em:** aplicações web e APIs (auth/session, IDOR, lógica de negócio) · segurança de agentes LLM e comunicação entre modelos · ferramentas próprias em Python/C.

**Selected work**

- **[CVE-2026-48726](https://www.cve.org/CVERecord?id=CVE-2026-48726)** — Apache Airflow: a sessão sobrevive ao logout. Reportado de forma responsável, creditado como _finder_ no registro, corrigido na 3.2.2.
- **[§PROTON](https://github.com/zbern1976/proton)** — benchmark custo × qualidade de um formato compacto entre modelos de IA. Chamadas reais de API, juiz cego, reprodutível, MIT.

**Stack:** `Python` · `C` · `SQLite / SQL` · `Linux` · `Git` · `LLM APIs`
