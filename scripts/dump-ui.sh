#!/usr/bin/env bash
# Dump Android UI hierarchy to docs/locators/<screen_name>.xml
set -euo pipefail

SCREEN_NAME="${1:-screen}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$REPO_ROOT/docs/locators"
OUT_FILE="$OUT_DIR/${SCREEN_NAME}.xml"
REMOTE="/sdcard/window_dump.xml"

ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
ADB="$ANDROID_HOME/platform-tools/adb"

if [[ ! -x "$ADB" ]]; then
  echo "ERROR: adb not found at $ADB" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

echo "Dumping UI to $OUT_FILE ..."
"$ADB" shell uiautomator dump "$REMOTE" >/dev/null
"$ADB" pull "$REMOTE" "$OUT_FILE" >/dev/null
"$ADB" shell rm -f "$REMOTE" >/dev/null 2>&1 || true

echo "UI dump saved: $OUT_FILE"
wc -l "$OUT_FILE"
