# Devcontainer Installation Notes

- Git LFS is installed and initialized during postCreateCommand.
- Python 3.9 base with scientific stack installed via `requirements.txt`.
- SUAVE is installed in editable mode from `trunk` using `python3.9 setup.py develop`.
- Jupyter is available; use Command Palette: "Jupyter: Create New Jupyter Notebook".
- Ports exposed: 8888 (Jupyter), 3000, 7860. In Codespaces, forwarded ports are auto-detected.
- Matplotlib backend defaults to Agg in headless mode.