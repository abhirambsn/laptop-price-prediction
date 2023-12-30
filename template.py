from pathlib import Path

# Path: template.py

def create_template():
    files = [
        ".github/workflows/.gitkeep",
        "app/__init__.py",
        "app/models/.gitkeep",
        "app/logs/.gitkeep",
        "app/utils/__init__.py",
        "logs/.gitkeep",
        "data/.gitkeep",
        "pipeline/__init__.py",
        "pipeline/utils/__init__.py",
        "experiment/trails.ipynb",
        "models/.gitkeep",
        "README.md",
        "config.yaml",
        ".gitignore"
    ]

    for file in files:
        # Create the parent directories if the don't exist
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        # Create the file if it doesn't exist
        Path(file).touch(exist_ok=True)

if __name__ == "__main__":
    create_template()