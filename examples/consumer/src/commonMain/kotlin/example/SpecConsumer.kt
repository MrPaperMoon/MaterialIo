package example

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.height
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import io.material.specs.app_bars.AppBarCommon
import io.material.specs.app_bars.AppBarLargeFlexible

/** Minimal consumer of the library through Gradle composite dependency substitution. */
@Composable
fun SpecConsumer() {
    Box(
        modifier = Modifier
            .height(AppBarLargeFlexible.containerHeight)
            .background(AppBarCommon.containerColor),
    ) {
        Text(text = "Material 3", style = AppBarLargeFlexible.titleFont)
    }
}
