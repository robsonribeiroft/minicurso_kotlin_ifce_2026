// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 42
// 09_launch_async.kt · launch, async e runBlocking
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

import kotlinx.coroutines.*
import kotlin.system.measureTimeMillis

suspend fun buscarNotas(): List<Double> { delay(1_000); return listOf(8.0, 9.0) }
suspend fun buscarFaltas(): Int { delay(1_000); return 2 }

//sampleStart
fun main() = runBlocking {
    val job: Job = launch {
        repeat(3) { i ->
            println("Processando $i")
            delay(200)
        }
    }

    val tempo = measureTimeMillis {
        val notas = async { buscarNotas() }     // 1 s
        val faltas = async { buscarFaltas() }   // 1 s
        println("${notas.await()} / ${faltas.await()}")
    }
    println("Em paralelo: $tempo ms")     // ~1000

    job.join()
}
//sampleEnd
