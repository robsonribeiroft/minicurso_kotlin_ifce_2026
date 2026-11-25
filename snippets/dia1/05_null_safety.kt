// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 15
// 05_null_safety.kt · Null safety: o fim do NullPointerException
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

fun buscarApelido(id: Int): String? = if (id == 1) "Kodee" else null

fun main() {
//sampleStart
    val nome: String = "Kotlin"
    // val nada: String = null         // não compila

    var apelido: String? = buscarApelido(2) // pode ser nulo

    val tam1 = apelido?.length          // Int? → null
    val tam2 = apelido?.length ?: 0     // Elvis → 0
    println("$nome $tam1 $tam2")

    apelido = buscarApelido(1)
    apelido?.let { println("Oi, $it!") } // só se não for nulo
    val tam3 = apelido!!.length   // NPE se for nulo
    println(tam3)
//sampleEnd
}
