from pathlib import Path

def scan(path):
    root = Path(path).expanduser()
    
    # Define directories we want to completely ignore
    ignored_dirs = {".git", "node_modules", ".venv", "__pycache__", "knowledge_index.egg-info"}
    # Define target file extensions
    valid_suffixes = {".md", ".py", ".js", ".ts"}

    # os.walk style manual recursive traversal using Path
    # This allows us to modify 'dirs' in-place to stop recursion
    stack = [root]
    
    while stack:
        current_dir = stack.pop()
        
        try:
            for item in current_dir.iterdir():
                if item.is_dir():
                    # If the folder name is in our ignore list, skip it entirely
                    if item.name in ignored_dirs:
                        continue
                    stack.append(item)
                elif item.is_file():
                    if item.suffix in valid_suffixes:
                        yield item
        except PermissionError:
            # Safely skip folders your system user doesn't have rights to read
            continue
