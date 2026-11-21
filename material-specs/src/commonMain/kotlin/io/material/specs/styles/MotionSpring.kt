package io.material.specs.styles

/**
 * Spring parameters from [Material motion specs](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs).
 *
 * @property dampingRatio Dimensionless spring damping ratio.
 * @property stiffness Spring stiffness used by Compose animation springs.
 */
data class MotionSpring(val dampingRatio: Float, val stiffness: Float) {
    companion object {
        /** `md.sys.motion.spring.fast.spatial`, Standard / Android context. */
        val fastSpatialStandard: MotionSpring = MotionSpring(dampingRatio = 0.9f, stiffness = 1400f)

        /** `md.sys.motion.spring.fast.spatial`, Expressive / Android context. */
        val fastSpatialExpressive: MotionSpring = MotionSpring(dampingRatio = 0.6f, stiffness = 800f)
    }
}
