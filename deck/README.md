# Deck do minicurso: build agêntico com DeckCraft + MCP

Os slides são gerados por código. Cada slide vira uma lista de comandos do [DeckCraft](https://github.com/storytold/deckcraft) (`slide.new`, `shape.insert`, `shape.fill`, `text.select`, `format.color`, `insert.picture`, `slide.notes`...). Essa lista é enviada ao servidor MCP `deckcraft-cli mcp` pela tool `batch`, os mesmos verbos que um agente de IA usa.

```
content.py ──► design.py ──► build.py ──► mcp_client.py ══ JSON-RPC/stdio ══► deckcraft-cli mcp
 slides,        tokens e       um batch        cliente MCP mínimo                 .deckcraft · .pptx · PDFs
 notas, tempos  componentes    por slide
      ▲
      └── código lido de snippets/ (//sampleStart … //sampleEnd): slide e exemplo nunca divergem
```

## Arquivos

| Arquivo | Função |
|---|---|
| `tools/content.py` | os 54 slides, as notas do apresentador e o tempo de cada slide |
| `tools/design.py` | design system: tokens de cor, tipografia, realce de sintaxe e componentes |
| `tools/build.py` | build via MCP. Também sincroniza o cabeçalho dos snippets, gera os índices, os PDFs por dia e o guia |
| `tools/readme_assets.py` | banners, cartão e badges do README, gerados no mesmo tema |
| `tools/desafios_src.py` | fonte única dos desafios e gabaritos (`<<TODO||solução>>`) |
| `tools/validate.py` | compila e executa todo o código com o Kotlin 2.4.21 |
| `tools/mcp_client.py` | cliente MCP (JSON-RPC 2.0 sobre stdio) |

## Como reconstruir

Requisitos:
- `deckcraft-cli` 0.18.1 ([releases](https://github.com/storytold/deckcraft/releases)). O build procura em `~/.local/opt/deckcraft-cli-0.18.1/` ou na variável `DECKCRAFT_CLI`.
- Os pacotes de marca da JetBrains (logos do ecossistema e o mascote Kodee) nas pastas `Kotlin Ecosystem Logos/` e `kotlin_mascot_2/`. Eles não são redistribuídos aqui.
- Para validar o código: `kotlinc` 2.4.21 e o `kotlinx-coroutines-core-jvm` em `deck/build/libs/`.

```bash
python3 deck/tools/desafios_src.py          # gera desafios/ e solucoes/
python3 deck/tools/validate.py              # valida snippets, desafios e gabaritos
python3 -I deck/tools/build.py --preview    # deck, PDFs, imagens do README, guia e índices
```

## Tema (resumo)

| Elemento | Regra |
|---|---|
| Fundo e tinta | `#FAFAFC` / `#121216` |
| Bordas e sombras | borda de 2 pt e sombra dura de 4 pt |
| Gradiente assinatura | `#7F52FF → #C711E1 → #F88909`, **só** na capa, nos divisores e no encerramento |
| Tints, só por significado | Purple `#F3EEFF` (conceito), Orange `#FFF7ED` (atenção), Info `#EFF6FF` (saiba mais), Success `#ECFDF5` / Error `#FFF1F2` (Faça / Evite) |
| Código | sempre em fundo `#FFFFFF`, sem ligaduras (JetBrains Mono NL) |
| Sintaxe | palavras-chave `#7F52FF` · tipos `#2563EB` · strings `#059669` · números e anotações `#C26100` · comentários `#76768A` |
