# MCP Connectors — v0.1

In v0.1, real MCP connections (Pipedrive, Gmail, Notion, etc.) are made **through Claude Code**, not through this Python package. The engine only records the *declaration* that a tool has been connected.

## Workflow

1. User picks a tool during `bin/opowai connect <thematic>`.
2. Claude Code spins up the matching MCP (or the user installs it via `/integrate-mcp`).
3. Once the MCP is live, run `bin/opowai connect <thematic> --tool <tool_id>` to record it.

## Supported tools (per thematic)

| Thematic | Popular tools | MCP path |
|----------|--------------|----------|
| `crm`      | pipedrive, hubspot, salesforce, close, attio, folk | Smithery / `/integrate-mcp` |
| `email`    | gmail, outlook, front, hey, superhuman             | Native Claude Code integrations |
| `calendar` | gcal, outlook-cal, calendly, cal-com               | Native Claude Code integrations |
| `docs`     | notion, confluence, coda, obsidian, slite          | Notion MCP, others via Smithery |
| `chat`     | slack, teams, discord                              | Slack/Teams MCPs |
| `project`  | linear, jira, notion-projects, asana, clickup      | Linear/Jira MCPs |
| `analytics`| posthog, amplitude, mixpanel, stripe, metabase     | Tool-specific MCPs |
| `transcript`| granola, gong, fireflies, otter, tactiq, loom     | Granola, Gong MCPs |
| `code`     | github, gitlab, bitbucket                          | GitHub MCP |
| `other`    | free-form                                          | Custom — `/integrate-mcp` |

## v0.2 — planned

- `/opowai-test-connector <tool>` — pings each MCP to verify it's actually live
- Connector health checks surfaced in `/opowai-status`
- Automatic MCP installation triggered by `bin/opowai connect`
