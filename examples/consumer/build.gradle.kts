plugins {
    kotlin("multiplatform") version "2.4.20"
    kotlin("plugin.compose") version "2.4.20"
}

kotlin {
    jvm()

    sourceSets.commonMain.dependencies {
        implementation("io.material:material-specs:0.1.0")
    }
}
