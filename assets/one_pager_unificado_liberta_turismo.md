# One-Pager Executivo Unificado: Ecossistema de Vouchers 24h Liberta Turismo

**Produto:** Ecossistema de Vouchers de 24 Horas (App de Controle, App de Vendas e Painel Gestor)
**Cliente:** Liberta Turismo
**Autor:** Manus AI
**Data:** 17 de Novembro de 2025

## 1. O Problema e a Oportunidade

A Liberta Turismo enfrenta custos elevados e inflexibilidade operacional devido Ã  dependÃªncia de um sistema de terceiros para a venda de passagens. O modelo atual nÃ£o permite a otimizaÃ§Ã£o da frota em tempo real nem oferece a melhor experiÃªncia de flexibilidade para o turista.

**Oportunidade:** Substituir o sistema de passagens por um **Ecossistema de Vouchers de 24 Horas** de uso ilimitado, ativado no primeiro embarque, que oferece:
1.  **ReduÃ§Ã£o de Custos** e dependÃªncia de terceiros.
2.  **OtimizaÃ§Ã£o de Frota** baseada em dados de ocupaÃ§Ã£o em tempo real.
3.  **Melhor ExperiÃªncia** para o turista com liberdade total por 24h.

## 2. Proposta de Valor Central

O ecossistema transforma a venda de transporte em **venda de experiÃªncia**, simplificando a jornada do turista e fornecendo Ã  Liberta o controle total sobre sua operaÃ§Ã£o e dados.

| Stakeholder | Valor Entregue |
| :--- | :--- |
| **Liberta Turismo (OperaÃ§Ã£o)** | Controle total da frota, otimizaÃ§Ã£o de combustÃ­vel, dados de ocupaÃ§Ã£o em tempo real e reduÃ§Ã£o de despesas mensais. |
| **TripulaÃ§Ã£o** | Ferramenta **offline-first** para validaÃ§Ã£o rÃ¡pida e segura, garantindo o controle de lotaÃ§Ã£o. |
| **Vendedores Externos** | Ferramenta de vendas dedicada com comissionamento automÃ¡tico e transparente. |
| **Turista** | **Liberdade Total** por 24 horas para ir e vir ilimitadamente, sem a necessidade de mÃºltiplas compras. |

## 3. Ecossistema do Produto

O sistema Ã© composto por trÃªs pilares que se integram para gerenciar todo o ciclo de vida do voucher.

| Componente | UsuÃ¡rio Principal | Funcionalidades Chave | Foco Operacional |
| :--- | :--- | :--- | :--- |
| **App de Controle** | TripulaÃ§Ã£o | Scan de QR Code, Busca Manual, **Modo Offline**, Regra de Gap de Embarque, Dashboard de LotaÃ§Ã£o. | **ValidaÃ§Ã£o e OperaÃ§Ã£o** (MVP Principal) |
| **App de Vendas** | Vendedores Externos | Venda de vouchers, GeraÃ§Ã£o de QR Code, Envio por e-mail, Recebimento (CartÃ£o/Pix), SeparaÃ§Ã£o de Comissionamento. | **GeraÃ§Ã£o de Receita** |
| **Painel Gestor** | EscritÃ³rio/Gestores | Monitoramento em tempo real da frota, GestÃ£o de EmbarcaÃ§Ãµes (capacidade, Gap), GestÃ£o de Vouchers (CRUD), RelatÃ³rios e Logs de SincronizaÃ§Ã£o. | **Monitoramento e InteligÃªncia** |

## 4. EstratÃ©gia de Desenvolvimento (Roadmap Modular)

O desenvolvimento serÃ¡ focado no **App de Controle** como MVP, seguido pelas ferramentas de Vendas e GestÃ£o.

| Fase | MÃ³dulos Principais | Objetivo |
| :--- | :--- | :--- |
| **FASE 1: Core do App de Controle (MVP MÃ­nimo)** | Auth/Login, Scan de QR Code, ValidaÃ§Ã£o BÃ¡sica, Busca Manual. | **Validar o conceito central:** Permitir que o tripulante valide um voucher. |
| **FASE 2: App de Controle Operacional** | **Modo Offline**, SincronizaÃ§Ã£o, Troca de EmbarcaÃ§Ã£o (com senha), Regra de Gap de Embarque, Dashboard de LotaÃ§Ã£o. | **Tornar o app robusto:** Garantir a operaÃ§Ã£o em alto mar e o controle de lotaÃ§Ã£o. |
| **FASE 3: Painel Gestor Simplificado** | Monitoramento de Frota, GestÃ£o de EmbarcaÃ§Ãµes, GestÃ£o de Vouchers (CRUD). | **Escalar e Otimizar:** Fornecer controle e inteligÃªncia de negÃ³cio. |
| **FASE 4: App de Vendas e Backend Unificado** | GeraÃ§Ã£o de Voucher, IntegraÃ§Ã£o de Pagamento, Comissionamento, Venda via Website. | **Gerar Receita:** Habilitar a venda de vouchers e o fluxo financeiro. |

## 5. Requisitos TÃ©cnicos Chave

*   **Arquitetura:** Backend unificado para servir todos os aplicativos e o website de compra.
*   **Offline-First:** O App de Controle deve ser totalmente funcional sem conexÃ£o.
*   **Regra CrÃ­tica:** A lÃ³gica de **Gap de Embarque** (configurÃ¡vel por embarcaÃ§Ã£o) Ã© essencial para diferenciar embarque, desembarque e scans duplicados.
*   **Tecnologia:** CompatÃ­vel com *vibe coding* (Reflex/Lovable) para desenvolvimento Ã¡gil.

## 6. PrÃ³ximos Passos

1.  **RevisÃ£o e AprovaÃ§Ã£o** do PRD e EspecificaÃ§Ã£o UX/UI do App de Controle.
2.  **InÃ­cio do Desenvolvimento** da FASE 1 e FASE 2 (App de Controle).
3.  **DefiniÃ§Ã£o Detalhada** dos requisitos do App de Vendas e Painel Gestor (FASE 3 e 4).
