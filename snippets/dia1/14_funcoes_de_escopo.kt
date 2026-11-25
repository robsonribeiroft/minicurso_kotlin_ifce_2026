// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 27
// 14_funcoes_de_escopo.kt · Funções de escopo: let, run, with, apply, also
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

data class Aluno(val nome: String, val curso: String, val nota: Double)

class Conexao {
    var host = "localhost"
    var porta = 0
    override fun toString() = "$host:$porta"
}

fun main() {
    val turma = listOf(Aluno("Ana", "ECO", 9.0), Aluno("Caio", "ADS", 8.0))
    val nomeOuNull: String? = "  Kodee  "
//sampleStart
    val aluno = Aluno("Ana", "ECO", 9.1).also { println("Criado: $it") }
    val conexao = Conexao().apply { host = "ifce.edu.br"; porta = 5432 }
    val tamanho = nomeOuNull?.let { it.trim().length } ?: 0
    val resumo = with(turma) { "$size alunos, média ${sumOf { it.nota } / size}" }
    val dobro = aluno.run { nota * 2 }
//sampleEnd
    println("$conexao | $tamanho | $resumo | $dobro")
}
