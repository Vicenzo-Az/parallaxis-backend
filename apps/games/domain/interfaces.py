"""
Interfaces (ports) do bounded context `games` — ADR004.

A implementar:

    from abc import ABC, abstractmethod

    class GameDataProvider(ABC):
        @abstractmethod
        def search_games(self, query: str) -> list[...]: ...

        @abstractmethod
        def get_game_details(self, external_id: str) -> ...: ...

Regra de ouro: use_cases/ conhece só esta interface. A implementação real
(IGDBGameProvider) mora em infra/providers/igdb_provider.py e nunca é
importada diretamente por um use case — só injetada.
"""
