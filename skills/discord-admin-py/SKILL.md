# Discord Admin App - AI Coding Agent Guide

This is an inference.sh multi-function app for Discord server administration.

## App Structure

```
discord-admin-py/
├── inf.yml           # Configuration (name, category, secrets)
├── inference.py       # Main app with all functions
├── requirements.txt  # Python dependencies (aiohttp)
└── skills/           # This file - AI agent guidance
```

## How It Works

- **Multi-Function App**: All public methods in the `App` class become callable functions
- **Function Discovery**: Methods with Pydantic input/output types extending BaseAppInput/BaseAppOutput are auto-discovered
- **Secrets**: Requires `DISCORD_BOT_TOKEN` environment variable

## Adding New Functions

When adding new Discord API functionality:

1. Create Input class extending `BaseAppInput` with Pydantic Field annotations
2. Create Output class extending `BaseAppOutput` with Pydantic Field annotations
3. Add async method to App class with typed input parameter and return type
4. Use `self._validate_snowflake(name, value)` for Discord ID validation
5. Use `self._request(method, endpoint, data)` for API calls
6. Use `metadata.log(message)` for progress logging

## API Base

Discord API v10: `https://discord.com/api/v10`

All endpoints: `/channels`, `/guilds`, `/members`, `/roles`, `/webhooks`, etc.

## Example: Adding a New Function

```python
class GetInviteInput(BaseAppInput):
    invite_code: str = Field(description="Invite code")

class GetInviteOutput(BaseAppOutput):
    code: str
    guild_id: str

async def get_invite(self, input_data: GetInviteInput, metadata) -> GetInviteOutput:
    self._validate_snowflake("invite_code", input_data.invite_code)
    result = await self._request("GET", f"/invites/{input_data.invite_code}")
    return GetInviteOutput(code=result["code"], guild_id=result["guild"]["id"])
```

## Testing

```bash
# Test a function
infsh app dev --function send_message --input '{"channel_id": "123", "content": "Hello"}'

# Validate functions
infsh app validate
```

## References

- [Discord API Docs](https://discord.com/developers/docs/reference)
- [inference.sh Multi-Function Apps](https://inference.sh/docs/extend/multi-function-apps)
