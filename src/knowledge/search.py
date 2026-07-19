import sys
from knowledge.storage import KnowledgeDB

def main():
    # Ensure the user passed a search term in the terminal
    if len(sys.argv) < 2:
        print("Usage: python -m knowledge.search '<query_string>'")
        sys.exit(1)
        
    query_string = sys.argv[1]
    db = KnowledgeDB()
    
    print(f"Searching for: '{query_string}'...\n")
    results = db.search(query_string)
    
    if not results:
        print("No matches found.")
        return
        
    for index, (path, title, snippet) in enumerate(results, start=1):
        print(f"[{index}] {title}")
        print(f"    Path:    {path}")
        print(f"    Snippet: {snippet}")
        print("-" * 50)

if __name__ == "__main__":
    main()
