---
name: awesome-list-pr
description: "Register open-source projects to awesome GitHub lists via PRs. Use when the user wants to submit a project to awesome lists, add a repo to curated lists, promote an open-source project on GitHub, or mentions 'awesome list', 'awesome-macos', 'awesome-rust', 'awesome-cli', 'curated list PR', 'register to awesome', or any variation of submitting to GitHub's awesome-* repositories."
---

# Awesome List PR

Automate submitting open-source projects to relevant GitHub awesome lists via properly formatted pull requests.

## Overview

GitHub's "awesome" lists are community-curated collections of high-quality resources. Getting your project listed drives discovery and credibility. Each list has its own contribution format, so the key challenge is matching the right format for each repo.

## Workflow

### Step 1: Gather Project Info

Read the project's README, `Package.swift`, `Cargo.toml`, `package.json`, or equivalent to extract:

- **Name** and short description
- **Primary language** (Swift, Rust, TypeScript, Go, Python, etc.)
- **Category** (menu bar app, CLI tool, library, web app, etc.)
- **License** (MIT, Apache, etc.)
- **GitHub URL**

If the user hasn't specified which project, check the current working directory.

### Step 2: Find Relevant Awesome Lists

Based on the project's language and category, identify candidate awesome lists. Common ones:

| Language/Type | Awesome Lists |
|---|---|
| macOS app (Swift) | `serhii-londar/open-source-mac-os-apps`, `iCHAIT/awesome-macOS`, `phmullins/awesome-macos` |
| Swift library | `matteocrippa/awesome-swift` |
| Rust | `rust-unofficial/awesome-rust` |
| CLI tool (any lang) | `agarrharr/awesome-cli-apps` |
| Go | `avelino/awesome-go` |
| Python | `vinta/awesome-python` |
| TypeScript/JS | `sindresorhus/awesome-nodejs` |
| React | `enaqx/awesome-react` |
| General macOS | `jaywcjlove/awesome-mac` |

Search GitHub for `awesome-{language}` or `awesome-{category}` if the project doesn't fit the table above. Confirm with the user which lists to target before proceeding.

### Step 3: Fork and Clone Each Target Repo

For each awesome list:

```bash
# Fork if not already forked
gh repo fork <owner>/<repo> --clone=false

# Clone the fork
gh repo clone <your-username>/<repo> /tmp/<repo>-pr
cd /tmp/<repo>-pr
```

If the fork already exists, clone it and pull the latest upstream changes.

### Step 4: Read Contribution Guidelines

**This is the most important step.** Each awesome list has different formatting rules.

1. Check for `CONTRIBUTING.md` or `contributing.md`
2. Read the existing entries near where your project would go
3. Note the exact format: badge styles, link patterns, description conventions, alphabetical ordering

#### Known Formats

**serhii-londar/open-source-mac-os-apps** — JSON format:
```json
{
  "title": "My App",
  "category": ["menubar", "developer-tools"],
  "description": "Short description of the app.",
  "homepage": "https://github.com/user/repo",
  "icon_url": "https://raw.githubusercontent.com/user/repo/main/icon.png",
  "open_source": true,
  "license": "MIT",
  "language": "swift",
  "screenshots": [],
  "official": true,
  "url": "https://github.com/user/repo"
}
```
Edit `applications.json`. Entries are in an array — add at the end or in alphabetical position. Be careful with trailing commas (the file may use non-standard JSON).

**iCHAIT/awesome-macOS** — Markdown with OSS/Freeware icons:
```markdown
- [App Name](https://github.com/user/repo) - Short description. [![Open-Source Software][OSS Icon]](https://github.com/user/repo) ![Freeware][Freeware Icon]
```
Add alphabetically within the appropriate section. Icons are reference-style links defined at the bottom of the file.

**phmullins/awesome-macos** — Markdown with simpler icons:
```markdown
- [App Name](https://github.com/user/repo) - Short description. ![Open Source][oss]
```
Add alphabetically. Icon references use `[oss]` style, defined at the bottom.

**rust-unofficial/awesome-rust** — Simple markdown list:
```markdown
* [user/repo](https://github.com/user/repo) - Short description
```
Find the right category section. Alphabetical within section.

**agarrharr/awesome-cli-apps** — Dash-style markdown:
```markdown
- [app-name](https://github.com/user/repo) - Short description.
```
Find the right category. Alphabetical within section.

For any list not documented above, always read 5-10 existing entries to match the exact format before adding your entry.

### Step 5: Create Branch and Add Entry

```bash
cd /tmp/<repo>-pr
git checkout -b add-<project-name>

# Edit the appropriate file (README.md, readme.md, applications.json, etc.)
# Match the EXACT format of existing entries
# Place alphabetically within the correct section
```

**Common pitfalls:**
- File might be `README.md` or `readme.md` — check with `ls *.md`
- JSON files may have trailing commas — use string manipulation, not strict JSON parsers
- Some repos require entries in specific sections — read section headers carefully
- Badge/icon reference names differ between repos (e.g., `[OSS Icon]` vs `[oss]`)

### Step 6: Commit, Push, and Open PR

```bash
git add -A
git commit -m "Add <Project Name>"
git push origin add-<project-name>

# Create PR following the repo's PR template
gh pr create \
  --repo <original-owner>/<repo> \
  --title "Add <Project Name>" \
  --body "Added [Project Name](url) to the <Section> section.

<Brief description of what the project does.>"
```

Check if the repo has a PR template (`.github/PULL_REQUEST_TEMPLATE.md`) and follow it.

### Step 7: Report Results

After all PRs are created, provide a summary:

```
Created PRs:
- <owner>/<repo> #123 — <status>
- <owner>/<repo> #456 — <status>
```

## Tips

- **Batch multiple projects**: If the user has several repos, batch entries into a single PR per awesome list when they fit the same list.
- **Check existing entries**: Before creating a PR, search the list to make sure the project isn't already listed.
- **Star the repo**: Many awesome lists require the submitter to have starred the list repo. Remind the user.
- **Wait for CI**: Some lists run automated link checks. If CI fails, fix the entry format.
- **Don't spam**: Be selective. Only submit to lists where the project genuinely fits. Low-quality submissions get rejected and may get the user flagged.
