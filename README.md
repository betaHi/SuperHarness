<div align="center">

# 🔱 Super Harness

### Multi-Agent Orchestration for Production Coding Workflows

**Turn a one-line task into production-ready code through coordinated AI agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Platform: OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-blue)](https://github.com/openclaw/openclaw)

[Design Philosophy](#design-philosophy) · [How It Works](#how-it-works) · [Usage](#usage) · [Architecture](#architecture) · [Roadmap](#roadmap)

</div>

---

## The Problem

Single AI agents fail at complex coding tasks. Not sometimes — **predictably**.

Anthropic's research quantified this: a solo agent spent $9 over 20 minutes and produced code with **broken core functionality**. The same task through a multi-agent harness cost $125 over 4 hours — but the output **actually worked**.

Why? Two fundamental failure modes:

1. **Self-evaluation bias** — Agents confidently praise their own mediocre work. Anthropic observed this directly: *"agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre."*

2. **Context degradation** — As context windows fill, agents rush to finish, skip edge cases, and stub implementations they promised to complete.

**Super Harness solves both problems by separating roles: one agent plans, another builds, a third judges.**

---

## Design Philosophy

Super Harness is built on five principles distilled from Anthropic's harness engineering research and real-world production patterns:

### 1. Separate the Doer from the Judge

> The single most impactful architectural decision in agentic coding.

A Generator that writes code should never evaluate its own output. An independent Evaluator with strict criteria catches what the Generator misses — stubbed features, broken edge cases, security oversights. This mirrors how human engineering teams work: developers don't merge their own PRs.

### 2. Simplest Thing That Works

> *"Find the simplest solution possible, and only increase complexity when needed."* — Anthropic, Building Effective Agents

A bug fix doesn't need a 16-feature spec. Super Harness assesses task complexity upfront and routes accordingly:

- **Simple** → Skip spec, write code, review
- **Medium** → Generate spec, write code, review
- **Complex** → Generate spec, decompose into sprints, write code, review each

### 3. File-Based Communication

Agents communicate through structured Markdown files in `.harness/handoff/`, not through conversation. This is deliberate:

- **Traceable** — Every decision, every handoff is a file you can inspect
- **Persistent** — Survives context resets, agent restarts, session timeouts
- **Debuggable** — When something breaks, read the files to find where
- **Auditable** — Full paper trail of what each agent decided and why

### 4. Fail Fast, Escalate Early

Max 2 review-fix cycles, then escalate to the human. Infinite retry loops burn money without convergence. If two rounds of feedback can't fix it, the problem likely exceeds the agent's capability — and the human's judgment is worth more than another $50 in tokens.

### 5. Harness Evolves With Models

> *"Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing."* — Anthropic

Today's essential scaffolding is tomorrow's dead weight. Anthropic proved this: Opus 4.5 needed sprint decomposition and context resets; Opus 4.6 didn't. Every phase in Super Harness can be toggled off via flags (`--no-spec`, `--no-review`), making it easy to strip away components as models improve.

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                     User: "Build X"                     │
└──────────────────────────┬──────────────────────────────┘
                           ▼
              ┌────────────────────────┐
              │   Phase 1: Parse &     │
              │   Assess Complexity    │
              │   (Simple/Medium/      │
              │    Complex)            │
              └───────────┬────────────┘
                          ▼
              ┌────────────────────────┐
              │   Phase 2: Setup       │
              │   .harness/handoff/    │
              │   workspace            │
              └───────────┬────────────┘
                          ▼
              ┌────────────────────────┐
              │   Phase 3: Planner     │──── spec.md
              │   (skip if simple)     │
              └───────────┬────────────┘
                          ▼
              ┌────────────────────────┐
              │   Phase 4: Generator   │──── code + implementation.md
              │   (Claude Code/Codex)  │
              └───────────┬────────────┘
                          ▼
              ┌────────────────────────┐
         ┌───▶│   Phase 5: Evaluator   │──── review.md
         │    │   (independent review) │
         │    └───────────┬────────────┘
         │           PASS?│
         │        ┌───────┴───────┐
         │        │               │
         │       YES             NO
         │        │               │
         │        ▼               ▼
         │   ┌─────────┐   ┌──────────┐
         │   │ Phase 6  │   │ Fix Loop │
         │   │ Report   │   │ (max 2x) │
         │   └─────────┘   └────┬─────┘
         │                      │
         └──────────────────────┘
```

### The Handoff Protocol

All inter-agent communication flows through structured files:

```
.harness/handoff/
├── task.md              # Original task + metadata + complexity assessment
├── spec.md              # Product spec from Planner (what to build, not how)
├── implementation.md    # Generator's notes (files changed, decisions, TODOs)
├── review.md            # Evaluator's verdict (PASS/FAIL + specific issues)
└── sprint-N-brief.md    # Per-sprint scope (multi-sprint only)
```

Each file follows a strict schema so downstream agents can parse reliably. No ambiguity, no "I think the previous agent meant..."

---

## Usage

### Basic

```bash
# Full pipeline: spec → code → review
/super-harness "Add JWT-based authentication with refresh tokens"

# Simple fix: skip spec, go straight to code → review
/super-harness "Fix the null pointer exception in auth.ts line 42" --no-spec

# Design only: generate spec without coding
/super-harness "Design a caching layer with Redis" --spec-only
```

### Advanced

```bash
# Force multi-sprint for large tasks
/super-harness "Refactor monolith payment module into microservice" --sprint multi

# Skip review for rapid prototyping
/super-harness "Build a quick prototype of the dashboard" --no-review

# Custom retry limit
/super-harness "Implement search with Elasticsearch" --max-retries 3

# Target specific repo
/super-harness "Add dark mode support" --repo /path/to/frontend

# Use specific model for sub-agents
/super-harness "Optimize database queries" --model claude-opus-4.6
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--repo` | cwd | Target repository path |
| `--spec-only` | false | Generate spec only, don't code |
| `--no-spec` | false | Skip spec generation |
| `--no-review` | false | Skip code review |
| `--max-retries` | 2 | Max review → fix cycles |
| `--model` | agent default | Model for sub-agents |
| `--sprint` | auto | `auto`, `single`, or `multi` |

---

## Architecture

### Why These Roles?

| Role | Purpose | Why It Exists |
|------|---------|---------------|
| **Planner** | Expand task → spec | Without a planner, agents under-scope. They start coding before understanding the full picture. |
| **Generator** | Implement code | The core builder. Uses Claude Code, Codex, or other coding agents. |
| **Evaluator** | Independent review | Agents can't judge their own work objectively. Separation is the key lever. |
| **Orchestrator** | Route & coordinate | Decides complexity, manages retries, handles escalation. |

### Complexity Routing

Not every task needs the full pipeline. Over-orchestrating simple tasks wastes time and money.

```
"Fix typo in README"          → [Code] → [Review]           ~$1, 2min
"Add user login"              → [Spec] → [Code] → [Review]  ~$15, 20min
"Rebuild payment system"      → [Spec] → [Sprint×N] → [Review×N]  ~$80, 2hr
```

### The Review-Fix Loop

When the Evaluator fails a submission:

```
Round 1: Generator builds → Evaluator finds 3 issues (🔴×1, 🟡×2)
Round 2: Generator fixes  → Evaluator finds 1 issue (🟡×1)
Round 3: Generator fixes  → Evaluator: PASS ✅

— OR —

Round 1: Generator builds → Evaluator finds issues
Round 2: Generator fixes  → Evaluator still finds issues
→ ESCALATE to human (with full context attached)
```

The 2-round limit is intentional. Anthropic's data shows improvement plateaus after 2-3 iterations. Beyond that, you're burning tokens without convergence.

---

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) — Agent platform
- At least one coding agent:
  - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (`claude` CLI) — recommended
  - [Codex](https://github.com/openai/codex) (`codex` CLI)

---

## Roadmap

| Version | Feature | Status |
|---------|---------|--------|
| **V1** | Spec → Code → Review pipeline with file-based handoff | ✅ Current |
| **V2** | Automated test runner (execute tests, not just read code) | 🔧 Planned |
| **V3** | Playwright-based UI verification for frontend tasks | 🔧 Planned |
| **V4** | Dynamic agent selection (pick best agent per task type) | 💭 Exploring |
| **V5** | Sprint contracts (Generator & Evaluator negotiate "done" criteria before coding) | 💭 Exploring |

---

## Research Foundation

Super Harness is grounded in published research and production engineering:

- **[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)** — Anthropic's three-agent architecture (Planner → Generator → Evaluator) and the finding that separating evaluation from generation is the highest-leverage intervention.

- **[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)** — The principle of minimal complexity: *"find the simplest solution possible, and only increase complexity when needed."*

- **[Claude Code Architecture](https://github.com/instructkr/claude-code)** — The `coordinator/`, `AgentTool`, and `TeamCreateTool` patterns from Claude Code's leaked source, demonstrating production-grade multi-agent orchestration via file-based communication.

- **[Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)** — Evidence that environment configuration alone can swing benchmark results by several percentage points, reinforcing the need for controlled harness design.

---

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas where help is most needed:
- Real-world testing across different project types
- Evaluator prompt tuning for stricter/better reviews
- Additional coding agent integrations
- Sprint decomposition heuristics

---

## License

MIT

---

<div align="center">

*Built for engineers who want AI agents that actually ship working code.*

**[⭐ Star this repo](https://github.com/betaHi/SuperHarness)** if you find it useful.

</div>
