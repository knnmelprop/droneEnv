#!/usr/bin/env bash
set -euo pipefail

# Detect Codespaces and headless env
IN_CODESPACES=${CODESPACES:-false}
HEADLESS=1
if [[ -n "${DISPLAY:-}" ]]; then
  HEADLESS=0
fi

# Prefer safe backend in headless or Codespaces
if [[ "$IN_CODESPACES" = "true" || "$HEADLESS" -eq 1 ]]; then
  export MPLBACKEND=${MPLBACKEND:-Agg}
else
  export MPLBACKEND=${MPLBACKEND:-Agg}
fi

# Ensure directories
mkdir -p /workspace/student_competition/results /workspace/student_competition/plots

# Ensure PYTHONPATH contains SUAVE trunk and student frameworks
export PYTHONPATH="/workspace/trunk:/workspace/student_competition:${PYTHONPATH:-}"

# Summarize environment
echo "Environment summary:"
echo "  Codespaces: $IN_CODESPACES"
echo "  Headless: $HEADLESS"
echo "  MPLBACKEND: ${MPLBACKEND}"
echo "  PYTHONPATH: ${PYTHONPATH}"
echo "  External tools:"
echo "    AVL_BIN=${AVL_BIN:-}"
echo "    SU2_BIN=${SU2_BIN:-}"
echo "    OPENVSP_BIN=${OPENVSP_BIN:-}"
echo "    GMSH_BIN=${GMSH_BIN:-}"

PORT=${PORT:-8888}
TOKEN_OPT="--ServerApp.token=${JUPYTER_TOKEN:-}"

case "${1:-jupyter}" in
  jupyter)
    echo "Starting Jupyter Lab on 0.0.0.0:${PORT}"
    exec jupyter lab --ip=0.0.0.0 --port="${PORT}" --no-browser ${TOKEN_OPT}
    ;;
  notebook)
    echo "Starting Jupyter Notebook on 0.0.0.0:${PORT}"
    exec jupyter notebook --ip=0.0.0.0 --port="${PORT}" --no-browser ${TOKEN_OPT}
    ;;
  bash)
    exec bash
    ;;
  python)
    shift || true
    exec python "$@"
    ;;
  run)
    shift || true
    exec "$@"
    ;;
  *)
    exec "$@"
    ;;

esac