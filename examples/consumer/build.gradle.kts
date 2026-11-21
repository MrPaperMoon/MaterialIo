plugins {
    kotlin("multiplatform") version "2.4.20"
    kotlin("plugin.compose") version "2.4.20"
}

kotlin {
    jvm()

    sourceSets.commonMain.dependencies {
        val group = if (providers.gradleProperty("materialSpecsRepository").isPresent) {
            "com.github.MrPaperMoon.MaterialIo"
        } else {
            "io.material"
        }
        val version = providers.gradleProperty("materialSpecsVersion").orElse("0.1.0").get()
        implementation("$group:material-specs:$version")
    }
}
