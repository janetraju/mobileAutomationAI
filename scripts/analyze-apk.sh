#!/usr/bin/env bash
# Extract package, activity, label, and app-type hints from APK/IPA.
set -euo pipefail

APK_PATH="${1:-}"
if [[ -z "$APK_PATH" || ! -f "$APK_PATH" ]]; then
  echo "Usage: $0 <path-to-apk>" >&2
  exit 1
fi

ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
AAPT="$(ls "$ANDROID_HOME/build-tools"/*/aapt 2>/dev/null | sort -V | tail -1)"

echo "=== File ==="
file "$APK_PATH"
echo ""

if [[ -x "$AAPT" ]]; then
  echo "=== Badging ==="
  "$AAPT" dump badging "$APK_PATH" | grep -E "package:|application-label:|launchable-activity:"
  echo ""
fi

echo "=== App type hints ==="
if unzip -l "$APK_PATH" 2>/dev/null | grep -q "libflutter.so"; then
  echo "APP_TYPE=flutter"
elif unzip -l "$APK_PATH" 2>/dev/null | grep -q "flutter_assets/"; then
  echo "APP_TYPE=flutter"
elif unzip -l "$APK_PATH" 2>/dev/null | grep -q "index.android.bundle"; then
  echo "APP_TYPE=rn"
elif unzip -l "$APK_PATH" | grep -qi "webview"; then
  echo "APP_TYPE=hybrid"
else
  echo "APP_TYPE=native"
fi

if unzip -l "$APK_PATH" | grep -q "assets/flutter_assets/.env"; then
  echo ""
  echo "=== Bundled flutter .env (non-secret keys only) ==="
  unzip -p "$APK_PATH" assets/flutter_assets/.env 2>/dev/null | grep -E '^(env|base_url|web_base_url)=' || true
fi
