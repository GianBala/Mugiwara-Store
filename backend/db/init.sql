-- ============================================================================
--  Mugiwara Store — Esquema do Banco de Dados (PostgreSQL 16)
--  Modelagem relacional na 3FN. Cria tabelas, constraints, VIEW e PROCEDURE.
--
--  Convenção de nomes: tabelas e colunas em snake_case (padrão PostgreSQL).
--  Este script roda automaticamente na 1ª inicialização do container (initdb).
-- ============================================================================

-- ---------------------------------------------------------------------------
--  Tabela: endereco_cep  (dados de logradouro reaproveitáveis por CEP)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS endereco_cep (
    cep         VARCHAR(9)   PRIMARY KEY,
    logradouro  VARCHAR(255),
    bairro      VARCHAR(100),
    cidade      VARCHAR(100),
    estado      VARCHAR(2)
);

-- ---------------------------------------------------------------------------
--  Tabela: produto  (catálogo da loja)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS produto (
    id_produto          SERIAL        PRIMARY KEY,
    nome                VARCHAR(100)  NOT NULL,
    descricao           TEXT,
    preco               NUMERIC(10,2) NOT NULL CONSTRAINT ck_produto_preco_positivo CHECK (preco > 0),
    quantidade_estoque  INTEGER       NOT NULL DEFAULT 0 CONSTRAINT ck_produto_estoque_nao_negativo CHECK (quantidade_estoque >= 0),
    categoria           VARCHAR(50)   NOT NULL,
    fabricado_em_mari   BOOLEAN       NOT NULL DEFAULT FALSE,
    imagem              VARCHAR(255)
);

-- ---------------------------------------------------------------------------
--  Tabela: cliente
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente            SERIAL        PRIMARY KEY,
    nome                  VARCHAR(150)  NOT NULL,
    email                 VARCHAR(100)  NOT NULL UNIQUE,
    senha_hash            VARCHAR(255)  NOT NULL,
    numero_endereco       VARCHAR(20),
    complemento_endereco  VARCHAR(100),
    cep                   VARCHAR(9)    REFERENCES endereco_cep (cep),
    torce_flamengo        BOOLEAN       NOT NULL DEFAULT FALSE,
    assiste_one_piece     BOOLEAN       NOT NULL DEFAULT FALSE,
    natural_de_sousa      BOOLEAN       NOT NULL DEFAULT FALSE
);

-- ---------------------------------------------------------------------------
--  Tabela: cliente_telefone  (atributo multivalorado -> tabela própria, 3FN)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cliente_telefone (
    id_cliente  INTEGER      NOT NULL REFERENCES cliente (id_cliente) ON DELETE CASCADE,
    telefone    VARCHAR(20)  NOT NULL,
    PRIMARY KEY (id_cliente, telefone)
);

-- ---------------------------------------------------------------------------
--  Tabela: funcionario  (vendedores / gestores da loja)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS funcionario (
    id_funcionario  SERIAL        PRIMARY KEY,
    nome            VARCHAR(150)  NOT NULL,
    email           VARCHAR(100)  NOT NULL UNIQUE,
    senha_hash      VARCHAR(255)  NOT NULL,
    cargo           VARCHAR(50)   NOT NULL DEFAULT 'Vendedor'
);

-- ---------------------------------------------------------------------------
--  Tabela: pedido
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pedido (
    id_pedido        SERIAL                    PRIMARY KEY,
    data_pedido      TIMESTAMP WITH TIME ZONE  NOT NULL DEFAULT NOW(),
    forma_pagamento  VARCHAR(50)               NOT NULL,
    status_pagamento VARCHAR(50)               NOT NULL DEFAULT 'APROVADO',
    valor_total      NUMERIC(10,2)             NOT NULL CONSTRAINT ck_pedido_valor_nao_negativo CHECK (valor_total >= 0),
    id_cliente       INTEGER                   NOT NULL REFERENCES cliente (id_cliente),
    id_funcionario   INTEGER                   REFERENCES funcionario (id_funcionario)
);

-- ---------------------------------------------------------------------------
--  Tabela: item_pedido  (itens de cada pedido)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS item_pedido (
    id_pedido                INTEGER        NOT NULL REFERENCES pedido (id_pedido) ON DELETE CASCADE,
    id_produto               INTEGER        NOT NULL REFERENCES produto (id_produto),
    quantidade               INTEGER        NOT NULL CONSTRAINT ck_item_quantidade_positiva CHECK (quantidade > 0),
    preco_unitario_na_venda  NUMERIC(10,2)  NOT NULL CONSTRAINT ck_item_preco_positivo CHECK (preco_unitario_na_venda > 0),
    PRIMARY KEY (id_pedido, id_produto)
);

-- Índices auxiliares para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_produto_categoria    ON produto (categoria);
CREATE INDEX IF NOT EXISTS idx_pedido_cliente       ON pedido (id_cliente);
CREATE INDEX IF NOT EXISTS idx_pedido_funcionario   ON pedido (id_funcionario);
CREATE INDEX IF NOT EXISTS idx_pedido_data          ON pedido (data_pedido);


-- ============================================================================
--  VIEW: vw_vendas_por_vendedor
--  Consolida PEDIDO + FUNCIONARIO + ITEM_PEDIDO + PRODUTO para relatórios
--  de vendas por vendedor (usada no Painel do Funcionário / Relatório Mensal).
-- ============================================================================
CREATE OR REPLACE VIEW vw_vendas_por_vendedor AS
SELECT
    f.id_funcionario,
    f.nome                                   AS nome_vendedor,
    f.cargo,
    p.id_pedido,
    p.data_pedido,
    DATE_TRUNC('month', p.data_pedido)::date AS mes_referencia,
    ip.id_produto,
    prod.nome                                AS nome_produto,
    ip.quantidade,
    ip.preco_unitario_na_venda,
    (ip.quantidade * ip.preco_unitario_na_venda) AS subtotal_item,
    p.valor_total                            AS valor_total_pedido
FROM pedido p
JOIN funcionario f  ON f.id_funcionario = p.id_funcionario
JOIN item_pedido ip ON ip.id_pedido     = p.id_pedido
JOIN produto prod   ON prod.id_produto  = ip.id_produto;


-- ============================================================================
--  PROCEDURE: criar_pedido_completo
--  Transação atômica que:
--    1. Valida existência do cliente;
--    2. Percorre os itens (JSONB), validando estoque de cada produto;
--    3. Calcula o subtotal e aplica o desconto conforme perfil do cliente;
--    4. Insere o pedido e seus itens;
--    5. Baixa o estoque dos produtos.
--  Em caso de qualquer violação, a transação inteira é revertida (ROLLBACK
--  implícito ao lançar EXCEPTION).
--
--  Parâmetros:
--    p_id_cliente      -> cliente que realiza a compra
--    p_id_funcionario  -> vendedor responsável (pode ser NULL em autoatendimento)
--    p_forma_pagamento -> ex.: 'PIX', 'CARTAO', 'BOLETO'
--    p_itens           -> JSONB no formato [{"id_produto": 1, "quantidade": 2}, ...]
--    p_perc_desconto   -> percentual (0..1) a aplicar caso o cliente seja elegível
--    p_id_pedido       -> (INOUT) devolve o id do pedido criado
-- ============================================================================
CREATE OR REPLACE PROCEDURE criar_pedido_completo(
    IN    p_id_cliente      INTEGER,
    IN    p_id_funcionario  INTEGER,
    IN    p_forma_pagamento VARCHAR,
    IN    p_itens           JSONB,
    IN    p_perc_desconto   NUMERIC,
    INOUT p_id_pedido       INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_item            JSONB;
    v_id_produto      INTEGER;
    v_quantidade      INTEGER;
    v_preco           NUMERIC(10,2);
    v_estoque         INTEGER;
    v_subtotal        NUMERIC(12,2) := 0;
    v_elegivel        BOOLEAN;
    v_valor_final     NUMERIC(12,2);
BEGIN
    -- 1. Cliente precisa existir (integridade referencial explícita)
    PERFORM 1 FROM cliente WHERE id_cliente = p_id_cliente;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Cliente % inexistente', p_id_cliente
            USING ERRCODE = 'foreign_key_violation';
    END IF;

    -- 2. Valida estoque e acumula o subtotal
    FOR v_item IN SELECT * FROM jsonb_array_elements(p_itens)
    LOOP
        v_id_produto := (v_item ->> 'id_produto')::INTEGER;
        v_quantidade := (v_item ->> 'quantidade')::INTEGER;

        IF v_quantidade IS NULL OR v_quantidade <= 0 THEN
            RAISE EXCEPTION 'Quantidade inválida para o produto %', v_id_produto;
        END IF;

        SELECT preco, quantidade_estoque
          INTO v_preco, v_estoque
          FROM produto
         WHERE id_produto = v_id_produto
           FOR UPDATE;               -- trava a linha até o fim da transação

        IF NOT FOUND THEN
            RAISE EXCEPTION 'Produto % inexistente', v_id_produto
                USING ERRCODE = 'foreign_key_violation';
        END IF;

        IF v_estoque < v_quantidade THEN
            RAISE EXCEPTION 'Estoque insuficiente para o produto % (disponível: %, solicitado: %)',
                v_id_produto, v_estoque, v_quantidade
                USING ERRCODE = 'check_violation';
        END IF;

        v_subtotal := v_subtotal + (v_preco * v_quantidade);
    END LOOP;

    -- 3. Desconto: aplica-se se o cliente atende a pelo menos um dos critérios
    SELECT (torce_flamengo OR assiste_one_piece OR natural_de_sousa)
      INTO v_elegivel
      FROM cliente
     WHERE id_cliente = p_id_cliente;

    v_valor_final := v_subtotal;
    IF v_elegivel THEN
        v_valor_final := v_subtotal * (1 - COALESCE(p_perc_desconto, 0));
    END IF;

    -- 4. Cria o pedido
    INSERT INTO pedido (forma_pagamento, status_pagamento, valor_total, id_cliente, id_funcionario)
    VALUES (p_forma_pagamento, 'APROVADO', v_valor_final, p_id_cliente, p_id_funcionario)
    RETURNING id_pedido INTO p_id_pedido;

    -- 5. Insere itens e baixa o estoque
    FOR v_item IN SELECT * FROM jsonb_array_elements(p_itens)
    LOOP
        v_id_produto := (v_item ->> 'id_produto')::INTEGER;
        v_quantidade := (v_item ->> 'quantidade')::INTEGER;

        SELECT preco INTO v_preco FROM produto WHERE id_produto = v_id_produto;

        INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario_na_venda)
        VALUES (p_id_pedido, v_id_produto, v_quantidade, v_preco);

        UPDATE produto
           SET quantidade_estoque = quantidade_estoque - v_quantidade
         WHERE id_produto = v_id_produto;
    END LOOP;
END;
$$;
