// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 18
// 08_lacos.kt · Laços, ranges e progressões
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

fun main() {
//sampleStart
    for (i in 1..5) print(i)             // 12345
    for (i in 0..<5) print(i)            // 01234
    for (i in 10 downTo 0 step 2) print(i)
    println()

    val linguagens = listOf("Kotlin", "Java", "C")
    for ((i, nome) in linguagens.withIndex()) {
        println("$i: $nome")
    }

    val capitais = mapOf("CE" to "Fortaleza", "PE" to "Recife")
    for ((sigla, capital) in capitais) {
        println("$sigla = $capital")
    }

    repeat(3) { println("Olá #$it") }
    externo@ for (i in 1..3) {
        for (j in 1..3) {
            if (j == 2) continue@externo
            println("i=$i j=$j")
        }
    }
//sampleEnd
}
