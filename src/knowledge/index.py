from pathlib import Path
import tomllib

from knowledge.sources.git import scan


def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    for source in config["sources"]:
        if source["type"] == "git":
            print(f"Scanning {source['path']}")

            for file in scan(source["path"]):
                print(file)


if __name__ == "__main__":
    main()