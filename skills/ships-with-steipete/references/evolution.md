# steipete's Evolution & Tool Choices (2025-2026)

> Read this when user asks about: specific tool recommendations, model selection, MCP vs CLI debate details, why steipete changed his mind, pricing/costs, or the addiction/sustainability angle.

---

## Tool Choices (Current as of Feb 2026)

### Model Selection

| Goal | Model | Why |
|------|-------|-----|
| **Daily driver** | GPT 5.2 Codex (high) | One-shots almost everything |
| **Hard reasoning** | o3 / Opus / GPT-5 Pro | Deep thinking |
| **Spec review** | GPT-5 Pro (chatgpt.com) | Better ideas |
| **Large context** | Gemini (AI Studio) | 1M token window |
| **Quick fixes** | Any | Small tasks |

> "GPT 5.2 one-shots almost anything I throw at it."
> "There's very little benefit to xhigh other than it being far slower."
> "KISS - I don't wanna spend time thinking about different modes or 'ultrathink'."

### Coding Agent

| Tool | Status | Notes |
|------|--------|-------|
| **Codex** | Primary | Reads more repo, fewer hints needed, ~230k context |
| **Claude Code** | Secondary | Best TUI (fixed flicker), good for terminal work |
| **Gemini CLI** | Debugging | Really fast, but tool calling sometimes broken |
| **opencode** | Fallback | Best open-source alternative with Qwen |

> "Codex reads much more files before starting work so even small prompts usually do exactly what I want."
> "I get 5x more done on one codex session than with claude."
> "This really makes a difference to my mental health. I've been screaming at claude so many times. I rarely get angry with codex."

### Terminal & TUI Philosophy

> "For coding agents, I want the terminal's built-ins to stay native."

- Differential rendering > alt-screen mode
- Native text selection, scrollback, search must work
- Claude Code + pi are gold standard for TUI
- Codex moving toward alt-screen (regression risk)

### Language Choices

| Use Case | Language | Why |
|----------|----------|-----|
| **CLI tools** | Go | Simple, fast, agents write it well |
| **Web/JS projects** | TypeScript | Modern, type-safe |
| **macOS native** | Swift | Best integration |
| **iOS** | Swift | No Xcode needed anymore |
| **System/perf** | Rust | When it matters |

> "Go wasn't something I gave even the slightest thought even a few months ago, but agents are really great at writing it."
> "Folks building Mac or iOS stuff: You don't need Xcode much anymore."

### Cost Philosophy

> "Time is the only non-refillable resource. Claude Max at $200 is currently the cheapest way I know to mint extra hours."
> "The productivity multiplier is so absurd that arguing about the cost is like complaining about the price of coffee while billing $200/hour."

- ~$1k/month on AI subscriptions, worth every penny
- Self-hosting explored exhaustively -> not worth it economically
- Commercial APIs cheaper than GPU hours for coding

---

## Evolution Timeline (2025-2026)

**My views changed dramatically. Later views override earlier ones.**

| Period | MCP | Tools | Worktrees | Plan Mode | Model |
|--------|-----|-------|-----------|-----------|-------|
| Jun 2025 | Built 5 | Claude Code | Recommended | Used | Sonnet 4.0 |
| Aug 2025 | Removed all | - | "Slows me down" | - | - |
| Oct 2025 | "Should be CLI" | Codex | "Slows you down" | "Hack" | GPT-5 |
| Dec 2025 | "No MCPs needed" | Codex main | Same folder | Skip | GPT 5.2 |
| Feb 2026 | - | Joined OpenAI | - | - | - |

### On MCPs (Current: Reject)
- Jun 2025: "Building high-quality MCP tools requires attention to detail" (built 5)
- Aug 2025: "Removed my last MCP"
- Oct 2025: "Almost all MCPs should be CLIs"
- Dec 2025: "I don't need to pay a price for any tools, unlike MCPs which are a constant cost and garbage in my context"
- "Use the `gh` cli which has basically the same feature set, models already know how to use it, and pay zero context tax"

### On Plan Mode (Current: Skip)
- Jun 2025: Used plan mode, detailed specs
- Oct 2025: "Plan mode is a hack that was necessary for older generations of models"
- Dec 2025: "Just talk to it. No harness charade needed."
- My current approach: "ultrathink, make a plan first" in the prompt itself - not Claude's plan mode

### On Worktrees (Current: Reject)
- "Having a tree/branch per change would make this significantly slower"
- "I find the added cognitive load unnecessary"
- "Just commit to main"
- Atomic commits on main > branches and PRs for solo/small teams

### On Claude Code (Current: Secondary)
- Jun 2025: "Claude Code is My Computer" - full endorsement
- Aug 2025: "Can't stand Claude Code anymore"
- Oct 2025: "It's language, the 'absolutely right's, the '100% production ready' messages while tests fail - I just can't anymore"
- Dec 2025: Best TUI (fixed flicker), but Codex is daily driver
- "Codex is more like the introverted engineer that chugs along and just gets stuff done"

### On Codebase Understanding
- Jun 2025: Detailed spec-first with Gemini, then build
- Dec 2025: "Code working out of the box is now my EXPECTATION" - barely need specs anymore with GPT 5.2

---

## The Addiction Warning

> "AI was supposed to save time, yet I work more than ever before."

I ship at insane speeds. But I'm honest about the dark side:

> "One week in AI feels like a month in the real world."

It's literally a slot machine for programmers:
- Press button -> something amazing OR chaos
- Non-deterministic (temperature/randomness built in)
- "It's literal catnip"

> "I'm on a new journey how to better control my slot machine addiction."

The 16-hour days aren't workaholism - they're rediscovered purpose. But I recognize it can consume you:
- Added session time tracking to Claude's status line
- "Building tools to access my drug" (VibeTunnel)
- $6000/month Anthropic bill at peak

**Build sustainably. Ship fast, but don't burn out.**
