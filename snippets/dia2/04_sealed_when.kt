// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 35
// 04_sealed_when.kt · sealed: hierarquias fechadas e when exaustivo
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
sealed interface EstadoTela {
    data object Carregando : EstadoTela
    data class Sucesso(val alunos: List<String>) : EstadoTela
    data class Erro(val msg: String, val codigo: Int) : EstadoTela
}

fun renderizar(estado: EstadoTela): String = when (estado) {
    EstadoTela.Carregando -> "Carregando..."
    is EstadoTela.Sucesso -> "${estado.alunos.size} alunos"
    is EstadoTela.Erro if estado.codigo == 404 -> "Não encontrado"
    is EstadoTela.Erro -> "Erro: ${estado.msg}"
}   // sem 'else': o compilador garante todos os casos
//sampleEnd

fun main() {
    listOf(
        EstadoTela.Carregando,
        EstadoTela.Sucesso(listOf("Ana", "Caio")),
        EstadoTela.Erro("tempo esgotado", 500),
        EstadoTela.Erro("rota", 404),
    ).forEach { println(renderizar(it)) }
}
