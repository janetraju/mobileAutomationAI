#!/usr/bin/env bash
# Install APK/IPA on connected device. Uses APP_PATH from .env or first argument.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APK_PATH="${1:-}"

if [[ -z "$APK_PATH" ]] && [[ -f "$REPO_ROOT/.env" ]]; then
  # shellcheck disable=SC1091
  source <(grep -E '^APP_PATH=' "$REPO_ROOT/.env" | sed 's/^/export /')
  APK_PATH="${APP_PATH:-}"
fi

if [[ -z "$APK_PATH" ]]; then
  echo "Usage: $0 <path-to-apk>  OR  set APP_PATH in .env" >&2
  exit 1
fi

if [[ ! -f "$APK_PATH" ]]; then
  echo "ERROR: App binary not found: $APK_PATH" >&2
  exit 1
fi

ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
ADB="$ANDROID_HOME/platform-tools/adb"

if [[ ! -x "$ADB" ]]; then
  echo "ERROR: adb not found at $ADB" >&2
  exit 1
fi

echo "Installing $APK_PATH ..."
"$ADB" install -r -d "$APK_PATH"
echo "Install complete."
