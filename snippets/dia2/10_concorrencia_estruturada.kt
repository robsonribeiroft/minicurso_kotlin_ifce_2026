// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 42
// 10_concorrencia_estruturada.kt · Concorrência estruturada
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

import kotlinx.coroutines.*

data class Painel(val perfil: String, val notas: List<Double>, val avisos: Int)

suspend fun buscarPerfil(id: Int): String { delay(300); return "Aluno $id" }
suspend fun buscarNotas(id: Int): List<Double> { delay(500); return listOf(9.0) }
suspend fun buscarAvisos(id: Int): Int { delay(200); return 3 }

//sampleStart
suspend fun painel(id: Int): Painel = coroutineScope {
    val perfil = async { buscarPerfil(id) }
    val notas = async { buscarNotas(id) }
    val avisos = async { buscarAvisos(id) }
    // se um falhar, os outros são cancelados
    Painel(perfil.await(), notas.await(), avisos.await())
}

fun main() = runBlocking {
    println(painel(42))
    val trataErro = CoroutineExceptionHandler { _, e ->
        println("isolado: ${e.message}")
    }
    supervisorScope {
        launch(trataErro) { error("falhou!") }  // isolado
        launch { delay(100); println("irmão terminou") }
    }
    println("o pai esperou todos os filhos")
}
//sampleEnd
