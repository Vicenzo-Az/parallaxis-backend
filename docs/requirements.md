# Parallaxis — Requisitos do Produto (MVP)

## 1. Contexto e Persona

**Persona única (auto-referida):** desenvolvedor(a) que joga com frequência, já tem o hábito de avaliar jogos de 1 a 10 mentalmente ou em listas soltas, tem interesse particular por jogos indie e fora do mainstream, e quer transformar esse hábito em histórico estruturado com análise de padrões — sem depender de rede social ou de dados de terceiros para gerar o insight.

**Problema central:** hoje as avaliações existem, mas não geram conhecimento de volta. Não há visibilidade estruturada sobre o próprio padrão de gosto (gêneros preferidos, divergência do consenso público, evolução ao longo do tempo).

**Fora de escopo do MVP:** filmes, séries, animes, música (entram em versões futuras); recursos sociais (seguir usuários, feed, comentários); recomendação colaborativa (baseada em outros usuários).

---

## 2. Requisitos Funcionais (RF)

### Autenticação e conta

- **RF01** — O usuário deve poder se cadastrar com e-mail e senha.
- **RF02** — O usuário deve poder fazer login e receber um token JWT de acesso.
- **RF03** — O usuário deve poder renovar sua sessão via refresh token, sem precisar logar novamente.
- **RF04** — O usuário deve poder editar dados básicos do próprio perfil (nome, e-mail).
- **RF05** — O usuário deve poder alterar a própria senha.

### Catálogo de jogos (integração IGDB)

- **RF06** — O usuário deve poder buscar jogos por nome, com resultados vindos da IGDB (nome, capa, gênero, ano de lançamento, plataformas, nota crítica agregada, quando disponível).
- **RF07** — O sistema deve armazenar em cache local os metadados de jogos já consultados, para reduzir dependência de disponibilidade da IGDB e melhorar tempo de resposta.

### Biblioteca pessoal e avaliações

- **RF08** — O usuário deve poder adicionar um jogo à sua biblioteca pessoal.
- **RF09** — O usuário deve poder atribuir uma nota de 1 a 10 (inteira) a um jogo da sua biblioteca.
- **RF10** — O usuário deve poder escrever uma review textual opcional para o jogo avaliado.
- **RF11** — O usuário deve poder marcar o status do jogo: _quero jogar_, _jogando_, _concluído_, _abandonado_.
- **RF12** — O usuário deve poder editar ou remover uma avaliação já registrada.
- **RF13** — O usuário deve poder listar sua biblioteca com filtros por gênero, status, plataforma e faixa de nota.
- **RF14** — Um mesmo jogo não pode ser adicionado duas vezes à biblioteca do mesmo usuário (ver RN01).

### Análise de gosto

- **RF15** — O sistema deve exibir a distribuição das notas do usuário por gênero.
- **RF16** — O sistema deve exibir a evolução das notas médias do usuário ao longo do tempo (por trimestre/ano de avaliação, não de lançamento do jogo).
- **RF17** — O sistema deve calcular e exibir a divergência entre a nota do usuário e a nota crítica agregada do jogo (quando disponível via IGDB), destacando os maiores desvios.
- **RF18** — O sistema deve recomendar jogos ainda não avaliados pelo usuário, com base em similaridade de atributos (gênero, tema) com os jogos mais bem avaliados por ele (ver RN04 sobre pré-condição).

### Dashboard

- **RF19** — O usuário deve visualizar um painel consolidado ao logar, com resumo da biblioteca (total de jogos, nota média, gênero predominante) e acesso rápido às análises.

---

## 3. Requisitos Não Funcionais (RNF)

| ID     | Requisito                                                                                                                                                                                                                                   |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF01  | Tempo de resposta da busca de jogos deve ser < 1s quando o dado estiver em cache, e < 3s em cache miss (dependente da IGDB).                                                                                                                |
| RNF02  | Senhas devem ser armazenadas com hash (bcrypt/argon2, via padrão do Django), nunca em texto plano.                                                                                                                                          |
| RNF03  | Tokens JWT de acesso devem expirar em no máximo 15 minutos; refresh token em até 7 dias.                                                                                                                                                    |
| RNF04  | Toda comunicação entre frontend e backend deve ocorrer via HTTPS em produção.                                                                                                                                                               |
| RNF05  | Metadados de jogos vindos da IGDB devem ser cacheados com TTL de 7 dias (dado que mudam raramente).                                                                                                                                         |
| RNF06  | O sistema deve funcionar de forma degradada (biblioteca e análises continuam acessíveis) mesmo se a IGDB estiver indisponível — apenas busca de novos jogos é afetada.                                                                      |
| RNF07a | **Backend** — cobertura de testes automatizados de no mínimo 80% na camada `use_cases/` (regras de negócio isoladas do framework); endpoints críticos (auth, avaliação) com teste de integração via API.                                    |
| RNF07b | **Frontend** — cobertura definida por criticidade de fluxo, não por percentual: testes obrigatórios para login/cadastro, fluxo de avaliação de jogo e exibição do dashboard de análise. Não é meta perseguir % de cobertura total do front. |
| RNF08  | A interface deve ser responsiva (mobile e desktop) e seguir diretrizes básicas de acessibilidade (contraste mínimo WCAG AA, navegação por teclado nos formulários principais).                                                              |
| RNF09  | Logs estruturados devem registrar erros de integração com IGDB e falhas de autenticação, sem registrar dados sensíveis (senha, token).                                                                                                      |
| RNF10  | O sistema deve suportar múltiplos usuários com isolamento total de dados (usuário A nunca acessa biblioteca de usuário B).                                                                                                                  |

---

## 4. Regras de Negócio (RN)

- **RN01** — Um jogo (identificado pelo ID externo da IGDB) só pode aparecer uma vez na biblioteca de um mesmo usuário. Tentativa de duplicar deve atualizar o registro existente, não criar um novo.
- **RN02** — A nota é um número inteiro de 1 a 10. Não há suporte a casas decimais nem a "sem nota" para um jogo com status _concluído_ (nota é obrigatória apenas quando o status é _concluído_ ou _abandonado_; jogos em _quero jogar_/_jogando_ podem não ter nota ainda).
- **RN03** — A data de avaliação registrada é a data em que o usuário salvou a nota, não a data de lançamento do jogo — isso é o que permite a análise de evolução temporal do gosto (RF16).
- **RN04** — O motor de recomendação (RF18) só é ativado após o usuário ter pelo menos 5 jogos avaliados com nota — abaixo disso, não há dado suficiente para inferir padrão, e o sistema deve comunicar isso ao usuário em vez de mostrar recomendação vazia ou aleatória. Mesmo acima do mínimo, o sistema deve exibir um aviso informando que a qualidade das recomendações melhora progressivamente conforme mais jogos são avaliados — gerenciando a expectativa do usuário sobre a precisão do resultado.
- **RN05** — O cálculo de divergência do mainstream (RF17) só se aplica a jogos que tenham nota crítica agregada disponível na IGDB; jogos sem essa informação são excluídos desse cálculo específico, mas continuam aparecendo normalmente na biblioteca.
- **RN06** — Edição de review e nota não tem limite de quantidade de vezes, mas cada edição atualiza a data de avaliação (RN03), refletindo na análise temporal.
- **RN07** — Ao excluir a conta, todos os dados pessoais associados ao usuário (incluindo todos os registros de `LibraryEntry`) são permanentemente removidos via cascade delete, em conformidade com o direito de eliminação de dados previsto na LGPD. Os registros de `Game` (cache compartilhado da IGDB) não são afetados, pois não constituem dado pessoal do usuário.
- **RN08** — A review textual (RF10) tem limite máximo de 8000 caracteres, referência equivalente ao limite adotado pela Steam para reviews de usuários.
- **RN09** — A nota do usuário (`score`, escala 1-10) e as notas da IGDB (`critic_rating`/`community_rating`, escala 0-100) estão em escalas diferentes por design — cada uma fiel à sua origem (input humano vs. dado bruto de API externa). Para o cálculo de divergência (RF17), a nota do usuário deve ser normalizada para a escala de 100 (`score * 10`) antes da comparação — nunca o inverso, para preservar a granularidade da escala maior.
