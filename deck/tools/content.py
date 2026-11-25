"""Conteúdo do minicurso v2 (4 h · 2 dias): slides, notas do apresentador e tempos (PRD D15).

Convenções das notas: FALE (roteiro), DEMO (ao vivo no Playground), PERGUNTE (interação),
TRANSIÇÃO (gancho para o próximo slide). O tempo de cada slide vai no argumento `min`
e o build calcula o horário acumulado do guia (D22).
Todo código exibido vem de snippets/ (fonte única, D21) via `code_file`.
"""
from __future__ import annotations

from design import (Slide, C, INK, WHITE, MUTED, BODY2, PURPLE, PURPLE_DEEP, ORANGE_DEEP, SUCCESS,
                    INFO, TINT, DEEP, GRAD, MONO, LOGO, EMOJI, BUILT, SURFACE, FOOTER)

X0, Y0, W, H = 48, 124, 864, 362   # área útil
REPO = "github.com/robsonribeiroft/minicurso_kotlin_ifce_2026"
D1, D2 = "snippets/dia1/", "snippets/dia2/"


class Deck:
    def __init__(self):
        self.slides: list[Slide] = []
        self.day = 0
        self.contingencia: dict[int, str] = {}

    def _add(self, kind, title, section, notes, minutes):
        s = Slide(self, kind, title, section, notes, minutes=minutes, day=self.day)
        self.slides.append(s)
        return s

    def content(self, section, title, notes="", min=3):
        return self._add("content", title, section, notes, min)

    def raw(self, kind, title, notes="", min=1):
        return self._add(kind, title, None, notes, min)

    # ---------------------------------------------------------- slides especiais
    def day_divider(self, n, titulo, agenda, notes, contingencia):
        """Divisor de dia: gradiente assinatura + agenda com horários (D25)."""
        self.day = n
        self.contingencia[n] = contingencia.strip()
        s = self.raw("day", f"Dia {n} · {titulo}", notes, min=0.5)
        s.rect([48, 60, 360, 420], gradient=GRAD, shadow=6, radius=18, angle=45)
        s.text([76, 96, 300, 30], "MINICURSO DE KOTLIN", size=12, bold=True, color=WHITE)
        s.text([76, 150, 300, 120], f"Dia {n}", size=96, bold=True, color=WHITE, line=1.0)
        s.text([76, 276, 300, 90], titulo, size=24, bold=True, color=WHITE, line=1.1)
        s.text([76, 420, 300, 30], "2 horas · Kotlin Playground", size=12, color=WHITE)
        s.rect([440, 60, 472, 420], fill=WHITE, radius=14)
        s.text([464, 80, 420, 28], "Agenda do dia", size=18, bold=True, color=PURPLE_DEEP)
        y = 124
        for hora, item, dur, destaque in agenda:
            if destaque:
                s.rect([456, y - 6, 440, 40], fill=TINT[destaque], shadow=0, line=None, radius=8)
            s.text([468, y + 2, 70, 24], hora, size=13, bold=True, font=MONO, color=INK)
            s.text([548, y + 2, 270, 24], item, size=14, color=INK)
            s.text([820, y + 2, 64, 24], dur, size=12, color=MUTED, align="right")
            y += 44
        return s

    def section(self, num, title, subtitle, topics, kodee, notes="", min=0.5):
        s = self.raw("section", f"{num} · {title}", notes, min=min)
        s.rect([48, 92, 300, 330], gradient=GRAD, shadow=6, radius=18, angle=45)
        s.text([48, 160, 300, 170], num, size=150, color=WHITE, bold=True, align="center")
        s.text([60, 380, 276, 24], f"DIA {self.day} · MÓDULO", size=12, color=WHITE, bold=True, align="center")
        nl = 2 if len(title) * 0.58 * 46 > 520 else 1
        s.text([392, 108, 520, 60 * nl], title, size=46, bold=True, line=1.0)
        sy = 108 + 56 * nl + 12
        s.text([392, sy, 420, 50], subtitle, size=17, color=BODY2)
        y = sy + 64
        for i, t in enumerate(topics):
            s.chip(392 + (i % 2) * 196, y + (i // 2) * 34, t, fill=SURFACE, size=10.5, h=24, w=184)
        s.kodee(kodee, (760, 300, 160, 190))
        return s


_decor = [0]
DECOR = ["excited", "pleased", "electrified", "surprised", "loving", "naughty", "welcoming", "shocked"]


def two_col(s, rel, items, split=0.6, title=None, tone="white", bsize=14.5, region=0, decor=True):
    """Código do snippet à esquerda, tópicos à direita (com um Kodee decorativo, D9)."""
    wl = int(W * split) - 12
    s.code_file(rel, [X0, Y0 + 6, wl, H - 6], region=region)
    bx, bw = X0 + wl + 24, W - wl - 24
    s.bullets([bx, Y0 + 6, bw, H - 6], items, size=bsize, tone=tone, title=title)
    if decor:
        name = DECOR[_decor[0] % len(DECOR)]
        _decor[0] += 1
        s.picture(EMOJI[name], (bx + bw - 76, Y0 + H - 78, 60, 60))


def grid(s, items, cols, rows=None, y=Y0, h=H, gap=20, size=13, title_size=15.5, feature=False):
    rows = rows or -(-len(items) // cols)
    cw = (W - gap * (cols - 1)) / cols
    ch = (h - gap * (rows - 1)) / rows
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        s.card([X0 + c * (cw + gap), y + r * (ch + gap), cw, ch], title=it.get("t"), body=it.get("b"),
               tone=it.get("tone", "white"), size=it.get("size", size), title_size=title_size,
               icon=it.get("i"), chip=it.get("chip"), feature=feature, chip_color=it.get("cc"))


def timeline(s, events, ly=186, card_h=250, size=14):
    n = len(events)
    gap = W / n
    s.rect([X0, ly - 2, W, 4], fill=INK, line=None, shadow=0, preset="rect")
    for i, (year, text) in enumerate(events):
        cx = X0 + gap * i + gap / 2
        atual = i == n - 1
        cw = max(64, len(year) * 9 + 30)
        s.chip(cx - cw / 2, ly - 44, year, fill=ORANGE_DEEP if atual else PURPLE, color=WHITE,
               size=12.5, h=26, w=cw, shadow=2)
        s.rect([cx - 8, ly - 8, 16, 16], fill=WHITE, shadow=0, preset="ellipse")
        s.rect([cx - gap / 2 + 5, ly + 28, gap - 10, card_h], fill=TINT["orange"] if atual else WHITE)
        s.text([cx - gap / 2 + 14, ly + 42, gap - 28, card_h - 24], text, size=size, line=1.15)


def do_dont(s, rel, faca, evite):
    """Faça × Evite empilhados (D12/D23): faixa Success/Error Tint + código em fundo branco."""
    for i, (tone, rotulo, texto) in enumerate([("success", "FAÇA", faca), ("error", "EVITE", evite)]):
        y = Y0 + 4 + i * 180
        s.rect([X0, y, W, 166], fill=TINT[tone])
        s.chip(X0 + 18, y + 18, rotulo, fill=DEEP[tone], color=WHITE, size=12, h=28, w=96, line=None)
        s.text([X0 + 18, y + 60, 210, 100], texto, size=13, color=INK, line=1.15)
        s.code_file(rel, [X0 + 248, y + 12, W - 266, 142], region=i, file=None)


def hora_do_desafio(s, desafios, minutos):
    """Slide 'Hora do desafio' em Orange Tint (D26)."""
    s.rect([X0, Y0, W, H], fill=TINT["orange"])
    cores = {"FÁCIL": SUCCESS, "MÉDIO": INFO, "DESAFIO": ORANGE_DEEP}
    for i, (nivel, nome, arquivo, treina) in enumerate(desafios):
        y = Y0 + 18 + i * 78
        s.rect([X0 + 18, y, 540, 66], fill=WHITE, shadow=3)
        s.chip(X0 + 32, y + 21, nivel, fill=cores[nivel], color=WHITE, size=9.5, h=24, w=84, line=None)
        s.text([X0 + 130, y + 10, 420, 22], nome, size=15.5, bold=True)
        s.text([X0 + 130, y + 36, 420, 20], f"`{arquivo}` · {treina}", size=11, color=BODY2)
    s.text([X0 + 18, Y0 + 262, 540, 90],
           "**1.** Abra o arquivo em `desafios/dia" + str(s.day) + "/` no repositório\n"
           "**2.** Cole tudo em **play.kotlinlang.org** (2.4.21 · JVM) e clique em **Run**\n"
           "**3.** Implemente os `TODO()` até todas as verificações passarem", size=13, spacing=6)
    s.rect([X0 + 586, Y0 + 18, 260, 120], fill=WHITE, shadow=3)
    s.text([X0 + 586, Y0 + 30, 260, 60], f"{minutos} min", size=46, bold=True, align="center",
           color=ORANGE_DEEP)
    s.text([X0 + 586, Y0 + 98, 260, 24], "em duplas, se quiser", size=12, align="center", color=BODY2)
    s.picture(BUILT["qr_repo"], (X0 + 600, Y0 + 158, 96, 96))
    s.text([X0 + 708, Y0 + 168, 140, 80], "Código e\ndesafios no\nrepositório", size=12, color=BODY2)
    s.kodee("jumping", (X0 + 650, Y0 + 262, 150, 96))


def intervalo(s, depois, dica):
    s.rect([X0, Y0 - 40, W, 340], fill=WHITE, radius=18)
    s.text([X0 + 40, Y0 + 10, 520, 90], "Intervalo", size=72, bold=True)
    s.text([X0 + 40, Y0 + 110, 540, 40], f"10 minutos · na volta: **{depois}**", size=22, color=BODY2)
    s.text([X0 + 40, Y0 + 170, 520, 80], dica, size=15, color=BODY2)
    s.kodee("sitting", (X0 + 590, Y0 - 20, 240, 290))


# =====================================================================
def build_deck() -> Deck:
    d = Deck()

    # ------------------------------------------------------------ CAPA
    s = d.raw("cover", "Kotlin: da história ao Multiplatform", min=1, notes="""
FALE: Boas-vindas à turma de Engenharia de Computação do IFCE. "São dois encontros de 2 horas, e vocês só precisam do navegador: tudo roda no Kotlin Playground."
PERGUNTE: "Quem já programou em Java? E em Kotlin? Quem já fez um app Android?" Use as respostas para calibrar exemplos.
DICA: Deixe play.kotlinlang.org aberto numa aba e o repositório em outra.
""")
    s.picture(LOGO["kotlin"], (48, 60, 190, 52), align="left")
    s.chip(48, 140, "MINICURSO · 4 H · 2 DIAS", fill=WHITE, size=10.5, h=24, shadow=2)
    s.text([48, 176, 500, 110], "Kotlin", size=96, bold=True, line=1.0)
    s.text([48, 290, 500, 40], "da história ao Multiplatform", size=28, bold=True, color=PURPLE_DEEP)
    s.text([48, 340, 480, 44], "Engenharia de Computação · Instituto Federal de Educação, Ciência e Tecnologia do Ceará — Campus Fortaleza",
           size=12.5, color=BODY2, line=1.15)
    x = 48
    for t in ["Fundamentos", "Funções", "Classes", "Corrotinas", "Multiplatform"]:
        x += s.chip(x, 404, t, fill=SURFACE, size=10.5, h=26) + 10
    s.text([48, 470, 460, 20], "Robson Freitas Ribeiro · Senior Android Engineer @ CI&T", size=11, color=BODY2)
    s.rect([566, 70, 346, 380], gradient=GRAD, shadow=8, radius=22, angle=45)
    s.rect([592, 96, 294, 328], fill=WHITE, shadow=0, radius=16)
    s.kodee("waving", (606, 112, 266, 296))

    # ------------------------------------------------------------ MINISTRANTE (D4/D14)
    s = d.content("Boas-vindas", "Quem está falando com vocês", min=3, notes="""
FALE: Apresente-se em até 2 minutos: Senior Android Engineer na CI&T desde 2021, mais de 8 anos com Kotlin e Jetpack Compose.
FALE: Cite um projeto por card: GloboPOP (feed de vídeos verticais da Globo, você definiu a arquitetura); BT (app nativo em Compose portado do iOS com ajuda de uma ferramenta de IA que converte Swift em Kotlin, e uma PoC em Kotlin Multiplatform); Ambev (arquitetura assíncrona com corrotinas, app usado em 18+ países); Mediline (agentes de IA que documentam e entregam microsserviços Java/Spring).
FALE: Gere identificação: "Também sou aluno de Engenharia de Computação aqui no IFCE." Conte como a pesquisa em sistemas embarcados no curso te levou ao Android.
FALE: Conexão com o minicurso: Kotlin, corrotinas e KMP, que vocês vão ver, são o seu dia a dia.
""")
    s.picture(BUILT["profile"], (X0, Y0 + 4, 196, 196), border=True)
    s.text([X0 + 226, Y0 + 2, 520, 44], "Robson Freitas Ribeiro", size=32, bold=True)
    s.text([X0 + 226, Y0 + 50, 520, 26], "Senior Android Engineer · CI&T", size=18, bold=True, color=PURPLE_DEEP)
    s.text([X0 + 226, Y0 + 84, 500, 48],
           "8+ anos com **Kotlin** e **Jetpack Compose**, hoje também com agentes de IA.\nAluno de **Engenharia de Computação no IFCE**, como vocês.",
           size=13.5, color=BODY2, line=1.2)
    x = X0 + 226
    for t in ["github.com/robsonribeiroft", "linkedin.com/in/robsonribeiroft"]:
        x += s.chip(x, Y0 + 158, t, fill=SURFACE, size=10.5, h=26, mono=True) + 10
    s.picture(BUILT["qr_linkedin"], (X0 + W - 96, Y0 + 4, 96, 96), border=True)
    s.text([X0 + W - 110, Y0 + 108, 110, 16], "LinkedIn", size=9.5, color=MUTED, align="center")
    projetos = [("Globo · GloboPOP", "Arquitetura do app e feed de vídeos verticais. Tech Lead substituto."),
                ("BT · British Telecom", "App nativo em Compose; IA que converte Swift → Kotlin; PoC em KMP."),
                ("Ambev", "Casos de uso assíncronos com corrotinas; app em 18+ países."),
                ("Mediline · EUA", "Agentes de IA que documentam e entregam microsserviços Java/Spring.")]
    cw = (W - 3 * 16) / 4
    for i, (t, b) in enumerate(projetos):
        s.card([X0 + i * (cw + 16), Y0 + 222, cw, 140], title=t, body=b, size=12, title_size=14)

    # ------------------------------------------------------------ EMENTA
    s = d.content("Boas-vindas", "Ementa: 4 horas em 2 dias", min=2, notes="""
FALE: Dia 1 é a base da linguagem: história rápida, fundamentos e funções. Dia 2 é modelagem com classes, concorrência com corrotinas e uma visão do ecossistema (Java, Multiplatform, Compose).
FALE: Cada dia termina com 3 desafios no Playground, com correção automática: o próprio programa diz ✅ ou ❌.
FALE: Todo código dos slides está no repositório, um arquivo por slide, com o nome no canto do bloco de código.
""")
    for i, (dia, titulo, itens) in enumerate([
        (1, "Fundamentos da linguagem", ["01 · História e filosofia", "02 · Fundamentos: tipos, null safety, when, coleções",
                                         "03 · Funções: lambdas, escopo, extensões", "Desafios: notas, palíndromos, boletim"]),
        (2, "Modelagem e concorrência", ["04 · Classes: data, sealed, object", "05 · Corrotinas e Flow",
                                         "06 · Além do Playground: Java, KMP, Compose", "Desafios: formas, calculadora, downloads"])]):
        cw = W / 2 - 10
        x = X0 + i * (cw + 20)
        s.rect([x, Y0 + 4, cw, 250], fill=WHITE)
        s.chip(x + 18, Y0 + 20, f"DIA {dia} · 2 H", fill=PURPLE, color=WHITE, size=10, h=24, line=None)
        s.text([x + 18, Y0 + 56, cw - 36, 30], titulo, size=19, bold=True, color=PURPLE_DEEP)
        s.text([x + 18, Y0 + 96, cw - 36, 150], "\n".join(itens), size=14, bullets=True, spacing=8)
    s.rect([X0, Y0 + 278, W, 84], fill=TINT["info"])
    s.text([X0 + 20, Y0 + 292, 700, 60],
           "**Ferramenta:** só o navegador, em `play.kotlinlang.org` (Kotlin 2.4.21, alvo JVM)\n**Código:** `" + REPO + "`",
           size=13.5, spacing=8)
    s.picture(BUILT["qr_repo"], (X0 + W - 82, Y0 + 288, 64, 64))

    # ================================================================ DIA 1
    d.day_divider(1, "Fundamentos da linguagem", [
        ("00:00", "Abertura e tour do Playground", "10'", None),
        ("00:10", "01 · História e filosofia", "10'", None),
        ("00:20", "02 · Fundamentos", "35'", None),
        ("00:55", "Intervalo", "10'", "surface"),
        ("01:05", "03 · Funções", "30'", None),
        ("01:35", "Hora do desafio", "25'", "orange"),
        ("02:00", "Fim do Dia 1", "", None),
    ], notes="""
FALE: Mostre a agenda e combine o intervalo. Peça para todos abrirem o Playground agora.
""", contingencia="""
- Atrasou até 10 min: no módulo 02, passe rápido por "Laços e ranges" e "Faça/Evite: coleções" (os arquivos ficam como estudo).
- Atrasou mais de 10 min: reduza "Tipos básicos" a 1 min e encurte a Hora do desafio para 15 min; os desafios 2 e 3 viram tarefa de casa.
- Adiantou: ao vivo, transforme o snippet de lambdas em um exercício ("crie operar com subtração").
""")

    s = d.content("Dia 1 · Abertura", "Tour do Kotlin Playground", min=3, notes="""
FALE: Mostre ao vivo cada número da tela: 1) versão do Kotlin (use 2.4.21); 2) alvo JVM; 3) Run; 4) a área de saída; 5) Share gera um link com o código.
FALE: Regra de ouro: cada arquivo do repositório é autocontido. Copie o arquivo INTEIRO (com o fun main) e cole no lugar do código do Playground.
FALE: Ctrl+Espaço abre o autocompletar; passar o mouse sobre um nome mostra o tipo inferido.
DEMO: Cole snippets/dia1/01_ola_kotlin.kt e rode.
""")
    wx, wy, ww, wh = X0, Y0 + 6, 540, 350
    s.rect([wx, wy, ww, wh], fill=WHITE, radius=12)
    s.rect([wx, wy, ww, 46], fill=SURFACE, shadow=0, radius=12)
    s.chip(wx + 14, wy + 12, "Kotlin 2.4.21 ▾", fill=WHITE, size=10, h=22)
    s.chip(wx + 140, wy + 12, "JVM ▾", fill=WHITE, size=10, h=22)
    s.chip(wx + ww - 186, wy + 12, "Share", fill=WHITE, size=10, h=22)
    s.chip(wx + ww - 100, wy + 12, "▶ Run", fill=PURPLE, color=WHITE, size=10.5, h=22)
    s.add(C("shape.insert", preset="line", rect=[wx, wy + 46, ww, 0.01]),
          C("shape.line", color=INK, width=2))
    s.code([wx + 18, wy + 70, ww - 36, 150], 'fun main() {\n    println("Olá, IFCE!")\n}', file=None, size=15)
    s.rect([wx + 18, wy + 244, ww - 36, 86], fill=SURFACE, shadow=0, radius=8)
    s.text([wx + 34, wy + 256, 300, 20], "Saída", size=10.5, bold=True, color=MUTED)
    s.text([wx + 34, wy + 280, 400, 24], "Olá, IFCE!", size=14, font=MONO)
    for n, (cx, cy) in enumerate([(wx + 70, wy + 2), (wx + 168, wy + 2), (wx + ww - 70, wy + 2),
                                  (wx + ww - 30, wy + 240), (wx + ww - 150, wy + 2)], start=1):
        s.rect([cx - 12, cy - 12, 24, 24], fill=ORANGE_DEEP, shadow=0, preset="ellipse", text=str(n))
        s.add(C("format.size", size=11), C("format.bold", on=True), C("format.color", color=WHITE),
              C("format.margins", left=0, right=0, top=0, bottom=0), C("format.align", align="center"),
              C("format.anchor", anchor="middle"))
    passos = ["**1** · Versão: use **2.4.21**", "**2** · Alvo: **JVM**", "**3** · **Run** executa",
              "**4** · A saída aparece embaixo", "**5** · **Share** gera um link"]
    s.text([X0 + 568, Y0 + 10, 296, 170], "\n".join(passos), size=14, spacing=9)
    s.rect([X0 + 568, Y0 + 190, 296, 166], fill=TINT["purple"])
    s.text([X0 + 584, Y0 + 204, 170, 140],
           "Cole o arquivo **inteiro**, com o `fun main()`.\n`Ctrl+Espaço` autocompleta.", size=12.5, line=1.15)
    s.picture(BUILT["qr_repo"], (X0 + 764, Y0 + 210, 88, 88))
    s.text([X0 + 756, Y0 + 304, 104, 40], "repositório\ndo curso", size=10, color=MUTED, align="center")

    # ================================================================ 01 HISTÓRIA
    d.section("01", "História e filosofia", "Por que uma empresa de ferramentas criou uma linguagem.",
              ["JetBrains, 2010", "Kotlin 1.0", "Google I/O 2017", "Kotlin 2.4"], "sitting", notes="""
FALE: Dez minutos de contexto: a história explica as decisões de design que vamos usar o tempo todo.
""")

    s = d.content("01 · História", "Por que a JetBrains criou o Kotlin?", min=3, notes="""
FALE: Em 2010 a JetBrains mantinha milhões de linhas de Java (IntelliJ IDEA). O Java 6 estava parado: sem lambdas, muito código repetitivo e NullPointerException por toda parte.
FALE: Scala era poderosa, mas compilava devagar. A meta era uma linguagem estática, concisa, segura, 100% interoperável com Java e com ótimo ferramental. Andrey Breslav liderou o design.
FALE: O nome vem da ilha de Kotlin, perto de São Petersburgo — assim como Java também é uma ilha.
PERGUNTE: "Quem já tomou um NullPointerException?" Tony Hoare chamou o null de "erro de um bilhão de dólares".
""")
    s.bullets([X0, Y0 + 6, 440, H - 6], [
        "**2010**: Java 6 parado, sem lambdas e verboso",
        "**NullPointerException**: o \"erro de um bilhão de dólares\"",
        "Scala: poderosa, mas compilação lenta",
        "Meta: **concisa, segura, interoperável**, com ótimo ferramental",
        "Design liderado por **Andrey Breslav**",
    ], size=15, title="O problema")
    s.rect([X0 + 464, Y0 + 6, 400, 196], fill=TINT["purple"])
    s.text([X0 + 486, Y0 + 24, 360, 30], "De onde vem o nome?", size=18, bold=True, color=PURPLE_DEEP)
    s.text([X0 + 486, Y0 + 62, 356, 130],
           "**Kotlin** é uma ilha no Golfo da Finlândia, perto de São Petersburgo, onde fica o time da JetBrains.\nAssim como **Java**, também é o nome de uma ilha.",
           size=14)
    s.kodee("naughty", (X0 + 570, Y0 + 222, 190, 140))

    s = d.content("01 · História", "Linha do tempo: 2010 → 2026", min=3.5, notes="""
FALE: 2010: projeto nasce na JetBrains. 2016: Kotlin 1.0, com compatibilidade retroativa. 2017: no Google I/O, suporte oficial no Android. 2019: Android "Kotlin-first".
FALE: 2023: Kotlin Multiplatform estável. 2024: Kotlin 2.0 com o compilador K2, e o Google passa a apoiar o KMP. 2025: Compose Multiplatform para iOS estável.
FALE: 2026: Kotlin 2.4 (junho) com context parameters e explicit backing fields estáveis; o Playground que vamos usar já está no 2.4.21.
""")
    timeline(s, [("2010", "Nasce o **Projeto Kotlin** na JetBrains."),
                 ("2016", "**Kotlin 1.0** estável."),
                 ("2017", "**Google I/O**: suporte oficial no Android."),
                 ("2019", "Android vira **Kotlin-first**."),
                 ("2023", "**KMP** estável."),
                 ("2024", "**Kotlin 2.0** e o compilador **K2**."),
                 ("2025", "**Compose MP para iOS** estável."),
                 ("2026", "**Kotlin 2.4** e Playground 2.4.21.")], size=13, card_h=150)

    s = d.content("01 · História", "Kotlin hoje: onde a linguagem está", min=3, notes="""
FALE: Android: linguagem oficial e Kotlin-first. Backend: Spring Boot e Ktor. Multiplatform: Netflix, McDonald's, Cash App, Philips, Forbes e o Google Workspace compartilham código Kotlin entre plataformas.
FALE: Dados e IA: Kotlin Notebook, DataFrame e o Koog, framework da JetBrains para agentes de IA.
PERGUNTE: "Em qual dessas áreas vocês se veem trabalhando?"
TRANSIÇÃO: "Para chegar em qualquer uma delas, o caminho começa nos fundamentos."
""")
    grid(s, [
        {"t": "Android", "b": "Linguagem oficial e **Kotlin-first**. Jetpack Compose."},
        {"t": "Backend", "b": "**Spring Boot**, **Ktor**, Exposed, microsserviços na JVM.", "i": LOGO["ktor_icon"]},
        {"t": "Multiplatform", "b": "Android, iOS, desktop e web com lógica (e UI) compartilhada.", "i": LOGO["kmp_icon"]},
        {"t": "Web", "b": "**Kotlin/Wasm** e **Kotlin/JS** no navegador."},
        {"t": "Dados & IA", "b": "Kotlin Notebook, DataFrame e agentes de IA com **Koog**.", "i": LOGO["notebook_icon"]},
        {"t": "Build & Tooling", "b": "**Gradle Kotlin DSL** (`build.gradle.kts`)."},
    ], cols=3, size=13)

    # ================================================================ 02 FUNDAMENTOS
    d.section("02", "Fundamentos", "Sintaxe essencial, sistema de tipos e controle de fluxo.",
              ["val & var", "Null safety", "when", "Coleções"], "greeting", notes="""
FALE: É o módulo mais importante. Rode cada exemplo no Playground e incentive a turma a alterar o código.
""")

    s = d.content("02 · Fundamentos", "Olá, Kotlin!", min=2, notes="""
FALE: Funções de nível superior: o main não precisa de classe. Ponto e vírgula é opcional. println vem da biblioteca padrão.
FALE: Templates de string: "$nome" para variáveis e "${expr}" para expressões.
DEMO: Rode 01_ola_kotlin.kt e mude o raio.
""")
    two_col(s, D1 + "01_ola_kotlin.kt", ["`fun main()` sem classe", "Sem ponto e vírgula", "`println` da stdlib",
                                        "Templates: `$var` e `${expr}`", "`import` como em Java"], split=0.6)

    s = d.content("02 · Fundamentos", "Variáveis: val e var", min=3, notes="""
FALE: val = referência imutável; var = mutável. Regra de ouro: comece com val e troque para var só quando precisar.
FALE: A inferência deduz o tipo, mas a tipagem continua estática. const val é constante de compilação.
PERGUNTE: "val garante que o OBJETO é imutável?" Não: val lista = mutableListOf() ainda aceita add(). Imutável é a referência.
""")
    two_col(s, D1 + "02_val_var.kt", ["`val`: referência **imutável**", "`var`: referência mutável",
                                     "Inferência com tipagem **estática**", "`const val`: constante de compilação",
                                     "Prefira `val` sempre que puder"], split=0.62)

    s = d.content("02 · Fundamentos", "Tipos básicos e a hierarquia", min=3, notes="""
FALE: Tudo é objeto na sintaxe, mas o compilador usa primitivos da JVM quando pode. Não há conversão implícita entre números: use toLong(), toDouble().
FALE: Any é a raiz dos tipos não nulos; Any? fica acima de tudo. Unit é o "void" (um tipo com um único valor). Nothing nunca retorna (throw, TODO()) e é subtipo de todos os tipos.
""")
    s.code_file(D1 + "03_tipos.kt", [X0, Y0 + 6, 500, H - 6])
    bx = X0 + 540
    s.box([bx + 90, Y0 + 10, 150, 42], "Any?", size=15, mono=True)
    s.box([bx + 90, Y0 + 88, 150, 42], "Any", tone="purple", size=15, mono=True)
    for i, t in enumerate(["Int", "String", "Aluno"]):
        s.box([bx + i * 112, Y0 + 178, 100, 42], t, tone="info", size=13, mono=True)
        s.arrow(bx + 50 + i * 112, Y0 + 178, bx + 165, Y0 + 130)
    s.arrow(bx + 165, Y0 + 88, bx + 165, Y0 + 52)
    s.box([bx + 90, Y0 + 290, 150, 42], "Nothing", tone="orange", size=15, mono=True)
    for i in range(3):
        s.arrow(bx + 165, Y0 + 290, bx + 50 + i * 112, Y0 + 220)
    s.text([bx + 248, Y0 + 296, 90, 30], "subtipo\nde todos", size=10, color=MUTED)

    s = d.content("02 · Fundamentos", "Strings: templates e raw strings", min=3, notes="""
FALE: Raw strings com aspas triplas preservam quebras de linha e dispensam escapes (JSON, SQL, regex). trimIndent() remove a indentação comum.
FALE: Interpolação multi-dólar ($$"...") é estável desde o 2.2: útil quando o texto tem "$" literal, como valores em reais.
FALE: buildString monta textos de forma eficiente.
""")
    two_col(s, D1 + "04_strings.kt", ["`$var` e `${expressao}`", "Raw strings `\"\"\"` sem escapes",
                                     "`trimIndent()`", "`$$\"...\"`: multi-dólar (2.2+)", "`buildString { }`"], split=0.62)

    s = d.content("02 · Fundamentos", "Null safety: o fim do NullPointerException", min=5, notes="""
FALE: O sistema de tipos separa String (nunca nulo) de String? (pode ser nulo). O compilador obriga a tratar o nulo antes de usar.
FALE: ?. retorna null em vez de explodir. ?: (Elvis) dá um valor padrão. !! diz "garanto que não é nulo" e lança NPE se for. let com ?. executa o bloco só se não for nulo.
DEMO: No Playground, descomente a linha do "val nada: String = null" e mostre o erro de compilação.
PERGUNTE: "Qual a diferença entre um bug achado em compilação e um em produção às 3h da manhã?"
""")
    two_col(s, D1 + "05_null_safety.kt", ["`T` nunca é nulo; `T?` pode ser", "`?.` chamada segura",
                                         "`?:` Elvis (valor padrão)", "`!!` asserção: use com cautela",
                                         "`?.let { }` só se não for nulo"], split=0.6)

    s = d.content("02 · Fundamentos", "Faça / Evite: lidando com nulos", min=3, notes="""
FALE: Em cima, o idiomático: o tipo String? obriga a decidir o que fazer com o nulo, e ?. + ?: deixam isso explícito numa linha.
FALE: Embaixo, o anti-pattern: !! "cala" o compilador, e o erro só aparece em produção. Em code review, todo !! merece uma pergunta.
DEMO: Rode 06_faca_evite_nulos.kt: a primeira função imprime "sem e-mail"; a segunda gera NullPointerException.
""")
    do_dont(s, D1 + "06_faca_evite_nulos.kt",
            "Trate o nulo de forma **explícita**, com `?.` e `?:`. O código diz o que acontece quando falta o dado.",
            "`!!` troca um erro de **compilação** por um **NPE em produção**.")

    s = d.content("02 · Fundamentos", "if e when são expressões", min=4, notes="""
FALE: if e when retornam valor, por isso não existe operador ternário.
FALE: when substitui o switch: aceita valores, faixas (in), tipos (is), condições e, desde o Kotlin 2.2, guard conditions ("is Int if x in 2..9").
FALE: Com sealed e enum, o when é exaustivo — veremos no Dia 2.
""")
    two_col(s, D1 + "07_if_when.kt", ["`if` retorna valor (sem ternário)", "`when` com valores, faixas e tipos",
                                     "**Guard conditions**: `is T if cond`", "Exaustivo com `sealed` (Dia 2)"], split=0.64)

    s = d.content("02 · Fundamentos", "Laços, ranges e progressões", min=3, notes="""
FALE: for itera sobre qualquer coisa com iterator(). 1..5 inclui o 5; 0..<5 exclui. downTo e step criam progressões.
FALE: withIndex() dá o índice; desestruturação funciona no for, inclusive em mapas. repeat(n) é ótimo para testes.
FALE: Rótulos (externo@) permitem continue/break do laço de fora.
""")
    two_col(s, D1 + "08_lacos.kt", ["`..` inclusivo, `..<` exclusivo", "`downTo` e `step`", "Desestruturação no `for`",
                                   "`repeat(n) { }`", "Rótulos `externo@`"], split=0.62)

    s = d.content("02 · Fundamentos", "Coleções: somente leitura × mutáveis", min=3, notes="""
FALE: List, Set e Map são somente leitura; MutableList, MutableSet e MutableMap são mutáveis.
FALE: "to" é uma função infix que cria um Pair, por isso mapOf("CE" to "Fortaleza") fica tão legível. [] acessa por índice ou chave; getOrNull evita exceções.
""")
    two_col(s, D1 + "09_colecoes.kt", ["`List`, `Set`, `Map`: só leitura", "`MutableList`, `MutableMap`...",
                                      "`to` cria um `Pair`", "`[]` para acesso indexado", "`getOrNull`, `getOrElse`"], split=0.62)

    s = d.content("02 · Fundamentos", "Faça / Evite: expondo coleções", min=2.5, notes="""
FALE: Exponha List e guarde a MutableList como detalhe privado: as regras de negócio (ex.: não aceitar nome vazio) ficam num só lugar.
FALE: Na versão frágil, qualquer parte do programa pode limpar a lista.
SAIBA MAIS: O Kotlin 2.4 tem "explicit backing fields", que eliminam a dupla _alunos/alunos. Está no material extra (v1).
""")
    do_dont(s, D1 + "10_faca_evite_colecoes.kt",
            "Exponha `List` e mantenha a `MutableList` **privada**. As regras ficam num só lugar.",
            "Uma `MutableList` **pública** deixa **qualquer** parte do código alterar os dados.")

    s = d.content("02 · Fundamentos", "Operações funcionais e sequências", min=3, notes="""
FALE: filter, map, groupBy, partition, sumOf, maxBy... A stdlib tem dezenas de operações prontas.
FALE: Em List, cada operação cria uma lista nova. asSequence()/generateSequence são preguiçosas: processam elemento a elemento, e permitem sequências infinitas.
TRANSIÇÃO: "Essas operações recebem funções como parâmetro. Depois do intervalo vamos entender como isso funciona."
""")
    two_col(s, D1 + "11_operacoes_funcionais.kt", ["`filter`, `map`, `groupBy`", "`sumOf`, `maxBy`, `partition`",
                                                  "Sequências: avaliação **preguiçosa**", "`generateSequence` infinita"],
            split=0.68, bsize=13.5)

    s = d.raw("break", "Intervalo", min=10, notes="Intervalo de 10 minutos. Deixe o slide projetado e retome pontualmente.")
    intervalo(s, "Funções", "Enquanto isso, tente mudar um snippet no Playground e rodar de novo.")

    # ================================================================ 03 FUNÇÕES
    d.section("03", "Funções", "Funções de primeira classe, lambdas e extensões.",
              ["Parâmetros nomeados", "Lambdas", "Funções de escopo", "Extensões"], "jumping", notes="""
FALE: Funções são cidadãs de primeira classe: guardadas em variáveis, passadas e retornadas. É a base de corrotinas, DSLs e Compose.
""")

    s = d.content("03 · Funções", "Declarando funções", min=6, notes="""
FALE: Valores padrão eliminam sobrecargas. Argumentos nomeados deixam a chamada autoexplicativa e aceitam qualquer ordem.
FALE: Corpo de expressão (=) para uma linha. vararg recebe N argumentos; o spread (*) passa um array existente.
DEMO: Adicione um parâmetro "sobrenome" com valor padrão e chame com argumento nomeado.
""")
    two_col(s, D1 + "12_funcoes.kt", ["Valores **padrão**", "Argumentos **nomeados**", "Corpo de expressão com `=`",
                                     "`vararg` e spread `*`", "Sem retorno → `Unit`"], split=0.64)

    s = d.content("03 · Funções", "Lambdas e funções de ordem superior", min=8, notes="""
FALE: Tipos de função: (Int, Int) -> Int. Uma lambda é um literal de função entre chaves; com um parâmetro só, ele se chama "it".
FALE: Trailing lambda: se o último parâmetro é uma função, a lambda vai fora dos parênteses. É isso que faz "lista.filter { }" e "launch { }" parecerem sintaxe nativa.
FALE: ::ehPar passa uma função existente. Lambdas capturam variáveis (closures): veja o contador.
EXERCÍCIO RÁPIDO (2 min): chamem operar com subtração usando trailing lambda.
""")
    two_col(s, D1 + "13_lambdas.kt", ["Tipos de função: `(A) -> B`", "Parâmetro implícito `it`", "**Trailing lambda**",
                                     "Referências com `::`", "Closures capturam variáveis"], split=0.64)

    s = d.content("03 · Funções", "Funções de escopo: let, run, with, apply, also", min=8, notes="""
FALE: As cinco executam um bloco no contexto de um objeto. Diferenças: como o objeto é referenciado (this ou it) e o que retornam (o objeto ou o resultado).
FALE: Regra prática: apply para configurar; also para efeitos colaterais (log); let para nulos e transformações; run/with para calcular algo com o objeto.
""")
    fns = [("let", "it", "resultado", "`x?.let { }`: nulos e transformações"),
           ("run", "this", "resultado", "calcular algo com o objeto"),
           ("with", "this", "resultado", "`with(obj) { }`: agrupar chamadas"),
           ("apply", "this", "o objeto", "**configurar** um objeto"),
           ("also", "it", "o objeto", "efeitos colaterais (log)")]
    cw = (W - 4 * 14) / 5
    for i, (fn, ref, ret, uso) in enumerate(fns):
        x = X0 + i * (cw + 14)
        s.rect([x, Y0 + 4, cw, 150], fill=WHITE)
        s.text([x + 14, Y0 + 16, cw - 28, 30], fn, size=22, bold=True, font=MONO, color=PURPLE_DEEP)
        s.text([x + 14, Y0 + 52, cw - 28, 40], f"ref: **{ref}**\nretorna: **{ret}**", size=11.5)
        s.text([x + 14, Y0 + 96, cw - 28, 50], uso, size=11, color=BODY2)
    s.code_file(D1 + "14_funcoes_de_escopo.kt", [X0, Y0 + 180, W, 182])

    s = d.content("03 · Funções", "Extension functions", min=7.5, notes="""
FALE: Extensões adicionam funções e propriedades a tipos que você não controla (String, Double, classes Java), sem herança.
FALE: Por baixo, são funções estáticas que recebem o objeto como primeiro parâmetro: resolvidas pelo tipo declarado, sem polimorfismo. Membros vencem extensões.
FALE: Receptor anulável (String?) pode ser chamado em null: é assim que isNullOrBlank() funciona.
TRANSIÇÃO: "Agora é com vocês: hora do desafio!"
""")
    two_col(s, D1 + "15_extensoes.kt", ["Funções em **qualquer tipo**", "Propriedades de extensão",
                                       "Receptor anulável: `String?.f()`", "Resolvidas **estaticamente**",
                                       "Membros têm prioridade"], split=0.62)

    s = d.content("Dia 1 · Desafios", "Hora do desafio · Dia 1", min=25, notes="""
FALE: Três desafios em ordem de dificuldade. Abram desafios/dia1 no repositório, colem o arquivo inteiro no Playground e rodem: cada verificação imprime ✅ ou ❌.
FALE: Circule pela sala. Desafio 1 (null safety) todo mundo deve terminar; 2 e 3 podem virar tarefa de casa.
DICAS: 1) toDoubleOrNull + takeIf { it in 0.0..10.0 }; 2) lowercase + semAcentos + filter { it.isLetterOrDigit() }; 3) groupBy + mapValues, maxByOrNull.
FECHAMENTO (últimos 3 min): mostre a solução do desafio 1 e lembre que os gabaritos saem no fim do curso.
""")
    hora_do_desafio(s, [("FÁCIL", "Notas válidas", "desafio1_notas_validas.kt", "null safety e Elvis"),
                        ("MÉDIO", "Palíndromos com acento", "desafio2_palindromo.kt", "extensões e Strings"),
                        ("DESAFIO", "Boletim da turma", "desafio3_boletim.kt", "data class, when, groupBy")], 25)

    return _dia2(d)


def _dia2(d: Deck) -> Deck:
    # ================================================================ DIA 2
    d.day_divider(2, "Modelagem, concorrência e ecossistema", [
        ("00:00", "Quiz do Dia 1", "5'", None),
        ("00:05", "04 · Classes e objetos", "30'", None),
        ("00:35", "05 · Corrotinas e Flow", "30'", None),
        ("01:05", "Intervalo", "10'", "surface"),
        ("01:15", "06 · Além do Playground", "15'", None),
        ("01:30", "Hora do desafio e encerramento", "30'", "orange"),
        ("02:00", "Fim do minicurso", "", None),
    ], notes="""
FALE: Retome a energia: "Hoje vamos modelar dados, escrever código concorrente e ver até onde o Kotlin vai além do Playground."
""", contingencia="""
- Atrasou até 10 min: pule "Herança e interfaces" (fica como estudo) e encurte "Por que corrotinas?" para a demo das 100 mil corrotinas.
- Atrasou mais de 10 min: no módulo 06, faça só a demo de interop e o slide de KMP; ecossistema e novidades viram leitura. A Hora do desafio fica com 15 min.
- Adiantou: rode a demo de Compose (bônus) com mais calma e proponha modificar o contador.
""")

    s = d.content("Dia 2 · Abertura", "Quiz relâmpago do Dia 1", min=4.5, notes="""
FALE: Leia cada pergunta e peça respostas em voz alta. Valorize quem errar e explicar o raciocínio.
RESPOSTA 1: imprime -1. x é null, então x?.length é null e o Elvis devolve -1.
RESPOSTA 2: val é referência imutável (não pode ser reatribuída); var pode. O conteúdo de uma MutableList em val ainda muda.
RESPOSTA 3: apply retorna o próprio objeto (útil para configurar); let retorna o resultado da lambda (aqui, 4).
""")
    perguntas = [("1", "O que este código imprime?", 'val x: String? = null\nprintln(x?.length ?: -1)'),
                 ("2", "Qual a diferença?", 'val nomes = mutableListOf("Ana")\nvar total = 0'),
                 ("3", "O que cada uma retorna?", 'Conexao().apply { porta = 80 }\n"ifce".let { it.length }')]
    for i, (n, q, code) in enumerate(perguntas):
        y = Y0 + 4 + i * 122
        s.rect([X0, y, W, 108], fill=TINT["purple"])
        s.rect([X0 + 18, y + 30, 46, 46], fill=PURPLE, shadow=0, preset="ellipse", text=n)
        s.add(C("format.size", size=20), C("format.bold", on=True), C("format.color", color=WHITE),
              C("format.align", align="center"), C("format.anchor", anchor="middle"),
              C("format.margins", left=0, right=0, top=0, bottom=0))
        s.text([X0 + 84, y + 40, 250, 30], q, size=17, bold=True, color=PURPLE_DEEP)
        s.code([X0 + 340, y + 14, 440, 80], code, file=None, max_size=17)
    s.kodee("surprised", (X0 + W - 70, Y0 + H - 64, 56, 56), emoji=True)

    # ================================================================ 04 CLASSES
    d.section("04", "Classes e objetos", "Orientação a objetos moderna, com menos cerimônia.",
              ["Propriedades", "data class", "sealed + when", "object"], "sharing", notes="""
FALE: Kotlin é orientada a objetos e funcional ao mesmo tempo. Aqui vemos como a linguagem reduz o código repetitivo da OO e incentiva imutabilidade.
""")

    s = d.content("04 · Classes", "Classes, construtores e propriedades", min=5, notes="""
FALE: Construtor primário no cabeçalho; val/var nos parâmetros já declaram propriedades. init roda na construção. Não existe "new".
FALE: Propriedades têm getter/setter gerados; customize com get()/set() e use "field" para o valor guardado. vagas é calculada a cada acesso.
DEMO: Tente t.capacidade = 0 e veja o require lançar a exceção.
""")
    two_col(s, D2 + "01_classes.kt", ["Construtor **primário** no cabeçalho", "`val`/`var` declaram propriedades",
                                     "Bloco `init`", "`get()`/`set()` e `field`", "Sem `new`"], split=0.6)

    s = d.content("04 · Classes", "data class", min=5, notes="""
FALE: data class gera equals, hashCode, toString, copy e componentN a partir do construtor.
FALE: copy() é a base da imutabilidade: em vez de alterar, crie uma cópia com o campo novo. É assim que o estado funciona no Compose.
PERGUNTE: "== entre dois objetos iguais de uma classe normal dá true?" Não: compara referência. Em data class, compara conteúdo.
""")
    two_col(s, D2 + "02_data_class.kt", ["`equals`, `hashCode`, `toString`", "`copy()` para atualizar imutavelmente",
                                        "`==` estrutural × `===` referência", "Desestruturação", "Ideal para DTOs e estado"],
            split=0.62)

    s = d.content("04 · Classes", "Herança e interfaces", min=4.5, notes="""
FALE: Classes e métodos são FINAL por padrão (Effective Java: "projete para herança ou proíba-a"). Para herdar, open; para sobrescrever, override é obrigatório.
FALE: Interfaces podem ter implementação padrão e propriedades abstratas, mas não guardam estado. Uma classe base, várias interfaces.
""")
    two_col(s, D2 + "03_heranca_interfaces.kt", ["Classes são `final` por padrão", "`open` permite herança",
                                                "`override` é obrigatório", "Interfaces com implementação padrão"],
            split=0.66, bsize=13.5)

    s = d.content("04 · Classes", "sealed: hierarquias fechadas e when exaustivo", min=6, notes="""
FALE: Uma sealed interface tem todos os subtipos conhecidos em compilação. O when sobre ela é EXAUSTIVO: sem else, e se surgir um estado novo, o compilador aponta todos os lugares a atualizar.
FALE: Padrão clássico: estados de tela (Carregando, Sucesso, Erro). data object dá um toString legível a singletons.
DEMO: Adicione "data object Vazio : EstadoTela" e mostre o erro de compilação no when.
""")
    two_col(s, D2 + "04_sealed_when.kt", ["Subtipos conhecidos em **compilação**", "`when` **exaustivo**, sem `else`",
                                         "**Guard conditions** no `when`", "Modela estados de UI"], split=0.68, bsize=13.5)

    s = d.content("04 · Classes", "Faça / Evite: when com sealed", min=4, notes="""
FALE: Com when exaustivo, criar Pagamento.Cripto quebra a compilação exatamente onde é preciso decidir a taxa. Com else, o código compila e cobra a taxa errada em silêncio.
DEMO: Adicione "data object Cripto : Pagamento" e veja qual função o compilador acusa.
""")
    do_dont(s, D2 + "05_faca_evite_when.kt",
            "`when` **exaustivo**: um tipo novo quebra a compilação **onde precisa** de decisão.",
            "`else` genérico **engole** tipos novos e erra **em silêncio**.")

    s = d.content("04 · Classes", "enum, object e companion object", min=5, notes="""
FALE: enum class com propriedades e métodos; entries lista os valores.
FALE: object declara um singleton thread-safe, sem código de padrão Singleton. companion object substitui o "static": útil para factories e constantes (aqui com construtor privado).
TRANSIÇÃO: "Já sabemos modelar dados. Agora: como fazer várias coisas ao mesmo tempo?"
""")
    two_col(s, D2 + "06_enum_object.kt", ["`enum class` com `entries`", "`object`: **singleton**",
                                         "`companion object` no lugar de `static`", "Factory com construtor privado"],
            split=0.62)

    # ================================================================ 05 CORROTINAS
    d.section("05", "Corrotinas", "Concorrência leve, estruturada e legível.",
              ["suspend", "launch & async", "Escopos", "Flow"], "regular-156px-more", notes="""
FALE: Corrotinas são o modelo de concorrência do Kotlin: código assíncrono que se lê como sequencial. O Playground já traz a biblioteca kotlinx.coroutines.
FALE: Gancho com Sistemas Operacionais: threads, escalonamento e I/O bloqueante × não bloqueante.
""")

    s = d.content("05 · Corrotinas", "Por que corrotinas?", min=5, notes="""
FALE: Uma thread do SO custa por volta de 1 MB de pilha e troca de contexto no kernel. Corrotinas rodam sobre poucas threads e SUSPENDEM sem bloquear.
DEMO: Rode 07_corrotinas_leves.kt: 100 mil corrotinas com delay(1000) terminam em pouco mais de 1 s.
FALE: Comparação: callbacks, Futures e RxJava funcionam, mas corrotinas mantêm o código sequencial e trazem cancelamento e Flow, em todas as plataformas Kotlin.
""")
    two_col(s, D2 + "07_corrotinas_leves.kt", ["Thread do SO: ~1 MB de pilha", "Corrotina: poucos **bytes**",
                                              "Suspende **sem bloquear** a thread", "100 mil em ~1 s no Playground"],
            split=0.6)

    s = d.content("05 · Corrotinas", "Funções suspend", min=5, notes="""
FALE: "suspend" marca uma função que pode pausar sem bloquear a thread; só pode ser chamada de outra suspend ou de uma corrotina.
FALE: O compilador transforma a função numa máquina de estados (Continuation Passing Style): cada ponto de suspensão vira um estado. Ótimo gancho com compiladores.
""")
    s.code_file(D2 + "08_suspend.kt", [X0, Y0 + 6, 500, H - 6])
    sx = X0 + 524
    s.text([sx, Y0 + 6, 340, 24], "O que o compilador gera", size=16, bold=True, color=PURPLE_DEEP)
    for i, (a, b) in enumerate([("estado 0", "chama buscarAluno()"), ("estado 1", "retoma → buscarNotas()"),
                                ("estado 2", "retoma → monta o boletim")]):
        y = Y0 + 44 + i * 96
        s.rect([sx, y, 340, 70], fill=WHITE)
        s.text([sx + 16, y + 12, 100, 46], a, size=14, bold=True, color=PURPLE_DEEP, font=MONO, anchor="middle")
        s.text([sx + 120, y + 12, 210, 46], b, size=12.5, anchor="middle")
        if i < 2:
            s.arrow(sx + 170, y + 70, sx + 170, y + 96)
    s.text([sx, Y0 + 336, 340, 24], "Máquina de estados + `Continuation`", size=11.5, color=MUTED)

    s = d.content("05 · Corrotinas", "launch, async e runBlocking", min=6, notes="""
FALE: runBlocking faz a ponte entre o mundo bloqueante e o de corrotinas (main e testes). launch dispara e retorna um Job. async retorna um Deferred; await() espera o resultado.
DEMO: Rode 09_launch_async.kt: duas chamadas de 1 s levam ~1 s em paralelo. Troque os async por chamadas diretas e compare: ~2 s.
""")
    two_col(s, D2 + "09_launch_async.kt", ["`runBlocking`: ponte para `main`", "`launch` → `Job`",
                                          "`async` → `Deferred<T>` + `await()`", "Paralelismo **explícito**"], split=0.64)

    s = d.content("05 · Corrotinas", "Concorrência estruturada", min=6, notes="""
FALE: Toda corrotina nasce num escopo e forma uma ÁRVORE: o pai só termina quando os filhos terminam; cancelar o pai cancela os filhos; erro num filho cancela os irmãos (exceto em supervisorScope).
FALE: Isso elimina vazamentos: nada fica rodando "solto" depois que a tela fecha. No Android: viewModelScope e lifecycleScope.
""")
    s.code_file(D2 + "10_concorrencia_estruturada.kt", [X0, Y0 + 6, 540, H - 6])
    tx = X0 + 564
    s.box([tx + 70, Y0 + 10, 160, 46], "coroutineScope", tone="purple", size=13, mono=True)
    for i, t in enumerate(["perfil", "notas", "avisos"]):
        bx = tx + i * 104
        s.box([bx, Y0 + 116, 92, 44], f"async\n{t}", size=11, mono=True)
        s.arrow(tx + 150, Y0 + 56, bx + 46, Y0 + 116)
    s.bullets([tx, Y0 + 186, 300, 176], ["Pai espera os filhos", "Cancelar o pai cancela os filhos",
                                         "Erro num filho cancela os irmãos", "`supervisorScope` isola falhas"],
              size=13, tone="purple")

    s = d.content("05 · Corrotinas", "Faça / Evite: escopo das corrotinas", min=3.5, notes="""
FALE: Um escopo com ciclo de vida (viewModelScope, um CoroutineScope cancelado ao fechar a tela) garante que nada continua rodando sem dono.
FALE: GlobalScope não tem dono: o trabalho sobrevive à tela, gasta recursos e pode causar bugs difíceis. A própria biblioteca marca como DelicateCoroutinesApi.
DEMO: Rode 11_faca_evite_escopo.kt: "notas" nunca aparece (foi cancelado); a corrotina do GlobalScope continua e imprime.
""")
    do_dont(s, D2 + "11_faca_evite_escopo.kt",
            "Escopo com **ciclo de vida**: fechar a tela **cancela** o trabalho.",
            "`GlobalScope` não tem dono: o trabalho **vaza** e ninguém cancela.")

    s = d.content("05 · Corrotinas", "Flow: fluxos assíncronos de dados", min=4, notes="""
FALE: suspend retorna UM valor; Flow emite VÁRIOS ao longo do tempo. É frio: só executa no collect.
FALE: Operadores familiares (map, filter) e de tempo (debounce), tratamento de erro com catch. Exemplos reais: leitura de sensores, busca enquanto o usuário digita, atualizações do banco.
TRANSIÇÃO: "Intervalo! Na volta: Kotlin além do Playground."
""")
    two_col(s, D2 + "12_flow.kt", ["`Flow<T>`: vários valores no tempo", "**Frio**: executa no `collect`",
                                  "`map`, `filter`, `catch`", "Base de UIs reativas"], split=0.64)

    s = d.raw("break", "Intervalo", min=10, notes="Intervalo de 10 minutos.")
    intervalo(s, "Além do Playground", "Que tal rodar 07_corrotinas_leves.kt com 1 milhão de corrotinas?")

    # ================================================================ 06 ALÉM DO PLAYGROUND
    d.section("06", "Além do Playground", "Java, Multiplatform, Compose e o ecossistema.",
              ["Interop Java", "KMP", "Compose MP", "Kotlin 2.4"], "in-love", notes="""
FALE: Quinze minutos de panorama: o que dá para fazer com Kotlin fora do navegador.
""")

    s = d.content("06 · Além do Playground", "100% interoperável com Java", min=4, notes="""
FALE: Kotlin roda na JVM e usa QUALQUER biblioteca Java: o próprio JDK (java.time, java.util), Spring, Jackson, JDBC...
FALE: Getters viram propriedades (getDayOfWeek() vira dayOfWeek). Interfaces Java de um método (Comparator, Runnable) aceitam lambdas (conversão SAM). E as extensões do Kotlin funcionam em classes Java (joinToString num ArrayList).
DEMO: Rode 13_interop_java.kt no Playground: tudo isso é Java, chamado de Kotlin.
FALE: O caminho inverso também funciona: Java chama Kotlin com @JvmStatic, @JvmOverloads etc. (material extra).
""")
    two_col(s, D2 + "13_interop_java.kt", ["Qualquer biblioteca da **JVM**", "Getters viram **propriedades**",
                                          "**SAM**: lambda vira interface Java", "Extensões Kotlin em classes Java"],
            split=0.7, bsize=13)

    s = d.content("06 · Além do Playground", "Kotlin Multiplatform (KMP)", min=3.5, notes="""
FALE: O código comum (commonMain) contém lógica de negócio, rede e dados. Cada plataforma tem seu source set para o que é específico. O compilador gera artefatos NATIVOS: .aar para Android, framework para iOS (via Kotlin/Native e LLVM), .jar para desktop, Wasm/JS para web.
FALE: Estável desde novembro de 2023; o Google recomenda para compartilhar lógica entre Android e iOS. Casos: Google Workspace, Netflix, McDonald's, Cash App.
""")
    s.picture(LOGO["kmp"], (X0, Y0 + 2, 300, 34), align="left")
    s.box([X0 + 282, Y0 + 66, 300, 74], "commonMain\nlógica de negócio, rede, dados", tone="purple", size=14)
    plats = [("androidMain", "Android\n.aar / APK"), ("iosMain", "iOS\nframework Swift"),
             ("jvmMain", "Desktop\n.jar"), ("wasmJsMain", "Web\nWasm / JS"), ("server", "Backend\nKtor / Spring")]
    pw = (W - 4 * 16) / 5
    for i, (ss, lab) in enumerate(plats):
        px = X0 + i * (pw + 16)
        s.arrow(X0 + 432, Y0 + 140, px + pw / 2, Y0 + 210)
        s.rect([px, Y0 + 210, pw, 140], fill=WHITE)
        s.text([px + 12, Y0 + 224, pw - 24, 22], ss, size=12, bold=True, font=MONO, color=PURPLE_DEEP)
        s.text([px + 12, Y0 + 258, pw - 24, 80], lab, size=14, line=1.15)

    s = d.content("06 · Além do Playground", "Compose Multiplatform: demo no navegador", min=4, notes="""
DEMO (validar antes da aula!): No Playground, mude o alvo para "Compose (Wasm)" e cole 14_bonus_compose.kt. Se a função de entrada não existir na versão do Playground, use o template de Compose dele e cole só a função Contador().
FALE: A mesma função @Composable roda em Android, iOS (estável desde 2025), desktop e web. UI = f(estado): quando "cliques" muda, o Compose redesenha só o necessário.
FALE: "var cliques by remember { mutableStateOf(0) }" usa delegação de propriedade, um recurso que está no material extra.
""")
    two_col(s, D2 + "14_bonus_compose.kt", ["UI declarativa: **UI = f(estado)**", "Android, **iOS**, desktop e **web**",
                                           "Alvo **Compose (Wasm)** no Playground", "Hot Reload no desktop"],
            split=0.66, bsize=13.5, decor=False)
    s.picture(LOGO["cmp_icon"], (X0 + W - 110, Y0 + 296, 44, 50))
    s.picture(LOGO["hotreload_icon"], (X0 + W - 58, Y0 + 296, 44, 50))

    s = d.content("06 · Além do Playground", "O ecossistema", min=1.5, notes="""
FALE: Um minuto por área, só para dar o mapa: Android (Compose), backend (Spring Boot e Ktor), dados e IA (Kotlin Notebook, Koog), ferramentas (IntelliJ IDEA, Android Studio, Gradle) e testes (kotlin.test, MockK).
""")
    grid(s, [
        {"t": "Android", "b": "Jetpack Compose, Kotlin-first."},
        {"t": "Backend", "b": "**Spring Boot** e **Ktor** com corrotinas.", "i": LOGO["ktor_icon"]},
        {"t": "Multiplatform", "b": "KMP + **Compose MP**.", "i": LOGO["cmp_icon"]},
        {"t": "Dados & IA", "b": "Kotlin Notebook, DataFrame, **Koog**.", "i": LOGO["notebook_icon"]},
        {"t": "Ferramentas", "b": "IntelliJ IDEA, Android Studio, Gradle KTS."},
        {"t": "Testes", "b": "`kotlin.test`, JUnit, **MockK**, Kotest."},
    ], cols=3, size=13)

    s = d.content("06 · Além do Playground", "Novidades do Kotlin 2.x", min=1.5, notes="""
FALE: 2.0 (2024): compilador K2. 2.1–2.2: guard conditions no when e interpolação multi-dólar (vocês usaram as duas!). 2.4 (jun/2026): context parameters e explicit backing fields estáveis, UUID estável e Java 26. 2.4.20 (set/2026): melhorias em stack traces de corrotinas e no Swift export.
DICA: Antes da aula, confira kotlinlang.org/docs/whatsnew.html.
""")
    timeline(s, [("2.0", "Compilador **K2** estável e mais rápido."),
                 ("2.1", "Preview: guard conditions e `$$`."),
                 ("2.2", "Guard conditions e multi-dólar **estáveis**."),
                 ("2.4", "**Context parameters** e **explicit backing fields** estáveis."),
                 ("2.4.20", "Stack traces de corrotinas e Swift export.")], size=14, card_h=160)

    s = d.content("Dia 2 · Desafios", "Hora do desafio · Dia 2", min=22, notes="""
FALE: Três desafios: formas (sealed + when), calculadora (recursão) e downloads (corrotinas). Mesmo processo: colar, rodar, ver ✅/❌.
DICAS: 1) when (this) sem else; 2) avaliar chama avaliar nos filhos; 3) coroutineScope { arquivos.map { async { baixar(it) } }.awaitAll().sum() }.
FECHAMENTO: Mostre a solução do desafio 3 ao vivo: é o resumo do módulo de corrotinas.
""")
    hora_do_desafio(s, [("FÁCIL", "Formas geométricas", "desafio1_formas.kt", "sealed e when exaustivo"),
                        ("MÉDIO", "Calculadora de expressões", "desafio2_calculadora.kt", "sealed e recursão"),
                        ("DESAFIO", "Downloads paralelos", "desafio3_downloads.kt", "async, timeout e Flow")], 20)

    s = d.content("Encerramento", "Para continuar estudando", min=3, notes="""
FALE: Indique a documentação oficial, os Kotlin Koans e a trilha de KMP.
FALE: No repositório, a pasta material-extra/v1-8h tem a versão estendida (8 h) do curso: DSLs, context parameters, generics, delegação, interop Java → Kotlin, Spring, testes e mais.
FALE: Os gabaritos dos desafios estão na branch "gabaritos" do repositório (publique agora: git push origin gabaritos).
""")
    grid(s, [
        {"t": "Documentação", "b": "`kotlinlang.org/docs`: guia oficial com exemplos executáveis.", "i": LOGO["kotlin_icon"]},
        {"t": "Kotlin Koans", "b": "Exercícios interativos com correção automática."},
        {"t": "Trilha KMP", "b": "Assistente `kmp.jetbrains.com` e a documentação de KMP.", "i": LOGO["kmp_icon"]},
        {"t": "Material extra", "b": "Versão de 8 h do curso em `material-extra/v1-8h`.", "tone": "info"},
        {"t": "Gabaritos", "b": "Branch `gabaritos` do repositório.", "tone": "success"},
        {"t": "Comunidade", "b": "Kotlin Slack, KotlinConf (YouTube), GDGs e meetups em Fortaleza.", "i": EMOJI["welcoming"]},
    ], cols=3, h=270, size=12.5, title_size=15)
    s.picture(BUILT["qr_repo"], (X0, Y0 + 292, 70, 70))
    s.text([X0 + 84, Y0 + 312, 600, 30], "**Repositório:** `" + REPO + "`", size=13)
    s.picture(LOGO["foundation"], (X0 + W - 230, Y0 + 316, 230, 30), align="right")

    s = d.raw("closing", "Obrigado!", min=5, notes="""
FALE: Recapitule em uma frase: Kotlin é concisa, segura, interoperável com todo o ecossistema Java, tem concorrência moderna com corrotinas e roda em todas as plataformas com KMP.
FALE: Convide a turma a terminar os desafios em casa e a conectar no LinkedIn/GitHub.
CURIOSIDADE: Este deck foi construído de forma agêntica: um agente de IA enviou os comandos ao DeckCraft pelo servidor MCP, slide por slide (deck/tools no repositório).
""")
    s.rect([48, 60, 864, 400], gradient=GRAD, shadow=8, radius=24, angle=45)
    s.text([90, 100, 520, 110], "Obrigado!", size=84, bold=True, color=WHITE, line=1.0)
    s.text([90, 214, 480, 40], "Perguntas? Vamos conversar sobre Kotlin.", size=22, color=WHITE, bold=True)
    s.text([90, 272, 480, 120],
           "Robson Freitas Ribeiro\ngithub.com/robsonribeiroft\nlinkedin.com/in/robsonribeiroft\nGabaritos: branch `gabaritos` do repositório",
           size=15, color=WHITE, line=1.3, on_dark=True)
    s.rect([620, 92, 260, 300], fill=WHITE, shadow=0, radius=20)
    s.kodee("jumping", (636, 106, 228, 272))
    s.picture(LOGO["kotlin"], (48, 480, 120, 34), align="left")
    s.text([200, 490, 712, 20], FOOTER, size=10, color=MUTED, align="right")
    return d
