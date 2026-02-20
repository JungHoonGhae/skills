# README Best Practices

Consolidated wisdom from Art of README, Make a README, and Standard README.

## Core Philosophy

### The README is Your One-Stop Shop

> "Your documentation is complete when someone can use your module without ever having to look at its code." — Ken Williams

A README's job is to **keep users out of the source code** by providing instructions sufficient to enjoy your abstractions.

### Brevity is a Feature

> The ideal README is as short as it can be without being any shorter.

Detailed documentation belongs in separate files. Keep README succinct.

### Care About People's Time

Your job isn't to "sell" people on your work. It's to let them evaluate objectively and decide quickly whether it meets their needs.

## Cognitive Funneling

Order sections from broad to specific, letting readers "short circuit" quickly:

```
Broad ──────────────────────────────────► Specific

Name → One-liner → Usage → API → Install → License
```

Each step takes the reader deeper. Those who reach the bottom are genuinely interested.

## Required Sections (All Types)

### 1. Name

**Status**: Required

- Must be self-explanatory
- Should match repository/package name
- If names don't match, explain why in description

### 2. Short Description

**Status**: Required

- Less than 120 characters
- No blockquote format (`> `)
- Must match package.json description
- Must match GitHub description

### 3. Usage

**Status**: Required (except pure docs repos)

- Code block showing common usage
- If CLI: show command invocations
- If library: show import + function call
- Include expected output if helpful

## Optional Sections

### Badges

**Status**: Optional

- Use Shields.io for generation
- Be judicious - each adds visual noise
- Consider: "What real value is this badge providing?"

### Installation

**Status**: Required by default

- Code block with install command
- List system requirements
- Include version requirements

### Table of Contents

**Status**: Required if README > 100 lines

- Link to all sections
- One-depth minimum (all ## headers)
- Don't include Title or ToC itself

### Background

**Status**: Optional

- Cover motivation
- Cover abstract dependencies
- Cover intellectual provenance
- Use for unfamiliar concepts

### API

**Status**: Optional

- Describe exported functions/objects
- Include signatures, return types, callbacks
- Note caveats
- Link to external API docs if using generator

### Contributing

**Status**: Required

- State if PRs accepted
- List requirements for contributing
- Link to CONTRIBUTING.md
- Link to Code of Conduct

### License

**Status**: Required

- Use SPDX identifier (MIT, Apache-2.0, etc.)
- State license owner
- Must be last section

## Style Guidelines

### Do

- **Show, don't tell** — Include runnable examples
- **Linkify aggressively** — Reference modules, concepts, people
- **Use structure** — Headers, tables, lists improve scannability
- **Include example files** — Let users run the code
- **Mention caveats up-front** — Don't hide limitations

### Don't

- **No installation steps** — Never assume setup is obvious
- **No examples** — Show, don't just tell
- **Wall of text** — Break up with headers and lists
- **Rely on images** — Inline critical information
- **Generic tone** — Write for YOUR audience

## Project Type Selection

| Type | Audience | Key Focus |
|------|----------|-----------|
| **Open Source** | Contributors, users | Install, Usage, Contributing, License |
| **Personal** | Future you, portfolio | What it does, Tech stack, Learnings |
| **Internal** | Teammates, new hires | Setup, Architecture, Runbooks |
| **Config** | Future you (confused) | What's here, Why, Gotchas |

## README Checklist

- [ ] One-liner explaining purpose
- [ ] Necessary background context & links
- [ ] Clear, runnable example of usage
- [ ] Installation instructions
- [ ] API documentation (if library)
- [ ] Cognitive funneling (broad → specific)
- [ ] Caveats mentioned up-front
- [ ] Doesn't rely on images for critical info
- [ ] License

## Sources

- [Art of README](https://github.com/hackergrrl/art-of-readme)
- [Make a README](https://www.makeareadme.com)
- [Standard README](https://github.com/RichardLitt/standard-readme)
