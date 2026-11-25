// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 1 · DESAFIO (slide 29)
// desafio1_notas_validas.kt
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM), clique em Run e deixe tudo ✅.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════
/*
 DESAFIO 1 · Notas válidas                                  nível: FÁCIL
 Treina: null safety, toDoubleOrNull(), operador Elvis, takeIf, mapNotNull.

 Uma planilha exportou as notas da turma como texto. Algumas células vieram
 vazias, com vírgula no lugar do ponto, com espaços ou com valores fora de 0..10.

 1) notaOuNull(texto): converta o texto em Double. Aceite "7,5" e "7.5" e ignore
    espaços nas pontas. Retorne null se não for número ou se estiver fora de 0..10.
 2) notasValidas(entradas): devolva só as notas válidas, na ordem original.
 3) mediaOuZero(notas): a média das notas, ou 0.0 se a lista estiver vazia.

 Rode o programa: cada verificação imprime ✅ ou ❌.
*/

fun notaOuNull(texto: String): Double? =
    TODO("Use trim(), replace(',', '.'), toDoubleOrNull() e takeIf { it in 0.0..10.0 }")

fun notasValidas(entradas: List<String>): List<Double> =
    TODO("Use mapNotNull com a função notaOuNull")

fun mediaOuZero(notas: List<Double>): Double =
    TODO("Cuidado: average() de lista vazia é NaN")

fun main() {
    val planilha = listOf("8.5", " 7,0 ", "", "dez", "11", "-1", "10", "6.25")
    verificar("\"8.5\" vira 8.5") { notaOuNull("8.5") == 8.5 }
    verificar("\" 7,0 \" vira 7.0") { notaOuNull(" 7,0 ") == 7.0 }
    verificar("\"dez\" e \"\" viram null") { notaOuNull("dez") == null && notaOuNull("") == null }
    verificar("fora de 0..10 vira null") { notaOuNull("11") == null && notaOuNull("-1") == null }
    verificar("filtra a planilha") { notasValidas(planilha) == listOf(8.5, 7.0, 10.0, 6.25) }
    verificar("média da planilha é 7.9375") { mediaOuZero(notasValidas(planilha)) == 7.9375 }
    verificar("média de lista vazia é 0.0") { mediaOuZero(emptyList()) == 0.0 }
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
