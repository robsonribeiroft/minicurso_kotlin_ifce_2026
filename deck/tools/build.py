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


def proteger(path: str, ligar: bool):
    """Liga/desliga o flag de imutabilidade do macOS (uchg) e o modo somente leitura."""
    if not os.path.exists(path):
        return
    import stat
    flags = os.stat(path).st_flags if hasattr(os, "chflags") else None
    if ligar:                       # chmod antes: arquivo imutável não aceita chmod
        os.chmod(path, 0o444)
        if flags is not None:
            os.chflags(path, flags | stat.UF_IMMUTABLE)
    else:
        if flags is not None:
            os.chflags(path, flags & ~stat.UF_IMMUTABLE)
        os.chmod(path, 0o644)


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


# ------------------------------------------------------------------ versão editável (v2)
VERSAO = "v2"
DECK = os.path.join(DECK_DIR, f"{NAME}_{VERSAO}")            # deck/Minicurso_Kotlin_v2.deckcraft
MANIFESTO = os.path.join(DECK_DIR, "build", f"manifesto_{VERSAO}.json")
THEME = [
    C("design.colors", colors={
        "dk1": "#121216", "lt1": "#FFFFFF", "dk2": "#3D3D4A", "lt2": "#F2F2F7",
        "accent1": "#7F52FF", "accent2": "#C711E1", "accent3": "#F88909",
        "accent4": "#2563EB", "accent5": "#059669", "accent6": "#E11D48",
        "hlink": "#5B32D6", "folHlink": "#C711E1"}),
    C("design.fonts", major="Inter", minor="Inter"),
    C("file.properties", title="Kotlin: da história ao Multiplatform",
      subject="Minicurso de Kotlin (4 h · 2 dias) — Engenharia de Computação, IFCE Fortaleza",
      author="Robson Freitas Ribeiro", keywords="Kotlin, Playground, Corrotinas, KMP", category="Minicurso"),
]


def sha256(path: str) -> str | None:
    import hashlib
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def ler_manifesto() -> dict:
    import json
    if os.path.exists(MANIFESTO):
        return json.load(open(MANIFESTO, encoding="utf-8"))
    return {"sha256": None, "slides": {}}


def gravar_manifesto(m: dict):
    import json
    os.makedirs(os.path.dirname(MANIFESTO), exist_ok=True)
    m["sha256"] = sha256(DECK + ".deckcraft")
    m["atualizado"] = time.strftime("%Y-%m-%d %H:%M:%S")
    json.dump(m, open(MANIFESTO, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def chaves(slides: list[Slide]) -> list[str]:
    """Chave estável de cada slide do content.py (dia + título), usada no manifesto."""
    vistos, out = {}, []
    for s in slides:
        base = f"d{s.day}:" + re.sub(r"[^a-z0-9]+", "-", s.title.lower()).strip("-")
        vistos[base] = vistos.get(base, 0) + 1
        out.append(base if vistos[base] == 1 else f"{base}#{vistos[base]}")
    return out


def app_aberto() -> bool:
    """O app DeckCraft (GUI) aberto pode gravar uma cópia do AutoRecover por cima do deck."""
    r = subprocess.run(["pgrep", "-x", "DeckCraft"], capture_output=True)
    return r.returncode == 0


def cmds_do_slide(s: Slide, at: int | None = None) -> list[dict]:
    cmds = chrome(s) + s.cmds
    if at is not None:
        cmds[0]["params"]["at"] = at
    cmds.append(C("transition.set", kind="fade", duration=300))
    if s.notes:
        cmds.append(C("slide.notes", text=s.notes))
    return cmds


def id_criado(resultado: str) -> int | None:
    import json
    for r in json.loads(resultado):
        if r.get("command") == "slide.new" and isinstance(r.get("result"), dict):
            return r["result"].get("id")
    return None


def exportar(mcp, slides: list[Slide], ids_por_dia: dict[int, list[int]] | None):
    """Exporta .pptx e PDFs a partir do documento ABERTO (inclui as edições humanas)."""
    base = os.path.join(DECK_DIR, NAME)
    mcp.call("export", {"path": DECK + ".pptx", "format": "pptx"})
    mcp.call("run_command", {"command": "file.export", "params": {
        "path": base + ".pdf", "format": "pdf", "layout": "slides", "textLayer": True}})
    if ids_por_dia:
        import json
        doc = json.loads(mcp.call("inspect_document", {}))
        pos = {sl["id"]: sl["index"] for sl in doc["slides"]}
        for dia, ids in ids_por_dia.items():
            idx = sorted(pos[i] for i in ids if i in pos)
            mcp.call("run_command", {"command": "file.export", "params": {
                "path": f"{base}_Dia{dia}.pdf", "format": "pdf", "layout": "slides",
                "slides": idx, "textLayer": True}})
    mcp.call("export", {"path": DECK + "_notas.pdf", "format": "pdf", "layout": "notes", "paper": "a4"})


def main():
    ap = argparse.ArgumentParser(description="Build do deck v2 (editável por humano, agente e script).")
    ap.add_argument("--cli", default=os.environ.get(
        "DECKCRAFT_CLI", os.path.expanduser("~/.local/opt/deckcraft-cli-0.18.1/deckcraft-cli")))
    ap.add_argument("--slides", help="atualiza SÓ estes slides (números do content.py, ex.: 6,12) "
                                     "no deck existente, preservando o resto e as edições humanas")
    ap.add_argument("--exportar", action="store_true",
                    help="só exporta PDFs/.pptx a partir do deck existente (com as edições humanas)")
    ap.add_argument("--forcar", action="store_true",
                    help="build completo mesmo que o deck tenha sido editado (as edições são perdidas)")
    ap.add_argument("--ignorar-app", action="store_true", help="roda mesmo com o app DeckCraft aberto")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--sem-readme", action="store_true", help="não gera as imagens do README")
    ap.add_argument("--scale", type=float, default=1.0)
    args = ap.parse_args()

    if app_aberto() and not args.ignorar_app:
        sys.exit("✋ O app DeckCraft está aberto. Feche-o (⌘Q) antes do build: o AutoRecover do app "
                 "pode gravar uma cópia antiga por cima do deck. (Use --ignorar-app por sua conta.)")

    prepare_assets()
    from content import build_deck  # noqa: E402
    deck = build_deck()
    slides: list[Slide] = deck.slides
    for i, s in enumerate(slides):
        s.number = i + 1
    usados = sync_snippets(slides)
    keys = chaves(slides)
    man = ler_manifesto()
    arquivo = DECK + ".deckcraft"
    for ext in (".deckcraft", ".pptx"):           # remove a trava antiga (uchg), se existir
        proteger(DECK + ext, False)

    editado = os.path.exists(arquivo) and man.get("sha256") not in (None, sha256(arquivo))
    incremental = bool(args.slides) or args.exportar
    # "edições externas" é persistente: depois de um --slides/--exportar o hash do manifesto
    # passa a ser o do deck editado, mas as edições humanas continuam lá e não podem ser perdidas.
    externas = editado or man.get("edicoes_externas", False)
    if not incremental and os.path.exists(arquivo) and (externas or not man.get("sha256")) and not args.forcar:
        sys.exit(f"✋ {os.path.relpath(arquivo, ROOT)} foi editado depois do último build (no app ou por "
                 "um agente).\n   Para não perder essas edições, use:\n"
                 "     --slides N[,M]  atualiza só esses slides a partir do content.py\n"
                 "     --exportar      gera PDFs/.pptx a partir do deck editado\n"
                 "     --forcar        regenera tudo (descarta as edições)")

    out_preview = os.path.join(DECK_DIR, "preview")
    if args.preview:
        shutil.rmtree(out_preview, ignore_errors=True)
        os.makedirs(out_preview, exist_ok=True)

    t0 = time.time()
    with DeckcraftMCP(args.cli, read_roots=[ROOT], write_roots=[DECK_DIR, os.path.join(ROOT, "assets")]) as mcp:
        if incremental:
            import json
            if not os.path.exists(arquivo):
                sys.exit(f"Não existe {arquivo}: rode o build completo primeiro.")
            mcp.call("open_presentation", {"path": arquivo})
            alvo = [int(x) for x in args.slides.split(",")] if args.slides else []
            for n in alvo:
                s, k = slides[n - 1], keys[n - 1]
                doc = json.loads(mcp.call("inspect_document", {}))
                pos = {sl["id"]: sl["index"] for sl in doc["slides"]}
                sid = man["slides"].get(k)
                if sid in pos:                               # substitui no mesmo lugar
                    at = pos[sid]
                    mcp.call("batch", {"commands": [C("slide.delete", ids=[sid])]})
                else:                                        # slide novo: depois do anterior do content
                    ant = man["slides"].get(keys[n - 2]) if n > 1 else None
                    at = pos[ant] + 1 if ant in pos else len(pos)
                    if n > 1 and ant not in pos:
                        print(f"  ! slide anterior a {n:02d} não está no deck; inserindo no fim")
                novo = id_criado(mcp.call("batch", {"commands": cmds_do_slide(s, at=at)}))
                man["slides"][k] = novo
                print(f"  ↻ slide {n:02d} '{s.title}' atualizado (posição {at + 1} no deck)")
            if alvo:
                mcp.call("save_presentation", {"path": arquivo})
            man["edicoes_externas"] = externas
        else:
            mcp.call("new_presentation", {"blank": True})
            mcp.call("batch", {"commands": THEME})
            man = {"versao": VERSAO, "slides": {}, "edicoes_externas": False}
            for s, k in zip(slides, keys):
                try:
                    man["slides"][k] = id_criado(mcp.call("batch", {"commands": cmds_do_slide(s)}))
                except Exception as e:
                    print(f"[ERRO] slide {s.number} '{s.title}': {str(e)[:800]}", file=sys.stderr)
                    raise
            print(f"  {len(slides)} slides enviados via MCP")
            mcp.call("run_command", {"command": "slide.go", "params": {"index": 0}})
            mcp.call("save_presentation", {"path": arquivo})

        capa = [keys[0], keys[1], keys[2]]
        ids_por_dia = {d: [man["slides"][k] for k, s in zip(keys, slides)
                           if (s.day == d or k in capa) and k in man["slides"]] for d in (1, 2)}
        exportar(mcp, slides, ids_por_dia)
        gravar_manifesto(man)
        if args.preview:
            mcp.call("export", {"path": os.path.join(out_preview, "slide.png"), "format": "png",
                                "all": True, "scale": args.scale})
        if not incremental and not args.sem_readme:
            import readme_assets
            readme_assets.build(mcp, deck)
    print(f"Concluído em {time.time() - t0:.1f}s → {os.path.relpath(arquivo, ROOT)}")

    write_indexes(slides, usados)
    write_guide(deck)


if __name__ == "__main__":
    main()
