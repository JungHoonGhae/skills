---
name: show-hn
description: "Post open-source projects to Hacker News as 'Show HN' submissions. Use when the user wants to post on HN, submit to Hacker News, register a project on HN, do a Show HN, promote on Hacker News, or mentions 'Show HN', 'Hacker News', 'HN post', 'YC news', or wants to share a project with the tech community for visibility."
---

# Show HN

Post open-source projects to Hacker News as "Show HN" submissions via browser automation.

## Overview

"Show HN" is Hacker News's format for sharing things you've made. It's one of the best free channels to reach developers and early adopters. A well-crafted Show HN post can drive significant traffic and GitHub stars.

## Requirements

- Browser automation tools (Playwright MCP or Claude-in-Chrome)
- User must be logged into Hacker News in the browser

## Workflow

### Step 1: Gather Project Info

Read the project's README and repo metadata to extract:

- **Project name**
- **One-line description** — what it does, in plain language
- **GitHub URL** (this becomes the submission URL)
- **Key differentiator** — what makes it interesting or unique

If the user hasn't specified which project, check the current working directory for a git repo.

### Step 2: Craft the Title

Show HN titles follow a strict format:

```
Show HN: <Project Name> – <Short description>
```

**Rules:**
- Must start with "Show HN:"
- Total length must be **80 characters or fewer** (HN truncates longer titles)
- Use an em dash (–) or hyphen (-) to separate name from description
- Be specific about what it does, not why it's great
- No ALL CAPS, no clickbait, no exclamation marks

**Good examples:**
- `Show HN: Captain's Log – Your ship sinks when you stop committing`
- `Show HN: TailBar – Tailscale menu bar app for macOS`
- `Show HN: Capx – CLI for Capacities.io note-taking`

**Bad examples:**
- `Show HN: An AMAZING new app that will CHANGE how you code!!!` (clickbait, caps, too long)
- `Show HN: My Side Project` (too vague)

### Step 3: Write the Text Body (Optional but Recommended)

The text field is optional but helps provide context. Keep it brief (2-4 sentences):

- What it does and who it's for
- What's technically interesting about it
- Link to a demo or screenshot if available

Don't write a sales pitch. HN users respond better to honest, technical descriptions.

**Example:**
```
Built this to gamify dev velocity with a pirate theme. It's a macOS menu bar app
(SwiftUI + Canvas) that tracks your git commits and GitHub pushes — your ship
physically sinks as inactivity grows. Supports fleet tracking across multiple repos.

GitHub: https://github.com/user/repo
```

### Step 4: Submit via Browser

Navigate to `https://news.ycombinator.com/submit` and fill in:

1. **title**: The "Show HN: ..." title from Step 2
2. **url**: The GitHub repo URL
3. **text**: The body text from Step 3 (leave empty if URL is provided and no additional context needed)

**Note:** HN allows either a URL or text body, not both in the traditional sense. If you provide a URL, the text field is still available but the submission links to the URL. If you only provide text (no URL), it becomes a text post.

Click "submit" to post.

### Step 5: Handle Rate Limiting

Hacker News rate-limits submissions, especially for newer accounts:

- **"posting too fast" error**: Wait at least 10-15 minutes between submissions
- **New accounts**: May need longer gaps between posts
- If rate-limited, inform the user and provide the pre-formatted title + text so they can post manually later

When submitting multiple projects, space them out. Don't try to post everything at once.

### Step 6: Report Results

Provide a summary with links:

```
Posted to Hacker News:
- "Show HN: Captain's Log – ..." → https://news.ycombinator.com/item?id=12345
- "Show HN: TailBar – ..." → rate limited, try again in 15 min
```

## Timing Tips

- **Best times to post**: Weekday mornings US time (8-11am ET / 5-8am PT) tend to get more visibility
- **Avoid weekends**: Lower traffic means less chance of hitting the front page
- **Don't repost immediately**: If a post doesn't get traction, wait at least a week before resubmitting

## What Makes a Good Show HN

- **Something you built**: Show HN is for your own projects, not links to other people's work
- **Working product**: It should be usable, not just an idea or landing page
- **Open source bonus**: HN users love being able to read the code
- **Respond to comments**: Be active in the thread. Answer questions, take feedback gracefully
- **Technical depth**: Be ready to discuss architecture, design decisions, and trade-offs
