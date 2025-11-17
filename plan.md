# Plano de Desenvolvimento - App de Controle Liberta Turismo

## Visão Geral
Desenvolvimento do App de Controle para tripulação validar vouchers de 24h, com foco em operação offline-first e controle de lotação.

**Stack:** Reflex (Python), PostgreSQL
**Cores:** Azul escuro (#2C5282) como primária, Verde para sucesso, Vermelho para erros, Amarelo para alertas

---

## Fase 1: Infraestrutura e Autenticação
**Objetivo:** Estabelecer a base de dados e sistema de login

- [ ] Criar schema do banco de dados (vouchers, embarcacoes, tripulantes, validacoes, logs_troca_embarcacao)
- [ ] Implementar sistema de autenticação (login/logout)
- [ ] Criar tela de login com email e senha
- [ ] Implementar gestão de sessão com rx.State
- [ ] Criar CRUD básico de embarcações (capacidade_maxima, gap_embarque_minutos)
- [ ] Criar CRUD básico de vouchers para testes

---

## Fase 2: Seleção de Embarcação e Dashboard
**Objetivo:** Permitir seleção de embarcação e visualizar status operacional

- [ ] Criar tela de seleção de embarcação pós-login
- [ ] Armazenar embarcação atual no estado (current_vessel_id, max_capacity, gap_embarque_minutos)
- [ ] Implementar dashboard principal com indicadores de lotação
- [ ] Criar componente de status de conexão (Online/Offline badge)
- [ ] Exibir histórico das últimas 50 validações locais
- [ ] Implementar barra de progresso de lotação (atual/máxima)

---

## Fase 3: Validação Core (Scan e Busca)
**Objetivo:** Implementar validação básica de vouchers

- [ ] Criar interface de scan de QR Code (captura e leitura)
- [ ] Implementar busca manual por número de voucher/CPF/RG/Passaporte
- [ ] Criar lógica de validação básica (status ativo, não expirado, dentro das 24h)
- [ ] Implementar regra de Gap de Embarque (embarque/desembarque/duplicado)
- [ ] Criar modals de feedback visual (Verde/Vermelho/Amarelo fullscreen)
- [ ] Atualizar contador de ocupação em tempo real

---

## Fase 4: Modo Offline e Sincronização
**Objetivo:** Garantir operação sem conexão e integridade de dados

- [ ] Implementar cache local de vouchers válidos (PWA/IndexedDB)
- [ ] Criar fila de sincronização para validações offline
- [ ] Implementar detecção de status de conexão
- [ ] Criar sincronização automática ao reconectar
- [ ] Adicionar indicador visual de itens pendentes de sync
- [ ] Testar fluxo completo offline → online

---

## Fase 5: Troca de Embarcação e Segurança
**Objetivo:** Permitir troca segura com rastreabilidade

- [ ] Criar modal de confirmação de troca de embarcação
- [ ] Implementar validação de senha para troca
- [ ] Registrar logs na tabela logs_troca_embarcacao
- [ ] Atualizar estado com nova embarcação
- [ ] Carregar novo gap_embarque e capacidade

---

## Fase 6: UI/UX Final e Polish
**Objetivo:** Refinar interface e experiência

- [ ] Aplicar Material Design 3 em todos os componentes
- [ ] Implementar micro-interações e transições suaves
- [ ] Adicionar mensagens técnicas de erro (data/hora de expiração)
- [ ] Otimizar performance do scan (< 1 segundo)
- [ ] Criar documentação de uso para tripulação
- [ ] Realizar testes de usabilidade

---

## Notas Técnicas
- **Regra Crítica:** Gap de Embarque diferencia embarque/desembarque/duplicado
- **Offline-First:** App deve funcionar 100% sem internet
- **Validação:** Todas as regras de negócio devem rodar localmente
- **Segurança:** Autenticação individual com rastreamento completo