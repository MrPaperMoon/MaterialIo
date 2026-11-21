plugins {
    kotlin("multiplatform")
    kotlin("plugin.compose")
    id("org.jetbrains.compose")
    id("com.android.kotlin.multiplatform.library")
    `maven-publish`
}

group = providers.gradleProperty("publicationGroup").orElse("io.material").get()
version = providers.gradleProperty("publicationVersion").orElse("0.1.0").get()

kotlin {
    android {
        namespace = "io.material.specs"
        compileSdk = 37
        minSdk = 23
        withHostTest {}
    }
    jvm()
    iosArm64()
    iosSimulatorArm64()
    js { browser() }
    @OptIn(org.jetbrains.kotlin.gradle.ExperimentalWasmDsl::class)
    wasmJs { browser() }

    sourceSets {
        commonMain.dependencies {
            api("org.jetbrains.compose.runtime:runtime:1.11.1")
            api("org.jetbrains.compose.foundation:foundation:1.11.1")
            api("org.jetbrains.compose.material3:material3:1.9.0")
            implementation("org.jetbrains.compose.components:components-resources:1.11.1")
        }
        commonTest.dependencies {
            implementation(kotlin("test"))
        }
    }
}

compose.resources {
    packageOfResClass = "io.material.specs.resources"
}

publishing {
    repositories {
        maven {
            name = "localBuild"
            url = rootProject.layout.buildDirectory.dir("repo").get().asFile.toURI()
        }
    }
}
