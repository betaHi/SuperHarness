# 🔱 Super Harness

**Multi-agent coding orchestrator for OpenClaw.**

Inspired by [Anthropic's Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — a Planner → Generator → Evaluator architecture adapted for OpenClaw's agent ecosystem.

## What It Does

Turn a one-line task description into working code through a coordinated multi-agent pipeline:

```
/super-harness "Add user authentication with JWT tokens"
```

→ Automatically orchestrates:
1. **📋 Planner** — Expands task into a detailed spec
2. **🐯 Generator** — Implements the code (Claude Code / Codex)
3. **🔱 Evaluator** — Reviews code with strict criteria
4. **🔄 Fix Loop** — Addresses review feedback (max 2 rounds)
5. **📊 Report** — Summarizes what was done

## Key Design Decisions

- **File-based communication** — Agents pass context via `.harness/handoff/` markdown files
- **Separate doer from judge** — Generator never self-evaluates; Reviewer is independent and strict
- **Smart complexity routing** — Simple tasks skip spec; complex tasks get multi-sprint decomposition
- **Fail fast** — 2 retries max, then escalate to human
- **Model-agnostic** — Works with Claude Code, Codex, or any coding agent

## Usage

```bash
# Full pipeline
/super-harness "Build a REST API for user management"

# Skip spec for simple tasks
/super-harness "Fix the null pointer in auth.ts line 42" --no-spec

# Only generate spec, don't code
/super-harness "Design a caching layer for the API" --spec-only

# Custom retry limit
/super-harness "Refactor the payment module" --max-retries 3

# Target specific repo
/super-harness "Add dark mode support" --repo /path/to/project
```

## Architecture

```
User: "Build X"
     ↓
[Phase 1] Parse & Assess Complexity
     ↓
[Phase 2] Setup Workspace (.harness/handoff/)
     ↓
[Phase 3] Planner Agent → spec.md
     ↓
[Phase 4] Generator Agent → code + implementation.md
     ↓
[Phase 5] Evaluator Agent → review.md
     ↓ (FAIL? → retry with feedback, max 2x)
[Phase 6] Report to User
```

## Handoff Files

All inter-agent communication happens through structured markdown files:

```
.harness/handoff/
├── task.md              # Original task + metadata
├── spec.md              # Product spec (from Planner)
├── implementation.md    # What was built (from Generator)
├── review.md            # Code review (from Evaluator)
└── sprint-N-brief.md    # Sprint scope (multi-sprint only)
```

## Requirements

- OpenClaw
- At least one coding agent: `claude` (Claude Code) or `codex` (OpenAI Codex)

## Roadmap

- **V1 (current):** Spec → Code → Review pipeline with file-based handoff
- **V2:** Add automated testing agent (run tests, not just read code)
- **V3:** Playwright-based UI verification for frontend tasks
- **V4:** Dynamic agent selection based on task type

## Credits

- Architecture inspired by [Anthropic's Harness Design Blog](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Patterns informed by [Claude Code's coordinator architecture](https://github.com/instructkr/claude-code)
- Built for the [OpenClaw](https://github.com/openclaw/openclaw) agent platform

## License

MIT
