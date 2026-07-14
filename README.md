# Parallaxis — Backend

Diário de jogos com análise de gosto e recomendação. Este repositório contém a API (Django + DRF) organizada em Clean Architecture.

> Repositório do frontend: (adicionar link aqui quando publicado)

## Stack

Django 5 · DRF · PostgreSQL · Redis · JWT (simplejwt) · IGDB API · drf-spectacular (OpenAPI) · pytest · Docker

## Arquitetura

Camadas por bounded context (`apps/users`, `apps/games`), cada uma com:

```text
domain/      → entidades e regras de negócio puras, sem Django
use_cases/   → orquestração da lógica de aplicação
infra/       → Django ORM, cliente IGDB, cache Redis
api/         → views, serializers, urls (DRF)
```

Regra de dependência: `api` → `use_cases` → `domain`, e `infra` implementa interfaces definidas em `domain`. Detalhes completos, com o porquê de cada decisão, em [`docs/architecture.md`](docs/architecture.md) e [`docs/adr-log.md`](docs/adr-log.md).

## Documentação do projeto

Todo o planejamento que precedeu o código está versionado aqui:

| Documento                                                        | Conteúdo                                                  |
| ---------------------------------------------------------------- | --------------------------------------------------------- |
| [`docs/requirements.md`](docs/requirements.md)                   | Requisitos funcionais, não funcionais e regras de negócio |
| [`docs/domain-model.md`](docs/domain-model.md)                   | Modelo de domínio e diagrama de classes                   |
| [`docs/database-model.md`](docs/database-model.md)               | Modelo Entidade-Relacionamento                            |
| [`docs/architecture.md`](docs/architecture.md)                   | Arquitetura do sistema e fluxo de dados                   |
| [`docs/adr-log.md`](docs/adr-log.md)                             | Decisões arquiteturais registradas                        |
| [`docs/folder-structure.md`](docs/folder-structure.md)           | Estrutura de pastas comentada                             |
| [`docs/engineering-standards.md`](docs/engineering-standards.md) | Testes, versionamento, deploy, segurança, observabilidade |
| [`docs/mvp-roadmap.md`](docs/mvp-roadmap.md)                     | Marcos de entrega e backlog futuro                        |

## Rodando localmente

```bash
cp .env.example .env   # preencha SECRET_KEY, credenciais IGDB (ver ADR004)
docker compose up --build
docker compose exec web python manage.py migrate
```

API disponível em `http://localhost:8000/api/`. Documentação interativa em `http://localhost:8000/api/docs/`.

## Testes

```bash
docker compose exec web pytest --cov=apps
```

## Licença

Projeto acadêmico/portfólio — sem licença comercial definida.
