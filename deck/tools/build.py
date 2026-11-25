"""Build agêntico v2: cada slide vira um `batch` de comandos enviado ao servidor MCP do DeckCraft.

    python3 -I deck/tools/build.py [--only 0,5,12] [--preview] [--sem-readme]

Saídas:
    deck/Minicurso_Kotlin.deckcraft · .pptx       documento editável (local)
    deck/Minicurso_Kotlin.pdf                     slides completos, sem notas (público)
    deck/Minicurso_Kotlin_Dia1.pdf · _Dia2.pdf    um PDF por dia, sem notas (público, D2/D34)
    deck/Minicurso_Kotlin_notas.pdf               páginas com notas (local)
    assets/readme/*.png                           banners, cartão e badges do README (D37–D39)
    GUIA_DO_APRESENTADOR.md                       guia por dia com horário acumulado (D22)
    snippets/diaN/README.md                       índice dos snippets e desafios por dia (D10)
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from design import ROOT, ASSETS_BUILD, KODEE, Slide, chrome, C  # noqa: E402
from mcp_client import DeckcraftMCP  # noqa: E402

DECK_DIR = os.path.join(ROOT, "deck")
NAME = "Minicurso_Kotlin"
BAR = "// ══════════════════════════════════════════════════════════════"


def prepare_assets():
    """Reduz as ilustrações do Kodee (3334 px) para 900 px."""
    os.makedirs(ASSETS_BUILD, exist_ok=True)
    for rel in KODEE.values():
        src = os.path.join(ROOT, rel)
        dst = os.path.join(ASSETS_BUILD, os.path.basename(rel))
        if not os.path.exists(dst):
            subprocess.run(["sips", "--resampleWidth", "900", src, "--out", dst],
                           check=True, stdout=subprocess.DEVNULL)


# ------------------------------------------------------------------ cabeçalhos (D28)
def sync_header(rel: str, linhas: list[str]):
    path = os.path.join(ROOT, rel)
    text = open(path, encoding="utf-8").read()
    link = "<cole aqui>"
    if text.startswith("// ══"):
        end = text.index("\n// ══", 5)
        head = text[:end]
        m = re.search(r"Link do Playground: (.*)", head)
        if m:
            link = m.group(1).strip()
        text = text[text.index("\n", end + 1) + 1:]
    header = [BAR] + [f"// {l}" for l in linhas] + [f"// Link do Playground: {link}", BAR]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(header) + "\n" + text)


def sync_snippets(slides: list[Slide]):
    usados = {}
    for s in slides:
        for rel in s.snippets:
            usados.setdefault(rel, s)
    for rel, s in usados.items():
        dia = rel.split("/")[1].replace("dia", "")
        sync_header(rel, [
            f"Minicurso de Kotlin · IFCE 2026 · Dia {dia} · slide {s.number:02d}",
            f"{os.path.basename(rel)} · {s.title}",
            "Como usar: cole TODO este arquivo em https://play.kotlinlang.org",
            "(versão 2.4.21, alvo JVM) e clique em Run.",
        ])
    soltos = [f for d in ("dia1", "dia2") for f in sorted(os.listdir(os.path.join(ROOT, "snippets", d)))
              if f.endswith(".kt") and f"snippets/{d}/{f}" not in usados]
    if soltos:
        print("  ! snippets sem slide:", soltos)
    # desafios e gabaritos → slide "Hora do desafio"
    hora = {s.day: s for s in slides if s.title.startswith("Hora do desafio")}
    for base in ("desafios", "solucoes"):
        for dia in ("dia1", "dia2"):
            pasta = os.path.join(ROOT, base, dia)
            if not os.path.isdir(pasta):
                continue
            n = int(dia[-1])
            for f in sorted(os.listdir(pasta)):
                if f.endswith(".kt"):
                    sync_header(f"{base}/{dia}/{f}", [
                        f"Minicurso de Kotlin · IFCE 2026 · Dia {n} · {'GABARITO' if base == 'solucoes' else 'DESAFIO'}"
                        f" (slide {hora[n].number:02d})",
                        f"{f}",
                        "Como usar: cole TODO este arquivo em https://play.kotlinlang.org",
                        "(versão 2.4.21, alvo JVM), clique em Run e deixe tudo ✅.",
                    ])
    return usados


def write_indexes(slides: list[Slide], usados: dict):
    """snippets/diaN/README.md: índice de snippets e desafios (D10)."""
    titulos = {1: "Dia 1 · Fundamentos da linguagem", 2: "Dia 2 · Modelagem, concorrência e ecossistema"}
    for n in (1, 2):
        linhas = [f"# Snippets · {titulos[n]}", "",
                  "Cada arquivo é autocontido: copie **o arquivo inteiro**, cole em "
                  "[play.kotlinlang.org](https://play.kotlinlang.org) (Kotlin **2.4.21**, alvo **JVM**) e clique em **Run**.",
                  "", "| Arquivo | Tema | Slide |", "|---|---|---|"]
        for rel, s in sorted(usados.items()):
            if rel.startswith(f"snippets/dia{n}/"):
                nome = os.path.basename(rel)
                extra = " (bônus · alvo Compose/Wasm)" if "bonus" in nome else ""
                linhas.append(f"| [`{nome}`]({nome}) | {s.title}{extra} | {s.number:02d} |")
        linhas += ["", f"## Desafios do Dia {n}", "",
                   f"Em [`desafios/dia{n}`](../../desafios/dia{n}): cada arquivo traz o enunciado, `TODO()` para você "
                   "implementar e verificações automáticas que imprimem ✅ ou ❌.", "",
                   "| Desafio | Arquivo |", "|---|---|"]
        pasta = os.path.join(ROOT, "desafios", f"dia{n}")
        for f in sorted(os.listdir(pasta)):
            txt = open(os.path.join(pasta, f), encoding="utf-8").read()
            m = re.search(r"DESAFIO (\d) · (.+?)\s{2,}nível: (\w+)", txt)
            if m:
                linhas.append(f"| {m.group(1)} · {m.group(2).strip()} ({m.group(3).lower()}) | "
                              f"[`{f}`](../../desafios/dia{n}/{f}) |")
        linhas += ["", "Os gabaritos são publicados na branch `gabaritos` ao fim do curso.", ""]
        with open(os.path.join(ROOT, "snippets", f"dia{n}", "README.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(linhas))


# ------------------------------------------------------------------ guia (D22)
def write_guide(deck):
    slides = deck.slides
    out = ["# Guia do apresentador · Minicurso de Kotlin (4 h · 2 dias)", "",
           "> Gerado a partir das notas do deck (`deck/tools/content.py`). Edite lá e rode o build.",
           "> O horário é acumulado desde o início de cada dia (00:00).", ""]
    for dia in (1, 2):
        out += [f"## Dia {dia}", ""]
        t = 0.0
        bloco = [s for s in slides if s.day == dia or (dia == 1 and s.day == 0)]
        for s in bloco:
            hh, mm = divmod(int(round(t)), 60)
            out += [f"### {hh:02d}:{mm:02d} · Slide {s.number:02d} · {s.title}  _(≈ {s.minutes:g} min)_", ""]
            if s.snippets:
                out += ["Código: " + ", ".join(f"`{r}`" for r in s.snippets), ""]
            out += [s.notes or "_(sem notas)_", ""]
            t += s.minutes
        hh, mm = divmod(int(round(t)), 60)
        out += [f"**Total planejado do Dia {dia}: {hh:02d}:{mm:02d}**", "",
                f"### Roteiro de contingência · Dia {dia}", "", deck.contingencia.get(dia, ""), ""]
    with open(os.path.join(ROOT, "GUIA_DO_APRESENTADOR.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    for dia in (1, 2):
        total = sum(s.minutes for s in slides if s.day == dia or (dia == 1 and s.day == 0))
        print(f"  Dia {dia}: {total:g} min planejados")


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cli", default=os.environ.get(
        "DECKCRAFT_CLI", os.path.expanduser("~/.local/opt/deckcraft-cli-0.18.1/deckcraft-cli")))
    ap.add_argument("--only", help="índices (0-based) para construir apenas alguns slides")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--sem-readme", action="store_true", help="não gera as imagens do README")
    ap.add_argument("--scale", type=float, default=1.0)
    args = ap.parse_args()

    prepare_assets()
    from content import build_deck  # noqa: E402
    deck = build_deck()
    slides: list[Slide] = deck.slides
    for i, s in enumerate(slides):
        s.number = i + 1
    usados = sync_snippets(slides)
    # recarrega o conteúdo: os cabeçalhos mudaram, mas os trechos exibidos não incluem o cabeçalho
    pick = set(int(x) for x in args.only.split(",")) if args.only else None
    chosen = [s for i, s in enumerate(slides) if pick is None or i in pick]

    out_preview = os.path.join(DECK_DIR, "preview")
    if args.preview:
        shutil.rmtree(out_preview, ignore_errors=True)
        os.makedirs(out_preview, exist_ok=True)

    t0 = time.time()
    with DeckcraftMCP(args.cli, read_roots=[ROOT], write_roots=[DECK_DIR, os.path.join(ROOT, "assets")]) as mcp:
        mcp.call("new_presentation", {"blank": True})
        mcp.call("batch", {"commands": [
            C("design.colors", colors={
                "dk1": "#121216", "lt1": "#FFFFFF", "dk2": "#3D3D4A", "lt2": "#F2F2F7",
                "accent1": "#7F52FF", "accent2": "#C711E1", "accent3": "#F88909",
                "accent4": "#2563EB", "accent5": "#059669", "accent6": "#E11D48",
                "hlink": "#5B32D6", "folHlink": "#C711E1"}),
            C("design.fonts", major="Inter", minor="Inter"),
            C("file.properties", title="Kotlin: da história ao Multiplatform",
              subject="Minicurso de Kotlin (4 h · 2 dias) — Engenharia de Computação, IFCE Fortaleza",
              author="Robson Freitas Ribeiro", keywords="Kotlin, Playground, Corrotinas, KMP", category="Minicurso"),
        ]})
        for s in chosen:
            cmds = chrome(s) + s.cmds
            cmds.append(C("transition.set", kind="fade", duration=300))
            if s.notes:
                cmds.append(C("slide.notes", text=s.notes))
            try:
                mcp.call("batch", {"commands": cmds})
            except Exception as e:
                print(f"[ERRO] slide {s.number} '{s.title}': {str(e)[:800]}", file=sys.stderr)
                raise
        print(f"  {len(chosen)} slides enviados via MCP")
        mcp.call("run_command", {"command": "slide.go", "params": {"index": 0}})

        if pick is None:
            base = os.path.join(DECK_DIR, NAME)
            mcp.call("save_presentation", {"path": base + ".deckcraft"})
            mcp.call("export", {"path": base + ".pptx", "format": "pptx"})
            mcp.call("run_command", {"command": "file.export", "params": {
                "path": base + ".pdf", "format": "pdf", "layout": "slides", "textLayer": True}})
            capa = [0, 1, 2]
            for dia in (1, 2):
                idx = sorted(set(capa + [i for i, s in enumerate(slides) if s.day == dia]))
                mcp.call("run_command", {"command": "file.export", "params": {
                    "path": f"{base}_Dia{dia}.pdf", "format": "pdf", "layout": "slides",
                    "slides": idx, "textLayer": True}})
            mcp.call("export", {"path": base + "_notas.pdf", "format": "pdf", "layout": "notes", "paper": "a4"})
        if args.preview:
            mcp.call("export", {"path": os.path.join(out_preview, "slide.png"), "format": "png",
                                "all": True, "scale": args.scale})
        if pick is None and not args.sem_readme:
            import readme_assets
            readme_assets.build(mcp, deck)
    print(f"Concluído em {time.time() - t0:.1f}s")

    if pick is None:
        write_indexes(slides, usados)
        write_guide(deck)


if __name__ == "__main__":
    main()
