# Devcontainer Installation Notes

- Git LFS is installed and initialized during postCreateCommand.
- Python 3.9 base with scientific stack installed via `requirements.txt`.
- SUAVE is installed in editable mode from `trunk` using `python3.9 setup.py develop`.
- Jupyter is available; use Command Palette: "Jupyter: Create New Jupyter Notebook".
- Ports exposed: 8888 (Jupyter), 3000, 7860. In Codespaces, forwarded ports are auto-detected.
- Matplotlib backend defaults to Agg in headless mode.

## Optional: SU2 and AVL

- Build args (configure in `devcontainer.json` → build.args):
  - `SU2_DOWNLOAD_URL`: prebuilt SU2 Linux tarball URL; populates `/opt/su2` and adds to `PATH`.
  - `AVL_DOWNLOAD_URL`: direct URL to an `avl` executable; installed to `/usr/local/bin/avl`.
- Environment variables available inside container:
  - `SU2_HOME=/opt/su2`, `SU2_RUN=/opt/su2/bin`, `SU2_BIN=/opt/su2/bin/SU2_CFD`
  - `AVL_BIN=/usr/local/bin/avl`
- Official docs:
  - SU2: see the installation section on the SU2 website for precompiled binaries or source builds.
  - AVL: see the MIT AVL page for downloads and usage.