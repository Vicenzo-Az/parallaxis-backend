"""
Entidades puras do bounded context `games` — sem import de Django.

A implementar (ver docs/domain-model.md e docs/database-model.md):
- Game: id, igdb_id, title, release_date, cover_url, critic_rating,
  community_rating, platforms, cached_at.
- Genre: id, name, igdb_genre_id.
- EntryStatus: enum WANT_TO_PLAY | PLAYING | COMPLETED | ABANDONED.
- LibraryEntry: id, user_id, game_id, status, score, review, rated_at,
  created_at — com o método update_rating(score, review) que aplica RN02,
  RN03, RN06, RN08, RN09 (ver docs/requirements.md). Este método é o lugar
  certo para essas regras, não o serializer nem a view.
"""
