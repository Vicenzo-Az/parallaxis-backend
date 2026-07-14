# Parallaxis — Estrutura de Pastas Comentada

## 1. Backend

Decisão de organização: em vez de um único app `api` genérico (como era no projeto anterior), separei em **dois bounded contexts** — `users` (conta/autenticação) e `games` (biblioteca, avaliação, análise de gosto). Motivo: são responsabilidades de negócio genuinamente diferentes, com ciclos de vida próprios, e separar deixa explícito onde cada regra mora — é uma aplicação prática de Single Responsibility no nível de módulo, não só de classe.

```py
backend/
├── config/                      # settings, urls raiz, wsgi/asgi (equivalente ao antigo "project/")
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py                # DEBUG=True aqui, nunca no base.py (corrige o problema identificado no projeto anterior)
│   │   └── prod.py                # ALLOWED_HOSTS explícito, DEBUG=False fixo
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── users/                   # bounded context: conta e autenticação
│   │   ├── domain/
│   │   │   ├── entities.py        # User (entidade pura, sem Django)
│   │   │   └── exceptions.py
│   │   ├── use_cases/
│   │   │   ├── register_user.py
│   │   │   ├── authenticate_user.py
│   │   │   └── delete_account.py  # aplica RN07 (cascade delete)
│   │   ├── infra/
│   │   │   ├── models.py          # Django ORM — mapeia para tabela users do MER
│   │   │   └── repositories.py
│   │   ├── api/
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   └── tests/
│   │       ├── test_use_cases.py
│   │       └── factories.py
│   │
│   └── games/                   # bounded context: biblioteca, avaliação, análise
│       ├── domain/
│       │   ├── entities.py        # Game, Genre, LibraryEntry, EntryStatus
│       │   ├── interfaces.py      # GameDataProvider (abstração, ver ADR004)
│       │   └── exceptions.py
│       ├── use_cases/
│       │   ├── search_games.py
│       │   ├── rate_game.py       # aplica RN01, RN02, RN09
│       │   ├── list_library.py
│       │   ├── taste_analysis.py  # TasteAnalysisService — RF15-RF17
│       │   └── recommend_games.py # RecommendationService — RF18, RN04
│       ├── infra/
│       │   ├── models.py          # Game, Genre, LibraryEntry (Django ORM)
│       │   ├── repositories.py
│       │   ├── providers/
│       │   │   └── igdb_provider.py   # implementa GameDataProvider
│       │   └── cache.py           # wrapper de django-redis
│       ├── api/
│       │   ├── views.py
│       │   ├── serializers.py
│       │   └── urls.py
│       └── tests/
│           ├── test_use_cases.py  # cobre a meta de 80% da RNF07a
│           ├── test_api.py
│           └── factories.py
│
├── docs/                        # os documentos que estamos produzindo agora
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── manage.py
```

**Por que `domain/` fica dentro de cada app, e não num app `core` compartilhado:** como só há dois bounded contexts e eles não compartilham entidades entre si (um `LibraryEntry` sempre pertence a um `games`, nunca é referenciado por regra de negócio de `users`), não há necessidade de um módulo compartilhado ainda. Se um terceiro contexto futuro precisar reusar algo, esse é o gatilho certo para extrair um `apps/shared/` — não antes (mesmo princípio de generalização tardia do ADR008).

## 2. Frontend

Decisão de organização: estrutura por **tipo de arquivo** (`pages/`, `components/`, `services/`), não por feature (`features/library/`, `features/auth/`). Para um projeto desse porte (poucas telas, um domínio central), organização por feature adicionaria uma camada de indireção sem ganho real — ela compensa em aplicações grandes com muitos times trabalhando em paralelo, que não é o nosso caso. Registro isso como decisão consciente, não como "não pensei na alternativa".

```py
frontend/
├── src/
│   ├── app/
│   │   ├── App.tsx                # composição de providers (QueryClient, AuthProvider) + router
│   │   └── queryClient.ts         # configuração do TanStack Query
│   │
│   ├── pages/                     # uma pasta por tela
│   │   ├── LoginPage/
│   │   ├── SignupPage/
│   │   ├── DashboardPage/
│   │   ├── LibraryPage/
│   │   └── GameDetailPage/
│   │
│   ├── components/
│   │   ├── ui/                    # componentes puros, sem lógica de negócio (Button, Input, Modal)
│   │   ├── layout/                 # Header, Sidebar, PageWrapper
│   │   └── domain/                # componentes ligados ao domínio (GameCard, RatingInput, GenreChart)
│   │
│   ├── services/                  # camada de acesso à API, tipada
│   │   ├── api.ts                 # client Axios centralizado + interceptor de refresh (bug corrigido)
│   │   ├── authService.ts
│   │   ├── libraryService.ts
│   │   └── analysisService.ts
│   │
│   ├── hooks/                     # custom hooks, muitos envolvendo TanStack Query
│   │   ├── useAuth.ts
│   │   ├── useLibrary.ts
│   │   └── useTasteAnalysis.ts
│   │
│   ├── context/
│   │   └── AuthContext.tsx        # reaproveitado do projeto anterior (route guards inclusos)
│   │
│   ├── routes/
│   │   ├── ProtectedRoute.tsx     # reaproveitado
│   │   ├── PublicRoute.tsx        # reaproveitado
│   │   └── RootRedirect.tsx       # reaproveitado
│   │
│   ├── types/                     # tipos TS — espelham as entidades de domínio do backend
│   │   ├── game.ts
│   │   ├── libraryEntry.ts
│   │   └── user.ts
│   │
│   └── lib/                       # utilitários puros
│       └── normalizeScale.ts      # implementa RN09 (conversão 1-10 → 0-100) no client, para exibição consistente
│
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

**Nota sobre `lib/normalizeScale.ts`:** essa é uma boa amostra de rastreabilidade entre regra de negócio e código — RN09 (normalização de escala para divergência) não é só uma regra de backend, o frontend também precisa dela sempre que quiser exibir a nota do usuário lado a lado com a nota da IGDB de forma comparável.
