"""Imagens do README com o mesmo tema dos slides (PRD D37–D39), geradas via DeckCraft MCP.

Cada imagem é um slide de uma apresentação auxiliar com tamanho próprio, exportado em PNG.
Fundo sólido #FAFAFC e borda #121216 (legível nos modos claro e escuro do GitHub, D38).
"""
from __future__ import annotations

import os

from design import (C, Slide, BG, INK, WHITE, BODY2, MUTED, PURPLE, PURPLE_DEEP, ORANGE_DEEP, SURFACE,
                    TINT, GRAD, MONO, KODEE, EMOJI, BUILT, ROOT)

OUT = os.path.join(ROOT, "assets", "readme")
REPO = "github.com/robsonribeiroft/minicurso_kotlin_ifce_2026"


def _slide(build):
    s = Slide(None, "readme", "", None, "")
    build(s)
    return [C("slide.new", layout="blank"), C("design.background", color=BG)] + s.cmds


def banner_capa(s):
    s.rect([20, 20, 600, 260], gradient=GRAD, shadow=6, radius=20, angle=30)
    s.text([52, 46, 540, 24], "MINICURSO · IFCE FORTALEZA · 2026", size=13, bold=True, color=WHITE)
    s.text([52, 82, 540, 90], "Kotlin", size=78, bold=True, color=WHITE, line=1.0)
    s.text([52, 174, 540, 34], "da história ao Multiplatform", size=24, bold=True, color=WHITE)
    s.text([52, 222, 540, 30], "4 horas · 2 dias · só o navegador (Kotlin Playground)", size=15, color=WHITE)
    s.rect([644, 20, 296, 260], fill=WHITE, radius=20)
    s.kodee("waving", (664, 34, 256, 232))


def banner_dia(n, titulo, agenda, kodee):
    def build(s):
        s.rect([20, 20, 300, 260], gradient=GRAD, shadow=6, radius=20, angle=30)
        s.text([48, 44, 260, 22], "MINICURSO DE KOTLIN", size=12, bold=True, color=WHITE)
        s.text([48, 76, 260, 90], f"Dia {n}", size=72, bold=True, color=WHITE, line=1.0)
        s.text([48, 170, 250, 80], titulo, size=18, bold=True, color=WHITE, line=1.1)
        s.rect([344, 20, 596, 260], fill=WHITE, radius=16)
        y = 40
        for hora, item in agenda:
            s.text([368, y, 70, 22], hora, size=13, bold=True, font=MONO)
            s.text([444, y, 330, 22], item, size=14)
            y += 36
        s.kodee(kodee, (780, 110, 150, 160))
    return build


def card_desafio(s):
    s.rect([20, 20, 920, 260], fill=TINT["orange"], radius=18)
    s.text([52, 44, 560, 50], "Hora do desafio", size=40, bold=True, color=ORANGE_DEEP)
    s.text([52, 104, 600, 140],
           "**1.** Abra um arquivo em `desafios/`\n**2.** Cole tudo em **play.kotlinlang.org** (2.4.21 · JVM)\n"
           "**3.** Clique em **Run** e implemente os `TODO()` até tudo passar",
           size=17, spacing=10)
    s.rect([660, 44, 120, 120], fill=WHITE, radius=10, shadow=3)
    s.picture(BUILT["qr_repo"], (668, 52, 104, 104))
    s.text([650, 172, 140, 40], "repositório", size=12, color=BODY2, align="center")
    s.kodee("jumping", (800, 56, 130, 210))


def badges(s):
    x = 8
    for texto, fill, cor in [("Kotlin 2.4.21", PURPLE, WHITE), ("Kotlin Playground", WHITE, INK),
                             ("4 h · 2 dias", SURFACE, INK), ("IFCE · 2026", ORANGE_DEEP, WHITE),
                             ("sem instalação", "#ECFDF5", "#059669")]:
        x += s.chip(x, 20, texto, fill=fill, color=cor, size=12, h=30, shadow=2) + 12


def build(mcp, deck):
    os.makedirs(OUT, exist_ok=True)
    escala = 1280 / 960
    # banners 960 × 300 pt → 1280 × 400 px
    mcp.call("new_presentation", {"blank": True})
    mcp.call("run_command", {"command": "design.slideSize", "params": {"w": 960, "h": 300, "scale": "none"}})
    imagens = [
        ("banner.png", banner_capa),
        ("dia1.png", banner_dia(1, "Fundamentos da linguagem",
                                [("00:00", "Abertura e tour do Playground"), ("00:10", "01 · História e filosofia"),
                                 ("00:20", "02 · Fundamentos"), ("01:05", "03 · Funções"),
                                 ("01:35", "Hora do desafio"), ("02:00", "Fim do Dia 1")], "greeting")),
        ("dia2.png", banner_dia(2, "Modelagem, concorrência e ecossistema",
                                [("00:00", "Quiz do Dia 1"), ("00:05", "04 · Classes e objetos"),
                                 ("00:35", "05 · Corrotinas e Flow"), ("01:15", "06 · Além do Playground"),
                                 ("01:30", "Hora do desafio"), ("02:00", "Encerramento")], "sharing")),
        ("desafio.png", card_desafio),
    ]
    for i, (nome, fn) in enumerate(imagens):
        mcp.call("batch", {"commands": _slide(fn)})
        mcp.call("run_command", {"command": "file.export", "params": {
            "path": os.path.join(OUT, nome), "format": "png", "slide": i, "scale": escala}})
    # badges 700 × 50 pt
    mcp.call("new_presentation", {"blank": True})
    mcp.call("run_command", {"command": "design.slideSize", "params": {"w": 680, "h": 72, "scale": "none"}})
    mcp.call("batch", {"commands": _slide(badges)})
    mcp.call("run_command", {"command": "file.export", "params": {
        "path": os.path.join(OUT, "badges.png"), "format": "png", "slide": 0, "scale": 2}})
    print("  imagens do README em assets/readme/")
