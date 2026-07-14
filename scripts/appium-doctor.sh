#!/usr/bin/env bash
# Appium environment health check.
set -euo pipefail

echo "=== Appium version ==="
appium --version || { echo "Appium not installed. Run: npm install -g appium@2"; exit 1; }

echo ""
echo "=== Installed drivers ==="
appium driver list --installed 2>/dev/null || true

echo ""
echo "=== Node / npm ==="
node --version
npm --version

echo ""
echo "=== Java ==="
java -version 2>&1 || echo "WARN: Java not found (required for Android)"

echo ""
echo "=== Android SDK ==="
echo "ANDROID_HOME=${ANDROID_HOME:-not set}"
if [[ -n "${ANDROID_HOME:-}" ]]; then
  "$ANDROID_HOME/platform-tools/adb" version 2>/dev/null || true
fi

echo ""
echo "=== Xcode (macOS / iOS) ==="
if command -v xcodebuild &>/dev/null; then
  xcodebuild -version
else
  echo "xcodebuild not available (skip for Android-only hosts)"
fi

echo ""
echo "Doctor complete."
