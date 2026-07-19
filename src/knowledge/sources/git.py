from pathlib import Path

def scan(path):
    root = Path(path).expanduser()
    
    # Expanded list of exact folder names we never want to look inside
    ignored_dirs = {
        ".git", "node_modules", ".venv", "venv", 
        "__pycache__", "knowledge_index.egg-info", "dist", "build"
    }
    valid_suffixes = {".md", ".py", ".js", ".ts"}

    stack = [root]
    
    while stack:
        current_dir = stack.pop()
        
        try:
            for item in current_dir.iterdir():
                if item.is_dir():
                    # If this directory or ANY of its parent directories match our blocklist, prune it
                    if item.name in ignored_dirs or any(p.name in ignored_dirs for p in item.parents):
                        continue
                    stack.append(item)
                elif item.is_file():
                    if item.suffix in valid_suffixes:
                        yield item
        except PermissionError:
            continue
