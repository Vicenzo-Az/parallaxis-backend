"""
TasteAnalysisService — RF15, RF16, RF17.

A implementar:
- genre_distribution(user_id): agrupa notas por gênero.
- temporal_evolution(user_id): média de notas por período, usando rated_at
  (RN03) — não a data de lançamento do jogo.
- mainstream_divergence(user_id): compara score do usuário com
  critic_rating/community_rating, aplicando a normalização de escala
  obrigatória de RN09 (score * 10, nunca o inverso) antes de comparar.
  Jogos sem rating externo disponível são excluídos deste cálculo (RN05).

Serviço stateless — sem tabela própria (ver ADR007). Calculado sob demanda.
"""
