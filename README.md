# JungHoonGhae Skills

[![skills.sh](https://skills-badge.vercel.app/badge/JungHoonGhae/skills?style=flat-square&label=installs)](https://skills.sh/JungHoonGhae/skills)
[![GitHub stars](https://img.shields.io/github/stars/JungHoonGhae/skills)](https://github.com/JungHoonGhae/skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/JungHoonGhae/skills/blob/main/LICENSE)

| [<img alt="GitHub Follow" src="https://img.shields.io/github/followers/JungHoonGhae?style=flat-square&logo=github&labelColor=black&color=24292f" width="156px" />](https://github.com/JungHoonGhae) | Follow [@JungHoonGhae](https://github.com/JungHoonGhae) on GitHub for more projects. |
| :-----| :----- |
| [<img alt="X link" src="https://img.shields.io/badge/Follow-%40lucas_ghae-000000?style=flat-square&logo=x&labelColor=black" width="156px" />](https://x.com/lucas_ghae) | Follow [@lucas_ghae](https://x.com/lucas_ghae) on X for updates. |

AI agent skills collection for Claude Code, OpenCode, and other AI coding assistants.

## Support

If these skills help you, consider supporting their maintenance:

<a href="https://www.buymeacoffee.com/lucas.ghae">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50">
</a>

## Skills

| Skill | Description | Triggers | Installs |
|-------|-------------|----------|----------|
| **[x-composer](skills/x-composer/)** | Post to X.com via Chrome CDP automation | "post to X", "tweet", "draft a tweet" | [![x-composer](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/x-composer?style=flat-square)](https://skills.sh/JungHoonGhae/skills/x-composer) |
| **[ships-with-steipete](skills/ships-with-steipete/)** | Get coaching from steipete's perspective on ideas and decisions | Idea validation, project feedback, decision review | [![ships-with-steipete](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/ships-with-steipete?style=flat-square)](https://skills.sh/JungHoonGhae/skills/ships-with-steipete) |
| **[readme-doctor](skills/readme-doctor/)** | Diagnose README problems and prescribe improvements | "fix my README", "analyze this README", "make README like [reference]" | [![readme-doctor](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/readme-doctor?style=flat-square)](https://skills.sh/JungHoonGhae/skills/readme-doctor) |
| **[oh-my-lilys](skills/oh-my-lilys/)** | Summarize YouTube, PDF, websites, and audio via lilys.ai CLI | "summarize URL", "generate report", "summarize video" | [![oh-my-lilys](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/oh-my-lilys?style=flat-square)](https://skills.sh/JungHoonGhae/skills/oh-my-lilys) |
| **[discord-admin-py](skills/discord-admin-py/)** | Discord server administration via inference.sh | Discord bot, channel management, role assignment | [![discord-admin-py](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/discord-admin-py?style=flat-square)](https://skills.sh/JungHoonGhae/skills/discord-admin-py) |
| **[openkakao-cli](skills/openkakao-cli/)** | OpenKakao CLI workflow for auth, chats, reads, and read-only automation | "openkakao", "openkakao-rs", "kakao chat CLI", "-950 token" | [![openkakao-cli](https://skills-badge.vercel.app/badge/JungHoonGhae/skills/openkakao-cli?style=flat-square)](https://skills.sh/JungHoonGhae/skills/openkakao-cli) |

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
npx skills add JungHoonGhae/skills@openkakao-cli
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

## Documentation

| Resource | Link |
|----------|------|
| skills.sh | [skills.sh/JungHoonGhae/skills](https://skills.sh/JungHoonGhae/skills) |
| GitHub | [github.com/JungHoonGhae/skills](https://github.com/JungHoonGhae/skills) |

## License

MIT
