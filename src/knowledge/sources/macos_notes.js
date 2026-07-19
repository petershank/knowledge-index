import { execSync } from "child_process";

/**
 * Streams raw title, body, and id from Notes.app via standard input.
 * No HTML manipulation, no tag parsing, just pure plaintext data extraction.
 */
function getRawNotes() {
  const appleScript = `
    tell application "Notes"
        set output to ""
        set allNotes to notes of default account
        repeat with currentNote in allNotes
            set noteID to id of currentNote
            set noteTitle to name of currentNote
            set noteBody to plaintext of currentNote
            
            set output to output & noteID & "|||" & noteTitle & "|||" & noteBody & "===ENDNOTE==="
        end repeat
        return output
    end tell
  `;

  try {
    // We provide a massive 100MB buffer to handle extensive note histories
    const stdout = execSync("osascript -", {
      input: appleScript,
      encoding: "utf-8",
      maxBuffer: 1024 * 1024 * 100,
    });

    const rawRows = stdout.split("===ENDNOTE===");
    const notes = [];

    for (const row of rawRows) {
      if (!row.trim()) continue;
      const [id, title, body] = row.split("|||");

      notes.push({
        id: id?.trim(),
        title: title?.trim(),
        body: body?.trim() || "",
      });
    }

    return notes;
  } catch (error) {
    console.error("Failed to fetch notes from AppleScript:", error.message);
    return [];
  }
}

// Main execution block: Output cleanly structured JSON straight to standard output
const notes = getRawNotes();
process.stdout.write(JSON.stringify(notes));
