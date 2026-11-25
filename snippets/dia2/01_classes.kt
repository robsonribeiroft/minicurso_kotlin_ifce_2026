// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 33
// 01_classes.kt · Classes, construtores e propriedades
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
class Turma(val curso: String, capacidade: Int = 40) {
    private val alunos = mutableListOf<String>()

    var capacidade = capacidade
        set(valor) {
            require(valor > 0) { "Capacidade inválida" }
            field = valor
        }

    val vagas: Int
        get() = capacidade - alunos.size

    init { println("Turma de $curso criada") }

    fun matricular(nome: String) { alunos += nome }
}

fun main() {
    val t = Turma("ECO")                 // sem 'new'
    t.matricular("Ana")
    println("Vagas: ${t.vagas}")
}
//sampleEnd
