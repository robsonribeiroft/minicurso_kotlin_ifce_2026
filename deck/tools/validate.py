"""Valida todo o código do minicurso com o mesmo Kotlin do Playground (2.4.21, JVM).

Regras (PRD D30):
  snippets/**   compilam e rodam sem erro (exceto *bonus_compose*, que é alvo Compose/Wasm)
  solucoes/**   compilam, rodam e imprimem só ✅
  desafios/**   compilam, rodam e imprimem pelo menos um ❌ (os TODO() ainda não feitos)

    python3 deck/tools/validate.py [filtro]
"""
import concurrent.futures as cf
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LIBS = sorted(glob.glob(os.path.join(ROOT, "deck", "build", "libs", "*.jar")))
CP = os.pathsep.join(LIBS)


def classe_main(path: str) -> str:
    nome = os.path.splitext(os.path.basename(path))[0]
    nome = re.sub(r"[^A-Za-z0-9_]", "_", nome)
    if nome[0].isdigit():
        nome = "_" + nome
    return nome[0].upper() + nome[1:] + "Kt" if not nome[0].isdigit() and nome[0] != "_" else nome + "Kt"


def validar(path: str):
    rel = os.path.relpath(path, ROOT)
    tipo = rel.split(os.sep)[0]
    out = tempfile.mkdtemp(prefix="kt_")
    try:
        c = subprocess.run(["kotlinc", path, "-cp", CP, "-d", out, "-nowarn"],
                           capture_output=True, text=True, timeout=300)
        if c.returncode != 0:
            return rel, False, "COMPILAÇÃO\n" + (c.stderr or c.stdout)[-1500:]
        r = subprocess.run(["kotlin", "-cp", os.pathsep.join([out, CP]), classe_main(path)],
                           capture_output=True, text=True, timeout=120)
        saida = r.stdout + r.stderr
        if r.returncode != 0:
            return rel, False, "EXECUÇÃO\n" + saida[-1500:]
        if tipo == "solucoes" and ("❌" in saida or "✅" not in saida):
            return rel, False, "GABARITO COM FALHA\n" + saida
        if tipo == "desafios" and "❌" not in saida:
            return rel, False, "DESAFIO SEM ❌ (os TODO deveriam falhar)\n" + saida
        return rel, True, saida.strip().splitlines()[-1] if saida.strip() else ""
    except subprocess.TimeoutExpired:
        return rel, False, "TEMPO ESGOTADO"
    finally:
        shutil.rmtree(out, ignore_errors=True)


def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    arquivos = sorted(glob.glob(os.path.join(ROOT, "snippets", "*", "*.kt"))
                      + glob.glob(os.path.join(ROOT, "desafios", "*", "*.kt"))
                      + glob.glob(os.path.join(ROOT, "solucoes", "*", "*.kt")))
    arquivos = [a for a in arquivos if "bonus_compose" not in a and filtro in a]
    falhas = 0
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for rel, ok, info in ex.map(validar, arquivos):
            print(f"{'OK ' if ok else 'ERR'} {rel}  {info if ok else ''}")
            if not ok:
                falhas += 1
                print("    " + info.replace("\n", "\n    "))
    print(f"\n{len(arquivos) - falhas}/{len(arquivos)} arquivos válidos "
          f"(bonus_compose não é validado: alvo Compose/Wasm)")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
