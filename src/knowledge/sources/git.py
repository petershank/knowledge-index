from pathlib import Path

def scan(path):
    root = Path(path).expanduser()
    
    # Exact folder names we never want to look inside
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
                    # Prune right here: if the directory is ignored, do not add it to the stack
                    if item.name in ignored_dirs:
                        continue
                    stack.append(item)
                elif item.is_file():
                    if item.suffix in valid_suffixes:
                        yield item
        except PermissionError:
            continue
