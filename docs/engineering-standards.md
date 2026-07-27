# Parallaxis — Padrões de Engenharia

## 1. Estratégia de Testes

Pirâmide de testes adaptada ao porte do projeto — mais peso na base (rápido, barato, roda a cada commit), menos no topo (lento, caro, roda só quando necessário):

| Nível                 | Escopo                                                                              | Ferramenta                         | Meta                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| Unitário (backend)    | `use_cases/` e `domain/`, isolados via `FakeGameProvider` e repositórios em memória | pytest + pytest-django             | ≥80% de cobertura (RNF07a)                                                                     |
| Integração (backend)  | Endpoints da API (`auth`, `library-entries`, `analysis`) com banco de teste real    | pytest-django + `APIClient` do DRF | Cobre os fluxos críticos: cadastro, login, avaliar jogo, listar biblioteca                     |
| Componente (frontend) | Componentes de domínio e páginas críticas                                           | Vitest + Testing Library           | Login, cadastro, fluxo de avaliação, dashboard (RNF07b)                                        |
| E2E                   | Fora do escopo do MVP                                                               | —                                  | Considerar Playwright só se o projeto crescer além do portfólio atual — não é prioridade agora |

**Regra prática:** todo `use_case` novo nasce com teste no mesmo PR que o implementa — não é etapa separada feita "depois". Isso é mais fácil de cumprir aqui do que pareceria em outros projetos, porque a camada de domínio já nasce desacoplada de Django (ADR001) — testar não exige banco de dados nem servidor rodando.

## 2. Convenções de Código

| Linguagem  | Lint/Format                                          | Configuração                 |
| ---------- | ---------------------------------------------------- | ---------------------------- |
| Python     | `ruff` (lint + format, substitui flake8+black+isort) | `pyproject.toml`, roda no CI |
| TypeScript | `eslint` + `prettier`                                | `.eslintrc`, roda no CI      |

Nomenclatura: classes de use case em inglês e verbo-sujeito (`RateGameUseCase`, não `GameRater`); nomes de branch, commits e documentação em português (consistente com o restante do projeto); nomes de variável/função em inglês no código (padrão de mercado), mensagens de erro voltadas ao usuário em português.

**Documentação de API obrigatória por view:** toda view baseada em `APIView` deve declarar `@extend_schema` (drf-spectacular) com o serializer de entrada e a especificação de resposta. Sem isso, o Swagger não gera o formulário de "Try it out", mesmo que o endpoint funcione corretamente via `curl`/cliente HTTP direto — a API funciona, mas fica sem valor prático como ferramenta de teste manual. View nova sem `@extend_schema` é sinal de tarefa incompleta, não só documentação pendente — mesmo critério de "pronto" que as metas de teste da seção 1.

## 3. Estratégia de Versionamento

**GitHub Flow** (já registrado no ADR010): branch curta a partir da `main` por funcionalidade/correção, Pull Request obrigatório mesmo trabalhando sozinho (força revisão própria antes do merge — hábito profissional real), merge direto na `main` após CI passar.

**Padrão de commit:** Conventional Commits, mensagens em português — mesmo padrão que você já usa:

```
feat: adiciona busca de jogos via IGDB
fix: corrige endpoint de refresh do token JWT
docs: adiciona MER do banco de dados
test: cobre RateGameUseCase com casos de RN02
refactor: extrai normalização de escala para lib compartilhada
```

**Nomenclatura de branch:** `feat/busca-jogos-igdb`, `fix/refresh-token-endpoint`.

## 4. Estratégia de Deploy

| Componente                  | Onde                                              | Como                                                                                                                                                      |
| --------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend (Django + Postgres) | Render ou Railway                                 | Deploy automático via GitHub Actions ao mergear na `main`; variáveis sensíveis (SECRET_KEY, credenciais IGDB) via secrets da plataforma, nunca commitadas |
| Redis                       | Instância gerenciada do mesmo provedor do backend | —                                                                                                                                                         |
| Frontend                    | Vercel ou Netlify                                 | Deploy automático por push, build do Vite                                                                                                                 |

**Pipeline de CI/CD (GitHub Actions), por repositório:**

1. Lint (`ruff` / `eslint`)
2. Testes (pytest / vitest)
3. Build (imagem Docker do backend / build estático do Vite)
4. Deploy (só na `main`, só se os passos anteriores passarem)

Isso é o item que **não existia em nenhum dos dois repositórios anteriores** — é uma adição pura de qualidade, não uma correção.

## 5. Segurança — Checklist

- [ ] `DEBUG=False` fixo em produção (`config/settings/prod.py`), nunca dependente de variável de ambiente esquecida (corrige a falha real identificada no projeto anterior).
- [ ] `ALLOWED_HOSTS` explícito com o domínio real, nunca `['*']`.
- [ ] Senhas com hash via Django (`PBKDF2`/`argon2`), nunca texto plano.
- [ ] Segredos (`SECRET_KEY`, credenciais IGDB) fora do código, via variável de ambiente/secret do provedor — `.env.example` versionado, `.env` real no `.gitignore`.
- [ ] HTTPS obrigatório em produção (RNF04).
- [ ] Token JWT de acesso com expiração curta (15 min) + refresh (RNF03).
- [ ] `permission_classes` explícito em toda view — nunca depender do default implícito do DRF (o bug de `DocumentoViewSet` do projeto anterior nasceu exatamente dessa omissão).
- [ ] Rate limiting básico no endpoint de login (proteção contra força bruta) — via `django-ratelimit` ou throttle nativo do DRF.
- [ ] CORS restrito ao domínio do frontend em produção, não `*`.
- [ ] Validação de input em toda entrada de usuário via serializers do DRF (nunca confiar em validação só do frontend).

## 6. Observabilidade

Nível proporcional ao porte do projeto — sem exagerar em ferramental para uma aplicação de portfólio, mas demonstrando o conceito de forma real:

- **Logging estruturado** via `structlog`, formato JSON em produção (facilita se algum dia for parseado por ferramenta externa).
- Eventos obrigatórios de log: falha de autenticação, falha de integração com IGDB (timeout, erro de token), exceções não tratadas nos use cases.
- **Nunca logar dados sensíveis**: senha, token JWT, review completa do usuário (só metadados como `user_id`, `game_id`, timestamp).
- Sentry fica como _stretch goal_ documentado no roadmap, não obrigatório para o MVP — adicionar exige conta externa e configuração extra que não é o foco central da demonstração técnica deste projeto.

---

Com isso, a fase de planejamento técnico está **completa**: requisitos, modelo de domínio, MER, arquitetura, ADRs, estrutura de pastas e padrões de engenharia — os 8 documentos que definimos no início.

Falta um único artefato antes do código: o **MVP e Roadmap** formal, que vai cortar precisamente o que entra na v1 (incluindo decidir onde a landing page que você mencionou entra) e o que fica para depois. Seguimos para ele?

Falta um único artefato antes do código: o **MVP e Roadmap** formal, que vai cortar precisamente o que entra na v1 (incluindo decidir onde a landing page que você mencionou entra) e o que fica para depois. Seguimos para ele?
