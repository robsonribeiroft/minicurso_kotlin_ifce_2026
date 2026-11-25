// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 26
// 13_lambdas.kt · Lambdas e funções de ordem superior
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
val soma: (Int, Int) -> Int = { a, b -> a + b }
val quadrado = { x: Int -> x * x }

fun operar(a: Int, b: Int, op: (Int, Int) -> Int) = op(a, b)

fun ehPar(n: Int) = n % 2 == 0

fun criarContador(): () -> Int {
    var c = 0
    return { ++c }                           // closure
}

fun main() {
    println(operar(2, 3, soma))              // 5
    println(operar(2, 3) { x, y -> x * y }) // trailing
    println(listOf(1, 2, 3, 4).filter(::ehPar))
    println(quadrado(9))
    val contar = criarContador()
    contar()
    println(contar())                        // 2
}
//sampleEnd
