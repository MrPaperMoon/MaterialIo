pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        providers.gradleProperty("materialSpecsRepository").orNull?.let { repositoryUrl ->
            maven(repositoryUrl)
        }
    }
}

rootProject.name = "MaterialSpecsConsumer"
if (!providers.gradleProperty("materialSpecsRepository").isPresent) {
    includeBuild("../..")
}
