// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · DESAFIO (slide 52)
// desafio1_formas.kt
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM), clique em Run e deixe tudo ✅.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════
/*
 DESAFIO 1 · Formas geométricas                             nível: FÁCIL
 Treina: sealed interface, data class, when exaustivo (sem else), extensões.

 1) Forma.area(): área de cada forma. Círculo: π·r². Retângulo: l·a. Triângulo: b·a/2.
 2) Forma.nome(): "círculo", "retângulo" ou "triângulo".
 3) List<Forma>.areaTotal(): soma das áreas.
 4) List<Forma>.maior(): a forma de maior área, ou null se a lista estiver vazia.

 Regra: nada de else nos when. O compilador deve garantir todos os casos.
*/
import kotlin.math.PI
import kotlin.math.abs

sealed interface Forma {
    data class Circulo(val raio: Double) : Forma
    data class Retangulo(val largura: Double, val altura: Double) : Forma
    data class Triangulo(val base: Double, val altura: Double) : Forma
}

fun Forma.area(): Double =
    TODO("when (this) com os três casos")

fun Forma.nome(): String =
    TODO("when (this) com os três casos")

fun List<Forma>.areaTotal(): Double =
    TODO("sumOf")

fun List<Forma>.maior(): Forma? =
    TODO("maxByOrNull")

fun main() {
    val formas = listOf(Forma.Retangulo(2.0, 3.0), Forma.Triangulo(4.0, 5.0), Forma.Circulo(1.0))
    verificar("área do círculo de raio 1 é π") { abs(Forma.Circulo(1.0).area() - PI) < 1e-9 }
    verificar("retângulo 2×3 = 6 e triângulo 4×5 = 10") {
        Forma.Retangulo(2.0, 3.0).area() == 6.0 && Forma.Triangulo(4.0, 5.0).area() == 10.0
    }
    verificar("nomes das formas") { formas.map { it.nome() } == listOf("retângulo", "triângulo", "círculo") }
    verificar("área total ≈ 19.14") { abs(formas.areaTotal() - (16.0 + PI)) < 1e-9 }
    verificar("maior forma é o triângulo; lista vazia dá null") {
        formas.maior() == Forma.Triangulo(4.0, 5.0) && emptyList<Forma>().maior() == null
    }
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
