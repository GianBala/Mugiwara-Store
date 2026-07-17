# Relatório do Projeto — Mugiwara Store

**Disciplina:** Tópicos Avançados em Ciência da Computação XI (Programação com Agentes)
**Atividade:** 04 — Implementação da Aplicação CRUD
**Grupo:** Deivily Breno Silva Carneiro · Deivison da Silva Costa · Giancarlo Silveira Cavalcante
**Data:** Julho de 2026

---

## 1. Introdução

Este relatório descreve a implementação da **Mugiwara Store**, o e-commerce temático de
*One Piece* planejado na Atividade 03. O foco do texto, conforme solicitado, não é apenas o
produto final, mas principalmente **o processo de desenvolvimento assistido por agentes de IA**,
a **experiência do grupo** durante a construção e **como o plano de testes se comportou na prática**.

A aplicação foi entregue como uma stack full-stack conteinerizada (Vue 3 + FastAPI + PostgreSQL 16),
com todas as funcionalidades planejadas implementadas e validadas, e sobe com um único comando
(`docker compose up -d --build`).

---

## 2. O processo de desenvolvimento com agentes

### 2.1. Abordagem geral

Adotamos um fluxo de **desenvolvimento dirigido por especificação**: em vez de escrever código
linha a linha, o grupo atuou como *arquiteto e revisor*, enquanto o agente atuou como *implementador*.
O documento da Atividade 03 (descrição do domínio, esquema de dados na 3FN, critérios de validação
CV-01 a CV-08 e de aceitação CA-01 a CA-07) funcionou como o **contrato** que guiou o agente. Ter
uma especificação madura foi determinante: quanto mais preciso o planejamento anterior, menos
ambíguas foram as decisões que o agente precisou tomar sozinho.

### 2.2. Fluxo de trabalho em camadas

O agente foi orientado a construir o sistema **de baixo para cima**, respeitando a arquitetura
planejada, o que tornou cada etapa verificável antes de prosseguir:

1. **Infraestrutura** — estrutura de pastas, `docker-compose.yml`, variáveis de ambiente.
2. **Banco de dados** — `init.sql` com as 7 entidades, constraints (`CHECK`, `UNIQUE`, `FK`),
   a `VIEW` de vendas e a `PROCEDURE` transacional; `seed.sql` com dados temáticos.
3. **Backend em camadas** — *core* (config, segurança, sessão), *models* (SQLAlchemy 2.0),
   *schemas* (Pydantic v2), *repositories*, *services* e *routers*.
4. **Testes automatizados** — antes de considerar o backend pronto.
5. **Frontend** — design system em Tailwind e as telas em Vue.
6. **Orquestração e validação** — build das imagens e verificação ponta a ponta.

Essa ordenação permitiu que o agente **rodasse os testes assim que o backend ficou pronto** e
só avançasse para o frontend com a lógica de negócio já comprovadamente correta.

### 2.3. Principais decisões técnicas tomadas em conjunto

Algumas decisões relevantes surgiram durante a implementação e foram deliberadas entre o grupo
e o agente:

- **Lógica de pedido em Python *e* stored procedure.** A Atividade 03 previa a procedure
  `criar_pedido_completo`. Mantivemos a procedure no PostgreSQL (requisito de banco) **e** replicamos
  a mesma lógica transacional na camada de serviço (`PedidoService`). Isso trouxe dois benefícios:
  a API fica testável em qualquer banco (inclusive SQLite nos testes) e a regra de negócio fica
  explícita no código. Ambas as implementações foram validadas de forma independente.
- **SQLAlchemy síncrono + `TestClient`.** Embora o plano citasse `httpx`/`pytest-asyncio`, optamos
  pelo modo síncrono do FastAPI com o `TestClient` (que é construído sobre o `httpx`). A troca
  reduziu drasticamente a complexidade dos testes sem perda de cobertura.
- **Autenticação unificada para dois perfis.** Como o critério CV-06 exige e-mail único entre
  clientes *e* funcionários, o endpoint de login busca nas duas tabelas e emite um JWT contendo o
  `role`, resolvido depois por *dependencies* (`requer_funcionario` / `requer_cliente`) que produzem
  os códigos HTTP 401/403 exigidos por CV-04.
- **Consulta de CEP tolerante a falhas.** A integração com o ViaCEP foi encapsulada com
  *fallback*: se o serviço estiver indisponível, o cadastro do cliente ainda é concluído.

### 2.4. Desafios enfrentados

O desenvolvimento assistido não foi isento de fricção. Os ajustes mais ilustrativos foram:

| Problema | Causa | Correção |
|---|---|---|
| `AssertionError: Status code 204 must not have a response body` | A rota `DELETE` tinha anotação de retorno `-> None`, que fez o FastAPI gerar um *response model* incompatível com o 204. | Remoção da anotação de retorno na rota de exclusão. |
| `error TS6310: Referenced project may not disable emit` | O `tsconfig.node.json` referenciado como projeto composto não podia usar `noEmit`. | Simplificação para `vue-tsc --noEmit` e remoção da referência de projeto. |

Ambos foram detectados **automaticamente ao rodar os testes e o build** — ou seja, o próprio
ciclo de verificação apontou os erros, que foram corrigidos e revalidados na sequência. Esse é,
na prática, o maior valor do fluxo com agentes: o *loop* "gerar → executar → observar erro →
corrigir" é curtíssimo.

---

## 3. A experiência do grupo

### 3.1. O que funcionou bem

- **Velocidade com consistência.** Um sistema com ~60 arquivos (backend em 5 camadas, frontend
  com 20+ componentes/telas, banco, Docker e testes) foi construído e validado em uma única sessão
  de trabalho, mantendo padrões de nomenclatura, tratamento de erros e estilo coesos em todo o código.
- **Aderência à especificação.** Por termos investido na Atividade 03, o agente conseguiu mapear
  cada critério (CV/CA) a um trecho concreto de código e a um teste, reduzindo retrabalho.
- **Qualidade do design.** A instrução de "design bonito e profissional" foi traduzida em um
  *design system* temático coerente (paleta *oceano/tesouro/coral*, tipografia *display*, componentes
  reutilizáveis), algo que costuma consumir bastante tempo manualmente.

### 3.2. Limitações percebidas

- **O agente é tão bom quanto a especificação.** Onde o planejamento era vago (por exemplo, o
  percentual exato de desconto), o agente precisou adotar uma premissa — que documentamos (10%).
  Cabe ao grupo revisar essas premissas.
- **Necessidade de revisão humana.** Decisões arquiteturais (procedure vs. serviço, síncrono vs.
  assíncrono) exigiram julgamento do grupo. O agente propõe caminhos, mas a responsabilidade técnica
  permanece com os desenvolvedores.
- **Detalhes de ambiente.** Pequenos atritos de plataforma (Windows/Docker Desktop, versões de
  bibliotecas) ainda demandam atenção humana.

### 3.3. Aprendizados

O principal aprendizado é que **o papel do desenvolvedor se desloca da digitação para a curadoria**:
especificar com clareza, revisar criticamente as decisões e, sobretudo, **exigir verificação**.
Um agente que "diz" que o código funciona vale pouco; um agente que **roda os testes, sobe os
containers e mostra as telas funcionando** é o que dá confiança real na entrega.

---

## 4. O plano de testes na prática

O plano previsto na Atividade 03 combinava três frentes: testes automatizados, testes de banco e
homologação manual. Todas foram exercitadas.

### 4.1. Testes automatizados (pytest)

Foram implementados **24 testes** que sobem uma instância isolada da API contra um banco SQLite em
memória (via `TestClient`), sem depender de servidor externo. Resultado da execução:

```
======================= 24 passed, 23 warnings in 8.75s =======================
```

A cobertura mapeia diretamente os critérios de validação:

| Critério | O que é testado | Arquivo |
|---|---|---|
| CV-01 | CRUD de produto + rejeição sem nome/categoria | `test_produtos.py` |
| CV-02 | Preço zero ou negativo é rejeitado (HTTP 422) | `test_produtos.py` |
| CV-03 | Compra acima do estoque é rejeitada | `test_pedidos.py` |
| CV-04 | Rotas protegidas: 401 sem token, 403 sem permissão | `test_produtos.py`, `test_auth.py` |
| CV-05 | Pedido com produto inexistente é rejeitado (404) | `test_pedidos.py` |
| CV-06 | E-mail duplicado (cliente e funcionário) é rejeitado (409) | `test_auth.py` |
| CV-07 | Desconto aplicado a clientes elegíveis (10%) | `test_descontos_relatorios.py` |
| CV-08 | Estoque baixo lista apenas produtos com `< 5` un. | `test_descontos_relatorios.py` |
| CA-01 a CA-06 | Navegação pública, cadastro, perfil, compra e relatório mensal | vários |

### 4.2. Testes de banco de dados

As constraints e os objetos de banco foram verificados diretamente no PostgreSQL em execução:

- **PROCEDURE `criar_pedido_completo`** — chamada via `CALL` com um cliente elegível gerou o
  pedido corretamente e aplicou o desconto: `2 × R$ 299,90 = R$ 599,80 → R$ 539,82` (−10%),
  além de baixar o estoque atomicamente.
- **VIEW `vw_vendas_por_vendedor`** — consultada com `GROUP BY`, consolidou as vendas por
  vendedor de forma consistente com os relatórios exibidos na interface.
- **Constraints** (`CHECK preco > 0`, `UNIQUE email`, `FK`) — presentes no schema e reforçadas
  pela validação Pydantic na borda da API.

### 4.3. Homologação manual (critérios de aceitação)

Cada integrante percorreu um roteiro de uso completo no navegador, validando os critérios CA-01
a CA-07. As verificações ponta a ponta contra a stack real (Docker) confirmaram:

- Catálogo público com busca e filtros (CA-01);
- Cadastro de cliente com endereço via CEP e login para os dois perfis (CA-02, CA-03);
- Compra completa com forma de pagamento e registro no histórico (CA-04);
- Cadastro de produto com imagem por **upload local** e por **URL** (CA-05);
- Relatório mensal com ranking de vendedores e totais corretos (CA-06);
- Layout responsivo e sem quebras em navegadores modernos (CA-07).

### 4.4. Tabela-resumo de rastreabilidade

| Critério | Método de teste | Status |
|---|---|:---:|
| CV-01 a CV-08 | Testes automatizados (pytest) | ✅ |
| Objetos de banco (VIEW, PROCEDURE, constraints) | Consulta direta (psql) | ✅ |
| CA-01 | Navegação manual no navegador | ✅ |
| CA-02 a CA-04 | Roteiro de homologação | ✅ |
| CA-05 | Upload manual + verificação no backend | ✅ |
| CA-06 | Acesso ao relatório + conferência manual | ✅ |
| CA-07 | Teste em navegadores desktop | ✅ |

### 4.5. Observação sobre o plano

Na prática, a fronteira entre "teste automatizado" e "regra de negócio" ficou mais nítida do que o
previsto: escrever os testes **antes de dar o backend por concluído** transformou os critérios CV em
uma *checklist executável*. Vários ajustes finos (por exemplo, o arredondamento do desconto em
`Decimal` e a semântica dos códigos 401 vs. 403) só ficaram evidentes porque havia um teste
correspondente falhando. O plano de testes deixou de ser um documento e passou a ser parte ativa
do ciclo de desenvolvimento.

---

## 5. Conclusão

A Mugiwara Store cumpriu integralmente o escopo planejado na Atividade 03: CRUD completo, controle
de estoque, autenticação por perfis, política de descontos, histórico de pedidos e relatórios
gerenciais, tudo conteinerizado e testado. Mais importante que o produto, porém, foi a comprovação
de que o desenvolvimento com agentes é **eficaz quando ancorado em três pilares**: uma especificação
clara, decisões arquiteturais revisadas por humanos e, acima de tudo, **verificação constante e
observável** — testes que rodam, containers que sobem e telas que funcionam. Foi essa disciplina de
verificação que converteu a velocidade do agente em confiança na entrega.
