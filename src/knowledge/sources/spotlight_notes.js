import { execSync } from "child_process";

function scanNotesViaSpotlight() {
  console.log("Querying macOS Spotlight metadata cache...");
  const startTime = Date.now();

  try {
    // kMDItemTitle gives the note name, kMDItemTextContent gives the entire note body text.
    const command = `mdfind -attr kMDItemTitle -attr kMDItemTextContent "kMDItemContentType == 'com.apple.notes.note'"`;

    // Using a large buffer just in case, though Spotlight data is compressed and compact
    const stdout = execSync(command, {
      encoding: "utf-8",
      maxBuffer: 1024 * 1024 * 50,
    });

    const lines = stdout.split("\n");
    let count = 0;

    console.log(`Command returned in ${Date.now() - startTime}ms!\n`);

    lines.forEach((line) => {
      if (!line.trim()) return;

      // mdfind -attr outputs rows formatted as: FilePath = Attributes...
      // We parse the path, title, and pre-indexed text content.
      if (
        line.includes("kMDItemTitle") &&
        line.includes("kMDItemTextContent")
      ) {
        count++;
        console.log(`[${count}] Raw Data Line Stream:`);
        console.log(line.slice(0, 300) + "...\n");
        console.log("-".repeat(50));
      }
    });

    console.log(`Processed ${count} notes total.`);
  } catch (error) {
    console.error("Spotlight query failed:", error.message);
  }
}

scanNotesViaSpotlight();
