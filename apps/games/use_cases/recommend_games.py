"""
RecommendationService — RF18.

A implementar:
- Pré-condição RN04: exige pelo menos 5 jogos avaliados com nota. Abaixo
  disso, retorna um resultado explícito de "dados insuficientes", não uma
  lista vazia silenciosa.
- Mesmo acima do mínimo, o resultado deve incluir um aviso de que a
  qualidade da recomendação melhora com mais avaliações (RN04).
- Algoritmo: similaridade de atributos (gênero, tema) com os jogos mais bem
  avaliados pelo usuário — content-based, sem dependência de outros
  usuários (não temos base de usuários para colaborativo).
"""
