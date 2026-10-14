# ADR 0001: Monorepo Único com Pipelines Isoladas por Linguagem

**Estado:** Aceite

**Contexto:**
Os projetos do portfólio cobrem 5 ecossistemas tecnológicos distintos: Python, Rust, C++, Java e C#. Recrutadores e avaliadores técnicos necessitam de uma visão consolidada do código num único local, mas a falha numa ferramenta ou versão de compilador não deve mascarar os testes bem-sucedidos das restantes tecnologias.

**Decisão:**
Adotar uma estrutura de monorepo poliglota onde cada projeto é modular e autónomo (com o seu próprio ficheiro de compilação, dependências, testes unitários e documentação). A Integração Contínua (GitHub Actions) executa tarefas especializadas e paralelas para cada linguagem de programação.

**Consequências:**

- **Vantagens:** Visão unificada de engenharia, facilidade de partilha do repositório e centralização de regras de segurança e testes.
- **Compromissos:** A configuração da pipeline de CI cresce à medida que mais ferramentas são adicionadas, exigindo dependências bem delimitadas por diretório.
