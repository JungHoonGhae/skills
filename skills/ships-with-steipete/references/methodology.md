# steipete's Methodology (Dec 2025 - Current)

> Read this when user asks about: AI coding workflow, agent setup, prompting strategy, context management, refactoring approach, or how steipete actually works day-to-day.

---

## Inference-Speed Shipping

> "I can ship code now at a speed that seems unreal."

**The new normal:**
- Code working out of the box is now my EXPECTATION
- I don't read code anymore - I watch the stream
- Most software doesn't require hard thinking
- Prompts got shorter: 1-2 sentences + screenshot

> "The amount of software I can create is now mostly limited by inference time and hard thinking. And let's be honest - most software does not require hard thinking."

## My Current Setup

- **3-8 parallel agents** in 3x3 terminal grid (Ghostty)
- **Same folder** (not worktrees)
- **Atomic commits** on main by agents
- **Short prompts + screenshots** (50% of my prompts contain an image)
- **Wispr Flow** for voice input
- **docs folder** for subsystem documentation
- **Tower** for visual Git diffs and easy reverts

## The Blast Radius

> "When I think of a change I have a pretty good feeling about how long it'll take and how many files it will touch. I can throw many small bombs at my codebase or a 'Fat Man' and a few small ones."

- If something takes too long, hit escape and ask "what's the status"
- Don't be afraid of stopping models mid-way, file changes are atomic
- Review changes in Tower (Git GUI with good diffing)
- If bad -> revert & give fresh context

## How I Actually Prompt

> "Those long websites about prompting are all bullshit."

My actual approach:
- **Explain from multiple angles** - ramble naturally
- **Redundancy helps** - explain the same thing 3 ways
- **Screenshots are gold** for multimodal debugging
- **Short and focused** - 1-2 sentences + image for most things
- **Cross-reference projects** - "look at ../vibetunnel and do the same"

For complex features:
- Start with "ultrathink, make a plan first and give me at least 3 options"
- Iterate on plans multiple times before green-lighting
- Then let the agent build

> "As I work more with agents, I tend to slow down, ask it to plan, present options, ultrathink, and then pick the best one. And always using a fresh context."

## Context Management (Critical)

> "Less is more. The more you allocate into the context window of an LLM... the worse the outcomes you're going to get."

- **Fresh sessions** for big features
- **Separate windows** = separate context (not subagents)
- **Markdown > HTML** to conserve tokens
- **Small CLIs > MCPs** for keeping context clean
- **Inject docs only when needed** - don't preload everything
- **docs folder pattern** - "I maintain docs for subsystems in a docs folder"
- Use `/clear` frequently to prevent context drift

## When Stuck: Oracle

> "oracle was a MASSIVE UNLOCK."

I built a CLI to query GPT-5 Pro when stuck. It does a speedrun across ~50 websites, thinks really hard, and usually nails the answer.

> "Sometimes it's fast and takes 10 minutes, but I had runs that took more than an hour."

With GPT 5.2, I need it less - but it's still useful for the hardest problems.

## Cross-Referencing Projects

> "I cross-reference projects all the time."

- "look at ../vibetunnel and do the same for Sparkle changelogs"
- This saves prompts and leverages solved patterns
- That's how I scaffold new projects

## Refactoring (20% of my time)

> "I spend about 20% of my time on refactoring. All done by agents."

- Refactor days are great when I need less focus or I'm tired
- `jscpd` for code duplication, `knip` for dead code
- Breaking apart large files, updating dependencies
- Tests + docs separately after feature complete

> "I do find these phases of iterating fast and then maintaining the codebase - paying back technical debt - to be far more productive, and far more fun."
