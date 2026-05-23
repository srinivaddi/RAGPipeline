from pathlib import Path

def get_project_root():
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent

    raise RuntimeError("Project root not found")
