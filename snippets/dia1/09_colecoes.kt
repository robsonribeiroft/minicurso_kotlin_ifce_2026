// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 20
// 09_colecoes.kt · Coleções: somente leitura × mutáveis
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

fun main() {
//sampleStart
    val cursos = listOf("ECO", "Telemática", "ADS")
    // cursos.add("X")                // List não tem add

    val notas = mutableListOf(7.5, 8.0)
    notas += 9.5                       // add

    val siglas = setOf("IFCE", "UFC", "IFCE")     // 2 itens
    val capitais = mapOf("CE" to "Fortaleza", "PE" to "Natal")

    println(capitais["CE"])            // Fortaleza
    println(cursos.getOrNull(10))      // null
    println("$notas $siglas")

    val estoque = mutableMapOf<String, Int>()
    estoque["café"] = 3
    println(estoque)
//sampleEnd
}
