<div align="center">

# Super Harness

### An Engineering Paradigm for AI-Assisted Software Development

**AI coding's next stage isn't better generation — it's better engineering systems.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

[The Five Layers](#the-five-layers) · [Why This Matters](#why-this-matters) · [Patterns](#patterns) · [Reference Implementation](#reference-implementation) · [Roadmap](#roadmap)

</div>

---

## What Is Super Harness?

Super Harness is not a framework. Not a tool. Not a library.

It is **an engineering paradigm** — a reusable set of patterns, protocols, and practices for building reliable AI-assisted coding workflows.

The core insight: the bottleneck in AI coding is no longer generation. Models can write code. The bottleneck is everything *around* the code — spec formation, task decomposition, environment design, quality assurance, and feedback loops.

> *"Building software still demands discipline, but the discipline shows up more in the scaffolding rather than the code."*
> — OpenAI, Harness Engineering

Super Harness codifies that scaffolding into a reproducible engineering paradigm that any team can adopt, adapt, and build upon.

---

## The Five Layers

AI-assisted software development operates across five distinct layers. Most tools today optimize for one or two. Super Harness addresses all five as an integrated system.

```
┌─────────────────────────────────────────────────┐
│ │
│ Layer 5: Execution │
│ Write code, run tests, debug, commit │
│ │
├─────────────────────────────────────────────────┤
│ │
│ Layer 4: Harness │
│ Environment, tools, constraints, feedback │
│ loops — everything the agent needs to work │
│ reliably over time │
│ │
├─────────────────────────────────────────────────┤
│ │
│ Layer 3: Plan │
│ Spec → task sequence, sprint decomposition, │
│ dependency ordering │
│ │
├─────────────────────────────────────────────────┤
│ │
│ Layer 2: Spec │
│ Intent → engineering input: requirements, │
│ constraints, acceptance criteria │
│ │
├─────────────────────────────────────────────────┤
│ │
│ Layer 1: Intent │
│ What the human actually wants to accomplish │
│ │
└─────────────────────────────────────────────────┘
```

### Layer 1: Intent

The raw human need. Often ambiguous, incomplete, implicit.

**The problem:** Most AI coding tools take a prompt and immediately jump to code. But a prompt is not a spec. *"Add authentication"* means entirely different things depending on context.

**The pattern:** Don't let agents start coding from raw intent. First, surface assumptions, clarify scope, and expose hidden constraints. Superpowers calls this *brainstorming* — *"it doesn't just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do."*

### Layer 2: Spec

The structured engineering input derived from intent.

**The problem:** Without an explicit spec, agent decisions go undocumented, requirements stay fuzzy, and you can't tell if the output meets them. As Kiro puts it: *"You guided the agent throughout, but those decisions aren't documented. Requirements are fuzzy and you can't tell if the application meets them."*

**The pattern:** Transform conversation into specification. Not a heavyweight document — a lightweight but explicit artifact that captures goals, constraints, boundaries, and acceptance criteria. The spec becomes the contract between human intent and agent execution.

**Key principle:** Specs define *what* to build, not *how* to code it. Anthropic learned this directly: *"if the planner tried to specify granular technical details upfront and got something wrong, the errors in the spec would cascade into the downstream implementation."*

### Layer 3: Plan

The bridge from spec to executable tasks.

**The problem:** A spec describes the destination. A plan describes the route. Without decomposition, agents attempt everything at once and lose coherence on complex tasks.

**The pattern:** Break the spec into ordered, discrete tasks. Each task has clear scope, defined inputs, and testable completion criteria. For complex work, organize tasks into sprints with explicit handoff artifacts between phases.

**Key principle:** Plan granularity should match task complexity. A bug fix needs no plan. A new module needs sprint decomposition. Over-planning simple tasks wastes resources; under-planning complex tasks causes drift.

### Layer 4: Harness

The engineering environment that enables agents to work reliably.

**The problem:** An agent's effective world is limited to what it can access in context. *"From the agent's point of view, anything it can't access in-context while running effectively doesn't exist."* — OpenAI

**The pattern:** Design the agent's working environment with the same rigor you'd design a production system:
- **Knowledge:** Documentation as system of record, machine-readable, current
- **Tools:** Integrated and accessible — linters, test runners, type checkers
- **Constraints:** Architecture rules enforced mechanically, not by hope
- **Feedback:** Automated verification loops — tests pass, types check, lints clean
- **Legibility:** *"Agent legibility is the goal"* — the agent's state and decisions should be inspectable

**Key principle:** For human engineers, implicit context fills many gaps. For agents, if it's not explicit, accessible, and verifiable, it doesn't exist.

### Layer 5: Execution

The actual coding, testing, debugging, and delivery.

**The problem:** This is where most attention goes today, but it's the *least* differentiating layer. Models can already write code. The quality of that code depends almost entirely on the quality of Layers 1-4.

**The pattern:** Separate roles. The builder should not judge its own work. Anthropic's research demonstrates this is the highest-leverage architectural decision: *"agents tend to respond by confidently praising the work — even when, to a human observer, the quality is obviously mediocre."* Independent evaluation catches what self-evaluation misses.

**Key principle:** Execution quality is a *downstream* effect of spec clarity, plan coherence, and harness reliability. Fix the upstream layers, and execution improves automatically.

---

## Why This Matters

### The evolving ecosystem

The AI coding community is converging on a shared realization: reliable AI-assisted development requires more than generation. Multiple projects and research efforts are exploring different parts of this space, each contributing valuable insights:
| Project / Research | Primary Contribution | Layers Addressed |
|--------------------|---------------------|------------------|
| [Superpowers](https://github.com/obra/superpowers) | Pioneered brainstorming-first workflow and composable skills | Intent, Spec, Plan, Execution |
| [Kiro](https://kiro.dev/) | Productized spec-driven development with structured requirements | Spec, Plan |
| [MoAI-ADK](https://github.com/modu-ai/moai-adk) | High-performance harness with 24 agents and 52 skills | Harness, Execution |
| [Harness Engineering](https://openai.com/index/harness-engineering/) (OpenAI) | Articulated environment design as engineering discipline | Harness |
| [Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) (Anthropic) | Demonstrated multi-agent separation as highest-leverage intervention | Execution |
| [OpenDev](https://arxiv.org/abs/2603.05344) | Academic analysis of scaffolding and context engineering | Harness, Execution |

Each of these advances the field in meaningful ways. Super Harness builds on their collective insights by attempting to organize these ideas into a unified five-layer model — not as a replacement for any existing tool, but as a shared mental model and engineering methodology that can inform how teams think about and build AI-assisted development workflows.

The five-layer model is one way to frame the problem. It draws heavily from the work above, and we encourage teams to explore the tools and ideas that best fit their needs.

### The shared thesis

A pattern is emerging across these projects and research efforts:

> **The differentiator in AI coding is shifting from generation to the engineering system around it.**

As generation commoditizes, the lasting value moves to spec formation, task decomposition, environment design, constraint enforcement, and feedback loops — Layers 2 through 4.

This isn't a novel claim — it's a convergent observation. Superpowers, Kiro, OpenAI, and Anthropic are all independently arriving at the same conclusion from different angles. Super Harness attempts to synthesize these observations into a coherent, reusable framework.

---

## Patterns

Super Harness defines reusable engineering patterns for each layer:

### Pattern: Spec Formation
Transform ambiguous intent into structured, verifiable requirements through guided elicitation.
→ [`patterns/spec-formation.md`](patterns/spec-formation.md)

### Pattern: Complexity-Based Routing
Assess task complexity and route through the appropriate pipeline — not every task needs every layer.
→ [`patterns/complexity-routing.md`](patterns/complexity-routing.md)

### Pattern: File-Based Handoff Protocol
Agents communicate through structured Markdown files, not conversation. Traceable, persistent, debuggable.
→ [`patterns/file-based-handoff.md`](patterns/file-based-handoff.md)

### Pattern: Independent Evaluation
Separate the builder from the judge. The agent that writes code should never be the one that reviews it.
→ [`patterns/independent-evaluation.md`](patterns/independent-evaluation.md)

### Pattern: Review-Fix Loop with Escalation
Maximum 2 automated fix cycles, then escalate to human judgment with full context.
→ [`patterns/review-fix-loop.md`](patterns/review-fix-loop.md)

### Pattern: Harness Evolution
Every harness component encodes an assumption about model limitations. Re-examine and simplify as models improve.
→ [`patterns/harness-evolution.md`](patterns/harness-evolution.md)

---

## Reference Implementation

Super Harness includes a reference implementation as an agent skill:

```bash
# Full five-layer pipeline
/super-harness "Add JWT-based authentication with refresh tokens"

# Skip spec for simple tasks (complexity routing)
/super-harness "Fix the null pointer in auth.ts" --no-spec

# Spec formation only
/super-harness "Design a caching layer with Redis" --spec-only
```

The reference implementation demonstrates the patterns in practice, but **the patterns are the product, not the implementation**. Teams can implement Super Harness patterns in any orchestration platform — LangGraph, CrewAI, shell scripts, or custom tooling.

→ [`SKILL.md`](SKILL.md) — Full reference implementation

---

## Repository Structure

```
SuperHarness/
├── README.md # This document — the paradigm
├── DESIGN.md # Design rationale (English)
├── DESIGN.zh.md # Design rationale (Chinese)
│
├── patterns/ # Reusable engineering patterns
│ ├── spec-formation.md
│ ├── complexity-routing.md
│ ├── file-based-handoff.md
│ ├── independent-evaluation.md
│ ├── review-fix-loop.md
│ └── harness-evolution.md
│
├── protocols/ # Communication protocols
│ └── handoff-schema.md # File-based handoff format spec
│
├── SKILL.md # Reference implementation (agent skill)
├── CONTRIBUTING.md
└── LICENSE
```

---

## Roadmap
| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Core patterns documented, reference implementation | Current |
| **Phase 2** | Eval benchmark — test cases for evaluator calibration | Next |
| **Phase 3** | Multiple reference implementations (LangGraph, shell scripts) | Planned |
| **Phase 4** | Community-contributed patterns and case studies | Exploring |
| **Phase 5** | Harness analytics — which layers are your bottleneck? | Exploring |

---

## Research Foundation

Super Harness synthesizes insights from three converging lines of work:

**Spec-driven development:**
- [Superpowers](https://github.com/obra/superpowers) — Brainstorming as spec formation; *"it doesn't just jump into trying to write code"*
- [Kiro](https://kiro.dev/) — *"Tame complexity with spec-driven development, advanced steering, and custom agents"*

**Harness engineering:**
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) — *"The team's primary job is no longer to write code, but to design environments, specify intent, and build feedback loops"*
- [Anthropic: Quantifying infrastructure noise in evals](https://www.anthropic.com/engineering/infrastructure-noise) — Environment configuration swings benchmarks by percentage points

**Multi-agent architecture:**
- [Anthropic: Harness design for long-running applications](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Planner → Generator → Evaluator; independent evaluation as highest-leverage intervention
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — *"Find the simplest solution possible, and only increase complexity when needed"*
- [Claude Code Architecture](https://github.com/instructkr/claude-code) — Production patterns: coordinator, AgentTool, TeamCreateTool, file-based communication

---

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

The highest-value contributions aren't code — they're **patterns**:
- Document a pattern you've found effective in AI-assisted development
- Share a case study of applying the five-layer model to a real project
- Contribute a reference implementation for a different platform
- Add test cases to the evaluator benchmark

---

## License

MIT

---

<div align="center">

*AI coding's next stage isn't better generation — it's better engineering systems.*

*Super Harness is one framework for thinking about and building them.*

**[Star this repo](https://github.com/betaHi/SuperHarness)** if this framework helps you think about AI-assisted development.

</div>
