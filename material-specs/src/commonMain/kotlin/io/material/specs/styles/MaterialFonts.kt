package io.material.specs.styles

import androidx.compose.runtime.Composable
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import io.material.specs.resources.Res
import io.material.specs.resources.roboto_bold
import io.material.specs.resources.roboto_medium
import io.material.specs.resources.roboto_regular
import org.jetbrains.compose.resources.Font

/** Bundled Roboto for the [Material type scale](https://m3.material.io/styles/typography/type-scale-tokens). */
object MaterialFonts {
    /** The same font files are used on every supported platform. */
    val roboto: FontFamily
        @Composable get() = FontFamily(
            Font(Res.font.roboto_regular, FontWeight.Normal),
            Font(Res.font.roboto_medium, FontWeight.Medium),
            Font(Res.font.roboto_bold, FontWeight.Bold),
        )
}
