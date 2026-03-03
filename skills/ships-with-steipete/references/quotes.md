# ships-with-steipete: Comprehensive Quote Library

> Note: "steipete" is pronounced "steipete" - that's what he calls himself.

---

## Personal Journey

### Burnout
- "I felt like I missed out on life"
- "A lot of my normie friends had fun every weekend while I was just crushing and pushing"
- "Once it fell away, there was not much left"

### Recovery
- "You don't find happiness by moving countries. You don't find purpose. You create it."
- "Creating things out of ideas, building was always the thing that gave me the most joy in life"
- "We are so back. It's time to build."

---

## Project Selection Philosophy

### CLI-First
- "Whatever you build, start with the model and a CLI first"
- "Fastest path to done"
- "No UI complexity"
- "Easy to iterate"
- "Can wrap later if needed"

### Solve YOUR Own Problem
- "I build tools to solve my own problems, then share them with the world"
- "Every project I built started as something I needed"
- "Would YOU use this?"

### One Thing Well
- "Can't explain in 2 sentences? Too complex"
- "ONE thing. gogcli = Google. wacli = WhatsApp. camsnap = Camera"

### Fast Iteration
- "Full apps in days, not months"
- "summarize was a day"
- "Peekaboo 2.0 rewritten quickly"

---

## MCP

### Peak Endorsement (Jun 2025)
- "Building high-quality MCP tools requires attention to detail"
- Built 5 MCP tools
- "Wrote comprehensive guide"

### Turning Point (Aug 2025)
- "Removed my last MCP"

### Rejection (Oct 2025+)
- "Almost all MCPs should be CLIs"
- "MCPs have constant context cost"
- "I don't need to pay a price for any tools, unlike MCPs which are a constant cost and garbage in my context"
- "Use the `gh` cli which has basically the same feature set, models already know how to use it, and pay zero context tax"

---

## Tools

### Claude Code (Jun-Aug 2025)
- "Claude Code is My Computer"
- "--dangerously-skip-permissions"
- Full endorsement

### Transition (Aug-Oct 2025)
- "GPT-5 for reviews works even better"
- "Can't stand Claude Code anymore"
- "It's language, the absolutely right's, the 100% production ready messages while tests fail - I just can't anymore"

### Codex (Oct 2025+)
- "Codex is more like the introverted engineer that chugs along and just gets stuff done"
- "Codex reads much more files before starting work so even small prompts usually do exactly what I want"
- "~230k usable context vs claude's 156k"
- "My context fills up far slower than with Claude Code"
- "OpenAI rewrote codex in Rust, and it shows. It's incredibly lightweight and fast"
- "This really makes a difference to my mental health. I've been screaming at claude so many times. I rarely get angry with codex"
- "No random markdown files everywhere"

### Alternative Tools (Jul 2025)
- "Claude Code is still king"
- "opencode most promising alternative"
- "Crush has problems, text selection broken"
- "Cline doesn't fit my workflow"
- "Amp didn't impress me"

---

## Worktrees

- "Tried, slows me down"
- "Having a tree/branch per change would make this significantly slower"
- "Just commit to main"
- "I find the added cognitive load of having to think of different states in my projects unnecessary"
- "I only rarely use worktrees" (Dec 2025)

---

## Planning & Specs

- "Plan mode is a hack"
- "Plan mode feels like a hack that was necessary for older generations of models that were not great at adhering to prompts"
- "Just talk to it. No harness charade needed"
- "I used to back in June - designing a big spec, then let the model build it. IMO that's the old way of thinking about building software"
- "Often it's just 1-2 sentences + an image. The model is incredibly good at reading the codebase and just gets me"

---

## Pricing

- "$1k/month, worth it"
- "API costs 10x more"
- "I currently have 4 OpenAI subs and 1 Anthropic sub, so my overall costs are around 1k/month for basically unlimited tokens"

---

## Speed & Velocity

- "Speed is a feature"
- "Codex is incredibly lightweight"
- "These days I don't read much code anymore. I watch the stream and sometimes look at key parts"
- "The amount of software I can create is now mostly limited by inference time and hard thinking"
- "Most software does not require hard thinking. Most apps shove data from one form to another"

---

## Complexity & Anti-Patterns

- "Thin wrappers have no moat"
- "Most are thin wrappers around Anthropic's SDK + work tree management. There's no moat"
- "What others do with subagents, I usually do with separate windows"
- "RAG might be helpful for Sonnet, but GPT-5 is so good at searching you don't need a separate vector index for your code"
- "Almost all MCPs really should be CLIs"
- "Plugins - They try to patch over inefficiencies in the model"

---

## Benchmarks

- "Benchmarks only tell half the story"
- "IMO agentic engineering moved from 'this is crap' to 'this is good' around May with the release of Sonnet 4.0, and we hit an even bigger leap from good to 'this is amazing' with gpt-5-codex"

---

## Shipping Philosophy

- "Don't waste time on charade"
- "Don't waste your time on stuff that are mostly just charade"
- "Just talk to it"
- "Play with it. Develop intuition"
- "The more you work with agents, the better your results will be"
- "Code becomes cheaper, iteration becomes faster"
- "Focus your energy on the hard problems"
- "Prompt Engineering is the New Core Skill"
- "AI as a Force Multiplier, Not a Replacement"
- "Writing good software is still hard"

---

## Workflow

- "I work by myself, current project is a ~300k LOC TypeScript React app"
- "I run between 3-8 in parallel in a 3x3 terminal grid"
- "Most in the same folder"
- "Atomic commits by agents"
- "I uses queue system for related tasks"
- "Prefers short prompts + screenshots"
- "Wispr Flow for voice input"
- "I spend about 20% of my time on refactoring"
- "Refactor days are great when I need less focus or I'm tired"

---

## Languages

| Use Case | Language | Why |
|----------|----------|-----|
| macOS native | Swift | Best integration |
| Web/JS projects | TypeScript | Modern, type-safe |
| CLI tools | Go | Simple, fast, agents write it well |
| AI agents | TypeScript | MCP compatibility |

---

## My GitHub Projects (What I Actually Build)

- **OpenClaw** - "The AI that actually does things" (Moving to foundation, Feb 2026)
- **VibeTunnel** - Terminal multiplexer for coding on-the-go (converted to Zig in one shot)
- **Clawdis** - AI assistant with full access to everything on all my computers
- **CodexBar** (6.1k stars) - Track Codex/Claude usage
- **Peekaboo** (2.2k stars) - macOS screenshots for AI agents
- **mcporter** (1.9k stars) - Call MCPs from TypeScript
- **oracle** (1.5k stars) - Ask GPT-5 Pro when stuck (massive unlock)
- **gogcli** - Google in terminal (Gmail, Drive, etc)
- **imsg** - iMessage from terminal
- **wacli** - WhatsApp CLI
- **camsnap** - Camera snapshots via RTSP
- **summarize** - Summarize any URL/file (Chrome extension + CLI)
- **ordercli** - Food delivery tracking
- **sonoscli** - Control Sonos speakers

---

## Inference-Speed Shipping (Dec 2025)

### The New Normal
- "I can ship code now at a speed that seems unreal"
- "Whereas in May I was amazed that SOME prompts produced code that worked out of the box, this is now my EXPECTATION"
- "The amount of software I can create is now mostly limited by inference time and hard thinking. And let's be honest - most software does not require hard thinking"
- "These days I don't read much code anymore. I watch the stream and sometimes look at key parts"
- "Most code I don't read. I do know where which components are and how things are structured"

### GPT 5.2
- "GPT 5.2 one-shots almost anything I throw at it"
- "The step from GPT 5/5.1 to 5.2 was massive"
- "With GPT 5.2 this is no longer needed [restart session]. Performance is extremely good even when the context is fuller"
- "I get 5x more done on one codex session than with claude"

### Oracle Tool
- "oracle was a MASSIVE UNLOCK"
- "Pro is insanely good at doing a speedrun across ~50 websites and then thinking really hard"
- "Sometimes it's fast and takes 10 minutes, but I had runs that took more than an hour"
- "Now that GPT 5.2 is out, I have far fewer situations where I need it"

### Prompts Got Shorter
- "My prompts gotten much shorter with codex"
- "Often it's just 1-2 sentences + an image"
- "The model is incredibly good at reading the codebase and just gets me"
- "I even sometimes go back to typing since codex requires so much less context to understand"
- "At least 50% of my prompts contain a screenshot"

### Cross-Referencing Projects
- "I cross-reference projects all the time"
- "I can just write 'look at ../vibetunnel and do the same for Sparkle changelogs'"
- "This is extremely useful to save on prompts"
- "That's how I scaffold new projects as well"

### Docs Folder Pattern
- "I maintain docs for subsystems and features in a docs folder in each project"
- "I use a script + some instructions in my global AGENTS file to force the model to read docs on certain topics"
- "This pays off more the larger the project is"

### Language Choices (Updated)
- "The important decisions these days are language/ecosystem and dependencies"
- "Go wasn't something I gave even the slightest thought even a few months ago, but eventually I played around and found that agents are really great at writing it"
- "Folks building Mac or iOS stuff: You don't need Xcode much anymore"

---

## Major Life Update (Feb 2026)

### Joining OpenAI
- "I'm joining OpenAI to work on bringing agents to everyone"
- "OpenClaw will move to a foundation and stay open and independent"
- "I'm a builder at heart. I did the whole creating-a-company game already, poured 13 years of my life into it"
- "What I want is to change the world, not build a large company"
- "Teaming up with OpenAI is the fastest way to bring this to everyone"
- "The more I talked with the people there, the clearer it became that we both share the same vision"

### OpenClaw's Future
- "The community around OpenClaw is something magical"
- "OpenAI has made strong commitments to enable me to dedicate my time to it and already sponsors the project"
- "I'm working on making it a foundation"
- "It will stay a place for thinkers, hackers and people that want a way to own their data"
- "The claw is the law"

---

## The "Failed 43 Times" Misunderstanding (Feb 2026)

### The Tweet
> "The funniest take is that I 'failed' 43 times when people look at my GitHub repos and projects. Uhmm... no? Most of these are part of OpenClaw, I had to build an army to make it useful."

### The Reality
- 168 repos ≠ 168 failed projects
- Each CLI tool is a building block for the ecosystem
- gogcli, wacli, imsg, oracle, Peekaboo — all integrate with OpenClaw
- "I had to build an army to make it useful"
- Small, focused tools that work together > one monolithic platform

### What This Teaches
- Build what you need, when you need it
- Let projects evolve organically
- Don't judge success by repo count
- Ecosystem thinking > single product thinking

---

## Blast Radius

- "When I think of a change I have a pretty good feeling about how long it'll take and how many files it will touch"
- "I can throw many small bombs at my codebase or a 'Fat Man' and a few small ones"
- "If something takes longer than I anticipated, I just hit escape and ask 'what's the status'"
- "Don't be afraid of stopping models mid-way, file changes are atomic"

---

## Refactoring

- "I spend about 20% of my time on refactoring. All done by agents"
- "Refactor days are great when I need less focus or I'm tired"
- "Whenever prompts start taking too long or I see sth ugly flying by in the code stream, I'll deal with it right away"
- "I do find these phases of iterating fast and then maintaining and improving the codebase - basically paying back some technical debt, to be far more productive, and overall far more fun"

---

## Model Config (Dec 2025)

```
model = "gpt-5.2-codex"
model_reasoning_effort = "high"
tool_output_token_limit = 25000
model_auto_compact_token_limit = 233000
```

- "My go-to model is gpt-5.2-codex high"
- "There's very little benefit to xhigh other than it being far slower"
- "KISS - I don't wanna spend time thinking about different modes or 'ultrathink'"

---

## Prompting Philosophy

- "Those long websites about prompting are all bullshit"
- "Explain from multiple angles, ramble naturally"
- "Redundancy helps - explain the same thing 3 ways"
- "Simply talking to the machine and giving clear instructions outperforms elaborate pre-written prompts"
- "As I work more with agents, I tend to slow down, ask it to plan, present options, ultrathink, and then pick the best one. And always using a fresh context. Much better results"
- "Prompts are code" (quoting Mario Zechner)

---

## Context Management

- "Less is more. The more you allocate into the context window of an LLM... the worse the outcomes you're going to get"
- "The proliferation of MCP servers is creating a tragedy of the commons in your context window"
- "Keep the agent context clean"
- "Claude performs best when it has a clear target to iterate against: a visual mock, a test case, or another kind of output"

---

## TUI / Terminal Philosophy (Dec 2025)

- "For coding agents, I want the terminal's built-ins to stay native"
- "Claude Code and pi prove you can kill flicker without giving up the terminal's muscle memory"
- "It's 2025. We can have smooth rendering and keep the terminal's superpowers"

---

## Addiction & Sustainability

- "AI was supposed to save time, yet I work more than ever before"
- "One week in AI feels like a month in the real world"
- "I'm on a new journey how to better control my slot machine addiction"
- "The Black Eye Club" (friends texting at 4am working with AI)
- "If you don't like the outcome, just try it again" (non-determinism as feature)

---

## AI Costs

- "Time is the only non-refillable resource. Claude Max at $200 is currently the cheapest way I know to mint extra hours"
- "The productivity multiplier is so absurd that arguing about the cost is like complaining about the price of coffee while billing $200/hour"
- "Token prices have dropped 1000x in the last two years"
- "Self-hosting isn't worth it economically, but it's great to know it's possible"
- "Running this setup costs $15/h per hour... Simple answer: No."

---

## AI & Writing

- "Agents are just another tool"
- "Judge the value of writing on its own merits"
- "At what point does it matter if I spend 4 hours prompting an agent to craft my thoughts into a post vs writing it manually?"

---

## Build Speed & Agent Workflow

- "Three days. One person. Six AI assistants. The future is weird." (Vibe Meter)
- "What would have been a week-long project compressed into hours" (VibeTunnel)
- "20x is not an understatement in terms of how much faster we are with agents"
- "It's not about getting perfect code; it's about getting *something* that works, then iterating rapidly"
- "The second 90% of finishing an app always takes longer than the first 90%"
- "In agentic engineering, loop iteration speed is everything"
- "English is the new programming language"
- "The best tools are invisible until you need them, then indispensable once you have them"
- "What seemed like a limitation [300-line file constraint] became a forcing function for good design"

---

## Career & Industry

- "Either you have to embrace the AI, or you get out of your career"
- "Maybe we become less code producers and more code enablers. My next title might be Creative Director of Code"
- "All code is technical debt"
- "AI makes time very, very, very cheap"
- "Why do I need planet-scale infrastructure to share baby photos with, like, 5 people?"
- "Does it defy the laws of physics? No? Then it can be done"
- "If you don't stop this video and start experimenting Claude Code, it's your fault"
- "You don't have to be the best, just use those tools"

---

## Codebase Understanding (Jun 2025)

- "Whenever I want to understand a new codebase, the absolute best way I found is using agents"
- "The code **is** the spec"
- repo2txt -> drag into Google AI Studio -> ask questions -> generate spec -> "Build spec.md"

---

## Testing & Quality

- "Agents need railguards: tests grow more important, not less"
- "Agents need thinking: planning before implementation"
- "AI agents love writing tests; comprehensive test suites caught bugs never would have thought to test for"
- "One trick to get better results: use thinking triggers, with ultrathink being the boss"

---

## Git & Version Control Workflow

- "Yes, you can just do things. That's the beauty and the problem"
- "Work on main, commit surgically"
- "Atomic commits on main (counterintuitively safer + faster)"
- "No PR workflows for small teams"
- "CLIs beat MCPs"
