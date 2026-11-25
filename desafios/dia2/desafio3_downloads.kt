// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · DESAFIO (slide 53)
// desafio3_downloads.kt
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM), clique em Run e deixe tudo ✅.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════
/*
 DESAFIO 3 · Downloads paralelos                            nível: DESAFIO
 Treina: suspend, coroutineScope, async/awaitAll, withTimeoutOrNull, Flow.

 A função baixar() já está pronta: cada download leva 1 segundo.

 1) baixarTodos(arquivos): baixe TODOS em paralelo e devolva a soma dos tamanhos.
    5 arquivos devem terminar em menos de 1,5 s (sequencial levaria 5 s).
 2) baixarComLimite(arquivo, limiteMs): devolva o tamanho, ou null se o download
    passar de limiteMs.
 3) progresso(arquivos): um Flow que emite quantos arquivos já foram baixados
    (1, 2, ..., n). Pode baixar um de cada vez.
*/
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlin.system.measureTimeMillis

// Não altere: simula o download de um arquivo (1 s cada).
suspend fun baixar(arquivo: String): Int {
    delay(1_000)
    return arquivo.length * 100          // "tamanho" em KB
}

suspend fun baixarTodos(arquivos: List<String>): Int =
    TODO("coroutineScope { arquivos.map { async { ... } }.awaitAll().sum() }")

suspend fun baixarComLimite(arquivo: String, limiteMs: Long): Int? =
    TODO("withTimeoutOrNull")

fun progresso(arquivos: List<String>): Flow<Int> =
    TODO("flow { } com emit a cada arquivo baixado")

fun main() {
    val arquivos = listOf("a.pdf", "b.png", "slides.pdf", "notas.txt", "video.mp4")
    verificar("soma dos tamanhos é 3800 KB") { runBlocking { baixarTodos(arquivos) } == 3800 }
    verificar("5 downloads em menos de 1,5 s") {
        measureTimeMillis { runBlocking { baixarTodos(arquivos) } } < 1_500
    }
    verificar("limite de 500 ms devolve null; de 1500 ms devolve 100") {
        runBlocking { baixarComLimite("x", 500) == null && baixarComLimite("y", 1_500) == 100 }
    }
    verificar("progresso emite 1, 2") { runBlocking { progresso(listOf("a", "b")).toList() } == listOf(1, 2) }
}

// ───────────── Autoavaliação: não altere daqui para baixo ─────────────
fun verificar(descricao: String, teste: () -> Boolean) {
    val resultado = try {
        if (teste()) "✅ Passou" else "❌ Falhou"
    } catch (e: NotImplementedError) {
        "❌ Ainda não implementado (TODO)"
    } catch (e: Exception) {
        "❌ Erro: ${e::class.simpleName}: ${e.message}"
    }
    println("$resultado — $descricao")
}
