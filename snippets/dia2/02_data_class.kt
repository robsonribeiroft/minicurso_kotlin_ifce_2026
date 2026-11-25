// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 33
// 02_data_class.kt · data class
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
data class Produto(
    val nome: String,
    val preco: Double,
    val estoque: Int = 0,
)

fun main() {
    val p1 = Produto("Teclado", 199.9)
    val p2 = p1.copy(preco = 179.9)    // imutabilidade

    println(p1)                        // toString gerado
    println(p1 == Produto("Teclado", 199.9)) // true
    println(p1 === p2)                 // false: referência

    val (nome, preco) = p2             // desestruturação
    println("$nome: $preco")
}
//sampleEnd
