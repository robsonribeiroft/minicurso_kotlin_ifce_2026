// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 27
// 15_extensoes.kt · Extension functions
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
fun String.contarVogais(): Int =
    lowercase().count { it in "aeiouáéíóúâêôãõ" }

fun Double.emReais(): String = "R$ %.2f".format(this)

val String.iniciais: String
    get() = split(" ").filter { it.isNotBlank() }
        .joinToString("") { it.first().uppercase() }

fun String?.ouPadrao(padrao: String = "N/A") =
    if (this.isNullOrBlank()) padrao else this

fun main() {
    println("Engenharia de Computação".contarVogais())
    println(1234.5.emReais())
    println("instituto federal ceara".iniciais)   // IFC
    val apelido: String? = null
    println(apelido.ouPadrao())                    // N/A
}
//sampleEnd
