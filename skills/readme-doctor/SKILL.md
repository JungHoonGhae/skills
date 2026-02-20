---
name: readme-doctor
description: Analyze GitHub repositories to generate README templates based on common patterns. Use when the user provides a GitHub ID/URL and wants to create a README for their current project. Triggers on requests like "create a README based on my GitHub style", "generate README from my repos", "analyze my GitHub for README patterns", or "make a README matching my other projects".
---

# README Doctor

Generate README templates by analyzing common patterns across a user's GitHub repositories.

## Workflow

1. **Identify project type** → OSS, Personal, Internal, or Config
2. **Parse GitHub input** → Extract username/org from ID or URL
3. **Fetch repositories** → Get latest 3+ repos via `gh` CLI
4. **Read READMEs** → Extract content from each repo
5. **Analyze patterns** → Find common sections, styles, formatting
6. **Detect project info** → Auto-scan current directory for metadata
7. **Generate template** → Create README.md with detected patterns + project info

## Project Types

Different audiences need different information. **Always ask** if unclear.

| Type | Audience | Key Sections | Template |
|------|----------|--------------|----------|
| **Open Source** | Contributors, users | Install, Usage, Contributing, License | `templates/oss.md` |
| **Personal** | Future you, portfolio | What it does, Tech stack, Learnings | `templates/personal.md` |
| **Internal** | Teammates, new hires | Setup, Architecture, Runbooks | `templates/internal.md` |
| **Config** | Future you (confused) | What's here, Why, Gotchas | `templates/xdg-config.md` |

## Cognitive Funneling

Order sections from **broad to specific**, letting readers "short circuit" quickly:

```
Name → One-liner → Usage → API → Install → License
```

Each step takes the reader deeper. Those who reach the bottom are genuinely interested.

> The ideal README is as short as it can be without being any shorter.

## Step 1: Identify Project Type

**Ask:** "What type of project is this?"

| Task | When |
|------|------|
| **Creating** | New project, no README yet |
| **Adding** | Need to document something new |
| **Updating** | Capabilities changed, content is stale |
| **Reviewing** | Checking if README is still accurate |

### Project Type Questions

**Creating initial README:**
1. What type of project? (OSS, Personal, Internal, Config)
2. What problem does this solve in one sentence?
3. What's the quickest path to "it works"?
4. Anything notable to highlight?

**See** `references/section-checklist.md` for which sections to include by type.

## Step 2: Parse GitHub Input

Accept both formats:

```bash
# From GitHub ID (username or org)
input: "torvalds"
input: "facebook"

# From GitHub URL
input: "https://github.com/torvalds"
input: "https://github.com/facebook/react"
```

Extract username/org:
```bash
# URL pattern
echo "https://github.com/torvalds" | sed 's|.*github.com/||' | cut -d'/' -f1

# Direct ID
username="torvalds"
```

## Step 3: Fetch Repositories

Use `gh` CLI to get the user's/org's latest repositories:

```bash
# List repos sorted by last updated (for user)
gh repo list <username> --limit 10 --json name,description,url,updatedAt,stargazerCount --jq 'sort_by(.updatedAt) | reverse | .[0:5]'

# For organization
gh repo list <orgname> --limit 10 --json name,description,url,updatedAt,stargazerCount --jq 'sort_by(.updatedAt) | reverse | .[0:5]'

# Alternative: API call
gh api /users/<username>/repos --paginate | jq '[.[] | {name, description, html_url, updated_at, stargazers_count}] | sort_by(.updated_at) | reverse | .[0:5]'
```

Select repos with:
- Most recent activity (`updatedAt`)
- Non-empty README (check via API)
- Prefer repos with stars (indicates maintained projects)

## Step 4: Read README Content

For each selected repository:

```bash
# Get README via gh API
gh api /repos/<owner>/<repo>/readme --jq '.content' | base64 -d

# Alternative: raw URL
curl -s https://raw.githubusercontent.com/<owner>/<repo>/main/README.md
curl -s https://raw.githubusercontent.com/<owner>/<repo>/master/README.md
```

Store each README for pattern analysis. Minimum 3 READMEs required.

## Step 5: Analyze Patterns

### Section Detection

Identify common sections across READMEs:

```
Typical sections to detect:
- Title/Header (H1, project name)
- Description/Badges
- Installation
- Usage/Quick Start
- Features
- Configuration
- API Reference
- Examples/Demo
- Contributing
- License
- Acknowledgments
- Changelog
- Screenshots/Demo
```

Analysis approach:
1. Parse markdown headers (`#`, `##`, `###`)
2. Count frequency of each section name
3. Note section ordering patterns
4. Identify badge patterns (shields.io, etc.)
5. Detect code block languages (bash, python, js, etc.)

### Style Detection

Analyze formatting patterns:

```
Style elements:
- Badge usage (presence, style, position)
- Emoji usage in headers/sections
- Code block formatting (language tags, line numbers)
- Image usage (screenshots, logos, diagrams)
- Table usage (for configs, comparisons)
- List style (bullet vs numbered)
- Quote usage (highlights, tips)
- Link style (inline vs reference)
- TOC (Table of Contents) presence
- Section divider usage (---, ***)
```

### Common Patterns Summary

Output analysis as structured data:

```json
{
  "sections": {
    "Installation": { "frequency": 1.0, "positions": [2, 3, 2] },
    "Usage": { "frequency": 0.8, "positions": [3, 4, 3] },
    "License": { "frequency": 0.6, "positions": [6, 7, 5] }
  },
  "styles": {
    "badges": true,
    "emoji_headers": false,
    "code_blocks": ["bash", "javascript"],
    "images": true,
    "toc": false
  },
  "section_order": ["Title", "Description", "Installation", "Usage", "License"]
}
```

## Step 6: Detect Project Info

Auto-detect from current directory:

### Package Managers & Configs

```bash
# Node.js (package.json)
[ -f package.json ] && cat package.json | jq '{name, description, version, author, license, repository, keywords}'

# Python (pyproject.toml, setup.py)
[ -f pyproject.toml ] && cat pyproject.toml | grep -E "^(name|version|description|authors)" | head -10
[ -f setup.py ] && grep -E "(name=|version=|description=|author=)" setup.py | head -10

# Rust (Cargo.toml)
[ -f Cargo.toml ] && grep -E "^(name|version|description|authors|license)" Cargo.toml

# Go (go.mod)
[ -f go.mod ] && head -5 go.mod

# Ruby (Gemfile, *.gemspec)
[ -f *.gemspec ] && grep -E "(name|version|summary|description)" *.gemspec | head -10

# Java (pom.xml, build.gradle)
[ -f pom.xml ] && grep -E "<(name|description|version)>" pom.xml | head -10
```

### Project Type Detection

```bash
# Detect project type
if [ -f "package.json" ]; then
  project_type="node"
  framework=$(cat package.json | jq -r '.dependencies | keys[] | select(. == "react" or . == "vue" or . == "next" or . == "express")' | head -1)
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
  project_type="python"
elif [ -f "Cargo.toml" ]; then
  project_type="rust"
elif [ -f "go.mod" ]; then
  project_type="go"
elif [ -f "pom.xml" ]; then
  project_type="java"
else
  project_type="unknown"
fi
```

### Git Info

```bash
# Get repo info from git remote
git remote get-url origin 2>/dev/null | sed 's/.*github.com[/:]//' | sed 's/.git$//'
git log -1 --format='%an' 2>/dev/null  # Last committer as author hint
```

## Step 7: Generate README Template

Create README.md combining:

1. **Detected patterns** from GitHub analysis
2. **Project info** from auto-detection
3. **Placeholder content** for user to fill

### Template Structure

```markdown
# {project_name}

{badges if detected}

{description from package.json or placeholder}

## {Installation heading}

{code block with appropriate package manager}

## {Usage heading}

{example code or placeholder}

{Additional sections based on detected patterns}

## License

{license from package.json or placeholder}
```

### Language-Specific Install Commands

```bash
# Node.js
npm install {project_name}
yarn add {project_name}
pnpm add {project_name}

# Python
pip install {project_name}
poetry add {project_name}

# Rust
cargo add {project_name}

# Go
go get github.com/{owner}/{project_name}
```

## Output

Write the generated README to the current working directory:

```bash
# Write to file
cat > README.md << 'EOF'
{generated content}
EOF

echo "✅ README.md created"
```

## Example Usage

```
User: "Create a README based on my GitHub style. My username is octocat."

Process:
1. Fetch repos from github.com/octocat
2. Get READMEs from latest 5 repos
3. Analyze: 80% have Installation/Usage sections, badges at top, no emoji
4. Detect: package.json exists → Node.js project, name: "my-app"
5. Generate: README.md with detected patterns + project info

Output:
# my-app

[![npm version](https://badge.fury.io/js/my-app.svg)](https://badge.fury.io/js/my-app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A brief description of my-app.

## Installation

\`\`\`bash
npm install my-app
\`\`\`

## Usage

\`\`\`javascript
// Example usage
const myApp = require('my-app');
\`\`\`

## License

MIT
```

## Scripts

### analyze_readme_patterns.py

Located in `scripts/`. Analyzes README content to extract patterns.

Usage:
```bash
python3 scripts/analyze_readme_patterns.py readme1.md readme2.md readme3.md
```

Returns JSON with detected patterns.

### detect_project_info.py

Located in `scripts/`. Auto-detects project metadata from current directory.

Usage:
```bash
python3 scripts/detect_project_info.py
```

Returns JSON with project info.

## Error Handling

- **No GitHub input**: Prompt user for username/org
- **Less than 3 repos with READMEs**: Proceed with available, warn user
- **gh CLI not authenticated**: Guide user through `gh auth login`
- **Project detection fails**: Use placeholders, inform user
- **API rate limit**: Suggest waiting or using authenticated requests

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth login`)
- Python 3.6+ for analysis scripts
- `jq` for JSON processing (optional but recommended)

## Templates

Ready-to-use templates by project type:

| Template | Use For |
|----------|---------|
| `templates/oss.md` | Open source libraries and tools |
| `templates/personal.md` | Side projects, portfolio pieces |
| `templates/internal.md` | Team codebases, internal services |
| `templates/xdg-config.md` | Dotfiles, config directories |

## References

Deeper guidance for edge cases:

| File | Content |
|------|---------|
| `references/section-checklist.md` | Which sections by project type |
| `references/best-practices.md` | Consolidated README wisdom |
| `references/templates.md` | Language-specific patterns |

## README Checklist

After generating, verify:

- [ ] One-liner explaining purpose (< 120 chars)
- [ ] Necessary background context & links
- [ ] Clear, runnable example of usage
- [ ] Installation instructions
- [ ] API documentation (if library)
- [ ] Cognitive funneling (broad → specific)
- [ ] Caveats mentioned up-front
- [ ] License

## Common Mistakes to Avoid

- **No install steps** — Never assume setup is obvious
- **No examples** — Show, don't just tell
- **Wall of text** — Use headers, tables, lists
- **Stale content** — Add "last reviewed" date for internal/config
- **Generic tone** — Write for YOUR audience
