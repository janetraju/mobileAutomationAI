#!/usr/bin/env bash
# Start Android emulator. Set AVD_NAME or pass via invoke emulator:start --avd=<name>
set -euo pipefail

AVD_NAME="${AVD_NAME:-Pixel_10}"
HEADLESS="${HEADLESS:-false}"
ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
EMULATOR="$ANDROID_HOME/emulator/emulator"

if [[ ! -x "$EMULATOR" ]]; then
  echo "ERROR: emulator not found at $EMULATOR. Set ANDROID_HOME." >&2
  exit 1
fi

ARGS=(-avd "$AVD_NAME" -no-snapshot-load)
if [[ "$HEADLESS" == "true" ]]; then
  ARGS+=(-no-window -no-audio)
fi

echo "Starting emulator: $AVD_NAME (headless=$HEADLESS)"
"$EMULATOR" "${ARGS[@]}" &
EMULATOR_PID=$!

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/wait-for-device.sh"

echo "Emulator ready (PID $EMULATOR_PID)"

# Block here so this terminal stays attached to the emulator for its whole
# lifetime — otherwise invoke's pty closes right after boot and the emulator
# (still a background job in this session) gets SIGHUP'd and shuts down.
wait "$EMULATOR_PID"
