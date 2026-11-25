// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · DESAFIO (slide 53)
// desafio2_calculadora.kt
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM), clique em Run e deixe tudo ✅.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════
/*
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
    TODO("when (e) chamando avaliar recursivamente")

fun mostrar(e: Expr): String =
    TODO("when (e) com templates de String")

fun simplificar(e: Expr): Expr =
    TODO("Simplifique esq e dir primeiro; depois use when com guard conditions")

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
