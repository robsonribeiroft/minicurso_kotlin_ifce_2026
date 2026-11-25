// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 34
// 03_heranca_interfaces.kt · Herança e interfaces
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

//sampleStart
interface Autenticavel {
    val usuario: String
    fun login() = println("$usuario entrou") // padrão
}

abstract class Pessoa(val nome: String) {
    abstract fun papel(): String
    open fun apresentar() = "Sou $nome, ${papel()}"
}

class Professor(nome: String, val area: String) :
    Pessoa(nome), Autenticavel {
    override val usuario = nome.lowercase()
    override fun papel() = "professor de $area"
    override fun apresentar() = super.apresentar() + "!"
}
//sampleEnd

fun main() {
    val p = Professor("Robson", "Kotlin")
    println(p.apresentar())
    p.login()
}
