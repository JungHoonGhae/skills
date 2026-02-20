#!/usr/bin/env node
/**
 * CDP Smart Launch - Open a URL in Chrome with CDP, reusing existing instance if available.
 *
 * Usage: node cdp-launch.js [URL]
 *   Default URL: https://x.com/compose/post
 *
 * Examples:
 *   node cdp-launch.js                              # Open compose
 *   node cdp-launch.js https://x.com/home           # Open home feed
 *   node cdp-launch.js "https://x.com/search?q=AI"  # Open search
 */
const CDP = require("chrome-remote-interface");
const { execSync } = require("child_process");

const PORT = 9222;
const PROFILE = `${process.env.HOME}/.chrome-cdp-profile`;
const url = process.argv[2] || "https://x.com/compose/post";

(async () => {
  try {
    await fetch(`http://127.0.0.1:${PORT}/json/version`);
    console.log("CDP already running. Opening new tab...");
    const client = await CDP({ port: PORT });
    await client.Target.createTarget({ url });
    console.log(`Opened: ${url}`);
    await client.close();
  } catch {
    console.log("Starting Chrome with CDP...");
    execSync(
      `open -na "Google Chrome" --args ` +
        `--remote-debugging-port=${PORT} ` +
        `--no-first-run ` +
        `--no-default-browser-check ` +
        `--user-data-dir="${PROFILE}" ` +
        `--new-window "${url}"`,
      { stdio: "inherit" }
    );
    console.log(`Chrome started. Opened: ${url}`);
  }
})();
