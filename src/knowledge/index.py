from pathlib import Path
import tomllib

from knowledge.sources.git import scan
from knowledge.models import create_document_from_file


def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    for source in config["sources"]:
        if source["type"] == "git":
            print(f"Scanning {source['path']}")

            for file_path_str in scan(source["path"]):
                file_path = Path(file_path_str)
                doc = create_document_from_file(file_path)
                
                if doc:
                    print(f"ID: {doc.id}")
                    print(f"Title: {doc.title}")
                    print(f"Snippet: {repr(doc.content[:40])}")
                    print("-" * 20)


if __name__ == "__main__":
    main()
