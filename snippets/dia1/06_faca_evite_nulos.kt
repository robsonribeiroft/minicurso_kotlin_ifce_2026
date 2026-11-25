// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · slide 16
// 06_faca_evite_nulos.kt · Faça / Evite: lidando com nulos
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

data class Usuario(val nome: String, val email: String?)

//sampleStart
fun dominio(u: Usuario): String =
    u.email?.substringAfter("@") ?: "sem e-mail"
//sampleEnd

//sampleStart
fun dominioArriscado(u: Usuario): String =
    u.email!!.substringAfter("@")
//sampleEnd

fun main() {
    val ana = Usuario("Ana", null)
    println(dominio(ana))                                       // sem e-mail
    println(runCatching { dominioArriscado(ana) }.exceptionOrNull()) // NullPointerException
}
