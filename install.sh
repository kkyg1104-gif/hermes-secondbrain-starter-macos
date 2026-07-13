#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  bash install.sh --vault PATH [--setup-qmd] [--qmd-collection NAME] [--year YYYY] [--overwrite]

Examples:
  bash install.sh --vault "$HOME/Documents/SecondBrain"
  bash install.sh --vault "$HOME/Documents/SecondBrain" --setup-qmd --qmd-collection my-secondbrain

This creates an empty personal Obsidian SecondBrain / LLM Wiki skeleton.
It creates zero real projects, agendas, people, decisions, concepts, or sources.
USAGE
}

VAULT=""
YEAR="$(date +%Y)"
SETUP_QMD=0
QMD_COLLECTION="my-secondbrain"
OVERWRITE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vault)
      VAULT="${2:-}"
      shift 2
      ;;
    --year)
      YEAR="${2:-}"
      shift 2
      ;;
    --setup-qmd)
      SETUP_QMD=1
      shift
      ;;
    --qmd-collection)
      QMD_COLLECTION="${2:-}"
      shift 2
      ;;
    --overwrite)
      OVERWRITE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$VAULT" ]]; then
  echo "ERROR: --vault PATH is required." >&2
  usage >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP="$SCRIPT_DIR/scripts/bootstrap_personal_secondbrain.py"

if [[ ! -f "$BOOTSTRAP" ]]; then
  echo "ERROR: bootstrap script not found: $BOOTSTRAP" >&2
  exit 1
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "ERROR: python3 is required." >&2
  exit 1
fi

ARGS=("$BOOTSTRAP" "$VAULT" --year "$YEAR")
if [[ "$OVERWRITE" -eq 1 ]]; then
  ARGS+=(--overwrite)
fi
if [[ "$SETUP_QMD" -eq 1 ]]; then
  ARGS+=(--setup-qmd --qmd-collection "$QMD_COLLECTION")
fi

"$PYTHON_BIN" "${ARGS[@]}"

cat <<NEXT

DONE.

Next recommended checks:
  1. Open the vault in Obsidian: $VAULT
  2. Confirm Agent Rules and Tag Registry exist.
  3. If qmd was not configured, install and run:
       npm install -g @tobilu/qmd
       qmd collection add "$VAULT" --name "$QMD_COLLECTION"
       qmd context add qmd://$QMD_COLLECTION "My personal Obsidian SecondBrain / LLM Wiki."
       qmd update && qmd embed
       qmd search "My SecondBrain Agent Rules" --collection "$QMD_COLLECTION"
NEXT
