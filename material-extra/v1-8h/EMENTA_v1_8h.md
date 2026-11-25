# Ementa — Minicurso de Kotlin: da história ao Multiplatform

**Público:** estudantes de Engenharia de Computação — IFCE, Campus Fortaleza
**Carga horária sugerida:** 8 h (2 encontros de 4 h)
**Pré-requisitos:** lógica de programação e noções de orientação a objetos. Conhecer Java, C ou Python ajuda, mas não é obrigatório.
**Ambiente:** navegador (Kotlin Playground), IntelliJ IDEA ou Android Studio, JDK 21.

## Objetivo geral

Capacitar o estudante a ler e escrever Kotlin idiomático, compreender o modelo de concorrência com corrotinas, integrar Kotlin ao ecossistema Java e conhecer o desenvolvimento multiplataforma com Kotlin Multiplatform (KMP) e Compose Multiplatform.

## Objetivos específicos

- Conhecer a origem, as motivações de design e a evolução da linguagem até o Kotlin 2.4.
- Dominar a sintaxe essencial: variáveis, tipos, null safety, expressões `if`/`when`, coleções.
- Aplicar funções de ordem superior, lambdas, funções de escopo e extensões.
- Modelar domínios com classes, `data class`, `sealed`, `object`, delegação e generics.
- Usar recursos avançados: DSLs type-safe, context parameters, `Result` e plugins do compilador.
- Escrever código concorrente com corrotinas, concorrência estruturada e `Flow`.
- Usar bibliotecas Java em Kotlin e expor código Kotlin para Java.
- Entender a arquitetura de um projeto KMP e o papel do Compose Multiplatform.
- Conhecer o ecossistema: Ktor, Exposed, Spring, ferramentas, testes, dados e IA.

## Conteúdo programático

| Módulo | Tema | Tópicos | Tempo |
|---|---|---|---|
| 01 | História | JetBrains e a motivação (2010), Kotlin 1.0 (2016), Google I/O 2017, Android Kotlin-first (2019), KMP estável (2023), Kotlin 2.0/K2 (2024), Kotlin 2.4 (2026); filosofia da linguagem | 20 min |
| 02 | Fundamentos | `fun main`, compilação para JVM/Native/Wasm/JS, `val`/`var`, tipos e hierarquia (`Any`, `Unit`, `Nothing`), strings, null safety, smart casts, `if`/`when` como expressões, laços e ranges, coleções e sequências | 50 min |
| 03 | Funções | parâmetros padrão e nomeados, lambdas, trailing lambdas, funções de escopo, `inline`/`reified`, `infix`, `operator`, `tailrec`, extension functions e properties | 45 min |
| 04 | Classes e objetos | construtores e propriedades, `lateinit`, `lazy`, explicit backing fields, herança e interfaces, `data class`, `sealed`, `enum`, `object`, `companion object`, `value class`, delegação, generics e variância, visibilidade | 55 min |
| 05 | Recursos avançados | DSLs com lambdas com receptor, context parameters, exceções e `Result`, anotações, KSP e plugins do compilador | 30 min |
| 06 | Corrotinas | `suspend`, `launch`/`async`/`runBlocking`, dispatchers e `withContext`, concorrência estruturada, cancelamento e timeouts, `Flow`, `StateFlow`, `SharedFlow`, `Channel` | 55 min |
| 07 | Interoperabilidade Java | usando bibliotecas Java, conversão SAM, platform types e JSpecify, `@JvmStatic`/`@JvmOverloads`/`@JvmField`, Spring Boot e Gradle Kotlin DSL | 30 min |
| 08 | Kotlin Multiplatform | source sets, `expect`/`actual`, estrutura de projeto, Compose Multiplatform e Hot Reload, bibliotecas KMP, Kotlin/Native, Wasm e JS, casos de uso | 50 min |
| 09 | Ecossistema | Ktor e Exposed, ferramentas (IntelliJ, Kotlin LSP, Gradle/Amper, Kotlin Notebook), testes (`kotlin.test`, `runTest`, MockK), dados e IA (DataFrame, Koog), novidades do 2.x | 30 min |
| 10 | Mão na massa | projeto integrador TaskFlow (modelo, repositório com `StateFlow`, extensões, corrotinas) e exercícios | 45 min |

**Encontro 1:** módulos 01–05 · **Encontro 2:** módulos 06–10 (incluindo intervalos de ~10 min).

## Metodologia

Exposição dialogada curta seguida de código ao vivo (Kotlin Playground / IntelliJ IDEA), exercícios rápidos ao fim de cada módulo e projeto integrador no encerramento.

## Avaliação (sugestão)

Participação nos exercícios em aula e entrega opcional de um dos desafios do módulo 10 (API TaskFlow com Ktor ou app Compose Multiplatform).

## Referências

- Documentação oficial: https://kotlinlang.org/docs
- Kotlin Koans: https://kotlinlang.org/docs/koans.html
- Kotlin Multiplatform: https://kotlinlang.org/docs/multiplatform/ e https://kmp.jetbrains.com
- Novidades das versões: https://kotlinlang.org/docs/whatsnew.html
- Corrotinas: https://kotlinlang.org/docs/coroutines-guide.html
- Ktor: https://ktor.io · Exposed: https://www.jetbrains.com/exposed/
- Estudos de caso: https://kotlinlang.org/case-studies/
