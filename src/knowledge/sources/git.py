from pathlib import Path

def scan(path):
    root = Path(path).expanduser()

    for item in root.rglob("*"):
        if item.is_file() and item.suffix in [".md", ".py", ".js", ".ts"]:
            yield item