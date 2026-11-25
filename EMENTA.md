# Ementa · Minicurso de Kotlin: da história ao Multiplatform

| | |
|---|---|
| **Público** | Estudantes de Engenharia de Computação · IFCE, Campus Fortaleza |
| **Carga horária** | **4 h**, em **2 encontros de 2 h** (com intervalo de 10 min em cada) |
| **Ministrante** | Robson Freitas Ribeiro · Senior Android Engineer na CI&T |
| **Pré-requisitos** | Lógica de programação e noções de orientação a objetos |
| **Ferramenta** | Somente o navegador: [Kotlin Playground](https://play.kotlinlang.org/) (Kotlin **2.4.21**, alvo **JVM**) |
| **Material** | Slides, snippets executáveis e desafios em [`github.com/robsonribeiroft/minicurso_kotlin_ifce_2026`](https://github.com/robsonribeiroft/minicurso_kotlin_ifce_2026) |

## Objetivo geral

Capacitar o estudante a ler e escrever Kotlin idiomático, modelar dados com classes da linguagem, escrever código concorrente com corrotinas e conhecer o alcance do Kotlin além da JVM (interoperabilidade com Java, Kotlin Multiplatform e Compose Multiplatform).

## Objetivos específicos

Ao final, o estudante será capaz de:

- explicar a origem e as decisões de design do Kotlin;
- usar `val`/`var`, o sistema de tipos, null safety, `if`/`when` como expressões e coleções;
- escrever funções com parâmetros padrão e nomeados, lambdas, funções de escopo e extensões;
- modelar domínios com `class`, `data class`, `sealed` com `when` exaustivo, `enum` e `object`;
- escrever código concorrente com `suspend`, `launch`/`async`, concorrência estruturada e `Flow`;
- reconhecer boas práticas e anti-patterns comuns (slides "Faça / Evite");
- situar Kotlin no ecossistema: bibliotecas Java, KMP, Compose Multiplatform e novidades do 2.x.

## Conteúdo programático

### Dia 1 · Fundamentos da linguagem (2 h)

| Horário | Bloco | Tópicos |
|---|---|---|
| 00:00 | Abertura · 10 min | apresentação do ministrante, ementa, tour do Kotlin Playground |
| 00:10 | 01 · História e filosofia · 10 min | JetBrains (2010), Kotlin 1.0 (2016), Google I/O 2017, Kotlin-first, KMP estável, Kotlin 2.0/K2, Kotlin 2.4 (2026); onde a linguagem é usada |
| 00:20 | 02 · Fundamentos · 35 min | `fun main`, `val`/`var`, tipos e hierarquia (`Any`, `Unit`, `Nothing`), strings e templates, null safety, `if`/`when` (com guard conditions), laços e ranges, coleções, operações funcionais e sequências · Faça/Evite: `!!` e coleções mutáveis expostas |
| 00:55 | Intervalo · 10 min | |
| 01:05 | 03 · Funções · 30 min | parâmetros padrão e nomeados, `vararg`, lambdas e funções de ordem superior, trailing lambdas, funções de escopo (`let`, `run`, `with`, `apply`, `also`), extension functions e properties |
| 01:35 | Hora do desafio · 25 min | Notas válidas (fácil) · Palíndromos com acento (médio) · Boletim da turma (desafio) |

### Dia 2 · Modelagem, concorrência e ecossistema (2 h)

| Horário | Bloco | Tópicos |
|---|---|---|
| 00:00 | Quiz do Dia 1 · 5 min | 3 perguntas rápidas de revisão |
| 00:05 | 04 · Classes e objetos · 30 min | construtores e propriedades, `data class`, herança e interfaces, `sealed` + `when` exaustivo, `enum`, `object` e `companion object` · Faça/Evite: `else` genérico em `when` |
| 00:35 | 05 · Corrotinas · 30 min | por que corrotinas, funções `suspend`, `launch`/`async`/`runBlocking`, concorrência estruturada, `Flow` · Faça/Evite: `GlobalScope` |
| 01:05 | Intervalo · 10 min | |
| 01:15 | 06 · Além do Playground · 15 min | interoperabilidade com Java (demo com `java.time`), Kotlin Multiplatform, Compose Multiplatform (demo Compose/Wasm no Playground), ecossistema e novidades do Kotlin 2.x |
| 01:30 | Hora do desafio e encerramento · 30 min | Formas geométricas (fácil) · Calculadora de expressões (médio) · Downloads paralelos (desafio) · indicações de estudo |

## Metodologia

Exposição dialogada curta seguida de código ao vivo no Kotlin Playground. Todo exemplo dos slides tem um arquivo correspondente em `snippets/`, autocontido e executável. Cada dia termina com três desafios com **autoavaliação**: o próprio programa verifica a solução e imprime ✅ ou ❌.

## Avaliação

Participação nos desafios em sala. Os gabaritos são publicados na branch `gabaritos` do repositório ao fim do curso.

## Para aprofundar

- Versão estendida (8 h) deste minicurso: [`material-extra/v1-8h`](material-extra/v1-8h), com DSLs, context parameters, generics e variância, delegação, interop Java ↔ Kotlin, Spring, testes e mais.
- Documentação oficial: <https://kotlinlang.org/docs>
- Kotlin Koans: <https://kotlinlang.org/docs/koans.html>
- Corrotinas: <https://kotlinlang.org/docs/coroutines-guide.html>
- Kotlin Multiplatform: <https://kotlinlang.org/docs/multiplatform/> e <https://kmp.jetbrains.com>
- Novidades das versões: <https://kotlinlang.org/docs/whatsnew.html>
