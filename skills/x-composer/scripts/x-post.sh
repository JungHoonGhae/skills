#!/bin/bash
# x-post.sh — One-command X.com post: open compose → paste text → ready to post
#
# Usage:
#   echo "Hello world" | x-post.sh
#   x-post.sh "Hello world"
#   x-post.sh <<< "Multi-line
#   post content"

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"

# Read text from argument or stdin
if [ -n "$1" ]; then
  TEXT="$1"
else
  TEXT="$(cat)"
fi

if [ -z "$TEXT" ]; then
  echo "Usage: x-post.sh <text> or echo <text> | x-post.sh" >&2
  exit 1
fi

# Step 1: Open X.com compose page
NODE_PATH=$(npm root -g) node "$SCRIPTS_DIR/cdp-launch.js" "https://x.com/compose/post" 2>&1

# Step 2: Wait for page load
sleep 3

# Step 3: Convert text to JSON segments
SEGMENTS=$(echo "$TEXT" | python3 -c "
import sys, json
lines = sys.stdin.read()
segments = []
parts = lines.split('\n')
for i, part in enumerate(parts):
    if part:
        segments.append({'text': part})
    if i < len(parts) - 1:
        segments.append({'enter': True})
print(json.dumps(segments))
")

# Step 4: Type into compose box
echo "$SEGMENTS" | NODE_PATH=$(npm root -g) node "$SCRIPTS_DIR/cdp-type.js"

echo ""
echo "Draft ready. Review in browser and click Post."
