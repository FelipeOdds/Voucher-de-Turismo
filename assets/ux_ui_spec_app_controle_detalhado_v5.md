# EspecificaÃ§Ã£o UX/UI Aprofundada - App de Controle Liberta Turismo

**Autor:** Manus AI
**Data:** 17 de Novembro de 2025
**VersÃ£o:** 5.0 (Visual e Componentizada - Foco em Designer/Vibe Coding)
**Foco:** Blueprint Visual, Componentes (Google Material Design) e Fluxos

## 1. Diretrizes Visuais e ComponentizaÃ§Ã£o

O design do aplicativo deve seguir o **Google Material Design 3** (atualizado) para garantir uma experiÃªncia de usuÃ¡rio moderna, intuitiva e acessÃ­vel.

| Componente | ReferÃªncia Material Design | Uso no App de Controle |
| :--- | :--- | :--- |
| **BotÃµes** | `Filled Button` (PrimÃ¡rio), `Outlined Button` (SecundÃ¡rio) | **[ESCANEAR QR CODE]** (PrimÃ¡rio), **[BUSCA MANUAL]** (SecundÃ¡rio). |
| **Indicadores** | `Badge` (para status), `Linear Progress Indicator` (para lotaÃ§Ã£o) | **ð´ Offline / ð¢ Online** (Badge), **Barra de LotaÃ§Ã£o** (Progress Indicator). |
| **Feedback** | `Full-screen Modal` (com cores de fundo) | Telas de **VERDE** (Sucesso), **VERMELHO** (Erro), **AMARELO** (Alerta). |
| **Input** | `Text Field` (Filled ou Outlined) | Campo de `Senha` (Modal de Troca), Campo de `Busca Manual`. |
| **NavegaÃ§Ã£o** | `Bottom Navigation Bar` (se houver mais telas) ou `Top App Bar` | NavegaÃ§Ã£o entre Dashboard, Scan e Busca. |

## 2. Mapa de Telas (Sitemap) e Fluxograma Visual (ASCII Art)

### 2.1. Mapa de Telas (Sitemap)

```mermaid
graph TD
    A[1. /login] --> B[2. /select-vessel];
    B --> C[3. /dashboard (Home)];
    C --> C1[3.1. /dashboard/scan];
    C --> C2[3.2. /dashboard/search];
    C --> M1(Modal: Feedback);
    C --> M2(Modal: Troca de EmbarcaÃ§Ã£o);
    M2 --> M3(Modal: ConfirmaÃ§Ã£o de Senha);
```

### 2.2. Fluxograma de ValidaÃ§Ã£o (ASCII Art)

```
+---------------------------------+
| 1. INÃCIO: Scan QR Code         |
+---------------------------------+
        |
        v
+---------------------------------+
| 2. DECISÃO: Voucher VÃ¡lido?     |
|    (Offline - Cache Local)      |
+---------------------------------+
        | SIM
        v
+---------------------------------+
| 3. DECISÃO: Expirado (24h)?     |
|    (Offline - Data ExpiraÃ§Ã£o)   |
+---------------------------------+
        | NÃO
        v
+---------------------------------+
| 4. DECISÃO: JÃ¡ Embarcado?       |
|    (Offline - Ãltimo Log Local) |
+---------------------------------+
        | NÃO (Primeiro Uso/Desembarcado)
        v
+---------------------------------+
| 5. DECISÃO: EMBARQUE - LotaÃ§Ã£o? |
|    (Offline - OcupaÃ§Ã£o < Max?)  |
+---------------------------------+
        | SIM (EspaÃ§o)
        v
+---------------------------------+
| 5a. SUCESSO: EMBARQUE (+1)      |
|     (Feedback VERDE)            |
+---------------------------------+
        |
        v
+---------------------------------+
| FIM (Salva Log Local)           |
+---------------------------------+

        ^
        | NÃO (Lotado)
+---------------------------------+
| 5b. ERRO: LotaÃ§Ã£o MÃ¡xima        |
|     (Feedback VERMELHO)         |
+---------------------------------+
        |
        v
+---------------------------------+
| FIM (Salva Log Local)           |
+---------------------------------+

        ^
        | SIM (JÃ¡ Embarcado)
+---------------------------------+
| 6. DECISÃO: DESEMBARQUE/DUPLICADO|
|    (Tempo >= Gap de Embarque?)  |
+---------------------------------+
        | SIM (>= Gap)
        v
+---------------------------------+
| 6a. SUCESSO: DESEMBARQUE (-1)   |
|     (Feedback VERDE)            |
+---------------------------------+
        |
        v
+---------------------------------+
| FIM (Salva Log Local)           |
+---------------------------------+

        ^
        | NÃO (< Gap)
+---------------------------------+
| 6b. ALERTA: Scan Duplicado      |
|     (Feedback AMARELO - Ignora) |
+---------------------------------+
        |
        v
+---------------------------------+
| FIM (Salva Log Local)           |
+---------------------------------+

```

## 3. Blueprint Visual das Telas Principais (Sketch ASCII)

### 3.1. Tela: `/dashboard` (Home)

```
+---------------------------------+
| < Top App Bar >                 |
|                                 |
| [Icone Menu]      [Icone Sair]  |
|                                 |
| ð¢ Online (Badge)               |
|                                 |
| EmbarcaÃ§Ã£o: [Nome da EmbarcaÃ§Ã£o]|
| [BotÃ£o Trocar]                  |
|                                 |
| LotaÃ§Ã£o Atual:                  |
| **45 / 100** (Texto Grande)     |
| [===================-----] (Barra Progresso)
|                                 |
| Gap de Embarque: 15 minutos     |
|                                 |
| [ESCANEAR QR CODE] (Filled Button - PrimÃ¡rio)
|                                 |
| [BUSCA MANUAL] (Outlined Button - SecundÃ¡rio)
|                                 |
| --- Ãltimas ValidaÃ§Ãµes ---      |
| [Item 1: Embarque - 14:30]      |
| [Item 2: Desembarque - 14:20]   |
| [Item 3: Alerta - 14:15]        |
| ...                             |
+---------------------------------+
```

### 3.2. Modal: Feedback (VERDE - Sucesso)

```
+---------------------------------+
| < Full-Screen Modal - Fundo VERDE >
|                                 |
|                                 |
|         [Icone Check]           |
|                                 |
| **EMBARQUE AUTORIZADO**         |
|                                 |
| Passageiro: John Doe            |
| Voucher: 123456                 |
|                                 |
|                                 |
| < Fecha Automaticamente em 3s > |
|                                 |
+---------------------------------+
```

### 3.3. Modal: Feedback (VERMELHO - Erro CrÃ­tico)

```
+---------------------------------+
| < Full-Screen Modal - Fundo VERMELHO >
|                                 |
|                                 |
|         [Icone X]               |
|                                 |
| **VOUCHER EXPIRADO**            |
|                                 |
| Validade encerrada em:          |
| 15/11/2025 Ã s 14:30             |
|                                 |
|                                 |
| [OK] (Filled Button - Branco)   |
|                                 |
+---------------------------------+
```

## 4. Detalhamento dos Elementos CrÃ­ticos por Tela (Mantido)

*(O conteÃºdo da seÃ§Ã£o 3. Detalhamento dos Elementos CrÃ­ticos por Tela do documento anterior foi mantido, mas serÃ¡ omitido aqui para brevidade. Ele detalha o Estado e Comportamento CrÃ­tico de cada elemento.)*
