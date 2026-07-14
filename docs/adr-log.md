# Parallaxis — Architecture Decision Records (ADR Log)

Formato resumido por decisão: Contexto → Decisão → Consequências. Todas com status **Aceito**.

---

## ADR001 — Django com Clean Architecture em camadas, em vez de Django "padrão"

**Contexto:** o backend do projeto anterior não tinha nenhuma separação de camadas — toda regra de negócio vivia em views/serializers.
**Decisão:** adotar `domain/`, `use_cases/`, `infra/`, `api/` como camadas explícitas, com regra de dependência unidirecional (para dentro).
**Consequências:** mais arquivos e indireção do que Django convencional; em troca, regra de negócio testável isoladamente do framework, e trocar peças de infraestrutura (ex: provider de dados) não exige tocar em lógica de domínio.

## ADR002 — PostgreSQL como banco de dados

**Contexto:** necessidade de queries relacionais/agregadas para a análise de gosto (RF15-RF17).
**Decisão:** PostgreSQL, reaproveitando setup Docker já existente no projeto anterior.
**Consequências:** suporte nativo a `JSONB` (usado em `Game.platforms`) e a `CHECK constraints` complexas (usadas nas regras de score/status).

## ADR003 — Redis apenas como cache, sem fila de mensagens/Celery no MVP

**Contexto:** avaliado no documento de arquitetura — nenhum fluxo do MVP exige processamento assíncrono real.
**Decisão:** Redis via `django-redis`, papel único de cache (metadados IGDB, TTL 7 dias). Celery fica fora do MVP.
**Consequências:** menos peças móveis para operar/testar; se o motor de recomendação ficar pesado no futuro, essa decisão precisa ser revisitada.

## ADR004 — IGDB como provider de dados de jogos, com abstração via interface

**Contexto:** comparação entre RAWG (API key simples, mas com sinais reportados de instabilidade) e IGDB (mais estável, mantida pela Twitch, porém exige OAuth2 client-credentials).
**Decisão:** IGDB por trás da interface `GameDataProvider`, seguindo Dependency Inversion — a aplicação não conhece a IGDB diretamente.
**Consequências:** overhead de implementar e manter renovação de token OAuth2; em troca, maior confiabilidade de longo prazo e possibilidade de trocar/adicionar provider (ex: Steam, no futuro) sem reescrever regra de negócio.

## ADR005 — UUID como chave primária em todas as tabelas

**Contexto:** IDs sequenciais expõem informação e permitem enumeração de recursos via URL.
**Decisão:** UUID em vez de auto-incremento em todas as entidades.
**Consequências:** chaves maiores (16 bytes vs 4/8), leve custo de performance de índice — aceitável no volume de dados esperado; ganho de segurança por obscuridade de recurso.

## ADR006 — Autenticação via JWT (simplejwt), reaproveitando padrão do projeto anterior

**Contexto:** o projeto anterior já tinha esse fluxo implementado, mas com um bug real no endpoint de refresh do frontend.
**Decisão:** manter JWT com access token curto (15 min) e refresh token (7 dias), corrigindo o bug de rota identificado.
**Consequências:** não requer infraestrutura de sessão server-side; exige atenção a onde o token é armazenado no frontend (decisão de segurança tratada à parte, ver estratégia de auth nos padrões de engenharia).

## ADR007 — Análise de gosto e recomendação computadas sob demanda, não persistidas

**Contexto:** volume de dados esperado (biblioteca pessoal) é pequeno o suficiente para tornar pré-computação desnecessária.
**Decisão:** `TasteAnalysisService` e `RecommendationService` calculam resultado em tempo real a cada chamada, sem tabela de snapshot.
**Consequências:** elimina problema de invalidação de cache de snapshot; se o volume crescer, a evolução natural é cache de resultado (Redis, TTL curto), não uma nova tabela.

## ADR008 — Ratings externos (`critic_rating`/`community_rating`) como campos explícitos, não generalizados

**Contexto:** IGDB fornece dois valores distintos (crítica e comunidade); Steam pode ser adicionada no futuro.
**Decisão:** dois campos fixos no MVP, em vez de uma tabela genérica `ExternalRating(source, type, value)`.
**Consequências:** simplicidade agora; quando uma segunda fonte externa for de fato implementada, essa é a decisão que deve ser revisitada e refatorada — não antes (evita generalização prematura).

## ADR009 — Frontend em React 19 + TypeScript + Vite + TanStack Query

**Contexto:** o projeto anterior usava JS puro sem gerenciamento de estado de servidor padronizado (chamadas manuais com `useEffect`/`useState`).
**Decisão:** adicionar TypeScript (diferenciação de stack frente ao TCC, que também é Django+React) e TanStack Query para cache/loading/erro de chamadas de API.
**Consequências:** curva de configuração de tipos (especialmente tipando respostas da IGDB via cache local), mas elimina boilerplate de estado de requisição manual e é o padrão atual de mercado.

## ADR010 — GitHub Flow como estratégia de versionamento

**Contexto:** projeto solo, sem ciclos de release formais nem múltiplas versões em produção simultâneas.
**Decisão:** branch curta por feature + Pull Request + merge direto na `main`, sem branches `develop`/`release`/`hotfix` do Git Flow.
**Consequências:** simplicidade de fluxo; adequado porque não há necessidade de suportar múltiplas versões em paralelo, que é o cenário que justificaria Git Flow.
