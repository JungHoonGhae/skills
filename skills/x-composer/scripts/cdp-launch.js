#!/usr/bin/env node
/**
 * CDP Smart Launch - Open a URL in Chrome with CDP.
 *
 * Features:
 *   - Scans ports 9222-9230 for existing CDP instance
 *   - Launches Chrome on first available port if none found
 *   - Handles port conflicts (e.g., Capacities on 9222)
 *   - Outputs the active port for other scripts to use
 *
 * Usage: node cdp-launch.js [URL]
 *   Default URL: https://x.com/compose/post
 */
const CDP = require("chrome-remote-interface");
const { execFileSync } = require("child_process");
const { writeFileSync } = require("fs");

const PORT_RANGE = [9222, 9223, 9224, 9225, 9226, 9227, 9228, 9229, 9230];
const PROFILE = `${process.env.HOME}/.chrome-cdp-profile`;
const PORT_FILE = `${process.env.HOME}/.chrome-cdp-port`;
const url = process.argv[2] || "https://x.com/compose/post";

async function checkCDP(port) {
  try {
    const res = await fetch(`http://127.0.0.1:${port}/json/version`);
    const info = await res.json();
    if (info.Browser && info.Browser.startsWith("Chrome/")) {
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

async function isPortInUse(port) {
  try {
    await fetch(`http://127.0.0.1:${port}/json/version`);
    return true;
  } catch {
    return false;
  }
}

function savePort(port) {
  writeFileSync(PORT_FILE, String(port));
}

(async () => {
  // Step 1: Scan for existing Chrome CDP instance
  for (const port of PORT_RANGE) {
    if (await checkCDP(port)) {
      console.log(`Found Chrome CDP on port ${port}. Opening new tab...`);
      try {
        const client = await CDP({ port });
        await client.Target.createTarget({ url });
        console.log(`Opened: ${url}`);
        await client.close();
        savePort(port);
        return;
      } catch (e) {
        console.error(`Failed to use port ${port}: ${e.message}`);
      }
    }
  }

  // Step 2: Find first available port and launch Chrome
  let launchPort = null;
  for (const port of PORT_RANGE) {
    if (!(await isPortInUse(port))) {
      launchPort = port;
      break;
    }
  }

  if (!launchPort) {
    console.error("All ports 9222-9230 are in use. Kill other CDP apps first.");
    process.exit(1);
  }

  console.log(`Starting Chrome with CDP on port ${launchPort}...`);
  execFileSync("open", [
    "-na", "Google Chrome", "--args",
    `--remote-debugging-port=${launchPort}`,
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${PROFILE}`,
    "--new-window", url,
  ], { stdio: "inherit" });
  savePort(launchPort);
  console.log(`Chrome started on port ${launchPort}. Opened: ${url}`);
})();
