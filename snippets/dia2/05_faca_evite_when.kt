// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 37
// 05_faca_evite_when.kt · Faça / Evite: when com sealed
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

sealed interface Pagamento {
    data class Pix(val chave: String) : Pagamento
    data class Cartao(val parcelas: Int) : Pagamento
    data object Boleto : Pagamento
}

//sampleStart
fun taxa(p: Pagamento): Double = when (p) {
    is Pagamento.Pix -> 0.0
    is Pagamento.Cartao -> 0.02 * p.parcelas
    Pagamento.Boleto -> 1.5
}
//sampleEnd

//sampleStart
fun taxaFragil(p: Pagamento): Double = when (p) {
    is Pagamento.Pix -> 0.0
    else -> 1.5                 // e se surgir Pagamento.Cripto?
}
//sampleEnd

fun main() {
    println(taxa(Pagamento.Cartao(3)))         // 0.06
    println(taxaFragil(Pagamento.Cartao(3)))   // 1.5: errado e silencioso
}
