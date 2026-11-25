// ══════════════════════════════════════════════════════════════
// Minicurso de Kotlin · IFCE 2026 · Dia 2 · slide 50
// 14_bonus_compose.kt · Compose Multiplatform: demo no navegador
// Como usar: cole TODO este arquivo em https://play.kotlinlang.org
// (versão 2.4.21, alvo JVM) e clique em Run.
// Link do Playground: <cole aqui>
// ══════════════════════════════════════════════════════════════

// BÔNUS (demo do ministrante). No Playground, escolha o alvo "Compose (Wasm)".
// Se a função de entrada abaixo não existir na sua versão do Playground, use o
// template de Compose do próprio Playground e cole apenas a função Contador().
import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.CanvasBasedWindow

//sampleStart
@Composable
fun Contador() {
    var cliques by remember { mutableStateOf(0) }
    Column(
        Modifier.padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Text("Olá, IFCE!", fontSize = 28.sp)
        Text("Cliques: $cliques")
        Button(onClick = { cliques++ }) {
            Text("Clique aqui")
        }
    }
}
//sampleEnd

@OptIn(ExperimentalComposeUiApi::class)
fun main() {
    CanvasBasedWindow { MaterialTheme { Contador() } }
}
