// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 14
// 04_strings.kt · Strings: templates e raw strings
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

fun main() {
//sampleStart
    val aluno = "Ana"
    val notas = listOf(8.5, 9.0, 10.0)
    println("Média de $aluno: ${notas.average()}")

    val sql = """
        SELECT * FROM alunos
        WHERE curso = 'ECO'
    """.trimIndent()
    println(sql)

    val preco = $$"Preço: R$ 10 para $$aluno" // 2.2+
    println(preco)

    val csv = buildString {
        appendLine("nome;nota")
        notas.forEach { appendLine("$aluno;$it") }
    }
    print(csv)
//sampleEnd
}
