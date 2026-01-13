# shoop_bot_frontend
boot da shoop

🛡️ v14.0 - [Sentinel Edition: Inteligência Semântica & Busca em Cascata]
Status: Atual / Estável
Foco: Precisão de Busca e Evasão de Bloqueios.
🚀 O que mudou nesta versão?
Módulo de NLP (Processamento de Linguagem Natural): Integração com a inteligência spaCy. O robô agora "lê" o produto como um humano, separando o que é Marca, Modelo e Produto, ignorando palavras inúteis (promoção, oferta, original).
Mecanismo de Busca em Cascata: Implementação de 4 níveis de tentativa automática. Se o robô não encontra o item com o nome completo, ele simplifica a busca progressivamente até achar resultados válidos, eliminando o erro de "Nenhum Produto Encontrado".
Lematização de Dados: O bot converte automaticamente palavras (ex: "Fritadeiras") para o radical (ex: "Fritadeira"), garantindo que anúncios com nomes escritos de forma diferente sejam capturados.
Sentinel Stealth (CDP): Transição para conexão via Chrome DevTools Protocol. O robô agora opera "pendurado" em uma instância real do Chrome, tornando-se 100% indetectável pelos sistemas anti-bot da Shopee.
Aquecimento de Perfil (Warm-up): O robô agora simula navegação humana orgânica (rolagens e cliques na home) antes de acessar áreas críticas, aumentando a confiança da conta perante a plataforma.
🧠 Explicação para Leigos
"Nesta versão, o robô deixou de ser um simples buscador de textos e ganhou um cérebro que entende português. Se você procurar uma Air Fryer, ele sabe que 'Air Fryer' é o produto e 'Mondial' é a marca. Se ele não achar o modelo exato de primeira, ele 'abaixa o rigor' sozinho até encontrar a melhor oferta para você, sempre garantindo que não seja uma capinha ou acessório."