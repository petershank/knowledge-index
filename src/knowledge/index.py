from pathlib import Path
import tomllib

from knowledge.sources.git import scan
from knowledge.models import create_document_from_file
from knowledge.storage import KnowledgeDB


def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    db = KnowledgeDB()
    total_saved = 0

    for source in config["sources"]:
        if source["type"] == "git":
            print(f"Scanning {source['path']}...")

            for file_path_str in scan(source["path"]):
                file_path = Path(file_path_str)
                doc = create_document_from_file(file_path)
                
                if doc:
                    db.save_document(doc)
                    total_saved += 1

    print(f"Successfully indexed {total_saved} total documents into the database!")


if __name__ == "__main__":
    main()
