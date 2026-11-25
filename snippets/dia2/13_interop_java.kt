// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 47
// 13_interop_java.kt · 100% interoperável com Java
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

import java.time.LocalDate
import java.time.temporal.ChronoUnit

//sampleStart
fun main() {
    val hoje = LocalDate.of(2026, 12, 1)      // java.time
    val prova = LocalDate.of(2026, 12, 10)
    val dias = ChronoUnit.DAYS.between(hoje, prova)
    println("Faltam $dias dias")
    println(prova.dayOfWeek)                  // getDayOfWeek()

    val nomes = java.util.ArrayList<String>() // coleção Java
    nomes.add("Caio"); nomes.add("Ana")
    nomes.sortWith(Comparator { a, b -> a.compareTo(b) }) // SAM
    println(nomes.joinToString())             // extensão Kotlin

    val sorteio = java.util.Random(2026).nextInt(100)
    println("Sorteado: $sorteio")
}
//sampleEnd
