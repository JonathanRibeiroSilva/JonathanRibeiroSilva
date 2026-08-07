<div align="center">

<img alt="&gt;_ J4yz0n · pentester em formação · full stack" src="https://capsule-render.vercel.app/api?type=rect&color=000000&fontColor=39FF5E&height=120&section=header&text=%3E_%20jonathan%20ribeiro&fontSize=40&fontAlignY=44&desc=pentester%20em%20forma%C3%A7%C3%A3o%20%C2%B7%20desenvolvedor%20full%20stack&descSize=16&descAlignY=68&descColor=8B919C" width="100%"/>

<img alt="Pentester em formação • Desenvolvedor Full Stack" src="https://readme-typing-svg.demolab.com?font=IBM+Plex+Mono&weight=600&size=19&duration=3200&pause=900&color=39FF5E&background=000000&center=true&vCenter=true&width=1000&height=52&lines=Pentester+em+forma%C3%A7%C3%A3o+%E2%80%A2+Desenvolvedor+Full+Stack;Sei+onde+a+autentica%C3%A7%C3%A3o+cede;Sei+onde+o+gateway+confia+demais"/>

<a href="https://www.linkedin.com/in/jonathan-ribeiro-da-silva"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-000000?style=for-the-badge&logo=linkedin&logoColor=00D4FF"/></a> <a href="https://tryhackme.com/p/J4yz0n"><img alt="TryHackMe" src="https://img.shields.io/badge/TryHackMe-000000?style=for-the-badge&logo=tryhackme&logoColor=39FF5E"/></a> <a href="mailto:jonathanribeirodasilva@outlook.com.br"><img alt="E-mail" src="https://img.shields.io/badge/E--mail-000000?style=for-the-badge&logo=maildotru&logoColor=FF2EC4"/></a>

</div>

---

> **Meu objetivo é atuar como Pentester.** Anos construindo aplicações me deram o mapa por dentro:
> sei onde a autenticação cede, onde o gateway confia demais e por que a correção proposta
> funciona no código real.

<details>
<summary>🇬🇧 <b>English</b></summary>

> **My goal is to work as a Pentester.** Years of building applications gave me the map from the
> inside: I know where authentication gives, where the gateway trusts too much, and why a proposed
> fix actually holds in real code.

</details>

---

## `01` / Sobre · About

```console
┌──(jonathan㉿kali)-[~]
└─$ whoami

  User      : j4yz0n
  Hostname  : Jonathan Ribeiro
  Papel     : Pentester em formação · Dev Full Stack
  SO        : Kali Linux 2026.1
  Formação  : Tecnologia + trilhas de segurança ofensiva
  Objetivo  : Pentester em time de segurança ofensiva, onde a
              leitura de código faz diferença no relatório final
```

Sou apaixonado por cibersegurança. Construo sistemas distribuídos de dia e estudo ataques de noite,
e uma prática alimenta a outra. Estudo com laboratório próprio, não só com vídeo.

<details>
<summary>🇬🇧 <b>English</b></summary>

I'm passionate about cybersecurity. I build distributed systems by day and study attacks by night,
and each side sharpens the other. I learn in my own lab, not just from videos.

</details>

---

## `02` / Metodologia · Methodology

Seis etapas, sempre na mesma ordem.

```console
┌──(jonathan㉿kali)-[~]
└─$ recon --target alvo.com --passive
[01] entender tudo que o alvo expõe antes de tocar em qualquer serviço

┌──(jonathan㉿kali)-[~]
└─$ nmap -sV -p- legacy.alvo.com && ffuf -w wordlist.txt
[02] transformar a superfície em lista concreta de serviços, rotas e papéis

┌──(jonathan㉿kali)-[~]
└─$ review --owasp-top10 --scope api/v1
[03] cruzar comportamento observado com falhas conhecidas e lógica de negócio

┌──(jonathan㉿kali)-[~]
└─$ poc idor --from 1042 --to 1043 --scope-check
[04] provar o impacto com o menor ruído possível, dentro do escopo acordado

┌──(jonathan㉿kali)-[~]
└─$ diff --patch authz-invoices
[05] propor a correção que sustenta no código e na arquitetura — não só no WAF

┌──(jonathan㉿kali)-[~]
└─$ report build --severity high --evidence ./poc
[06] relatório que qualquer dev reproduz, prioriza e corrige sem me chamar
```

| # | Etapa · Stage | Ferramental |
|:--|:--|:--|
| `01` | Reconhecimento · Recon | OSINT · crt.sh · amass · whois |
| `02` | Enumeração · Enumeration | Nmap · ffuf · Burp Suite |
| `03` | Identificação · Identification | OWASP Top 10 · Burp Repeater · leitura de código |
| `04` | Exploração · Exploitation | Burp Suite · curl · script próprio |
| `05` | Mitigação · Mitigation | defesa em profundidade · code review · hardening |
| `06` | Documentação · Documentation | CVSS · markdown · evidência versionada |

---

## `03` / Ferramentas · Tools

Nada de barra de progresso. Cada item aqui apareceu em um laboratório, em um writeup ou em um
sistema que eu coloquei em produção.

<details>
<summary>🇬🇧 <b>English</b></summary>

No progress bars. Everything here showed up in a lab, in a writeup or in a system I shipped to
production — and I can explain what I did with it.

</details>

<h4>Cyber Security &nbsp;<code>foco principal</code></h4>
<p>
  <img height="44" alt="OWASP Top 10" title="OWASP Top 10" src="https://cdn.simpleicons.org/owasp/0f7a2e/39ff5e"/>&nbsp;&nbsp;
  <img height="44" alt="Segurança Web" title="Segurança Web" src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/web-security.svg"/>&nbsp;&nbsp;
  <img height="44" alt="Redes" title="Redes" src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/network.png"/>&nbsp;&nbsp;
  <img height="44" alt="Active Directory" title="Active Directory" src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/active-directory.png"/>&nbsp;&nbsp;
  <img height="44" alt="Hardening" title="Hardening" src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/hardening.png"/>&nbsp;&nbsp;
  <img height="44" alt="Linux" title="Linux" src="https://cdn.simpleicons.org/linux/0f7a2e/39ff5e"/>&nbsp;&nbsp;
  <img height="44" alt="Análise de logs" title="Análise de logs" src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/log-analysis.svg"/>
</p>

<h4>Pentest &nbsp;<code>prática em laboratório</code></h4>
<p>
  <img height="44" alt="Kali Linux" title="Kali Linux" src="https://cdn.simpleicons.org/kalilinux/0b7c96/00d4ff"/>&nbsp;&nbsp;
  <img height="44" alt="Nmap" title="Nmap" src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/nmap.png"/>&nbsp;&nbsp;
  <img height="44" alt="Burp Suite" title="Burp Suite" src="https://cdn.simpleicons.org/burpsuite/0b7c96/00d4ff"/>&nbsp;&nbsp;
  <img height="44" alt="THC Hydra" title="THC Hydra" src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/hydra.png"/>&nbsp;&nbsp;
  <img height="44" alt="Hashcat" title="Hashcat" src="https://cdn.simpleicons.org/hashcat/0b7c96/00d4ff"/>&nbsp;&nbsp;
  <img height="44" alt="John the Ripper" title="John the Ripper" src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/john-the-ripper.png"/>&nbsp;&nbsp;
  <img height="44" alt="Wireshark" title="Wireshark" src="https://cdn.simpleicons.org/wireshark/0b7c96/00d4ff"/>
</p>

<h4>Desenvolvimento &nbsp;<code>vantagem competitiva</code></h4>
<p>
  <img height="44" alt="Python" title="Python" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="Java" title="Java" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="JavaScript" title="JavaScript" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="TypeScript" title="TypeScript" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="C" title="C" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="React" title="React" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="Vue.js" title="Vue.js" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="Node.js" title="Node.js" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="PostgreSQL" title="PostgreSQL" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="Redis" title="Redis" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="Git" title="Git" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="Vim" title="Vim" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vim/vim-original.svg"/>
</p>

<h4>Infraestrutura &nbsp;<code>onde a aplicação vive</code> &nbsp;·&nbsp; <code>CI/CD</code></h4>
<p>
  <img height="44" alt="Docker" title="Docker" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="RabbitMQ" title="RabbitMQ" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rabbitmq/rabbitmq-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="GitHub Actions" title="GitHub Actions" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/githubactions/githubactions-original.svg"/>&nbsp;&nbsp;
  <img height="44" alt="GitHub" title="GitHub" src="https://cdn.simpleicons.org/github/24292f/e6e8ec"/>&nbsp;&nbsp;
  <img height="44" alt="Cloudflare" title="Cloudflare" src="https://cdn.simpleicons.org/cloudflare"/>&nbsp;&nbsp;
  <img height="44" alt="PowerShell" title="PowerShell" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/powershell/powershell-original.svg"/>
</p>

---

## `04` / Projetos · Projects

### <img src="https://raw.githubusercontent.com/JonathanRibeiroSilva/JonathanRibeiroSilva/main/assets/cyph3r-x.png" height="26" align="top" alt=""/> [Cyph3r X](https://github.com/JonathanRibeiroSilva/Cyph3r-X) — cofre de senhas desktop, open source

`0 segredos legíveis no banco local` &nbsp; `600k iterações PBKDF2` &nbsp; `Fernet` &nbsp; `MIT`

Gerenciadores de senha na nuvem pedem confiança cega — você não sabe o que o servidor guarda, nem o
que ele consegue ler sobre você. Cyph3r X é um cofre **100% local**, empacotado num único `.exe`:
banco SQLite na máquina do usuário, nada sincroniza com a nuvem e a DEK nunca toca o disco.

> [!IMPORTANT]
> **Como eu ataquei o meu próprio cofre** — bypass da proteção anti-captura de tela · timing na
> verificação da master key · exfiltração via clipboard · fuzzing do importador (integrity check,
> allow-list de tabelas, bloqueio de triggers/views).
> Cada achado virou **issue + teste de regressão**.

<details>
<summary>🇬🇧 <b>English</b></summary>

Cloud password managers ask for blind trust — you don't know what the server stores, nor what it can
read about you. Cyph3r X is a **fully local** vault shipped as a single `.exe`: the SQLite database
stays on the user's machine, nothing syncs to the cloud, and the DEK never touches disk.

**How I attacked my own vault** — screen-capture protection bypass · timing on master key
verification · clipboard exfiltration · importer fuzzing. Every finding became an issue plus a
regression test.

</details>

<p>
  <img height="34" alt="Python" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"/>&nbsp;
  <img height="34" alt="Flask" src="https://cdn.simpleicons.org/flask/24292f/e6e8ec"/>&nbsp;
  <img height="34" alt="SQLite" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg"/>&nbsp;
  <code>Waitress</code> <code>PyWebView</code> <code>PBKDF2-HMAC-SHA256</code> <code>Fernet</code> <code>PyInstaller</code>
</p>

<a href="https://github.com/JonathanRibeiroSilva/Cyph3r-X/releases/latest/download/Cyph3r-X.exe"><img alt="Baixar .exe Windows" src="https://img.shields.io/badge/Baixar_.exe_%C2%B7_Windows-000000?style=for-the-badge&logo=windows&logoColor=00D4FF"/></a> <a href="https://github.com/JonathanRibeiroSilva/Cyph3r-X"><img alt="Código-fonte" src="https://img.shields.io/badge/C%C3%B3digo--fonte-000000?style=for-the-badge&logo=github&logoColor=39FF5E"/></a>

### [RunasERP](https://github.com/DenebCorp/RunasERP) — ERP em microsserviços

`8+ microsserviços` &nbsp; `100% dockerizado` &nbsp; `1 gateway central` &nbsp; `APIs REST versionadas`

Operação de varejo rodando em planilhas: estoque, pedidos e pagamentos sem fonte única de verdade e
sem trilha de auditoria. Virou um ERP em microsserviços com gateway centralizado, autenticação por
token, filas assíncronas para eventos de pedido e integração de pagamento com Mercado Pago.

A superfície ficou reduzida a um único gateway atrás de Cloudflare, segredos fora do repositório,
autorização por papel em cada serviço — e revisei os endpoints com a mesma checklist que uso em
pentest.

<details>
<summary>🇬🇧 <b>English</b></summary>

A retail operation running on spreadsheets: inventory, orders and payments with no single source of
truth and no audit trail. It became a microservices ERP with a central gateway, token
authentication, async queues for order events and Mercado Pago payment integration. The attack
surface is reduced to one gateway behind Cloudflare, secrets out of the repo, and role-based
authorization in every service — reviewed with the same checklist I use on a pentest.

</details>

<p>
  <img height="34" alt="FastAPI" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg"/>&nbsp;
  <img height="34" alt="PostgreSQL" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg"/>&nbsp;
  <img height="34" alt="RabbitMQ" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rabbitmq/rabbitmq-original.svg"/>&nbsp;
  <img height="34" alt="Redis" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg"/>&nbsp;
  <img height="34" alt="Docker" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg"/>&nbsp;
  <img height="34" alt="Nginx" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nginx/nginx-original.svg"/>&nbsp;
  <img height="34" alt="React" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg"/>&nbsp;
  <img height="34" alt="TypeScript" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg"/>
</p>

---

## `05` / Certificados · Certificates

<details>
<summary><code>Get-Certification | Format-Table -AutoSize</code></summary>

<br>

| Emissor | Trilha | Ano | Status |
|:--|:--|:--|:--|
| Cisco Academy | Gerenciamento de Ameaças Cibernéticas | 2025 | concluído |
| Cisco Academy | Introdução a Cibersegurança | 2025 | concluído |
| SCRUMstudy | Scrum Fundamentals Certified | 2024 | concluído |
| Fundação Bradesco | Ética no Desenvolvimento de Sistemas | 2023 | concluído |
| Prof. Pietro M. Oliveira | Lógica de Programação em Linguagem C | 2023 | concluído |
| Fundação Bradesco | Fundamentos de Lógica de Programação | 2023 | concluído |

</details>

---

## `06` / Contato · Contact

<div align="center">

<img alt="Estatísticas do GitHub" height="170" src="https://github-stats-extended.vercel.app/api?username=JonathanRibeiroSilva&show_icons=true&hide=stars&include_all_commits=true&hide_border=true&bg_color=000000&title_color=39FF5E&text_color=E6E8EC&icon_color=00D4FF"/> <img alt="Linguagens mais usadas" height="170" src="https://github-stats-extended.vercel.app/api/top-langs?username=JonathanRibeiroSilva&layout=compact&hide_border=true&bg_color=000000&title_color=39FF5E&text_color=E6E8EC"/>

<img alt="Sequência de contribuições" src="https://streak-stats.demolab.com?user=JonathanRibeiroSilva&locale=pt_BR&background=000000&border=1F2328&stroke=1F2328&ring=39FF5E&fire=FF2EC4&currStreakNum=E6E8EC&sideNums=E6E8EC&currStreakLabel=39FF5E&sideLabels=6E7581&dates=6E7581"/>

<br><br>

<a href="mailto:jonathanribeirodasilva@outlook.com.br"><img alt="E-mail" src="https://img.shields.io/badge/E--mail-000000?style=for-the-badge&logo=maildotru&logoColor=FF2EC4"/></a> <a href="https://www.linkedin.com/in/jonathan-ribeiro-da-silva"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-000000?style=for-the-badge&logo=linkedin&logoColor=00D4FF"/></a> <a href="https://tryhackme.com/p/J4yz0n"><img alt="TryHackMe" src="https://img.shields.io/badge/TryHackMe-000000?style=for-the-badge&logo=tryhackme&logoColor=39FF5E"/></a>

<br>

<sub><code>fuso GMT-3 · Brasil</code> &nbsp; <code>resposta em até 24h</code> &nbsp; <code>remoto ou híbrido</code></sub>

<br><br>

<sub>Feito com atenção a detalhes e à superfície de ataque.</sub>

</div>
