# Parallaxis — MVP e Roadmap

## 1. Critério de corte

O MVP é exatamente o escopo já formalizado em RF01–RF19 (`requirements.md`). O que falta aqui é organizar a **ordem de entrega**: como fatiar 1-2 meses de trabalho solo em marcos que geram valor demonstrável a cada etapa, em vez de só ter algo funcional no último dia.

Princípio de fatiamento: cada marco termina em algo **testável de ponta a ponta**, não em uma camada isolada (ex: não faz sentido terminar "só o backend" nas primeiras 3 semanas e só ver a UI funcionando no fim — isso esconde problema de integração até tarde demais).

## 2. Marcos (Milestones)

### M0 — Fundação (Semana 1)

**Objetivo:** repositórios criados, ambiente reproduzível, autenticação funcionando ponta a ponta.
**Entregáveis:** setup Docker Compose (Postgres + Redis), esqueleto de camadas (`domain/use_cases/infra/api`), CI básico (lint + testes rodando no GitHub Actions), models e migrations de `User`, endpoints de cadastro/login/refresh (RF01–RF05), tela de login/cadastro no frontend consumindo a API real.
**Critério de aceite:** usuário consegue se cadastrar, logar, e permanecer logado após expiração do access token (refresh funcionando) — testado manualmente e via teste automatizado de integração.
**RFs cobertos:** RF01–RF05.

### M1 — Integração com IGDB (Semana 2)

**Objetivo:** busca de jogos funcionando com dado real externo, já com a abstração de provider.
**Entregáveis:** interface `GameDataProvider` + `IGDBGameProvider` (OAuth2 client-credentials com renovação de token), cache Redis com TTL de 7 dias (RNF05), endpoint de busca (RF06–RF07), tela de busca no frontend.
**Critério de aceite:** buscar um jogo real retorna resultado da IGDB na primeira vez (cache miss) e do cache na segunda (log confirma a diferença de origem).
**RFs cobertos:** RF06, RF07.

### M2 — Biblioteca e Avaliação (Semana 3–4)

**Objetivo:** o núcleo do produto — usuário consegue montar a própria biblioteca.
**Entregáveis:** models `Game`, `Genre`, `LibraryEntry` com todas as constraints do MER, use cases de adicionar/avaliar/editar/remover (RF08–RF14) aplicando RN01, RN02, RN06, RN09, tela de biblioteca com filtros (RF13) no frontend.
**Critério de aceite:** todas as regras de negócio (RN01–RN09) cobertas por teste automatizado, não só validadas manualmente — este é o marco com maior densidade de regra de negócio, então é o que mais define a nota de qualidade do projeto.
**RFs cobertos:** RF08–RF14.

### M3 — Análise de Gosto e Recomendação (Semana 5–6)

**Objetivo:** a parte que diferencia o produto de um catálogo comum.
**Entregáveis:** `TasteAnalysisService` (distribuição por gênero, evolução temporal, divergência do mainstream — RF15–RF17), `RecommendationService` (RF18, com a regra de mínimo de 5 avaliações e aviso progressivo — RN04), dashboard consolidado (RF19) com gráficos (Recharts) no frontend.
**Critério de aceite:** com uma biblioteca de teste (dados reais seus, já que você vai usar o produto de verdade), os três relatórios de análise retornam valores coerentes e verificáveis manualmente.
**RFs cobertos:** RF15–RF19.

### M4 — Polimento, Acessibilidade e Deploy (Semana 6–8)

**Objetivo:** projeto pronto para ser mostrado a um recrutador sem ressalvas.
**Entregáveis:** responsividade mobile (RNF08), verificação básica de contraste/navegação por teclado, cobertura de teste atingindo as metas da RNF07a/b, pipeline de deploy automático funcionando (Render/Railway + Vercel), README completo (screenshots, link do demo, diagrama de arquitetura), checklist de segurança (seção 5 dos Padrões de Engenharia) revisado item a item.
**Critério de aceite:** uma pessoa que nunca viu o projeto consegue, a partir só do README, entender o que o sistema faz, como rodar localmente, e acessar o demo publicado.

## 3. Roadmap pós-MVP (backlog consciente, não esquecido)

Registrado aqui para não se perder, mas **fora do escopo de execução atual** — cada item tem seu próprio gatilho de quando faria sentido implementar:

| Item                                                 | Gatilho para implementar                                                                                                            |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Landing page pública + mais páginas institucionais   | Depois do MVP funcional, quando o foco vira "vitrine" em vez de "produto"                                                           |
| Filmes, séries e animes (TMDB)                       | Depois de validar que o padrão de análise de gosto funciona bem só com jogos                                                        |
| Generalização de ratings externos (`ExternalRating`) | No momento em que uma segunda fonte (Steam) for de fato implementada — gatilho já registrado no ADR008                              |
| Celery para processamento assíncrono                 | Se o motor de recomendação ficar pesado o suficiente para não caber no tempo de resposta síncrono — gatilho já registrado no ADR003 |
| Sentry / observabilidade externa                     | Se o projeto for exposto a uso real além de você e recrutadores testando                                                            |
| Testes E2E (Playwright)                              | Se o número de fluxos críticos crescer a ponto de teste manual não ser mais suficiente                                              |

**Explicitamente descartado, não só adiado** (já registrado em `requirements.md`): recursos sociais (seguir usuários, feed, comentários) e recomendação colaborativa — esses não são "próxima versão", são decisão de posicionamento de produto que não muda com o tempo.
