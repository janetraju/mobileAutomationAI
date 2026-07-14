#!/usr/bin/env bash
# Wait until adb reports a connected device in 'device' state.
set -euo pipefail

ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
ADB="$ANDROID_HOME/platform-tools/adb"
TIMEOUT="${DEVICE_WAIT_TIMEOUT:-180}"
INTERVAL=2
ELAPSED=0

if [[ ! -x "$ADB" ]]; then
  echo "ERROR: adb not found at $ADB. Set ANDROID_HOME." >&2
  exit 1
fi

echo "Waiting for Android device (timeout ${TIMEOUT}s)..."
while [[ $ELAPSED -lt $TIMEOUT ]]; do
  if "$ADB" devices | awk 'NR>1 && $2=="device" {found=1} END {exit !found}'; then
    echo "Device connected."
    exit 0
  fi
  sleep "$INTERVAL"
  ELAPSED=$((ELAPSED + INTERVAL))
done

echo "ERROR: No device connected within ${TIMEOUT}s." >&2
"$ADB" devices
exit 1
