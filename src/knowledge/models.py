# src/knowledge/models.py
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

@dataclass
class Document:
    id: str               # 64-character SHA-256 hash of the absolute path
    content: str          # Raw text content of the file
    title: str            # Filename (e.g., "README.md")
    source_type: str      # 'git', 'macos_notes', etc.
    path: str             # Absolute file path for human viewing/opening
    modified_at: datetime # File's last modified timestamp
    metadata: Dict[str, str] = field(default_factory=dict)


def generate_path_hash(file_path: Path) -> str:
    """Generates a stable, unique SHA-256 hash from a normalized file path."""
    normalized_path = str(file_path.resolve())
    return hashlib.sha256(normalized_path.encode("utf-8")).hexdigest()


def create_document_from_file(file_path: Path, source_type: str = "git") -> Optional[Document]:
    """Reads a file from disk and normalizes it into a Document object."""
    try:
        # Read text content cleanly, skipping binary artifacts if they appear
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        
        # Extract system metadata
        modified_timestamp = file_path.stat().st_mtime
        modified_at = datetime.fromtimestamp(modified_timestamp)
        
        # Instantiate Document with our stable path hash
        return Document(
            id=generate_path_hash(file_path),
            content=content,
            title=file_path.name,
            source_type=source_type,
            path=str(file_path.resolve()),
            modified_at=modified_at,
            metadata={"extension": file_path.suffix}
        )
    except Exception as e:
        print(f"Skipping {file_path} due to error: {e}")
        return None
