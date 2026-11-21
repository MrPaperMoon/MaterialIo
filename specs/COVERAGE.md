# Token coverage

Snapshot: `2026-11-19_06-20-01`. All published table tokens have an API mapping.

Shared token sets are counted once, under their owning component. See `api-index.json`.

| Specs page | Kotlin package | Objects | Token properties |
| --- | --- | ---: | ---: |
| [All buttons](https://m3.material.io/components/all-buttons/specs) | `all_buttons` | 0 | 0 |
| [App bars](https://m3.material.io/components/app-bars/specs) | `app_bars` | 10 | 114 |
| [Badges](https://m3.material.io/components/badges/specs) | `badges` | 1 | 13 |
| [Bottom sheets](https://m3.material.io/components/bottom-sheets/specs) | `bottom_sheets` | 1 | 13 |
| [Button groups](https://m3.material.io/components/button-groups/specs) | `button_groups` | 10 | 55 |
| [Buttons](https://m3.material.io/components/buttons/specs) | `buttons` | 16 | 554 |
| [Cards](https://m3.material.io/components/cards/specs) | `cards` | 3 | 81 |
| [Carousel](https://m3.material.io/components/carousel/specs) | `carousel` | 1 | 27 |
| [Checkbox](https://m3.material.io/components/checkbox/specs) | `checkbox` | 1 | 81 |
| [Chips](https://m3.material.io/components/chips/specs) | `chips` | 4 | 316 |
| [Date pickers](https://m3.material.io/components/date-pickers/specs) | `date_pickers` | 3 | 229 |
| [Dialogs](https://m3.material.io/components/dialogs/specs) | `dialogs` | 2 | 101 |
| [Divider](https://m3.material.io/components/divider/specs) | `divider` | 1 | 2 |
| [Extended FABs](https://m3.material.io/components/extended-fab/specs) | `extended_fab` | 12 | 298 |
| [FAB menu](https://m3.material.io/components/fab-menu/specs) | `fab_menu` | 7 | 117 |
| [FABs](https://m3.material.io/components/floating-action-button/specs) | `floating_action_button` | 21 | 469 |
| [Icon buttons](https://m3.material.io/components/icon-buttons/specs) | `icon_buttons` | 13 | 382 |
| [Lists](https://m3.material.io/components/lists/specs) | `lists` | 4 | 206 |
| [Loading indicator](https://m3.material.io/components/loading-indicator/specs) | `loading_indicator` | 1 | 8 |
| [Menus](https://m3.material.io/components/menus/specs) | `menus` | 4 | 262 |
| [Navigation bar](https://m3.material.io/components/navigation-bar/specs) | `navigation_bar` | 4 | 85 |
| [Navigation drawer](https://m3.material.io/components/navigation-drawer/specs) | `navigation_drawer` | 1 | 67 |
| [Navigation rail](https://m3.material.io/components/navigation-rail/specs) | `navigation_rail` | 7 | 124 |
| [Progress indicators](https://m3.material.io/components/progress-indicators/specs) | `progress_indicators` | 5 | 56 |
| [Radio button](https://m3.material.io/components/radio-button/specs) | `radio_button` | 1 | 26 |
| [Scroll fields](https://m3.material.io/components/scroll-fields/specs) | `scroll_fields` | 1 | 28 |
| [Search](https://m3.material.io/components/search/specs) | `search` | 2 | 85 |
| [Segmented buttons](https://m3.material.io/components/segmented-buttons/specs) | `segmented_buttons` | 1 | 46 |
| [Side sheets](https://m3.material.io/components/side-sheets/specs) | `side_sheets` | 1 | 31 |
| [Sliders](https://m3.material.io/components/sliders/specs) | `sliders` | 6 | 127 |
| [Snackbar](https://m3.material.io/components/snackbar/specs) | `snackbar` | 1 | 40 |
| [Split buttons](https://m3.material.io/components/split-button/specs) | `split_button` | 5 | 61 |
| [Switch](https://m3.material.io/components/switch/specs) | `switch` | 1 | 78 |
| [Tabs](https://m3.material.io/components/tabs/specs) | `tabs` | 2 | 83 |
| [Text fields](https://m3.material.io/components/text-fields/specs) | `text_fields` | 6 | 589 |
| [Time pickers](https://m3.material.io/components/time-pickers/specs) | `time_pickers` | 3 | 230 |
| [Toolbars](https://m3.material.io/components/toolbars/specs) | `toolbars` | 6 | 112 |
| [Tooltips](https://m3.material.io/components/tooltips/specs) | `tooltips` | 2 | 51 |

Total: 170 objects, 5247 token properties, 20 supplementary diagram measurements.

## Diagram coverage

The six App bar measurement diagrams have been visually reviewed. Additional measurements
are in `measurement-overrides.json`. Other component diagrams are preserved as source URLs
in `pages/*.json`; their numbers have not all been transcribed to Kotlin.

## Context coverage

The API uses 3P / Android / Static / Default, Standard motion, Mobile, None overlay.
System colors resolve against the current Compose MaterialTheme. The snapshots retain all
published contexts, but the API does not expose an automatic native-platform context switch.
