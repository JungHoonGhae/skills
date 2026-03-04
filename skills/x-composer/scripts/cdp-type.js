#!/usr/bin/env node
/**
 * CDP Type - Type text into the focused X.com compose box.
 *
 * Features:
 *   - Auto-detects CDP port (reads ~/.chrome-cdp-port or scans 9222-9230)
 *   - Falls back to clipboard + AppleScript paste if CDP unavailable
 *
 * Usage: echo '<JSON>' | node cdp-type.js
 *
 * JSON format: array of segments
 *   [{"text": "Hello"}, {"enter": true}, {"text": "World"}]
 *
 * Segment types:
 *   {"text": "string"}  - Insert text (supports emoji/unicode)
 *   {"enter": true}     - Press Enter (line break)
 *   {"enter": 2}        - Press Enter N times
 */
const CDP = require("chrome-remote-interface");
const { readFileSync, existsSync } = require("fs");
const { execFileSync } = require("child_process");

const PORT_FILE = `${process.env.HOME}/.chrome-cdp-port`;
const PORT_RANGE = [9222, 9223, 9224, 9225, 9226, 9227, 9228, 9229, 9230];
const DELAY = 50;

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString().trim();
}

async function checkChromeCDP(port) {
  try {
    const res = await fetch(`http://127.0.0.1:${port}/json/version`);
    const info = await res.json();
    return info.Browser && info.Browser.startsWith("Chrome/");
  } catch {
    return false;
  }
}

async function findPort() {
  // Try saved port first
  if (existsSync(PORT_FILE)) {
    const saved = parseInt(readFileSync(PORT_FILE, "utf8").trim());
    if (saved && await checkChromeCDP(saved)) return saved;
  }
  // Scan port range
  for (const port of PORT_RANGE) {
    if (await checkChromeCDP(port)) return port;
  }
  return null;
}

function segmentsToPlainText(segments) {
  let text = "";
  for (const seg of segments) {
    if (seg.text) text += seg.text;
    if (seg.enter) {
      const count = typeof seg.enter === "number" ? seg.enter : 1;
      text += "\n".repeat(count);
    }
  }
  return text;
}

async function typeViaCDP(port, segments) {
  const targets = await CDP.List({ port });
  const target = targets.find(t => t.url.includes("x.com") && t.type === "page");
  if (!target) {
    console.error("No X.com tab found via CDP.");
    return false;
  }

  const client = await CDP({ target: target.webSocketDebuggerUrl });
  const { Input } = client;

  for (const seg of segments) {
    if (seg.text) {
      await Input.insertText({ text: seg.text });
      await new Promise(r => setTimeout(r, DELAY));
    }
    if (seg.enter) {
      const count = typeof seg.enter === "number" ? seg.enter : 1;
      for (let i = 0; i < count; i++) {
        await Input.dispatchKeyEvent({
          type: "keyDown", key: "Enter", code: "Enter",
          windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13,
        });
        await Input.dispatchKeyEvent({ type: "keyUp", key: "Enter", code: "Enter" });
        await new Promise(r => setTimeout(r, DELAY));
      }
    }
  }

  console.log("Draft entered via CDP. Review in browser and post manually.");
  await client.close();
  return true;
}

function typeViaClipboard(segments) {
  const text = segmentsToPlainText(segments);
  execFileSync("pbcopy", [], { input: text });
  console.log("Text copied to clipboard.");

  // Focus Chrome and paste
  execFileSync("osascript", ["-e", 'tell application "Google Chrome" to activate']);
  // Small delay for focus
  execFileSync("sleep", ["1"]);
  execFileSync("osascript", [
    "-e", 'tell application "System Events" to keystroke "v" using command down',
  ]);
  console.log("Pasted into browser. Review and post manually.");
  return true;
}

(async () => {
  const raw = await readStdin();
  if (!raw) {
    console.error("No input. Pipe JSON segments via stdin.");
    process.exit(1);
  }

  const segments = JSON.parse(raw);

  // Try CDP first
  const port = await findPort();
  if (port) {
    console.log(`Using CDP on port ${port}...`);
    const ok = await typeViaCDP(port, segments);
    if (ok) return;
  }

  // Fallback: clipboard + AppleScript paste
  console.log("CDP unavailable. Using clipboard fallback...");
  typeViaClipboard(segments);
})();
