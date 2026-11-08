# Maintaining the WorkMagic plugin

One repository, one set of skills, one MCP server — published to several agent platforms. The
repository root **is** the plugin folder, because Gemini CLI only reads a manifest at the root.

```
workmagic-agent-plugin/
├── skills/                      # the 9 customer skills (synced from WorkMagic's internal skills repo — don't edit here)
├── .mcp.json                    # MCP server, Claude / Codex / Cursor format
├── mcp.json                     # MCP server, Agent Plugins format (ChatGPT, Copilot, …)
├── .claude-plugin/              # Claude: plugin.json + marketplace.json
├── .codex-plugin/plugin.json    # Codex
├── .agents/plugins/marketplace.json  # Codex marketplace (`codex plugin marketplace add`)
├── .cursor-plugin/              # Cursor: plugin.json + marketplace.json
├── plugin.json                  # Agent Plugins 1.0 + extensions.com.openai (ChatGPT listing data)
├── gemini-extension.json        # Gemini CLI
├── assets/logo.png              # TODO: square PNG, at least 512×512
├── README.md                    # customer-facing; every directory shows it
├── CHANGELOG.md                 # release notes; the release workflow publishes each version's section
├── examples/                    # sample conversations on the demo store (synthetic data)
├── .github/workflows/release.yml
└── tools/                       # maintenance scripts (not part of the plugin's behavior)
```

## Where each platform lists it

| Platform | What gets listed | How to publish | Notes |
|---|---|---|---|
| **Claude** | MCP connector **and** plugin (two listings, paired) | claude.ai/directory/manage → *MCP connector* (server URL), then *Plugin bundle* (this repo, path `.`) | Any paid plan can submit; on Team/Enterprise an Owner |
| **ChatGPT** | One plugin = skills + the MCP server | OpenAI plugin portal: upload `dist/workmagic-chatgpt.zip`, verify the domain (`/.well-known/openai-apps-challenge` on mcp.workmagic.io), add test account, 5 positive + 3 negative test cases, a video | Needs a verified OpenAI org; website, support, privacy and terms URLs; MCP tool changes go live after a daily scan, skill changes need a new ZIP |
| **Codex** | Plugin | Git marketplace now (`codex plugin marketplace add …`); official directory via the same OpenAI portal | |
| **Cursor** | Plugin | Install from this repo; the official marketplace (cursor/plugins) is curated by Cursor — contact them for a listing | |
| **GitHub Copilot / VS Code** | Plugin (Agent Plugins format) and/or MCP server | Plugin: install from repo. Server: publish `server.json` (maintained in the MCP server repo) to the official MCP Registry with `mcp-publisher` — VS Code and GitHub's MCP registry read from it | |
| **Gemini CLI** | Extension | Public repo + GitHub topic `gemini-cli-extension`; the gallery crawler picks it up daily after a tagged release | Manifest must be at the repo root |
| **Everything else** | MCP server | Official MCP Registry (`io.github.workmagicio/workmagic-mcp` from the MCP server repo's `server.json`) | Smithery, PulseMCP etc. index the registry |


## Update the skills

```bash
python3 tools/sync_skills.py /path/to/skills-checkout
git diff                                  # review what changed upstream
```

The sync script stops if one of its patches no longer matches upstream, or if a shipped skill
still refers to the server-side skill loader or to a skill this release doesn't include.

## Release

1. Raise `version` in every manifest (all six must match) and add a `## [X.Y.Z]` section to
   `CHANGELOG.md`.
2. `python3 tools/check_manifests.py` — names, versions and MCP URLs agree; skills have frontmatter.
3. `claude plugin validate .`
4. Tag `vX.Y.Z` and push. The release workflow checks the manifests, builds the ChatGPT and Codex ZIPs and
   publishes a GitHub release with that version's changelog. Claude, Codex, Cursor and Gemini pick
   up the tag from the repo.
5. Upload the release's `workmagic-chatgpt.zip` to the OpenAI portal.

Ship small and often: each release shows up on the repo page and notifies everyone watching it.

### 本地验证 Codex 安装包

执行 README 的 Codex 本地安装命令。`python3 tools/build_zip.py codex` 从仓库配置构建独立的
`dist/workmagic-codex.zip`，包含 `.agents/plugins/marketplace.json`、
`.codex-plugin/plugin.json`、`.mcp.json` 及共享技能和资源。marketplace 的 `./` 源路径
指向解压后的根目录，不需要手工补文件。ChatGPT ZIP 继续仅包含 ChatGPT 所需配置。

## Repository presentation

Set once in the GitHub repo settings:

- **About → Description:** `Ask your WorkMagic marketing data anything — attribution, lift tests and budget plans in Claude, ChatGPT, Codex, Cursor, Copilot and Gemini.`
- **About → Website:** `https://workmagic.io`
- **About → Topics:** `mcp`, `mcp-server`, `claude`, `claude-plugin`, `chatgpt`, `codex`, `cursor`,
  `gemini-cli-extension`, `agent-skills`, `marketing-attribution`, `incrementality`, `mmm`,
  `ecommerce`, `shopify` (`gemini-cli-extension` is what puts it in the Gemini gallery)
- **Social preview:** a 1280×640 image with the logo and the tagline — it's the card shown when the
  repo link is shared on LinkedIn, X or Slack.
- **Releases** shown on the repo page; **Issues** on, so customers can report skill problems.

### Demo GIF (to record)

The README opens with a text demo. A 20–30 second GIF above it converts better; save it as
`assets/demo.gif` (under 5 MB) and add `![WorkMagic in Claude](assets/demo.gif)` under the badges.

1. Claude desktop, a fresh chat, WorkMagic connected to the demo store.
2. Type: *Compare Meta and Google attributed revenue under data-driven, last click, first click and
   any-click attribution for the last 30 days, and explain why they differ.*
3. Let the tool calls run; stop on the table and the first two explanation bullets.
4. Crop to the chat column, 2× playback speed for the waiting part.

### Samples in `examples/`

Every figure in `examples/` comes from the demo store's real WorkMagic output (synthetic orders,
Oct 12–29, 2026). When you add a sample, run it there and keep the numbers as returned.

## Not in this release

| Skill | Why |
|---|---|
| `lift-test-creation` | Needs a plugin edition before it can ship here |
| `attribution-weekly-report` | Depends on a host artifact tool and scheduled tasks that differ per platform |
| `media-buyer-read`, `media-buyer-input-capture` | Only useful for AI Media Buyer customers |
