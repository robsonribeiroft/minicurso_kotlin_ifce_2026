// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 41
// 08_suspend.kt · Funções suspend
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

import kotlinx.coroutines.*

data class Aluno(val nome: String)

//sampleStart
suspend fun buscarAluno(id: Int): Aluno {
    delay(300)                      // simula a rede
    return Aluno("Ana")
}

suspend fun buscarNotas(aluno: Aluno): List<Double> {
    delay(500)
    return listOf(8.0, 9.5, 7.5)
}

suspend fun boletim(id: Int): String {
    val aluno = buscarAluno(id)     // suspende aqui...
    val notas = buscarNotas(aluno)  // ...e aqui
    return "${aluno.nome}: ${notas.average()}"
}
//sampleEnd

fun main() = runBlocking {
    println(boletim(1))
}
