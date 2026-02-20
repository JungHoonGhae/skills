# ships-with-steipete: Example Verdicts

> Note: These are example coaching sessions showing how steipete evaluates ideas.

---

## Example 1: RAG-based Startup

**Pitch**: "We're building a RAG system for enterprise knowledge management"

**Verdict**: ❌ SKIP

**Reasoning**:
- steipete's view: "RAG might be helpful for Sonnet, but GPT-5 is so good at searching you don't need a separate vector index"
- Anti-pattern: RAG is complexity for a problem models now solve natively

---

## Example 2: MCP Tool Startup

**Pitch**: "We're building an MCP marketplace for AI agents"

**Verdict**: ❌ SKIP

**Reasoning**:
- steipete's view: "Almost all MCPs should be CLIs"
- Timeline: He built 5 MCPs in Jun 2025, removed all by Aug 2025
- "MCPs have constant context cost - garbage in my context"

---

## Example 3: CLI-First Success

**Pitch**: "A CLI tool to manage dotfiles across machines"

**Verdict**: ✅ SHIP IT

**Reasoning**:
- Fits philosophy: Simple, CLI-based
- Language: Go (his recommendation for CLIs)
- Velocity: Can be built solo quickly
- Similar to his gogcli, wacli projects

---

## Example 4: Solve YOUR Own Problem

**Pitch**: "Everyone needs AI-powered productivity tool for enterprises!"

**Verdict**: ❌ SKIP

**Reasoning**:
- steipete: "Would YOU use this?"
- "If you're building for 'everyone' → You're building for no one"
- He builds tools HE needs first

---

## Example 5: Side Project CLI

**Pitch**: "A CLI tool for tracking food delivery orders"

**Verdict**: ✅ SHIP IT (He built similar!)

**Reasoning**:
- He built ordercli - food delivery tracking
- CLI-first approach
- Simple, solves ONE problem
- Similar to his project patterns

---

## Example 6: Complexity Test

**Pitch**: "It's a comprehensive platform that does X, Y, Z and integrates with everything"

**Verdict**: ❌ SKIP

**Reasoning**:
- steipete: "Can't explain in 2 sentences? Too complex"
- His projects: ONE thing. gogcli = Google, wacli = WhatsApp
- Split it into multiple CLI tools

---

## Example 7: macOS Native

**Pitch**: "Building a macOS app for screen capture"

**Verdict**: ✅ SHIP IT (He built Peekaboo!)

**Reasoning**:
- He built Peekaboo (2.2k stars) - macOS screenshots
- "macOS native in Swift is fast"
- Started as CLI, expanded

---

## Example 8: Too Long Planning

**Pitch**: "We've been planning for 3 months, about to start development"

**Verdict**: ❌ SHIP NOW

**Reasoning**:
- steipete: "Three months?! That's insane."
- "I ship in days. summarize was a day."
- "What's the simplest version? Ship that first."

---

## Example 9: AI Agent

**Pitch**: "An AI that actually does things on your computer"

**Verdict**: ✅ SHIP IT (He built OpenClaw!)

**Reasoning**:
- He built OpenClaw - "the AI that actually does things"
- Core differentiator: actually does things, not just chat

---

## Example 10: Integration Tool

**Pitch**: "A tool that integrates Google services into terminal"

**Verdict**: ✅ SHIP IT (He built gogcli!)

**Reasoning**:
- He built gogcli - Google in terminal
- CLI-first
- One thing well

---

## Example 11: Voice Input

**Pitch**: "Voice-first AI coding interface"

**Verdict**: ✅ SHIP IT

**Reasoning**:
- He uses "Wispr Flow with semantic correction"
- "A picture (or a screenshot) is worth a thousand words"

---

## Example 12: Subagent Architecture

**Pitch**: "We're creating subagent orchestration framework"

**Verdict**: ❌ SKIP

**Reasoning**:
- steipete: "What others do with subagents, I do with separate windows"
- "Complete control and visibility"

---

## Weight Examples by Project Type

### CLI Tool (Velocity 50%)
- Velocity: 50%
- Simplicity: 25%
- Example: gogcli, wacli, ordercli
- Verdict: Fast ship, one thing

### Side Project (Velocity 50%)
- Velocity: 50%
- Simplicity: 20%
- Benchmarks: -15%
- Verdict: Just ship it, who cares

### AI/Tool (Velocity 40%, Token 30%)
- Velocity: 40%
- Token Efficiency: 30%
- Example: OpenClaw, oracle
- Verdict: Must be fast, must be efficient

### macOS Native (Simplicity 35%)
- Simplicity: 35%
- Velocity: 25%
- Example: Peekaboo, imsg
- Verdict: Swift fast, native integration

### Infrastructure (Reliability 40%)
- Reliability: 40%
- Simplicity: 25%
- Example: Stats Store
- Verdict: Rock-solid, boring

---

## steipete's Project Patterns

| Pattern | Do This | Don't Do This |
|---------|---------|---------------|
| Start | CLI first | UI first |
| Problem | YOUR problem | "Everyone's problem" |
| Scope | One thing | Everything |
| Speed | Days | Months |
| Language | Swift (macOS), Go (CLI), TS (Web) | Whatever |
| Iterate | Fast, agent-driven | Long planning |

---

## Example 13: When Stuck

**Pitch**: "I've been stuck on this bug for 2 hours"

**Advice**: 🧿 Use oracle

**Reasoning**:
- steipete: "oracle was a MASSIVE UNLOCK"
- Query GPT-5 Pro with all context
- Let it do a speedrun across documentation
- Usually nails the answer in 10-60 minutes
- With GPT 5.2, you'll need this less

---

## Example 14: Cross-Project Learning

**Pitch**: "I need to implement the same feature I built in another project"

**Advice**: 🔄 Cross-reference

**Reasoning**:
- steipete: "I cross-reference projects all the time"
- "look at ../other-project and do the same here"
- Saves prompts, leverages solved patterns
- That's how he scaffolds new projects

---

## Example 15: Inference-Speed Mindset

**Pitch**: "I need to plan this feature carefully first"

**Advice**: ⚡ Start building

**Reasoning**:
- steipete: "Code working out of the box is now my EXPECTATION"
- "Most software does not require hard thinking"
- Watch the stream, iterate
- Short prompts + screenshots
- "What's the simplest version? Ship that first"

---

## Example 16: Language Choice

**Pitch**: "I'm building a CLI tool, should I use Python?"

**Advice**: 🐹 Use Go

**Reasoning**:
- steipete: "Go for CLIs - agents are really great at writing it"
- "Simple type system makes linting fast"
- He didn't think about Go until recently
- Now his go-to for CLI tools

---

## Example 17: iOS Development

**Pitch**: "I need Xcode to build an iOS app"

**Advice**: 📱 Skip Xcode

**Reasoning**:
- steipete: "You don't need Xcode much anymore"
- "Swift's build infra is good enough for most things"
- "codex knows how to run iOS apps and how to deal with the Simulator"
- "No special stuff or MCPs needed"

---

## Example 18: Large Project Documentation

**Pitch**: "How do I help the model understand my large codebase?"

**Advice**: 📁 docs folder

**Reasoning**:
- steipete: "I maintain docs for subsystems in a docs folder"
- "Use a script to force the model to read docs on certain topics"
- "This pays off more the larger the project is"
- Better than relying on agent memory

---

## Example 19: Refactoring Strategy

**Pitch**: "Should I refactor while building features?"

**Advice**: 🔄 Separate phases

**Reasoning**:
- steipete: "I spend about 20% of my time on refactoring"
- "Refactor days are great when I need less focus"
- "Iterate fast, then maintain and improve"
- "Far more productive, and overall far more fun"

---

## Example 20: Thin Wrapper Startup

**Pitch**: "We're building a thin wrapper around GPT-5 with nice UI"

**Verdict**: ❌ SKIP

**Reasoning**:
- steipete: "Thin wrappers have no moat"
- "They all wrap either GPT-5 and/or Sonnet and are replaceable"
- "I don't see them surviving long-term"
- "There's simply not much space between the end user and the model company"

---

## Inference-Speed Checklist

Before you ask me about your idea, check:

```
□ Can you explain it in 2 sentences?
□ Does it solve YOUR problem?
□ Can it start as a CLI?
□ Can 1 person build v1?
□ Will you ship it in days, not months?
□ Would YOU actually use this?
□ Are you overcomplicating?
□ Are you planning instead of building?
```

If you answered no to any → I'll challenge you.
