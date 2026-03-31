<div align="center">

# Super Harness

### An Engineering Paradigm for AI-Assisted Software Development

**AI coding's next stage isn't better generation — it's better engineering systems.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

[Quick Start](#quick-start) · [The Five Layers](#the-five-layers) · [Patterns](#patterns) · [Ecosystem](#ecosystem) · [Roadmap](#roadmap)

</div>

---

## Quick Start

```bash
# One line. That's it.
/super-harness "Add user authentication with JWT tokens"
```

What happens next:

```
You: "Add user authentication with JWT tokens"
                    |
Super Harness:      "Assessing... this is a medium-complexity task."
                    |
                    "Here's a spec. Take a look:"
                    |
                    [shows spec — goals, scope, acceptance criteria]
                    |
You:                "Looks good" (or suggest changes)
                    |
Super Harness:      "Building..."
                    |
                    "Done. Running independent code review..."
                    |
                    "Review passed. Here's what was built:"
                    |
                    [summary: files changed, decisions made, how to test]
```

Simple tasks skip the spec automatically. You stay in control at every step.

### More examples

```bash
# Bug fix — auto-detects simplicity, skips spec
/super-harness "Fix the null pointer in auth.ts line 42"

# Just want a spec, no coding yet
/super-harness "Design a caching layer with Redis" --spec-only

# I already have a spec — start from build
/super-harness --from build --spec docs/auth-spec.md

# Code is already written — just review it
/super-harness --from review

# Skip review for quick prototyping
/super-harness "Scaffold a basic Express API" --no-review
```

Start from wherever you are. Not every task needs every layer.

### Requirements

- A coding agent: [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (recommended) or [Codex](https://github.com/openai/codex)
- Git

---

## What Is This?

Super Harness is an engineering paradigm — a set of patterns, protocols, and practices for building reliable AI-assisted coding workflows.

The core observation: **the bottleneck in AI coding is no longer generation**. Models can write code. The bottleneck is everything around the code — clarifying intent, structuring requirements, designing the agent's working environment, and verifying the output.

> *"Building software still demands discipline, but the discipline shows up more in the scaffolding rather than the code."*
> — OpenAI, Harness Engineering

This repo contains:
1. **A five-layer mental model** for thinking about AI-assisted development
2. **Six reusable patterns** extracted from published research and production experience
3. **A reference implementation** you can use directly or adapt to your own tooling

---

## The Five Layers

```
  Layer 5: Execution      Write code, run tests, commit
  Layer 4: Harness        Environment, tools, constraints, feedback loops
  Layer 3: Plan           Task decomposition, sprint ordering
  Layer 2: Spec           Requirements, constraints, acceptance criteria
  Layer 1: Intent         What the human actually wants
```

Most tools optimize for Layer 5. The real leverage is in Layers 2-4.

**Not every task needs every layer.** A bug fix enters at Layer 5. A greenfield project starts at Layer 1. The system detects where you are and starts from there — or you tell it explicitly with `--from`.

### Layer 1: Intent

Raw human need — often ambiguous and incomplete.

Don't let agents code from raw intent. Surface assumptions first. As Superpowers puts it: *"It doesn't just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do."*

### Layer 2: Spec

Transform intent into structured engineering input — goals, scope, constraints, acceptance criteria.

Without a spec, agent decisions go undocumented and outputs are unverifiable. The spec is the contract between what you want and what gets built. Important: specs define *what*, not *how*. Over-specifying implementation details causes errors to cascade downstream.

### Layer 3: Plan

Break the spec into discrete, ordered tasks. Match granularity to complexity:
- Bug fix: no plan needed
- New feature: ordered task list
- Large project: sprint decomposition with handoff artifacts

### Layer 4: Harness

The agent's working environment. For agents, **if it's not explicit, accessible, and verifiable, it doesn't exist.**

Concretely:
- Documentation the agent can actually read (not a Confluence wiki it can't access)
- Tests it can run, linters it can invoke, type checkers it can call
- Architecture constraints enforced by tooling, not by hope
- Feedback loops: does the code compile, do tests pass, does lint clear?

### Layer 5: Execution

The actual coding. Important: **the builder should not judge its own work**.

Anthropic's research: *"Agents tend to confidently praise their work — even when the quality is obviously mediocre."* Independent evaluation is the highest-leverage intervention at this layer.

---

## Patterns

Six reusable patterns, each documented with Problem, Solution, and practical guidance:

| Pattern | What It Solves | Doc |
|---------|---------------|-----|
| **Spec Formation** | Agents jump to code before understanding the task | [spec-formation.md](patterns/spec-formation.md) |
| **Complexity Routing** | Simple tasks get over-orchestrated, complex tasks get under-served | [complexity-routing.md](patterns/complexity-routing.md) |
| **File-Based Handoff** | Context lost between agent sessions | [file-based-handoff.md](patterns/file-based-handoff.md) |
| **Independent Evaluation** | Agents can't objectively judge their own work | [independent-evaluation.md](patterns/independent-evaluation.md) |
| **Review-Fix Loop** | Review without a fix path is just a report | [review-fix-loop.md](patterns/review-fix-loop.md) |
| **Harness Evolution** | Harness components become dead weight as models improve | [harness-evolution.md](patterns/harness-evolution.md) |

---

## User Experience

Super Harness is designed around two principles: **you stay in control**, and **simple things stay simple**.

### Human checkpoints

The pipeline pauses at key decision points:

1. **After complexity assessment** — "This looks like a medium task. I'll generate a spec first."
2. **After spec generation** — "Here's the spec. Want to adjust before I start building?" *(This is the most important checkpoint.)*
3. **After review** — If FAIL: "Review found issues. Here's what needs fixing. Want me to auto-fix, or do you want to handle it?"
4. **After completion** — Full summary with files changed, decisions made, how to test.

You can skip checkpoints for speed (`--yes` to auto-approve) or add more (`--confirm-each-sprint` for multi-sprint tasks).

### Progressive complexity

Your first run should be a simple, successful experience:

```bash
# Start here. One task, automatic everything.
/super-harness "Add a health check endpoint to the API"
```

As you learn the system, unlock more control:

```bash
# Explicit complexity routing
/super-harness "Refactor auth module" --sprint multi

# Review-only mode: bring your own code, just want the review
/super-harness --review-only
```

### Progress feedback

Every phase reports its status:

```
[1/5] Assessing complexity... Medium
[2/5] Setting up workspace...
[3/5] Generating spec...
      Spec ready — review at .harness/handoff/spec.md
      > Approve spec? [yes / edit / abort]
[4/5] Building... (Claude Code)
      Sprint 1/1 complete.
[5/5] Reviewing...
      Verdict: PASS
      
Done. 3 files changed. Summary at .harness/handoff/implementation.md
```

---

## Ecosystem

The AI coding community is converging on a shared realization: reliable development requires more than generation. Multiple projects explore different parts of this space:

| Project / Research | Primary Contribution | Layers Addressed |
|--------------------|---------------------|------------------|
| [Superpowers](https://github.com/obra/superpowers) | Brainstorming-first workflow and composable skills | Intent, Spec, Plan, Execution |
| [Kiro](https://kiro.dev/) | Spec-driven development with structured requirements | Spec, Plan |
| [MoAI-ADK](https://github.com/modu-ai/moai-adk) | High-performance harness with specialized agents and skills | Harness, Execution |
| [Harness Engineering](https://openai.com/index/harness-engineering/) (OpenAI) | Environment design as engineering discipline | Harness |
| [Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) (Anthropic) | Multi-agent separation as highest-leverage intervention | Execution |

Super Harness builds on these insights by organizing them into a unified five-layer model. It's one way to frame the problem — not a replacement for any existing tool. We encourage teams to explore what fits best.

---

## Repository Structure

```
SuperHarness/
├── README.md                    # This document
├── SKILL.md                     # Reference implementation
├── DESIGN.md                    # Design rationale (English)
├── DESIGN.zh.md                 # Design rationale (Chinese)
├── patterns/                    # Reusable engineering patterns
│   ├── spec-formation.md
│   ├── complexity-routing.md
│   ├── file-based-handoff.md
│   ├── independent-evaluation.md
│   ├── review-fix-loop.md
│   └── harness-evolution.md
├── protocols/
│   └── handoff-schema.md        # File-based handoff format spec
├── CONTRIBUTING.md
└── LICENSE
```

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Core patterns, reference implementation, human checkpoints | Current |
| **Phase 2** | Eval benchmark for evaluator calibration | Next |
| **Phase 3** | Additional reference implementations (LangGraph, shell) | Planned |
| **Phase 4** | Community patterns and case studies | Exploring |

---

## Research Foundation

**Spec-driven development:**
- [Superpowers](https://github.com/obra/superpowers) — *"It doesn't just jump into trying to write code"*
- [Kiro](https://kiro.dev/) — *"Tame complexity with spec-driven development"*

**Harness engineering:**
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) — *"Design environments, specify intent, and build feedback loops"*
- [Anthropic: Infrastructure noise in evals](https://www.anthropic.com/engineering/infrastructure-noise) — Environment configuration swings benchmarks by percentage points

**Multi-agent architecture:**
- [Anthropic: Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Planner, Generator, Evaluator; independent evaluation as highest-leverage intervention
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — *"Find the simplest solution possible"*

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The highest-value contributions are **patterns** — document what works in your AI-assisted development practice and share it.

---

## License

MIT

---

<div align="center">

*The patterns are the product, not the implementation.*

*Super Harness is one framework for thinking about and building reliable AI-assisted development.*

</div>
