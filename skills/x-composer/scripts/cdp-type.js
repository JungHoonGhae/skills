#!/usr/bin/env node
/**
 * CDP Type - Type text into the focused X.com compose box.
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

const PORT = 9222;
const DELAY = 50;

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString().trim();
}

async function typeText(input, text) {
  await input.insertText({ text });
  await new Promise(r => setTimeout(r, DELAY));
}

async function pressEnter(input) {
  await input.dispatchKeyEvent({
    type: "keyDown", key: "Enter", code: "Enter",
    windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13,
  });
  await input.dispatchKeyEvent({ type: "keyUp", key: "Enter", code: "Enter" });
  await new Promise(r => setTimeout(r, DELAY));
}

(async () => {
  const raw = await readStdin();
  if (!raw) { console.error("No input. Pipe JSON segments via stdin."); process.exit(1); }

  const segments = JSON.parse(raw);
  const targets = await CDP.List({ port: PORT });
  const target = targets.find(t => t.url.includes("x.com") && t.type === "page");
  if (!target) { console.error("No X.com tab found. Open x.com first."); process.exit(1); }

  const client = await CDP({ target: target.webSocketDebuggerUrl });
  const { Input } = client;

  for (const seg of segments) {
    if (seg.text) await typeText(Input, seg.text);
    if (seg.enter) {
      const count = typeof seg.enter === "number" ? seg.enter : 1;
      for (let i = 0; i < count; i++) await pressEnter(Input);
    }
  }

  console.log("Draft entered. Review in browser and post manually.");
  await client.close();
})();
