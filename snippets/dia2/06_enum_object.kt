// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 37
// 06_enum_object.kt · enum, object e companion object
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
enum class Turno(val inicio: Int) {
    MANHA(7), TARDE(13), NOITE(18);
    fun descricao() = "${name.lowercase()}: ${inicio}h"
}

object Configuracoes {                    // singleton
    var tema = "claro"
}

class Usuario private constructor(val email: String) {
    companion object {
        const val DOMINIO = "@aluno.ifce.edu.br"
        fun criar(mat: String) = Usuario(mat + DOMINIO)
    }
}

fun main() {
    Turno.entries.forEach { println(it.descricao()) }
    Configuracoes.tema = "escuro"
    println(Configuracoes.tema)
    println(Usuario.criar("2026001").email)
}
//sampleEnd
