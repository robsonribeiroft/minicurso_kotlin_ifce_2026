"""Fonte única dos desafios: gera desafios/diaN/*.kt (com TODO) e solucoes/diaN/*.kt (gabarito).

Cada desafio é um texto Kotlin com marcadores  <<TODO("dica")||código da solução>>
— no desafio entra o TODO, no gabarito entra a solução. O bloco VERIFICAR é comum aos dois.

    python3 deck/tools/desafios_src.py
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

HEADER = """// ══════════════════════════════════════════════════════════════
// (cabeçalho gerado pelo build)
// ══════════════════════════════════════════════════════════════
"""

VERIFICAR = '''
// ───────────── Autoavaliação: não altere daqui para baixo ─────────────
fun verificar(descricao: String, teste: () -> Boolean) {
    val resultado = try {
        if (teste()) "✅ Passou" else "❌ Falhou"
    } catch (e: NotImplementedError) {
        "❌ Ainda não implementado (TODO)"
    } catch (e: Exception) {
        "❌ Erro: ${e::class.simpleName}: ${e.message}"
    }
    println("$resultado — $descricao")
}
'''

DESAFIOS = {}

DESAFIOS["dia1/desafio1_notas_validas.kt"] = '''/*
 DESAFIO 1 · Notas válidas                                  nível: FÁCIL
 Treina: null safety, toDoubleOrNull(), operador Elvis, takeIf, mapNotNull.

 Uma planilha exportou as notas da turma como texto. Algumas células vieram
 vazias, com vírgula no lugar do ponto, com espaços ou com valores fora de 0..10.

 1) notaOuNull(texto): converta o texto em Double. Aceite "7,5" e "7.5" e ignore
    espaços nas pontas. Retorne null se não for número ou se estiver fora de 0..10.
 2) notasValidas(entradas): devolva só as notas válidas, na ordem original.
 3) mediaOuZero(notas): a média das notas, ou 0.0 se a lista estiver vazia.

 Rode o programa: cada verificação imprime ✅ ou ❌.
*/

fun notaOuNull(texto: String): Double? =
    <<TODO("Use trim(), replace(',', '.'), toDoubleOrNull() e takeIf { it in 0.0..10.0 }")||texto.trim().replace(',', '.').toDoubleOrNull()?.takeIf { it in 0.0..10.0 }>>

fun notasValidas(entradas: List<String>): List<Double> =
    <<TODO("Use mapNotNull com a função notaOuNull")||entradas.mapNotNull(::notaOuNull)>>

fun mediaOuZero(notas: List<Double>): Double =
    <<TODO("Cuidado: average() de lista vazia é NaN")||if (notas.isEmpty()) 0.0 else notas.average()>>

fun main() {
    val planilha = listOf("8.5", " 7,0 ", "", "dez", "11", "-1", "10", "6.25")
    verificar("\\"8.5\\" vira 8.5") { notaOuNull("8.5") == 8.5 }
    verificar("\\" 7,0 \\" vira 7.0") { notaOuNull(" 7,0 ") == 7.0 }
    verificar("\\"dez\\" e \\"\\" viram null") { notaOuNull("dez") == null && notaOuNull("") == null }
    verificar("fora de 0..10 vira null") { notaOuNull("11") == null && notaOuNull("-1") == null }
    verificar("filtra a planilha") { notasValidas(planilha) == listOf(8.5, 7.0, 10.0, 6.25) }
    verificar("média da planilha é 7.9375") { mediaOuZero(notasValidas(planilha)) == 7.9375 }
    verificar("média de lista vazia é 0.0") { mediaOuZero(emptyList()) == 0.0 }
}
'''

DESAFIOS["dia1/desafio2_palindromo.kt"] = '''/*
 DESAFIO 2 · Palíndromos com acento                         nível: MÉDIO
 Treina: extension functions, operações em String, filter, interoperabilidade Java.

 Um palíndromo se lê igual nos dois sentidos, ignorando maiúsculas, acentos,
 espaços e pontuação: "Socorram-me, subi no ônibus em Marrocos".

 A extensão semAcentos() já está pronta (ela usa java.text.Normalizer, do Java).

 1) String.normalizar(): minúsculas, sem acentos e só com letras e dígitos.
 2) String.ehPalindromo(): true se o texto normalizado é igual ao seu reverso.
 3) palindromosDa(frases): só as frases que são palíndromos, na ordem original.
*/

fun String.semAcentos(): String =
    java.text.Normalizer.normalize(this, java.text.Normalizer.Form.NFD)
        .replace(Regex("\\\\p{Mn}+"), "")

fun String.normalizar(): String =
    <<TODO("Use lowercase(), semAcentos() e filter { it.isLetterOrDigit() }")||lowercase().semAcentos().filter { it.isLetterOrDigit() }>>

fun String.ehPalindromo(): Boolean =
    <<TODO("Compare normalizar() com normalizar().reversed()")||normalizar().let { it == it.reversed() }>>

fun palindromosDa(frases: List<String>): List<String> =
    <<TODO("Use filter com a extensão ehPalindromo()")||frases.filter { it.ehPalindromo() }>>

fun main() {
    verificar("\\"Ônibus, Já!\\" normaliza para \\"onibusja\\"") { "Ônibus, Já!".normalizar() == "onibusja" }
    verificar("frase com acento é palíndromo") { "Socorram-me, subi no ônibus em Marrocos".ehPalindromo() }
    verificar("\\"A base do teto desaba.\\" é palíndromo") { "A base do teto desaba.".ehPalindromo() }
    verificar("\\"Kotlin\\" não é palíndromo") { !"Kotlin".ehPalindromo() }
    verificar("filtra uma lista de frases") {
        palindromosDa(listOf("Arara", "IFCE", "Roma me tem amor")) == listOf("Arara", "Roma me tem amor")
    }
}
'''

DESAFIOS["dia1/desafio3_boletim.kt"] = '''/*
 DESAFIO 3 · Boletim da turma                               nível: DESAFIO
 Treina: data class, when, groupBy, mapValues, maxByOrNull, sortedBy, templates.

 1) Aluno.media(): média das notas do aluno (0.0 se não tiver notas).
 2) conceito(media): "A" se >= 9, "B" se >= 7, "C" se >= 5, senão "D". Use when.
 3) mediaPorCurso(turma): mapa curso → média das médias dos alunos do curso.
 4) destaque(turma): nome do aluno com a maior média, ou null se a turma estiver vazia.
 5) relatorio(turma): uma linha por aluno, ordenada por nome, no formato
    "Ana (ECO): 9.0 · A"
*/

data class Aluno(val nome: String, val curso: String, val notas: List<Double>)

fun Aluno.media(): Double =
    <<TODO("Lembre do caso sem notas")||if (notas.isEmpty()) 0.0 else notas.average()>>

fun conceito(media: Double): String =
    <<TODO("when sem argumento, do maior para o menor")||when {
        media >= 9.0 -> "A"
        media >= 7.0 -> "B"
        media >= 5.0 -> "C"
        else -> "D"
    }>>

fun mediaPorCurso(turma: List<Aluno>): Map<String, Double> =
    <<TODO("groupBy { it.curso } e depois mapValues")||turma.groupBy { it.curso }.mapValues { (_, alunos) -> alunos.map { it.media() }.average() }>>

fun destaque(turma: List<Aluno>): String? =
    <<TODO("maxByOrNull + ?.")||turma.maxByOrNull { it.media() }?.nome>>

fun relatorio(turma: List<Aluno>): List<String> =
    <<TODO("sortedBy + map com template de String")||turma.sortedBy { it.nome }.map { "${it.nome} (${it.curso}): ${it.media()} · ${conceito(it.media())}" }>>

fun main() {
    val turma = listOf(
        Aluno("Dani", "ADS", listOf(10.0, 9.0)),
        Aluno("Ana", "ECO", listOf(9.0, 9.0)),
        Aluno("Bruno", "ECO", listOf(6.0, 7.0)),
        Aluno("Caio", "ADS", listOf(8.0, 7.0)),
        Aluno("Eva", "ECO", listOf(4.0, 5.0)),
    )
    verificar("média da Ana é 9.0") { turma[1].media() == 9.0 }
    verificar("aluno sem notas tem média 0.0") { Aluno("Zé", "ECO", emptyList()).media() == 0.0 }
    verificar("conceitos A, B, C e D") {
        listOf(9.5, 7.5, 5.0, 4.9).map(::conceito) == listOf("A", "B", "C", "D")
    }
    verificar("média por curso") {
        val m = mediaPorCurso(turma)
        m.keys == setOf("ADS", "ECO") && m["ADS"] == 8.5 && kotlin.math.abs(m.getValue("ECO") - 6.6667) < 0.001
    }
    verificar("destaque é a Dani; turma vazia dá null") { destaque(turma) == "Dani" && destaque(emptyList()) == null }
    verificar("relatório ordenado por nome") {
        relatorio(turma).first() == "Ana (ECO): 9.0 · A" && relatorio(turma).last() == "Eva (ECO): 4.5 · D"
    }
}
'''

DESAFIOS["dia2/desafio1_formas.kt"] = '''/*
 DESAFIO 1 · Formas geométricas                             nível: FÁCIL
 Treina: sealed interface, data class, when exaustivo (sem else), extensões.

 1) Forma.area(): área de cada forma. Círculo: π·r². Retângulo: l·a. Triângulo: b·a/2.
 2) Forma.nome(): "círculo", "retângulo" ou "triângulo".
 3) List<Forma>.areaTotal(): soma das áreas.
 4) List<Forma>.maior(): a forma de maior área, ou null se a lista estiver vazia.

 Regra: nada de else nos when. O compilador deve garantir todos os casos.
*/
import kotlin.math.PI
import kotlin.math.abs

sealed interface Forma {
    data class Circulo(val raio: Double) : Forma
    data class Retangulo(val largura: Double, val altura: Double) : Forma
    data class Triangulo(val base: Double, val altura: Double) : Forma
}

fun Forma.area(): Double =
    <<TODO("when (this) com os três casos")||when (this) {
        is Forma.Circulo -> PI * raio * raio
        is Forma.Retangulo -> largura * altura
        is Forma.Triangulo -> base * altura / 2
    }>>

fun Forma.nome(): String =
    <<TODO("when (this) com os três casos")||when (this) {
        is Forma.Circulo -> "círculo"
        is Forma.Retangulo -> "retângulo"
        is Forma.Triangulo -> "triângulo"
    }>>

fun List<Forma>.areaTotal(): Double =
    <<TODO("sumOf")||sumOf { it.area() }>>

fun List<Forma>.maior(): Forma? =
    <<TODO("maxByOrNull")||maxByOrNull { it.area() }>>

fun main() {
    val formas = listOf(Forma.Retangulo(2.0, 3.0), Forma.Triangulo(4.0, 5.0), Forma.Circulo(1.0))
    verificar("área do círculo de raio 1 é π") { abs(Forma.Circulo(1.0).area() - PI) < 1e-9 }
    verificar("retângulo 2×3 = 6 e triângulo 4×5 = 10") {
        Forma.Retangulo(2.0, 3.0).area() == 6.0 && Forma.Triangulo(4.0, 5.0).area() == 10.0
    }
    verificar("nomes das formas") { formas.map { it.nome() } == listOf("retângulo", "triângulo", "círculo") }
    verificar("área total ≈ 19.14") { abs(formas.areaTotal() - (16.0 + PI)) < 1e-9 }
    verificar("maior forma é o triângulo; lista vazia dá null") {
        formas.maior() == Forma.Triangulo(4.0, 5.0) && emptyList<Forma>().maior() == null
    }
}
'''

DESAFIOS["dia2/desafio2_calculadora.kt"] = '''/*
 DESAFIO 2 · Calculadora de expressões                      nível: MÉDIO
 Treina: sealed interface, recursão, when exaustivo, data object/class, templates.

 Uma expressão é um número, uma soma, uma multiplicação ou uma negação:
     1 + (2 * 3)  é  Soma(Num(1), Mult(Num(2), Num(3)))

 1) avaliar(e): o valor inteiro da expressão.
 2) mostrar(e): texto com parênteses em toda soma e multiplicação:
    Num(1) → "1"   Soma → "(a + b)"   Mult → "(a * b)"   Neg → "-a"
 3) simplificar(e): aplica, de forma recursiva, x*0 = 0, x*1 = x e x+0 = x
    (nos dois lados). Dica: simplifique os filhos primeiro.
*/

sealed interface Expr {
    data class Num(val valor: Int) : Expr
    data class Soma(val esq: Expr, val dir: Expr) : Expr
    data class Mult(val esq: Expr, val dir: Expr) : Expr
    data class Neg(val expr: Expr) : Expr
}

fun avaliar(e: Expr): Int =
    <<TODO("when (e) chamando avaliar recursivamente")||when (e) {
        is Expr.Num -> e.valor
        is Expr.Soma -> avaliar(e.esq) + avaliar(e.dir)
        is Expr.Mult -> avaliar(e.esq) * avaliar(e.dir)
        is Expr.Neg -> -avaliar(e.expr)
    }>>

fun mostrar(e: Expr): String =
    <<TODO("when (e) com templates de String")||when (e) {
        is Expr.Num -> "${e.valor}"
        is Expr.Soma -> "(${mostrar(e.esq)} + ${mostrar(e.dir)})"
        is Expr.Mult -> "(${mostrar(e.esq)} * ${mostrar(e.dir)})"
        is Expr.Neg -> "-${mostrar(e.expr)}"
    }>>

fun simplificar(e: Expr): Expr =
    <<TODO("Simplifique esq e dir primeiro; depois use when com guard conditions")||when (e) {
        is Expr.Num -> e
        is Expr.Neg -> Expr.Neg(simplificar(e.expr))
        is Expr.Soma -> {
            val a = simplificar(e.esq)
            val b = simplificar(e.dir)
            when {
                a == Expr.Num(0) -> b
                b == Expr.Num(0) -> a
                else -> Expr.Soma(a, b)
            }
        }
        is Expr.Mult -> {
            val a = simplificar(e.esq)
            val b = simplificar(e.dir)
            when {
                a == Expr.Num(0) || b == Expr.Num(0) -> Expr.Num(0)
                a == Expr.Num(1) -> b
                b == Expr.Num(1) -> a
                else -> Expr.Mult(a, b)
            }
        }
    }>>

fun main() {
    val expr = Expr.Soma(Expr.Num(1), Expr.Mult(Expr.Num(2), Expr.Num(3)))
    verificar("1 + (2 * 3) = 7") { avaliar(expr) == 7 }
    verificar("negação: -(2 + 3) = -5") { avaliar(Expr.Neg(Expr.Soma(Expr.Num(2), Expr.Num(3)))) == -5 }
    verificar("mostrar com parênteses") { mostrar(expr) == "(1 + (2 * 3))" }
    verificar("mostrar negação") { mostrar(Expr.Neg(Expr.Num(4))) == "-4" }
    verificar("x * 0 vira 0") { simplificar(Expr.Mult(Expr.Num(0), expr)) == Expr.Num(0) }
    verificar("simplifica recursivamente: (1 * 7) + 0 vira 7") {
        simplificar(Expr.Soma(Expr.Mult(Expr.Num(1), Expr.Num(7)), Expr.Num(0))) == Expr.Num(7)
    }
}
'''

DESAFIOS["dia2/desafio3_downloads.kt"] = '''/*
 DESAFIO 3 · Downloads paralelos                            nível: DESAFIO
 Treina: suspend, coroutineScope, async/awaitAll, withTimeoutOrNull, Flow.

 A função baixar() já está pronta: cada download leva 1 segundo.

 1) baixarTodos(arquivos): baixe TODOS em paralelo e devolva a soma dos tamanhos.
    5 arquivos devem terminar em menos de 1,5 s (sequencial levaria 5 s).
 2) baixarComLimite(arquivo, limiteMs): devolva o tamanho, ou null se o download
    passar de limiteMs.
 3) progresso(arquivos): um Flow que emite quantos arquivos já foram baixados
    (1, 2, ..., n). Pode baixar um de cada vez.
*/
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlin.system.measureTimeMillis

// Não altere: simula o download de um arquivo (1 s cada).
suspend fun baixar(arquivo: String): Int {
    delay(1_000)
    return arquivo.length * 100          // "tamanho" em KB
}

suspend fun baixarTodos(arquivos: List<String>): Int =
    <<TODO("coroutineScope { arquivos.map { async { ... } }.awaitAll().sum() }")||coroutineScope {
        arquivos.map { async { baixar(it) } }.awaitAll().sum()
    }>>

suspend fun baixarComLimite(arquivo: String, limiteMs: Long): Int? =
    <<TODO("withTimeoutOrNull")||withTimeoutOrNull(limiteMs) { baixar(arquivo) }>>

fun progresso(arquivos: List<String>): Flow<Int> =
    <<TODO("flow { } com emit a cada arquivo baixado")||flow {
        arquivos.forEachIndexed { i, arquivo ->
            baixar(arquivo)
            emit(i + 1)
        }
    }>>

fun main() {
    val arquivos = listOf("a.pdf", "b.png", "slides.pdf", "notas.txt", "video.mp4")
    verificar("soma dos tamanhos é 3800 KB") { runBlocking { baixarTodos(arquivos) } == 3800 }
    verificar("5 downloads em menos de 1,5 s") {
        measureTimeMillis { runBlocking { baixarTodos(arquivos) } } < 1_500
    }
    verificar("limite de 500 ms devolve null; de 1500 ms devolve 100") {
        runBlocking { baixarComLimite("x", 500) == null && baixarComLimite("y", 1_500) == 100 }
    }
    verificar("progresso emite 1, 2") { runBlocking { progresso(listOf("a", "b")).toList() } == listOf(1, 2) }
}
'''

_MARK = re.compile(r"<<(TODO\(.*?\))\|\|(.*?)>>", re.S)


def render(text: str, solution: bool) -> str:
    return _MARK.sub(lambda m: m.group(2) if solution else m.group(1), text)


def main():
    for rel, text in DESAFIOS.items():
        for base, sol in (("desafios", False), ("solucoes", True)):
            path = os.path.join(ROOT, base, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            body = render(text, sol).rstrip() + "\n" + VERIFICAR
            if sol:
                body = body.replace("DESAFIO", "GABARITO · DESAFIO", 1)
            # preserva um cabeçalho já sincronizado pelo build
            head = HEADER
            if os.path.exists(path):
                old = open(path, encoding="utf-8").read()
                if old.startswith("// ══"):
                    end = old.index("\n// ══", 5)
                    head = old[: old.index("\n", end + 1) + 1]
            with open(path, "w", encoding="utf-8") as f:
                f.write(head + body)
            print("  ", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
