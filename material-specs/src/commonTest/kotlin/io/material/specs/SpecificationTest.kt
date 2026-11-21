package io.material.specs

import androidx.compose.ui.unit.dp
import io.material.specs.app_bars.AppBarCommon
import io.material.specs.app_bars.AppBarLargeFlexible
import io.material.specs.app_bars.AppBarMediumFlexible
import io.material.specs.app_bars.AppBarSmall
import io.material.specs.styles.MotionSpring
import kotlin.test.Test
import kotlin.test.assertEquals

class SpecificationTest {
    @Test
    fun appBarVariantsRetainTheirOwnHeightAndSharedIconSize() {
        assertEquals(24.dp, AppBarCommon.iconSize)
        assertEquals(64.dp, AppBarSmall.containerHeight)
        assertEquals(112.dp, AppBarMediumFlexible.containerHeight)
        assertEquals(120.dp, AppBarLargeFlexible.containerHeight)
        assertEquals(152.dp, AppBarLargeFlexible.withSubtitleContainerHeight)
    }

    @Test
    fun expressiveMotionIsDistinctFromStandardMotion() {
        assertEquals(0.9f, MotionSpring.fastSpatialStandard.dampingRatio)
        assertEquals(1400f, MotionSpring.fastSpatialStandard.stiffness)
        assertEquals(0.6f, MotionSpring.fastSpatialExpressive.dampingRatio)
        assertEquals(800f, MotionSpring.fastSpatialExpressive.stiffness)
    }
}
