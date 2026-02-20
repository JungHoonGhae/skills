# JungHoonGhae Skills

[![skills.sh](https://skills-badge.vercel.app/badge/JungHoonGhae/skills?style=flat-square&label=installs)](https://skills.sh/JungHoonGhae/skills)

AI agent skills collection for Claude Code, OpenCode, and other AI coding assistants.

## Skills

| Skill | Description | Triggers | Installs |
|-------|-------------|----------|----------|
| **[x-composer](skills/x-composer/)** | Post to X.com via Chrome CDP | "post to X", "tweet", "draft a tweet" | [![x-composer](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/x-composer?style=flat-square)](https://skills.sh/JungHoonGhae/skills/x-composer) |
| **[ships-with-steipete](skills/ships-with-steipete/)** | Get coaching from steipete's perspective | Idea validation, project feedback | [![ships-with-steipete](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/ships-with-steipete?style=flat-square)](https://skills.sh/JungHoonGhae/skills/ships-with-steipete) |
| **[readme-doctor](skills/readme-doctor/)** | Generate README from GitHub patterns | "create README", "README based on my style" | [![readme-doctor](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/readme-doctor?style=flat-square)](https://skills.sh/JungHoonGhae/skills/readme-doctor) |
| **[oh-my-lilys](skills/oh-my-lilys/)** | Summarize YouTube, PDF, websites via lilys.ai | "summarize URL", "generate report" | [![oh-my-lilys](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/oh-my-lilys?style=flat-square)](https://skills.sh/JungHoonGhae/skills/oh-my-lilys) |
| **[discord-admin-py](skills/discord-admin-py/)** | Discord server administration | Discord bot, channel management | [![discord-admin-py](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/discord-admin-py?style=flat-square)](https://skills.sh/JungHoonGhae/skills/discord-admin-py) |

## Installation

### Option 1: Install All Skills

```bash
npx skills add JungHoonGhae/skills
```

### Option 2: Install Specific Skills

```bash
npx skills add JungHoonGhae/skills@x-composer
npx skills add JungHoonGhae/skills@ships-with-steipete
npx skills add JungHoonGhae/skills@readme-doctor
npx skills add JungHoonGhae/skills@oh-my-lilys
npx skills add JungHoonGhae/skills@discord-admin-py
```

### Manual Installation

Copy to your skills directory:

```bash
# Claude Code
cp -r skills/* ~/.claude/skills/

# OpenCode
cp -r skills/* ~/.opencode/skills/

# Project-level
cp -r skills/* .claude/skills/
```

## Related Repositories

Some skills have separate repositories for package distribution:

| Skill | Repository | Purpose |
|-------|------------|---------|
| oh-my-lilys | [JungHoonGhae/oh-my-lilys](https://github.com/JungHoonGhae/oh-my-lilys) | npm package |
| discord-admin-py | [JungHoonGhae/discord-admin-py](https://github.com/JungHoonGhae/discord-admin-py) | inference.sh app |

## License

MIT
