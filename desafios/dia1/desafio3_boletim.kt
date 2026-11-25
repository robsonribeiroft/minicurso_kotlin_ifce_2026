// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · DESAFIO (slide 28)
// desafio3_boletim.kt
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM), clique em Run e deixe tudo ✅.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════
/*
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
    TODO("Lembre do caso sem notas")

fun conceito(media: Double): String =
    TODO("when sem argumento, do maior para o menor")

fun mediaPorCurso(turma: List<Aluno>): Map<String, Double> =
    TODO("groupBy { it.curso } e depois mapValues")

fun destaque(turma: List<Aluno>): String? =
    TODO("maxByOrNull + ?.")

fun relatorio(turma: List<Aluno>): List<String> =
    TODO("sortedBy + map com template de String")

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
