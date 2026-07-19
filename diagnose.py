# diagnose.py
import time
import tomllib
from pathlib import Path
from knowledge.sources.git import scan

def main():
    # 1. Target the global projects directory
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    
    # We will look inside whatever root path you set for your global git source
    git_source = next(s for s in config["sources"] if s["type"] == "git")
    root_path = Path(git_source["path"]).expanduser()
    
    print(f"Analyzing subdirectories inside {root_path}...\n")
    print(f"{'Repository Name':<30} | {'File Count':<10} | {'Time Taken':<10}")
    print("-" * 58)

    # 2. Scan each top-level project folder individually to isolate the performance leak
    for project_dir in root_path.iterdir():
        if project_dir.is_dir() and not project_dir.name.startswith('.'):
            
            start_time = time.time()
            file_count = 0
            
            # Run your scan logic specifically on just this one project
            try:
                for _ in scan(project_dir):
                    file_count += 1
            except Exception as e:
                print(f"Error scanning {project_dir.name}: {e}")
                continue
                
            elapsed_time = time.time() - start_time
            
            # Print status if it takes a significant amount of time or contains massive file counts
            if elapsed_time > 1.0 or file_count > 100:
                # Highlight projects taking way too long
                status = "⚠️ SLOW" if elapsed_time > 10.0 else ""
                print(f"{project_dir.name:<30} | {file_count:<10} | {elapsed_time:.2f}s {status}")

if __name__ == "__main__":
    main()
