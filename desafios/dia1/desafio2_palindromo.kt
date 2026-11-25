// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · DESAFIO (slide 29)
// desafio2_palindromo.kt
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM), clique em Run e deixe tudo ✅.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════
/*
 DESAFIO 2 · Palíndromos com acento                         nível: MÉDIO
 Treina: extension functions, operações em String, filter, interoperabilidade Java.

 Um palíndromo se lê igual nos dois sentidos, ignorando maiúsculas, acentos,
 espaços e pontuação: "Socorram-me, subi no ônibus em Marrocos".

 A extensão semAcentos() já está pronta (ela usa java.text.Normalizer, do Java).

 1) String.normalizar(): minúsculas, sem acentos e só com letras e dígitos.
 2) String.ehPalindromo(): true se o texto normalizado é igual ao seu reverso.
 3) palindromosDa(frases): só as frases que são palíndromos, na ordem original.
*/

fun String.semAcentos(): String =
    java.text.Normalizer.normalize(this, java.text.Normalizer.Form.NFD)
        .replace(Regex("\\p{Mn}+"), "")

fun String.normalizar(): String =
    TODO("Use lowercase(), semAcentos() e filter { it.isLetterOrDigit() }")

fun String.ehPalindromo(): Boolean =
    TODO("Compare normalizar() com normalizar().reversed()")

fun palindromosDa(frases: List<String>): List<String> =
    TODO("Use filter com a extensão ehPalindromo()")

fun main() {
    verificar("\"Ônibus, Já!\" normaliza para \"onibusja\"") { "Ônibus, Já!".normalizar() == "onibusja" }
    verificar("frase com acento é palíndromo") { "Socorram-me, subi no ônibus em Marrocos".ehPalindromo() }
    verificar("\"A base do teto desaba.\" é palíndromo") { "A base do teto desaba.".ehPalindromo() }
    verificar("\"Kotlin\" não é palíndromo") { !"Kotlin".ehPalindromo() }
    verificar("filtra uma lista de frases") {
        palindromosDa(listOf("Arara", "IFCE", "Roma me tem amor")) == listOf("Arara", "Roma me tem amor")
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
