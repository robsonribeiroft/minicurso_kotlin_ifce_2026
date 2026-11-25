// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 44
// 11_faca_evite_escopo.kt · Faça / Evite: escopo das corrotinas
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

import kotlinx.coroutines.*

//sampleStart
class TelaDeNotas {
    private val escopo = CoroutineScope(Dispatchers.Default)
    fun carregar() = escopo.launch { delay(500); println("notas") }
    fun fechar() = escopo.cancel()
}
//sampleEnd

//sampleStart
@OptIn(DelicateCoroutinesApi::class)
fun carregarSemDono() = GlobalScope.launch {
    delay(500); println("ninguém mais está ouvindo...")
}
//sampleEnd

fun main() = runBlocking {
    val tela = TelaDeNotas()
    tela.carregar()
    tela.fechar()           // cancelado: "notas" não é impresso
    carregarSemDono()       // continua rodando sozinho
    delay(700)
}
