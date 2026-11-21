# Sources and attribution

Material Design specifications and design token data are published by Google:
https://m3.material.io/components

The JSON snapshots are extracted from the publicly served Material Design website.
`specs/manifest.json` records the exact source URLs and snapshot version.
The token snapshots retain original token names, values, context labels and reference
chains; they omit unrelated author/account metadata. Each table records the SHA-256
of its original server response. Kotlin identifiers and Compose mappings are generated
by this project. This is an independent library, not an official Google package.

Roboto font files are from https://github.com/googlefonts/roboto/tree/main/src/hinted.
Their Apache License 2.0 is included in
`material-specs/src/commonMain/composeResources/font/Roboto-LICENSE.txt`.

Material illustrations remain attributed to Google. Their original URLs are retained
in `specs/pages`; the six local App bar measurement images are source evidence for
`specs/measurement-overrides.json`.
