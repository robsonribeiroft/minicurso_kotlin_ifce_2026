// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 12
// 02_val_var.kt · Variáveis: val e var
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
const val MAX_ALUNOS = 40   // constante de compilação

fun main() {
    val nome = "Kotlin"         // String inferida
    var versao: Double = 2.4    // tipo explícito
    versao = 2.5                // ok: é var
    // nome = "Java"            // erro: val é fixa

    val lista = mutableListOf(1, 2)
    lista.add(3)                // o conteúdo muda!
    println("$nome $versao $lista $MAX_ALUNOS")
}
//sampleEnd
