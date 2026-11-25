// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 44
// 12_flow.kt · Flow: fluxos assíncronos de dados
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

//sampleStart
fun temperaturas(): Flow<Double> = flow {
    val leituras = listOf(30.0, 35.2, 31.0, 36.8, 37.5)
    for (c in leituras) {
        emit(c)                  // emite ao longo do tempo
        delay(300)
    }
}

fun main() = runBlocking {
    temperaturas()               // frio: roda no collect
        .map { it * 9 / 5 + 32 } // °C → °F
        .filter { it > 95 }
        .catch { e -> println("Erro: $e") }
        .collect { println("Alerta: $it °F") }
    println("fim do fluxo")
}
//sampleEnd
