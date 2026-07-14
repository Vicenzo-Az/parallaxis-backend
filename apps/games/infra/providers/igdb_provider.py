"""
IGDBGameProvider — implementa GameDataProvider (domain/interfaces.py).

A implementar:
1. Autenticação client-credentials: POST para id.twitch.tv/oauth2/token
   com IGDB_CLIENT_ID/IGDB_CLIENT_SECRET (settings), guardando o token e sua
   expiração (em cache ou variável de instância) para evitar autenticar a
   cada requisição.
2. Consultas à API via linguagem Apicalypse (POST para api.igdb.com/v4/games
   com corpo tipo `fields name,genres.name,...; where ...;`).
3. Antes de consultar a IGDB, sempre checar o cache (cache.py) — só bater na
   API em cache miss.
4. Mapear a resposta da IGDB para as entidades de domain/entities.py — o
   restante da aplicação nunca deve ver o formato bruto da resposta da IGDB.

Lembrete (ADR004): esta é a ÚNICA classe do projeto que sabe que a IGDB
existe. Se um dia adicionarmos Steam/RAWG, a mudança fica isolada aqui.
"""
