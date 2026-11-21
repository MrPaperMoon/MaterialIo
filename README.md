# MaterialIo

Библиотека спецификаций Material 3 для Compose Multiplatform. Модуль `material-specs`
содержит Kotlin `object` с типизированными свойствами `Dp`, `TextUnit`, `TextStyle`,
`Color`, `Shape`, `FontWeight` и `Float`. UI-компоненты библиотека не реализует.

Источник: [Material 3 Components](https://m3.material.io/components).
Снимок сайта: **2026-11-19_06-20-01**, таблицы DSDB **41.1.12**.

## Состав

- 37 страниц Specs, 170 наборов токенов, 5 247 уникальных токенов.
- 20 дополнительных размеров, вручную проверенных на схемах App bars.
- Все состояния, присутствующие в таблицах: disabled, hovered, focused, pressed,
  selected и другие; Expressive и baseline-наборы сохранены отдельно.
- Имена объектов и свойств образованы из имен токенов, например
  `md.comp.app-bar.large-flexible.container.height` → `AppBarLargeFlexible.containerHeight`.
- У каждого объекта есть ссылка на Specs; у каждого свойства — исходное имя токена.
  Свойства со схем без токенов помечены отдельно. Deprecated-токены имеют `@Deprecated`.

**Граница покрытия:** все токены из опубликованных таблиц этих страниц преобразованы в API.
Это не означает, что все числа из графических схем уже перенесены в Kotlin:
схемы App bars проверены вручную, остальные требуют отдельной визуальной сверки.
Исходный текст Specs и ссылки на изображения сохранены в `specs/pages`.
Обзорная страница `all-buttons` собственных Specs не имеет.

## Подключение

### JitPack

Публичный репозиторий: [MrPaperMoon/MaterialIo](https://github.com/MrPaperMoon/MaterialIo).

В `settings.gradle.kts` приложения:

```kotlin
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io") {
            content { includeGroup("com.github.MrPaperMoon.MaterialIo") }
        }
    }
}
```

В `build.gradle.kts` общего модуля:

```kotlin
kotlin.sourceSets.commonMain.dependencies {
    implementation("com.github.MrPaperMoon.MaterialIo:material-specs:0.1.0")
}
```

Используется KMP-модуль `material-specs`, а не агрегирующий POM всего репозитория.
Gradle выбирает платформенный артефакт через Gradle Module Metadata.
Версия совпадает с Git-тегом. [Состояние сборки JitPack](https://jitpack.io/#MrPaperMoon/MaterialIo/0.1.0).

`jitpack.yml` публикует все KMP-публикации в Maven Local, откуда JitPack забирает
артефакты. Group и version задаются до генерации POM и `.module`, чтобы ссылки
на Android/JVM/JS/Wasm/iOS-публикации использовали те же координаты.

### Локальный исходный проект

Можно включить проект как composite build. В `settings.gradle.kts` приложения:

```kotlin
includeBuild("../MaterialIo")
```

В зависимостях общего source set:

```kotlin
commonMain.dependencies {
    implementation("io.material:material-specs:0.1.0")
}
```

Отдельный пример такого подключения находится в `examples/consumer` и проверяется
командой `./gradlew -p examples/consumer compileKotlinJvm`.

Для включения одного модуля вместо composite build:

```kotlin
// settings.gradle.kts
include(":material-specs")
project(":material-specs").projectDir = file("../MaterialIo/material-specs")

// build.gradle.kts общего модуля
kotlin.sourceSets.commonMain.dependencies {
    implementation(project(":material-specs"))
}
```

Во втором варианте корневой проект должен предоставлять плагины Kotlin Multiplatform,
Compose Compiler, Compose Multiplatform и `com.android.kotlin.multiplatform.library`.

## Использование

```kotlin
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.height
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import io.material.specs.app_bars.AppBarCommon
import io.material.specs.app_bars.AppBarLargeFlexible

@Composable
fun Header() {
    Box(
        Modifier
            .height(AppBarLargeFlexible.containerHeight) // 120.dp
            .background(AppBarCommon.containerColor),
    ) {
        Text("Title", style = AppBarLargeFlexible.titleFont)
    }
}
```

Числовые размеры доступны вне композиции. Типографика использует Roboto из ресурсов
библиотеки, поэтому свойства `TextStyle` и `FontFamily` читаются внутри `@Composable`.
В Compose нет встроенного `FontFamily.Roboto`; доступен `MaterialFonts.roboto`.
Для замены шрифта можно вызвать `titleFont.copy(fontFamily = yourFontFamily)`.

Цвета с системной ролью читаются из текущего `MaterialTheme.colorScheme`, поэтому
учитывают светлую, тёмную и пользовательскую палитру. Opacity — отдельное свойство;
оно автоматически не применяется к цвету. Единственный цвет без системной роли,
baseline `NavigationDrawer.scrimColor`, сохранён как исходное значение.

По умолчанию выбран опубликованный контекст **3P / Android / Static / Default**
(Standard motion, Mobile, None elevation overlay). Это общие Compose-значения,
не переключение на native iOS/Web-спецификации по платформе запуска.
Все исходные контексты, включая iOS, контрастность и variable typography,
сохранены в снимке `specs/tokens/*.json.gz`; автоматически они не выбираются API.
Составные spring-токены используют `MotionSpring.fastSpatialStandard`; отдельно
доступен `MotionSpring.fastSpatialExpressive`.

Процентные значения представлены долями `Float`: `100% = 1f`, `15% = 0.15f`.
Это указано в KDoc соответствующих свойств. `Dp` — размеры и elevation,
`sp` — размер текста, line height и letter spacing.

## Структура

```text
material-specs/src/commonMain/kotlin/io/material/specs/
  app_bars/
    AppBarCommon.kt
    AppBarSmall.kt
    AppBarMediumFlexible.kt
    AppBarLargeFlexible.kt
    ...
  buttons/
  button_groups/
  icon_buttons/
  text_fields/
  ...
  styles/
specs/
  manifest.json                # страницы и URL источников
  api-index.json               # исходный токен → Kotlin-свойство
  coverage.json                # точные количества
  pages/                      # текст Specs, конфигурация таблиц, ссылки на схемы
  tokens/*.json.gz             # значения и контексты, SHA-256 ответа источника
  measurement-overrides.json  # проверенные дополнительные размеры App bars
tools/
  fetch_specs.py
  generate_specs.py
  test_generator.py
```

## Сборка и обновление

Используются Kotlin 2.4.20, Compose Multiplatform 1.11.1, Material3 1.9.0,
AGP 9.4.0, Gradle 9.6.0. Нужен совместимый JDK и Android SDK 37;
путь к SDK задаётся через `ANDROID_HOME` или `local.properties`.

```shell
./gradlew :material-specs:jvmTest :material-specs:assembleAndroidMain
./gradlew :material-specs:compileKotlinJs :material-specs:compileKotlinWasmJs
```

На Windows используется `gradlew.bat`. Объявлены Android, JVM, JS, Wasm,
iOS ARM64 и iOS Simulator ARM64. Компиляция и публикация iOS KLIB проверены
на Windows: Kotlin позволяет кросс-компиляцию этой библиотеки без cinterop.
Для сборки и запуска конечного iOS-приложения нужен macOS с Xcode.
Проверка JS/Wasm — компиляция,
без запуска приложения в браузере.

Для Maven-публикации в `build/repo`:

```shell
./gradlew :material-specs:publishAllPublicationsToLocalBuildRepository
```

Обновление исходных данных требует сети; генерация и проверки снимка — нет:

```shell
python tools/fetch_specs.py
python tools/generate_specs.py
python tools/generate_specs.py --check
python -m unittest discover -s tools -p "test_*.py"
```

Генератор останавливается при неизвестном типе, единице измерения, отсутствующем
контексте или коллизии имён. При обновлении нужно отдельно проверить изменения
контекста, motion-токенов и дополнительных размеров со схем.

Шрифты Roboto распространяются с Apache License 2.0; текст лицензии лежит рядом
с файлами шрифтов. Источники и атрибуция перечислены в `NOTICE.md`.
