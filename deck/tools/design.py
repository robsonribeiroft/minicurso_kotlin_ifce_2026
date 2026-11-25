"""Design system v2 — neobrutalismo atenuado, light mode, tokens Kotlin (PRD D5–D8, D20).

Regras:
  • slides de conteúdo: só cores sólidas; tints apenas por significado
    (purple = conceito, orange = atenção, info = saiba mais, success/error = Faça/Evite)
  • gradiente assinatura (#7F52FF → #C711E1 → #F88909) só em capa, divisores e encerramento
  • borda #121216 de 2 pt e sombra dura de 4 pt; código sempre em fundo #FFFFFF

Cada componente apenas GERA comandos DeckCraft; quem executa é o build.py, via MCP (`batch`).
Slide: 960 × 540 pt. Área útil: x 48..912, y 116..490.
"""
from __future__ import annotations

import os
import re
import struct
import textwrap

# ------------------------------------------------------------------ tokens
BG = "#FAFAFC"            # fundo
INK = "#121216"           # texto e bordas
WHITE = "#FFFFFF"
SURFACE = "#F2F2F7"       # Surface Subtle: tags neutras, código inline
BORDER_SUBTLE = "#DCDCE6"
MUTED = "#76768A"         # Ink Muted: legendas e referências
BODY2 = "#3D3D4A"         # texto secundário (subtítulos) com contraste AA

PURPLE = "#7F52FF"        # Kotlin Purple
MAGENTA = "#C711E1"       # Kotlin Magenta
ORANGE = "#F88909"        # Kotlin Orange (só em gradiente / áreas grandes)
PURPLE_DEEP = "#5B32D6"
ORANGE_DEEP = "#C26100"
SUCCESS = "#059669"
ERROR = "#E11D48"
INFO = "#2563EB"

TINT = {"purple": "#F3EEFF", "orange": "#FFF7ED", "info": "#EFF6FF",
        "success": "#ECFDF5", "error": "#FFF1F2", "white": WHITE, "surface": SURFACE}
DEEP = {"purple": PURPLE_DEEP, "orange": ORANGE_DEEP, "info": INFO,
        "success": SUCCESS, "error": ERROR, "white": PURPLE_DEEP, "surface": INK}

GRAD = [[0, PURPLE], [0.5, MAGENTA], [1, ORANGE]]     # gradiente assinatura

FONT = "Inter"
MONO = "JetBrains Mono NL"   # sem ligaduras: "->" aparece como digitado

SYN = {"kw": PURPLE, "type": INFO, "str": SUCCESS, "tpl": PURPLE_DEEP,
       "num": ORANGE_DEEP, "ann": ORANGE_DEEP, "com": MUTED}

BORDER_W = 2
SHADOW = 4

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS_BUILD = os.path.join(ROOT, "deck", "build", "assets")
FOOTER = "Minicurso de Kotlin · Engenharia de Computação · IFCE Fortaleza · 2026"


def C(command: str, **params) -> dict:
    return {"command": command, "params": params}


# ------------------------------------------------------------------ imagens
def img_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as f:
        head = f.read(32)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", head[16:24])
    if head[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", head[6:10])
    raise ValueError(f"formato não suportado: {path}")


def asset(rel: str) -> str:
    small = os.path.join(ASSETS_BUILD, os.path.basename(rel))
    return small if os.path.exists(small) else os.path.join(ROOT, rel)


LOGO = {
    "kotlin": "Kotlin Ecosystem Logos/Kotlin/Primary/Dark/Kotlin Logo.png",
    "kotlin_white": "Kotlin Ecosystem Logos/Kotlin/Primary/Light/Kotlin Logo.png",
    "kotlin_icon": "Kotlin Ecosystem Logos/Kotlin/Primary/Kotlin icon.png",
    "kmp": "Kotlin Ecosystem Logos/Kotlin Multiplatform/Primary/Dark/Kotlin Multiplatform Logo.png",
    "kmp_icon": "Kotlin Ecosystem Logos/Kotlin Multiplatform/Primary/Kotlin Multiplatform icon.png",
    "cmp_icon": "Kotlin Ecosystem Logos/Compose Multiplatform/Primary/Compose Multiplatform icon.png",
    "ktor_icon": "Kotlin Ecosystem Logos/Ktor/Primary/Ktor icon.png",
    "exposed_icon": "Kotlin Ecosystem Logos/Exposed/Primary/Exposed icon.png",
    "notebook_icon": "Kotlin Ecosystem Logos/Kotlin Notebook/Kotlin Notebook icon.png",
    "hotreload_icon": "Kotlin Ecosystem Logos/Compose Hot Reload/Compose Hot Reload icon.png",
    "foundation": "Kotlin Ecosystem Logos/Kotlin Foundation /Kotlin Foundation black.png",
}
KODEE = {n: f"kotlin_mascot_2/Digital/PNG/Kodee_Assets_Digital_Kodee-{n}.png"
         for n in ["waving", "greeting", "jumping", "sitting", "sharing", "naughty", "in-love",
                   "regular-156px-more"]}
EMOJI = {n: f"kotlin_mascot_2/Digital/Emoji/png/kodee-{n}.png"
         for n in ["welcoming", "electrified", "grumpy", "naughty", "loving", "sad", "excited",
                   "surprised", "frightened", "broken-hearted", "frustrated", "shocked", "angry",
                   "lost", "pleased"]}
BUILT = {k: os.path.join(ASSETS_BUILD, v) for k, v in
         {"profile": "profile.png", "qr_repo": "qr_repo.png", "qr_linkedin": "qr_linkedin.png"}.items()}


# ------------------------------------------------------------------ snippets
def snippet_regions(rel: str) -> list[str]:
    """Trechos entre //sampleStart e //sampleEnd (ou o arquivo todo, sem o cabeçalho)."""
    text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    if text.startswith("// ══"):
        end = text.index("\n// ══", 5)
        text = text[text.index("\n", end + 1) + 1:]
    regions = re.findall(r"//sampleStart\n(.*?)//sampleEnd", text, re.S)
    if not regions:
        regions = [text]
    return [textwrap.dedent(r).strip("\n") for r in regions]


# ------------------------------------------------------------------ texto rico
_RICH = re.compile(r"(\*\*.+?\*\*|`[^`]+`|(?<![\w*])\*[^*\s][^*]*\*(?![\w*]))")


def parse_rich(text: str):
    """`**negrito**`, `*itálico*` e `` `código` `` → (texto, spans[(par, ini, fim, tipo)])."""
    paras, spans = [], []
    for pi, line in enumerate(text.split("\n")):
        out = ""
        for t in _RICH.split(line):
            if len(t) > 4 and t.startswith("**") and t.endswith("**"):
                s = len(out); out += t[2:-2]; spans.append((pi, s, len(out), "b"))
            elif len(t) > 2 and t.startswith("`") and t.endswith("`"):
                s = len(out); out += t[1:-1]; spans.append((pi, s, len(out), "code"))
            elif len(t) > 2 and t.startswith("*") and t.endswith("*"):
                s = len(out); out += t[1:-1]; spans.append((pi, s, len(out), "i"))
            else:
                out += t
        paras.append(out)
    return "\n".join(paras), spans


def span_cmds(spans, bold_color=INK, on_dark=False) -> list[dict]:
    if not spans:
        return []
    cmds = [C("text.edit")]
    for p, a, b, kind in spans:
        cmds.append(C("text.select", anchor=[p, a], caret=[p, b]))
        if kind == "b":
            cmds += [C("format.bold", on=True), C("format.color", color=bold_color)]
        elif kind == "i":
            cmds += [C("format.italic", on=True)]
        else:
            cmds += [C("format.font", family=MONO)]
            if not on_dark:
                cmds += [C("format.color", color=PURPLE_DEEP), C("format.highlight", color=SURFACE)]
    cmds.append(C("text.exit"))
    return cmds


# ------------------------------------------------------------------ realce Kotlin
KW = set("""fun val var if else when for while do return class object interface data sealed enum
open abstract override private public internal protected companion init constructor by in out is
as null true false this super try catch finally throw import package suspend inline reified
typealias value lateinit const operator infix tailrec where get set vararg crossinline noinline
annotation inner expect actual context field break continue""".split())


def _string_spans(pi, line, start, end, spans):
    """Divide uma string literal em trechos de texto e templates ($x, ${...}, $$x)."""
    k, seg = start, start
    while k < end:
        if line[k] == "$" and k + 1 < end and (line[k + 1] in "{$" or line[k + 1].isalpha()):
            st = k
            while k < end and line[k] == "$":
                k += 1
            if k < end and line[k] == "{":
                depth, m = 0, k
                while m < end:
                    if line[m] == "{":
                        depth += 1
                    elif line[m] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    m += 1
                if st > seg:
                    spans.append((pi, seg, st, "str"))
                spans.append((pi, st, k + 1, "tpl")); spans.append((pi, m, m + 1, "tpl"))
                seg = k = m + 1
            elif k < end and line[k].isalpha():
                if st > seg:
                    spans.append((pi, seg, st, "str"))
                m = k
                while m < end and (line[m].isalnum() or line[m] == "_"):
                    m += 1
                spans.append((pi, st, m, "tpl")); seg = k = m
        else:
            k += 1
    if seg < end:
        spans.append((pi, seg, end, "str"))


def highlight(code: str):
    spans = []
    in_triple = False
    for pi, line in enumerate(code.split("\n")):
        i, n = 0, len(line)
        prev_word = ""
        while i < n:
            if in_triple:
                j = line.find('"""', i)
                end = n if j < 0 else j + 3
                _string_spans(pi, line, i, end, spans)
                in_triple = j < 0
                i = end
                continue
            ch = line[i]
            if line.startswith("//", i):
                spans.append((pi, i, n, "com")); break
            if line.startswith("/*", i):
                j = line.find("*/", i + 2); end = n if j < 0 else j + 2
                spans.append((pi, i, end, "com")); i = end; continue
            if ch == "$" and line[i:].lstrip("$").startswith('"'):          # $$"..." multi-dólar
                q = i + len(line[i:]) - len(line[i:].lstrip("$"))
                j = q + 1
                while j < n and line[j] != '"':
                    j += 1
                _string_spans(pi, line, i, min(j + 1, n), spans); i = j + 1; continue
            if line.startswith('"""', i):
                j = line.find('"""', i + 3)
                if j < 0:
                    _string_spans(pi, line, i, n, spans); in_triple = True; break
                _string_spans(pi, line, i, j + 3, spans); i = j + 3; continue
            if ch == '"':
                j = i + 1
                while j < n and line[j] != '"':
                    j += 2 if line[j] == "\\" else 1
                end = min(j + 1, n)
                _string_spans(pi, line, i, end, spans)
                i = end; continue
            if ch == "'" and i + 2 < n:
                j = line.find("'", i + 1)
                if 0 < j - i <= 3:
                    spans.append((pi, i, j + 1, "str")); i = j + 1; continue
            if ch == "@" and i + 1 < n and line[i + 1].isalpha():
                j = i + 1
                while j < n and (line[j].isalnum() or line[j] in "_."): j += 1
                spans.append((pi, i, j, "ann")); i = j; continue
            if ch.isdigit() and (i == 0 or not (line[i - 1].isalnum() or line[i - 1] == "_")):
                j = i
                while j < n and (line[j].isalnum() or line[j] in "_."):
                    if line[j] == "." and j + 1 < n and line[j + 1] == ".": break
                    j += 1
                spans.append((pi, i, j, "num")); i = j; continue
            if ch.isalpha() or ch == "_":
                j = i
                while j < n and (line[j].isalnum() or line[j] == "_"): j += 1
                w = line[i:j]
                label = j < n and line[j] == "@"
                if w in KW and not label:
                    spans.append((pi, i, j, "kw"))
                elif prev_word != "fun" and w[0].isupper() and any(c.islower() for c in w):
                    spans.append((pi, i, j, "type"))
                prev_word = w
                i = j; continue
            if not ch.isspace():
                prev_word = ""
            i += 1
    return spans


def code_cmds(code: str) -> list[dict]:
    spans = [s for s in highlight(code) if s[2] > s[1]]
    if not spans:
        return []
    cmds = [C("text.edit")]
    for p, a, b, kind in spans:
        cmds.append(C("text.select", anchor=[p, a], caret=[p, b]))
        cmds.append(C("format.color", color=SYN[kind]))
        if kind == "kw":
            cmds.append(C("format.bold", on=True))
        elif kind == "com":
            cmds.append(C("format.italic", on=True))
    cmds.append(C("text.exit"))
    return cmds


# ------------------------------------------------------------------ Slide
class Slide:
    def __init__(self, deck, kind: str, title: str, section: str | None, notes: str,
                 minutes: float = 0, day: int = 0):
        self.deck, self.kind, self.title, self.section = deck, kind, title, section
        self.notes = notes.strip()
        self.minutes, self.day = minutes, day
        self.cmds: list[dict] = []
        self.number = 0
        self.snippets: list[str] = []      # arquivos de código usados neste slide

    def add(self, *cmds):
        for c in cmds:
            if isinstance(c, list):
                self.cmds.extend(c)
            else:
                self.cmds.append(c)
        return self

    # ---------------- primitivas
    def rect(self, rect, fill=WHITE, line=INK, width=BORDER_W, shadow=SHADOW, radius=10,
             preset="roundRect", gradient=None, text=None, angle=0):
        x, y, w, h = rect
        p = {"preset": preset, "rect": [x, y, w, h]}
        if text is not None:
            p["text"] = text
        self.add(C("shape.insert", **p))
        if gradient:
            self.add(C("shape.fill", gradient={"stops": gradient, "kind": "linear", "angle": angle}))
        elif fill is None:
            self.add(C("shape.fill", none=True))
        else:
            self.add(C("shape.fill", color=fill))
        self.add(C("shape.line", none=True) if line is None else C("shape.line", color=line, width=width))
        if shadow:
            self.add(C("shape.effects", shadow={"color": INK, "blur": 0, "dist": shadow, "dir": 45}))
        if preset == "roundRect":
            self.add(C("shape.adjust", index=0, value=int(min(50000, radius / max(1, min(w, h)) * 100000))))
        return self

    def text(self, rect, text, size=16, color=INK, bold=False, align="left", font=FONT,
             bullets=False, spacing=4, bullet_color=PURPLE, line=1.1, italic=False, anchor=None,
             on_dark=False):
        clean, spans = parse_rich(text)
        x, y, w, h = rect
        self.add(C("insert.textBox", rect=[x, y, w, h], text=clean),
                 C("format.font", family=font), C("format.size", size=size),
                 C("format.color", color=color), C("format.align", align=align),
                 C("format.margins", left=0, right=0, top=0, bottom=0))
        if bold:
            self.add(C("format.bold", on=True))
        if italic:
            self.add(C("format.italic", on=True))
        if anchor:
            self.add(C("format.anchor", anchor=anchor))
        self.add(C("format.paragraph", spaceAfter=spacing, lineSpacing=line))
        if bullets:
            self.add(C("format.bullets", on=True, char="■", color=bullet_color, size=70),
                     C("format.paragraph", indentLeft=18, indentFirst=-18))
        self.add(span_cmds(spans, bold_color=INK if color in (INK, MUTED, BODY2) else color,
                           on_dark=on_dark))
        return self

    def picture(self, rel, box, align="center", border=False):
        path = rel if os.path.isabs(rel) else asset(rel)
        iw, ih = img_size(path)
        x, y, w, h = box
        s = min(w / iw, h / ih)
        pw, ph = iw * s, ih * s
        px = x + (w - pw) / 2 if align == "center" else (x if align == "left" else x + w - pw)
        py = y + (h - ph) / 2
        self.add(C("insert.picture", path=path, rect=[round(px, 1), round(py, 1), round(pw, 1), round(ph, 1)]))
        if border:
            self.add(C("shape.line", color=INK, width=BORDER_W),
                     C("shape.effects", shadow={"color": INK, "blur": 0, "dist": SHADOW, "dir": 45}))
        return self

    def video(self, rel, box, size_px, poster_ms=0, autoplay=True, loop=True):
        """Vídeo local (não versionado). Sem o arquivo, desenha um placeholder em vez de falhar."""
        path = os.path.join(ROOT, rel)
        iw, ih = size_px
        x, y, w, h = box
        s = min(w / iw, h / ih)
        pw, ph = iw * s, ih * s
        rect = [round(x + (w - pw) / 2, 1), round(y + (h - ph) / 2, 1), round(pw, 1), round(ph, 1)]
        if not os.path.exists(path):
            self.rect(rect, fill=SURFACE, text=f"vídeo local não incluído: {os.path.basename(rel)}")
            self.add(C("format.size", size=12), C("format.color", color=MUTED), C("format.font", family=MONO))
            return self
        self.add(C("insert.video", path=path, rect=rect),
                 C("media.options", autoplay=autoplay, loop=loop),
                 C("media.posterFrame", ms=poster_ms),
                 C("shape.line", color=INK, width=BORDER_W),
                 C("shape.effects", shadow={"color": INK, "blur": 0, "dist": SHADOW, "dir": 45}))
        return self

    def chip(self, x, y, text, fill=WHITE, color=INK, size=10, h=22, gradient=None, shadow=0,
             width=BORDER_W, mono=False, w=None, line=INK):
        cw = w or (len(text) * size * (0.62 if mono else 0.6) + 26)
        self.rect([x, y, cw, h], fill=fill, gradient=gradient, width=width, shadow=shadow,
                  radius=h / 2, text=text, line=line)
        self.add(C("format.font", family=MONO if mono else FONT), C("format.size", size=size),
                 C("format.bold", on=True), C("format.color", color=color),
                 C("format.margins", left=4, right=4, top=0, bottom=0), C("format.anchor", anchor="middle"),
                 C("format.align", align="center"), C("format.wrap", on=False))
        return cw

    # ---------------- componentes
    def card(self, rect, title=None, body=None, tone="white", size=13, title_size=16,
             icon=None, chip=None, feature=False, chip_color=None):
        """Card neutro (branco, título Purple Deep) ou com tint por significado (tone)."""
        x, y, w, h = rect
        self.rect(rect, fill=TINT[tone])
        ty, tx = y + 14, x + 16
        if feature and icon:
            isz = min(84, h * 0.32)
            self.picture(icon, (x + 16, y + 16, isz, isz), align="left")
            ty = y + 16 + isz + 12
            icon = None
        elif icon:
            self.picture(icon, (x + w - 50, y + 10, 38, 38))
        if chip:
            self.chip(tx, ty, chip, fill=chip_color or DEEP[tone], color=WHITE, size=9.5, line=None)
            ty += 30
        if title:
            tw = w - 32 - (44 if icon else 0)
            cpl = max(6, tw / (title_size * 0.56))
            nlines = sum(-(-max(1, len(part)) // int(cpl)) for part in title.split("\n"))
            self.text([tx, ty, tw, 24], title, size=title_size, bold=True, color=DEEP[tone])
            ty += title_size * 1.22 * nlines + 8
        if icon:
            ty = max(ty, y + 50)
        if body:
            self.text([tx, ty, w - 32, max(20, y + h - ty - 10)], body, size=size, color=INK, spacing=4)
        return self

    def code(self, rect, code, file="Main.kt", size=None, max_size=16, fill=WHITE,
             chip_fill=INK, chip_text=WHITE):
        x, y, w, h = rect
        code = code.strip("\n")
        lines = code.split("\n")
        longest = max(len(l) for l in lines)
        if size is None:
            by_h = (h - 38) / (len(lines) * 1.24)
            by_w = (w - 40) / (max(longest, 10) * 0.6)
            size = round(max(8, min(max_size, by_h, by_w)) * 2) / 2
        self.rect(rect, fill=fill)
        self.add(C("insert.textBox", rect=[x + 20, y + 22, w - 36, h - 34], text=code),
                 C("format.font", family=MONO), C("format.size", size=size),
                 C("format.color", color=INK), C("format.align", align="left"),
                 C("format.margins", left=0, right=0, top=0, bottom=0),
                 C("format.wrap", on=False),
                 C("format.paragraph", spaceAfter=0, lineSpacing=1.0))
        self.add(code_cmds(code))
        if file:
            self.chip(x + 16, y - 11, file, fill=chip_fill, color=chip_text, size=9.5, mono=True)
        return self

    def code_file(self, rel, rect, region=0, **kw):
        """Bloco de código lido de snippets/ (fonte única); o chip mostra o nome do arquivo."""
        if rel not in self.snippets:
            self.snippets.append(rel)
        code = snippet_regions(rel)[region]
        return self.code(rect, code, file=kw.pop("file", os.path.basename(rel)), **kw)

    def arrow(self, x1, y1, x2, y2, color=INK, width=2):
        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)
        self.add(C("shape.insert", preset="line", rect=[x, y, max(w, 0.01), max(h, 0.01)]))
        if (x2 < x1) != (y2 < y1) and w > 0 and h > 0:
            self.add(C("shape.flip", axis="vertical"))
        if x2 < x1 and h == 0:
            self.add(C("shape.flip", axis="horizontal"))
        if y2 < y1 and w == 0:
            self.add(C("shape.flip", axis="vertical"))
        self.add(C("shape.line", color=color, width=width, tail="triangle", tailSize="med"))
        return self

    def box(self, rect, text, tone="white", size=13, bold=True, text_color=None,
            shadow=SHADOW, mono=False):
        self.rect(rect, fill=TINT[tone], shadow=shadow, text=text)
        self.add(C("format.font", family=MONO if mono else FONT), C("format.size", size=size),
                 C("format.color", color=text_color or (DEEP[tone] if tone != "white" else INK)),
                 C("format.align", align="center"),
                 C("format.anchor", anchor="middle"), C("format.margins", left=6, right=6, top=2, bottom=2))
        if bold:
            self.add(C("format.bold", on=True))
        return self

    def bullets(self, rect, items, size=15, tone="white", title=None):
        x, y, w, h = rect
        self.rect(rect, fill=TINT[tone])
        x, y, w, h = x + 18, y + 16, w - 36, h - 28
        if title:
            self.text([x, y, w, 24], title, size=size + 2, bold=True, color=DEEP[tone])
            y += size * 1.6 + 8
        self.text([x, y, w, h], "\n".join(items), size=size, bullets=True, spacing=7,
                  bullet_color=DEEP[tone] if tone != "white" else PURPLE)
        return self

    def kodee(self, name, box, emoji=False):
        return self.picture(EMOJI[name] if emoji else KODEE[name], box)


# ------------------------------------------------------------------ chrome do slide
def chrome(s: Slide) -> list[dict]:
    """Fundo sólido, pílula de seção, título e rodapé. Sem gradiente em slides de conteúdo (D6)."""
    cmds = []
    layout = "titleOnly" if s.kind == "content" else "blank"
    cmds.append(C("slide.new", layout=layout, **({"title": s.title} if layout == "titleOnly" else {})))
    cmds.append(C("design.background", color=BG))
    if s.kind == "content":
        cmds += [C("edit.selectAll"),
                 C("shape.setBounds", x=48, y=50, w=830, h=52),
                 C("format.autofit", mode="shrink"),
                 C("format.font", family=FONT), C("format.size", size=30), C("format.bold", on=True),
                 C("format.color", color=INK), C("format.align", align="left"),
                 C("format.anchor", anchor="middle"),
                 C("format.margins", left=0, right=0, top=0, bottom=0),
                 C("edit.deselect")]
    else:
        cmds.append(C("slide.rename", name=s.title))
    t = Slide(None, "", "", None, "")
    if s.kind == "content" and s.section:
        t.chip(48, 24, s.section.upper(), fill=WHITE, size=9.5, h=20)
    if s.kind not in ("cover", "closing", "day", "section"):
        t.picture(LOGO["kotlin_icon"], (48, 509, 14, 14))
        t.text([70, 509, 520, 16], FOOTER, size=8.5, color=MUTED)
        t.rect([872, 503, 40, 24], fill=WHITE, shadow=2, radius=6, text=f"{s.number:02d}")
        t.add(C("format.font", family=MONO), C("format.size", size=10), C("format.bold", on=True),
              C("format.color", color=INK), C("format.anchor", anchor="middle"),
              C("format.align", align="center"), C("format.margins", left=0, right=0, top=0, bottom=0))
    cmds += t.cmds
    return cmds
