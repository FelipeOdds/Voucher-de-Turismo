# Documento de Requisitos de Produto (PRD) - App de Controle Liberta Turismo (Otimizado para Reflex/Python)

**Autor:** Manus AI
**Data:** 17 de Novembro de 2025
**VersÃ£o:** 4.0 (Detalhado - Foco em Vibe Coding)
**Foco:** App de Controle (TripulaÃ§Ã£o) - Estrutura Modular por Item de Desenvolvimento

## 1. VISÃO GERAL E ARQUITETURA

### 1.1 Contexto e Objetivo
O App de Controle Ã© a ferramenta de validaÃ§Ã£o de vouchers de 24h, utilizada pela tripulaÃ§Ã£o da Liberta Turismo. O objetivo Ã© garantir o controle de lotaÃ§Ã£o, a validade dos vouchers e a rastreabilidade das operaÃ§Ãµes, com foco na **operaÃ§Ã£o offline**.

### 1.2 Stack TecnolÃ³gico
*   **Frontend/Backend:** Reflex (Python)
*   **Banco de Dados:** PostgreSQL (ou SQLite para desenvolvimento local)
*   **GestÃ£o de Estado:** `rx.State` (Estado do Reflex)
*   **PersistÃªncia Offline:** PWA/IndexedDB (para cache de vouchers e logs de validaÃ§Ã£o)

### 1.3 Estrutura de Dados (ReferÃªncia)
A estrutura de dados deve seguir o modelo definido na VersÃ£o 3.0 (Tabelas: `vouchers`, `embarcacoes`, `tripulantes`, `validacoes`, `logs_troca_embarcacao`).

## 2. REQUISITOS FUNCIONAIS (RF) - ORDEM DE DESENVOLVIMENTO

### FASE 0: Infraestrutura e Base de Dados (Backend)

#### RF00.1 - ConfiguraÃ§Ã£o de EmbarcaÃ§Ãµes
*   **Objetivo:** Permitir a gestÃ£o da frota e a configuraÃ§Ã£o da regra de negÃ³cio crÃ­tica (Gap de Embarque).
*   **Requisitos:**
    *   Endpoint para criaÃ§Ã£o/ediÃ§Ã£o de embarcaÃ§Ãµes.
    *   Campos obrigatÃ³rios: `nome`, `capacidade_maxima` (int), `gap_embarque_minutos` (int).
*   **CritÃ©rios de Aceite:**
    *   A API deve retornar o `gap_embarque_minutos` ao consultar uma embarcaÃ§Ã£o.

#### RF00.2 - GestÃ£o de Vouchers (CRUD BÃ¡sico)
*   **Objetivo:** Permitir a criaÃ§Ã£o manual de vouchers para testes e operaÃ§Ã£o inicial.
*   **Requisitos:**
    *   Endpoint para criaÃ§Ã£o de voucher com `nome_passageiro`, `cpf`, etc.
    *   O backend deve gerar o `qr_code_hash` e o `numero_voucher` Ãºnico.
*   **CritÃ©rios de Aceite:**
    *   Um voucher criado manualmente deve ser validado com sucesso pelo endpoint de validaÃ§Ã£o.

### FASE 1: Core - MÃ³dulos Essenciais (MVP MÃ­nimo)

#### RF01 - AutenticaÃ§Ã£o e Login
*   **Objetivo:** Permitir o acesso seguro e individualizado do tripulante.
*   **Requisitos:**
    *   Tela de Login com campos `email` e `senha`.
    *   Uso de `rx.State` para gerenciar o estado de login.
    *   Em caso de sucesso, armazenar o token de sessÃ£o (`rx.Cookie`).
*   **CritÃ©rios de Aceite:**
    *   **CA 1.1:** Login bem-sucedido redireciona para a tela de seleÃ§Ã£o de embarcaÃ§Ã£o.
    *   **CA 1.2:** Senha incorreta exibe `login_error_message` no `rx.State`.

#### RF02 - SeleÃ§Ã£o de EmbarcaÃ§Ã£o
*   **Objetivo:** Associar o tripulante Ã  embarcaÃ§Ã£o em que ele estÃ¡ operando.
*   **Requisitos:**
    *   ApÃ³s login, exibir lista de embarcaÃ§Ãµes ativas (consumindo RF00.1).
    *   Armazenar `current_vessel_id` e `current_vessel_name` no `rx.State`.
*   **CritÃ©rios de Aceite:**
    *   **CA 2.1:** A seleÃ§Ã£o da embarcaÃ§Ã£o carrega automaticamente o `max_capacity` e o `gap_embarque_minutos` para o `rx.State`.

#### RF03 - Scan de QR Code (Fluxo Principal)
*   **Objetivo:** Capturar o QR Code e iniciar o processo de validaÃ§Ã£o.
*   **Requisitos:**
    *   Componente de cÃ¢mera para leitura do QR Code.
    *   Extrair `voucher_id` e `hash` do QR Code.
    *   Chamar a funÃ§Ã£o de validaÃ§Ã£o (MÃ³dulo 1.4).
*   **CritÃ©rios de Aceite:**
    *   **CA 3.1:** O `qr_code_data` Ã© atualizado no `rx.State` apÃ³s a leitura.

#### RF04 - Busca Manual (Fallback)
*   **Objetivo:** Permitir a validaÃ§Ã£o caso o QR Code esteja ilegÃ­vel ou indisponÃ­vel.
*   **Requisitos:**
    *   Campo de busca por `NÃºmero do Voucher`, `CPF`, `RG` ou `Passaporte`.
    *   A busca deve retornar o passageiro e permitir a validaÃ§Ã£o.
*   **CritÃ©rios de Aceite:**
    *   **CA 4.1:** A busca manual aciona a mesma lÃ³gica de validaÃ§Ã£o do RF03.

### FASE 2: Operacional - MÃ³dulos CrÃ­ticos

#### RF05 - ValidaÃ§Ã£o de Voucher (Regras de NegÃ³cio Core)
*   **Objetivo:** Aplicar as regras de negÃ³cio bÃ¡sicas para determinar a validade do voucher.
*   **Requisitos:**
    *   Verificar se o voucher existe (RF00.2).
    *   Verificar se o voucher estÃ¡ `status == 'ativo'` e nÃ£o `cancelado`.
    *   Verificar se a data/hora atual estÃ¡ dentro das 24h de validade (contadas a partir da `data_primeira_validacao`).
*   **CritÃ©rios de Aceite:**
    *   **CA 5.1:** Se expirado, `validation_result.status` == 'error' e `feedback_message` contÃ©m a data/hora tÃ©cnica de expiraÃ§Ã£o.

#### RF06 - Regra de Gap de Embarque (LÃ³gica CrÃ­tica)
*   **Objetivo:** Diferenciar Embarque, Desembarque e Scan Duplicado.
*   **Requisitos:**
    *   A lÃ³gica deve ser implementada no `rx.State` para funcionar offline.
    *   Consultar o Ãºltimo registro de validaÃ§Ã£o do voucher na embarcaÃ§Ã£o atual.
    *   Comparar o tempo decorrido com o `current_vessel_gap_minutes` (RF02).
*   **CritÃ©rios de Aceite:**
    *   **CA 6.1 (Desembarque):** SE Ãºltimo registro foi EMBARQUE E tempo decorrido >= Gap, registrar `validacoes.tipo` = 'desembarque'.
    *   **CA 6.2 (Duplicado):** SE Ãºltimo registro foi EMBARQUE E tempo decorrido < Gap, registrar `validacoes.tipo` = 'ignorado' e exibir alerta.

#### RF07 - Modo Offline e SincronizaÃ§Ã£o (CRÃTICO)
*   **Objetivo:** Garantir a operaÃ§Ã£o contÃ­nua sem conexÃ£o e a integridade dos dados.
*   **Requisitos:**
    *   O app deve armazenar um cache local de vouchers vÃ¡lidos (via PWA/IndexedDB).
    *   Todas as validaÃ§Ãµes (RF06) devem ser salvas na `sync_queue` local se `is_offline` for True.
    *   Ao reconectar, o `rx.State` deve acionar a sincronizaÃ§Ã£o da `sync_queue` para o backend.
*   **CritÃ©rios de Aceite:**
    *   **CA 7.1:** O `ConnectionStatusIndicator` (UI) deve refletir o estado `is_offline` do `rx.State`.
    *   **CA 7.2:** ApÃ³s a sincronizaÃ§Ã£o, a `sync_queue` deve estar vazia e o `local_cache_status` atualizado.

#### RF08 - Troca de EmbarcaÃ§Ã£o com ConfirmaÃ§Ã£o de Senha
*   **Objetivo:** Permitir a troca de embarcaÃ§Ã£o com seguranÃ§a e rastreabilidade.
*   **Requisitos:**
    *   Modal de confirmaÃ§Ã£o que exige a `password_input` do tripulante.
    *   O backend deve validar a senha e registrar o log na tabela `logs_troca_embarcacao`.
    *   Em caso de sucesso, atualizar `current_vessel_id` no `rx.State`.
*   **CritÃ©rios de Aceite:**
    *   **CA 8.1:** Senha incorreta mantÃ©m o `current_vessel_id` inalterado.
    *   **CA 8.2:** Troca bem-sucedida registra um novo item na tabela `logs_troca_embarcacao`.

#### RF09 - Dashboard de LotaÃ§Ã£o e HistÃ³rico
*   **Objetivo:** Fornecer ao tripulante informaÃ§Ãµes operacionais em tempo real.
*   **Requisitos:**
    *   Exibir `current_occupancy` e `max_capacity` na tela principal.
    *   Exibir lista das Ãºltimas 50 validaÃ§Ãµes locais (`local_validation_history`).
*   **CritÃ©rios de Aceite:**
    *   **CA 9.1:** O `current_occupancy` Ã© atualizado imediatamente no `rx.State` apÃ³s cada embarque/desembarque.

## 3. REQUISITOS NÃO-FUNCIONAIS (RNF)

| RNF | DescriÃ§Ã£o | ImplicaÃ§Ã£o para Reflex |
| :--- | :--- | :--- |
| **Linguagem** | Python (Frontend e Backend) | Uso de classes `State` para gerenciar o estado da aplicaÃ§Ã£o e `rx.component` para a interface. |
| **Offline** | O app deve funcionar 100% offline. | **CRÃTICO:** Necessidade de implementar lÃ³gica de cache local (IndexedDB via JS/PWA) e sincronizaÃ§Ã£o bidirecional no *State* do Reflex. |
| **Performance** | Tempo de resposta do scan < 1 segundo. | O processamento do QR Code deve ser o mais leve possÃ­vel, idealmente com a lÃ³gica de validaÃ§Ã£o offline rodando localmente. |
| **SeguranÃ§a** | AutenticaÃ§Ã£o individual. | Uso de `rx.Cookie` ou sistema de sessÃ£o do Reflex para manter o estado de login. |

## 4. USER STORIES E CRITÃRIOS DE ACEITE (Reflex)

### US01 - Login e SeleÃ§Ã£o
*   **Como** tripulante, **quero** logar e selecionar minha embarcaÃ§Ã£o, **para** comeÃ§ar a trabalhar.
*   **CritÃ©rios de Aceite:**
    *   **CA 1.1:** O `rx.State.is_logged_in` muda para `True` apÃ³s o login.
    *   **CA 1.2:** O `rx.State.current_vessel_id` Ã© preenchido apÃ³s a seleÃ§Ã£o.

### US02 - Embarque Normal
*   **Como** tripulante, **quero** escanear o QR Code de um passageiro vÃ¡lido, **para** autorizar o embarque.
*   **CritÃ©rios de Aceite:**
    *   **CA 2.1:** O `rx.State.validation_result.status` Ã© 'success'.
    *   **CA 2.2:** O `rx.State.current_occupancy` Ã© incrementado em 1.
    *   **CA 2.3:** Um novo registro Ã© adicionado Ã  `validacoes` (tipo 'embarque').

### US03 - Desembarque (ApÃ³s Gap)
*   **Como** tripulante, **quero** escanear o QR Code de um passageiro jÃ¡ embarcado (apÃ³s o Gap), **para** registrar o desembarque.
*   **CritÃ©rios de Aceite:**
    *   **CA 3.1:** O `rx.State.validation_result.status` Ã© 'success'.
    *   **CA 3.2:** O `rx.State.current_occupancy` Ã© decrementado em 1.
    *   **CA 3.3:** Um novo registro Ã© adicionado Ã  `validacoes` (tipo 'desembarque').

### US04 - OperaÃ§Ã£o Offline
*   **Como** tripulante, **quero** validar vouchers sem internet, **para** nÃ£o interromper a operaÃ§Ã£o em alto mar.
*   **CritÃ©rios de Aceite:**
    *   **CA 4.1:** O `rx.State.is_offline` Ã© `True`.
    *   **CA 4.2:** O registro de validaÃ§Ã£o Ã© adicionado Ã  `rx.State.sync_queue` (lista de pendÃªncias).

### US05 - Troca Segura de EmbarcaÃ§Ã£o
*   **Como** tripulante, **quero** trocar de embarcaÃ§Ã£o, **para** cobrir um colega, confirmando com minha senha.
*   **CritÃ©rios de Aceite:**
    *   **CA 5.1:** A troca sÃ³ ocorre se a senha digitada for validada pelo backend.
    *   **CA 5.2:** O `rx.State.current_vessel_id` Ã© atualizado para o novo ID.
    *   **CA 5.3:** Um log Ã© registrado na tabela `logs_troca_embarcacao`.

## 5. UI/UX (ReferÃªncia)

Todos os requisitos de interface devem seguir a **EspecificaÃ§Ã£o UX/UI** (VersÃ£o 3.0) entregue anteriormente, incluindo:

*   **Tela Principal:** Dashboard com indicador de lotaÃ§Ã£o e status de conexÃ£o.
*   **Feedback Visual:** Uso de VERDE/VERMELHO/AMARELO para feedback imediato.
*   **Modal de ConfirmaÃ§Ã£o:** Uso do modal de senha para a Troca de EmbarcaÃ§Ã£o.
*   **Mensagens:** Uso de mensagens tÃ©cnicas (data/hora de expiraÃ§Ã£o).
