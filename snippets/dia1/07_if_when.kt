// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 18
// 07_if_when.kt · if e when são expressões
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
fun conceito(nota: Double) = when {
    nota >= 9.0 -> "A"
    nota >= 7.0 -> "B"
    nota >= 5.0 -> "C"
    else -> "Reprovado"
}

fun classificar(x: Any) = when (x) {
    0, 1 -> "binário"
    is Int if x in 2..9 -> "dígito"   // guard (2.2+)
    is Int -> "número"
    is String if x.isBlank() -> "texto vazio"
    is String -> "texto"
    else -> "desconhecido"
}

fun main() {
    val a = 7
    val b = 3
    val maior = if (a > b) a else b   // sem ternário
    println("$maior ${conceito(8.2)} ${classificar(5)}")
}
//sampleEnd
