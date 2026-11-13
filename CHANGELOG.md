# Changelog

All notable changes to the WorkMagic plugin. Versions follow [Semantic Versioning](https://semver.org).

## [1.0.2] — 2026-11-13

### Changed

- Skills: SQL query templates renamed `.sql` → `.txt`, and skill frontmatter
  custom keys moved under `metadata`, to satisfy the Claude plugin directory's
  file-type and frontmatter allowlists.
- Added `server.json` (MCP Registry, published as
  `io.github.workmagicio/workmagic-mcp`) and a generated `plugins/claude/`
  bundle for the Claude directory submission (plugin path `plugins/claude`).
- MCP tool annotations corrected server-side (platform-mcp): every tool sets
  `readOnlyHint`/`destructiveHint`/`openWorldHint` explicitly, and
  overwrite/update tools are `destructiveHint: true`.

Version jumps 1.0.0 → 1.0.2 to stay aligned with the MCP Registry server
version (1.0.1 was never released as a plugin package).

[1.0.2]: https://github.com/workmagicio/workmagic-agent-plugin/releases/tag/v1.0.2

## [1.0.0] — 2026-11-05

### Added

- Nine skills: attribution data query, intent clarification, model comparison, anomaly diagnosis,
  custom dimensions, edge routing, lift test readout, and Media Budget Optimizer read and create.
- WorkMagic MCP server connection (`https://mcp.workmagic.io/mcp`) with OAuth sign-in.
- Manifests for Claude, ChatGPT and other Agent Plugins clients, Codex, Cursor and Gemini CLI.
- Sample conversations in `examples/`.

[1.0.0]: https://github.com/workmagicio/workmagic-agent-plugin/releases/tag/v1.0.0
