// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 25
// 12_funcoes.kt · Declarando funções
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
fun saudacao(nome: String, periodo: String = "dia"): String {
    return "Bom $periodo, $nome!"
}

fun dobro(x: Int) = x * 2          // corpo de expressão

fun media(vararg notas: Double) = notas.average()

fun main() {
    println(saudacao("Ana"))              // Bom dia, Ana!
    println(saudacao(periodo = "noite", nome = "Caio"))
    println(dobro(21))
    println(media(7.0, 8.5, 10.0))
    val ns = doubleArrayOf(6.0, 9.0)
    println(media(*ns))                   // spread
}
//sampleEnd
