import json
import subprocess
import tomllib
from datetime import datetime
from pathlib import Path

from knowledge.models import create_document_from_file, Document
from knowledge.sources.git import scan
from knowledge.storage import KnowledgeDB


def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    db = KnowledgeDB()
    total_saved = 0

    # ==========================================
    # PHASE 1: Scan Git Source Repositories
    # ==========================================
    for source in config["sources"]:
        if source["type"] == "git":
            print(f"Scanning Git repository: {source['path']}...")
            repo_count = 0
            
            for file_path_str in scan(source["path"]):
                file_path = Path(file_path_str)
                doc = create_document_from_file(file_path)
                if doc:
                    db.save_document(doc)
                    repo_count += 1
                    total_saved += 1
            
            print(f"-> Indexed {repo_count} files from this Git source.")

    # ==========================================
    # PHASE 2: Execute macOS Notes Extraction
    # ==========================================
    print("\nExecuting macOS Notes.app sync (this will take up to 2 minutes)...")
    try:
        # Run the Node script and capture its pure JSON string output
        result = subprocess.run(
            ["node", "src/knowledge/sources/macos_notes.js"],
            capture_output=True,
            text=True,
            check=True
        )
        
        notes_data = json.loads(result.stdout)
        notes_count = 0
        
        for note in notes_data:
            # Map raw Node dictionary into our exact standardized Document domain object
            doc = Document(
                id=f"notes://{note['id']}",
                content=note['body'],
                title=note['title'],
                source_type="macos_notes",
                path=f"apple-notes://showNote?identifier={note['id']}",
                modified_at=datetime.now() # Fallback for now to satisfy data domain
            )
            db.save_document(doc)
            notes_count += 1
            total_saved += 1
            
        print(f"-> Indexed {notes_count} native apple notes successfully.")
            
    except Exception as e:
        print(f"❌ Skipped Apple Notes phase due to integration error: {e}")

    print(f"\n🎉 Successfully indexed {total_saved} total items into your Second Brain database!")


if __name__ == "__main__":
    main()
