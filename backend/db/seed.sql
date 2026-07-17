-- ============================================================================
--  Mugiwara Store — Dados de Demonstração (seed)
--  Roda automaticamente após o init.sql na 1ª inicialização do container.
--
--  Senha de TODOS os usuários de demonstração: senha123
-- ============================================================================

-- ---------------------------------------------------------------------------
--  Endereços (CEP)
-- ---------------------------------------------------------------------------
INSERT INTO endereco_cep (cep, logradouro, bairro, cidade, estado) VALUES
    ('58800-000', 'Rua Coração de Jesus',     'Centro',   'Sousa',          'PB'),
    ('22220-000', 'Rua do Catete',            'Flamengo', 'Rio de Janeiro', 'RJ'),
    ('01310-100', 'Avenida Paulista',         'Bela Vista','São Paulo',     'SP'),
    ('50030-230', 'Avenida Rio Branco',       'Recife',   'Recife',         'PE')
ON CONFLICT (cep) DO NOTHING;

-- ---------------------------------------------------------------------------
--  Funcionários  (senha: senha123)
-- ---------------------------------------------------------------------------
INSERT INTO funcionario (nome, email, senha_hash, cargo) VALUES
    ('Nami',    'nami@mugiwara.com',    '$2b$12$5Mvfu76lWAsa6z256wd2EeSKle99mnoNZZKJf3PIStMsJalQTSR/q', 'Gerente de Vendas'),
    ('Franky',  'franky@mugiwara.com',  '$2b$12$5Mvfu76lWAsa6z256wd2EeSKle99mnoNZZKJf3PIStMsJalQTSR/q', 'Vendedor')
ON CONFLICT (email) DO NOTHING;

-- ---------------------------------------------------------------------------
--  Clientes  (senha: senha123)
--    Luffy  -> assiste_one_piece + natural_de_sousa  => elegível a desconto
--    Robin  -> torce_flamengo                        => elegível a desconto
--    Buggy  -> nenhum critério                        => sem desconto
-- ---------------------------------------------------------------------------
INSERT INTO cliente (nome, email, senha_hash, numero_endereco, complemento_endereco, cep,
                     torce_flamengo, assiste_one_piece, natural_de_sousa) VALUES
    ('Monkey D. Luffy', 'luffy@mugiwara.com', '$2b$12$/KyvhBUNgPeSWw3U4gRC/ebgPlN4iU5xi0auJMQXmTK87IkwGUI9S',
        '100', 'Casa', '58800-000', FALSE, TRUE,  TRUE),
    ('Nico Robin',      'robin@mugiwara.com', '$2b$12$/KyvhBUNgPeSWw3U4gRC/ebgPlN4iU5xi0auJMQXmTK87IkwGUI9S',
        '22',  'Apto 8', '22220-000', TRUE, FALSE, FALSE),
    ('Buggy',           'buggy@mugiwara.com', '$2b$12$/KyvhBUNgPeSWw3U4gRC/ebgPlN4iU5xi0auJMQXmTK87IkwGUI9S',
        '3',   NULL, '01310-100', FALSE, FALSE, FALSE)
ON CONFLICT (email) DO NOTHING;

-- Telefones (atributo multivalorado)
INSERT INTO cliente_telefone (id_cliente, telefone) VALUES
    (1, '(83) 99999-0001'),
    (1, '(83) 98888-0002'),
    (2, '(21) 97777-0003')
ON CONFLICT DO NOTHING;

-- ---------------------------------------------------------------------------
--  Produtos  (catálogo temático One Piece)
--  Alguns com estoque < 5 para demonstrar o alerta de estoque baixo (CV-08).
-- ---------------------------------------------------------------------------
INSERT INTO produto (nome, descricao, preco, quantidade_estoque, categoria, fabricado_em_mari, imagem) VALUES
    ('Action Figure Luffy Gear 5',
     'Figura de ação do Monkey D. Luffy na forma Gear 5 (Nika), 25cm, articulada, edição de colecionador.',
     349.90, 12, 'Action Figures', TRUE,
     'https://images.unsplash.com/photo-1608889175123-8ee362201f81?w=600&q=80'),

    ('Action Figure Roronoa Zoro',
     'Zoro em pose de três espadas (Santoryu), pintura detalhada e base temática.',
     299.90, 8, 'Action Figures', FALSE,
     'https://images.unsplash.com/photo-1601814933824-fd0b574dd592?w=600&q=80'),

    ('Réplica Chapéu de Palha do Luffy',
     'Réplica oficial do icônico chapéu de palha, tamanho adulto, palha trançada à mão.',
     159.90, 30, 'Vestuário', FALSE,
     'https://images.unsplash.com/photo-1521369909029-2afed882baee?w=600&q=80'),

    ('Pôster Wanted — Luffy 3 Bilhões',
     'Pôster do cartaz de procurado do Luffy com a recompensa atualizada, papel couché 250g, 60x90cm.',
     49.90, 50, 'Pôsteres', TRUE,
     'https://images.unsplash.com/photo-1579965342575-16428a7c8881?w=600&q=80'),

    ('Réplica Espada Wado Ichimonji',
     'Réplica da katana Wado Ichimonji do Zoro, lâmina de aço inox, suporte de madeira incluso.',
     599.90, 4, 'Réplicas', FALSE,
     'https://images.unsplash.com/photo-1595429035839-c99c298ffdde?w=600&q=80'),

    ('Den Den Mushi Colecionável',
     'Caracol-telefone Den Den Mushi em resina pintada à mão, 15cm. Peça de coleção.',
     129.90, 20, 'Colecionáveis', TRUE,
     'https://images.unsplash.com/photo-1611604548018-d56bbd85d681?w=600&q=80'),

    ('Action Figure Nami',
     'Figura da navegadora Nami com Clima-Tact, 22cm, articulada.',
     279.90, 10, 'Action Figures', FALSE,
     'https://images.unsplash.com/photo-1633613286991-611fe299c4be?w=600&q=80'),

    ('Action Figure Sanji',
     'Vinsmoke Sanji em pose de Diable Jambe, com efeito de chamas translúcido.',
     289.90, 3, 'Action Figures', FALSE,
     'https://images.unsplash.com/photo-1608889825205-eebdb9fc5806?w=600&q=80'),

    ('Moletom Jolly Roger dos Chapéus de Palha',
     'Moletom preto com a bandeira pirata dos Mugiwara estampada. Algodão premium.',
     189.90, 25, 'Vestuário', TRUE,
     'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600&q=80'),

    ('Pôster Thousand Sunny',
     'Arte do navio Thousand Sunny navegando na Grand Line, 60x90cm.',
     54.90, 40, 'Pôsteres', FALSE,
     'https://images.unsplash.com/photo-1502680390469-be75c86b636f?w=600&q=80'),

    ('Log Pose Réplica',
     'Bússola Log Pose funcional (decorativa), pulseira ajustável, resina e metal.',
     99.90, 2, 'Colecionáveis', FALSE,
     'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&q=80'),

    ('Action Figure Tony Tony Chopper',
     'Chopper na forma Brain Point, super fofo, 12cm, com chifres removíveis.',
     149.90, 18, 'Action Figures', TRUE,
     'https://images.unsplash.com/photo-1591035897819-f4bdf739f446?w=600&q=80'),

    ('Caneca ASCE — Portgas D. Ace',
     'Caneca de cerâmica 350ml com a tatuagem ASCE. Muda de cor com líquido quente.',
     44.90, 60, 'Colecionáveis', TRUE,
     'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=600&q=80'),

    ('Action Figure Portgas D. Ace',
     'Ace com poderes da Mera Mera no Mi, efeito de fogo, 24cm, base vulcânica.',
     319.90, 6, 'Action Figures', FALSE,
     'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=600&q=80'),

    ('Poneglifo Réplica de Colecionador',
     'Réplica de um Poneglifo com inscrições em pedra, edição numerada e limitada.',
     799.90, 1, 'Colecionáveis', TRUE,
     '/static/products/prod_15.jpg')
ON CONFLICT DO NOTHING;

-- Imagens reais correlacionadas a cada item, servidas pelo backend
-- (/static/products/prod_<id>.jpg). Cada produto recebe a imagem do seu id.
UPDATE produto SET imagem = '/static/products/prod_' || id_produto || '.jpg'
 WHERE imagem IS NULL OR imagem LIKE 'https://images.unsplash.com/%' OR imagem LIKE '%.svg';

-- ---------------------------------------------------------------------------
--  Pedidos de exemplo (para popular o histórico e os relatórios de vendas)
--  Inseridos diretamente para termos dados nos relatórios desde o início.
-- ---------------------------------------------------------------------------
INSERT INTO pedido (data_pedido, forma_pagamento, status_pagamento, valor_total, id_cliente, id_funcionario) VALUES
    (NOW() - INTERVAL '3 days',  'PIX',    'APROVADO', 584.82, 1, 1),  -- pedido 1 (Nami)
    (NOW() - INTERVAL '10 days', 'CARTAO', 'APROVADO', 269.91, 2, 1),  -- pedido 2 (Nami)
    (NOW() - INTERVAL '35 days', 'BOLETO', 'APROVADO', 349.90, 3, 2);  -- pedido 3 (Franky, mês anterior)

INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario_na_venda) VALUES
    (1, 1, 1, 349.90),
    (1, 3, 2, 159.90),
    (2, 4, 1, 49.90),
    (2, 6, 1, 129.90),
    (2, 12, 1, 149.90),
    (3, 1, 1, 349.90);

-- Ajusta a sequência do pedido para não colidir com os IDs inseridos manualmente
SELECT setval('pedido_id_pedido_seq', (SELECT MAX(id_pedido) FROM pedido));
