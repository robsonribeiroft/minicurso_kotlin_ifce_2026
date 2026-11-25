// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 20
// 10_faca_evite_colecoes.kt · Faça / Evite: expondo coleções
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
class Turma {
    private val _alunos = mutableListOf<String>()
    val alunos: List<String> get() = _alunos
    fun matricular(nome: String) {
        if (nome.isNotBlank()) _alunos += nome
    }
}
//sampleEnd

//sampleStart
class TurmaFragil {
    val alunos = mutableListOf<String>()   // pública e mutável
}
//sampleEnd

fun main() {
    val t = Turma()
    t.matricular("Ana")
    // t.alunos.add("Intruso")    // não compila: List não tem add
    val f = TurmaFragil()
    f.alunos.add("")              // ninguém impede
    f.alunos.clear()
    println("${t.alunos} ${f.alunos}")
}
