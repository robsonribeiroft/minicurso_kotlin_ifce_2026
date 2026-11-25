// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 22
// 11_operacoes_funcionais.kt · Operações funcionais e sequências
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

data class Aluno(val nome: String, val curso: String, val nota: Double)

//sampleStart

fun main() {
    val turma = listOf(
        Aluno("Ana", "ECO", 9.1), Aluno("Bia", "ECO", 6.4),
        Aluno("Caio", "ADS", 8.2), Aluno("Davi", "ADS", 7.7),
    )
    val aprovados = turma.filter { it.nota >= 7 }.map { it.nome }
    val porCurso = turma.groupBy { it.curso }
    val media = turma.sumOf { it.nota } / turma.size
    val (bons, ruins) = turma.partition { it.nota >= 7 }
    val melhor = turma.maxBy { it.nota }
    println("$aprovados ${porCurso.keys} $media")
    println("${bons.size}/${ruins.size} ${melhor.nome}")

    val primos = generateSequence(2) { it + 1 } // infinita
        .filter { n -> (2..<n).none { n % it == 0 } }
        .take(5).toList()
    println(primos)                     // [2, 3, 5, 7, 11]
}
//sampleEnd
