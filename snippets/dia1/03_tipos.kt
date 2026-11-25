// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 13
// 03_tipos.kt · Tipos básicos e a hierarquia
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
fun log(msg: String): Unit = println(msg)

fun falhar(msg: String): Nothing = error(msg)

fun main() {
    val idade: Int = 20
    val populacao: Long = 2_700_000L
    val nota: Double = 9.5
    val ativo: Boolean = true
    val inicial: Char = 'K'
    val total: Long = idade.toLong() // sem conversão implícita
    log("$idade $populacao $nota $ativo $inicial $total")

    val qualquer: Any = "texto"
    println(qualquer is String)         // true
    println(runCatching { falhar("ops") }.isFailure)
}
//sampleEnd
