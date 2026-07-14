"""
Views da API do bounded context `games` — RF06-RF19.

A implementar:
- GameSearchView (GET /api/games/search/)
- LibraryEntryViewSet (CRUD /api/library-entries/) — RF08-RF14
- TasteAnalysisView (GET /api/analysis/taste/) — RF15-RF17
- RecommendationView (GET /api/analysis/recommendations/) — RF18
- DashboardView (GET /api/dashboard/) — RF19

Lembrete: toda view aqui é magra — recebe request, chama um use case,
serializa o resultado. Nenhuma regra de negócio deve viver neste arquivo.
"""
