#!/usr/bin/env bash
# JitPack provides the Android SDK; install the compile SDK required by this library.
set -eu

sdk_root="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-/opt/android-sdk}}"
if command -v sdkmanager >/dev/null 2>&1; then
    sdk_manager="$(command -v sdkmanager)"
elif [ -x "$sdk_root/cmdline-tools/latest/bin/sdkmanager" ]; then
    sdk_manager="$sdk_root/cmdline-tools/latest/bin/sdkmanager"
else
    sdk_manager="$sdk_root/tools/bin/sdkmanager"
fi

yes | "$sdk_manager" --licenses >/dev/null
"$sdk_manager" "platforms;android-37"
