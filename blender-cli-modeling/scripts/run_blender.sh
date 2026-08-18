#!/bin/zsh
set -euo pipefail

blender_cli_candidates=()

if [[ -n "${BLENDER_CLI_BIN:-}" ]]; then
  blender_cli_candidates+=("$BLENDER_CLI_BIN")
fi

blender_cli_candidates+=(
  '/Applications/Blender.app/Contents/MacOS/Blender'
  "$HOME/Library/Application Support/Steam/steamapps/common/Blender/Blender.app/Contents/MacOS/Blender"
  "$HOME/Applications/Blender.app/Contents/MacOS/Blender"
)

blender_cli_path_candidate="$(command -v blender 2>/dev/null || true)"
if [[ -n "$blender_cli_path_candidate" ]]; then
  blender_cli_candidates+=("$blender_cli_path_candidate")
fi

blender_cli_bin=''
for blender_cli_candidate in "${blender_cli_candidates[@]}"; do
  if [[ -f "$blender_cli_candidate" && -x "$blender_cli_candidate" ]]; then
    blender_cli_bin="$blender_cli_candidate"
    break
  fi
done

if [[ -z "$blender_cli_bin" ]]; then
  print -u2 'Blender CLI executable not found. Set BLENDER_CLI_BIN to Contents/MacOS/Blender.'
  exit 127
fi

if [[ "${1:-}" == '--resolve-only' ]]; then
  print -r -- "$blender_cli_bin"
  exit 0
fi

if (( $# == 0 )); then
  print -u2 'Usage: run_blender.sh <Blender arguments>'
  exit 64
fi

exec "$blender_cli_bin" \
  --background \
  --factory-startup \
  --disable-autoexec \
  --python-exit-code 1 \
  "$@"
