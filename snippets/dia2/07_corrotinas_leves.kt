// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 40
// 07_corrotinas_leves.kt · Por que corrotinas?
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

import kotlinx.coroutines.*

//sampleStart
fun main() = runBlocking {
    val inicio = System.currentTimeMillis()
    val jobs = List(100_000) {
        launch {
            delay(1_000)   // suspende, não bloqueia
        }
    }
    jobs.joinAll()
    val total = System.currentTimeMillis() - inicio
    println("100 mil corrotinas em $total ms")
}
//sampleEnd
