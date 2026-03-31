# 🔱 Super Harness — Design Document

## Why Super Harness?

### The Problem

Single AI agents fail at complex coding tasks in three predictable ways:

1. **Context Anxiety** — As the context window fills, agents start rushing to finish, cutting corners, and stubbing implementations they promised to complete. Anthropic explicitly observed this behavior in Sonnet 4.5.

2. **Self-Evaluation Bias** — When asked to evaluate their own code, agents invariably say "it's great" — even when the quality is obviously mediocre. Like asking a student to grade their own exam: nobody fails themselves. Anthropic confirmed: *"agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre."*

3. **Long-Task Drift** — Beyond a certain complexity threshold, single agents lose coherence: they go off-track, drop features, and produce incomplete implementations. Anthropic's controlled comparison: solo agent at $9/20min produced broken core functionality; three-agent harness at $125/4h produced working, feature-complete output.

### The Solution

**Separate roles. Each agent does one thing well.**

Inspired by Anthropic's GAN-style architecture (Generator + Evaluator adversarial loop), plus a Planner for upfront decomposition, forming a three-agent pipeline. The core insight:

> **"Separating the doer from the judge is the highest-leverage intervention."** An independent Evaluator is 10x stricter than a Generator's self-evaluation — and far easier to calibrate.

## Architecture

```
User: "Build X"
     │
     ▼
┌─────────────────────┐
│ Phase 1: Parse      │ ← Parse task, assess complexity
│ Phase 2: Setup      │ ← Create .harness/handoff/ workspace
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 3: Planner    │ ← Expand task into spec (complex tasks)
│ 📋 spec.md          │   Skip (simple tasks)
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 4: Generator  │ ← Claude Code / Codex writes code
│ 🐯 implementation.md│
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Phase 5: Evaluator  │ ← Independent review, strict judgment
│ 🔱 review.md        │
└─────────┬───────────┘
          │
     PASS?├── YES → Phase 6: Report ✅
          │
          └── NO → Back to Generator for fixes
                   (max 2 rounds, then escalate to human)
```

## Design Decisions

### 1. File-Based Communication (Handoff Protocol)

**Why not direct agent-to-agent conversation?**

- Files are **traceable** and **debuggable** — when something breaks, inspect the files to find exactly which phase went wrong
- Files are **persistent** — survive context resets, agent restarts, and session timeouts
- Files are **structured** — more precise than natural language conversation
- Both Anthropic and Claude Code use this pattern (*"Communication was handled via files"*)

```
.harness/handoff/
├── task.md              # Task description + metadata
├── spec.md              # Product specification
├── implementation.md    # Implementation notes
├── review.md            # Code review verdict
└── sprint-N-brief.md    # Sprint scope (multi-sprint only)
```

### 2. Smart Complexity Routing

**Why not run the full pipeline for everything?**

- Simple tasks (bug fixes) through the full pipeline is wasteful — $125 to fix a typo?
- Complex tasks skipping the spec will go off-track — Anthropic confirmed *"without a planner, agents under-scope"*

Dynamic routing based on assessed complexity:
- **Simple** → Skip spec, write code directly
- **Medium** → Generate spec, single sprint
- **Complex** → Generate spec, multiple sprints

### 3. Maximum 2 Retry Rounds

**Why not retry until it passes?**

- Infinite retries = infinite cost
- Anthropic's data: improvement plateaus after 2-3 iterations
- If 2 rounds can't fix it, the problem exceeds the agent's capability — hand it to the human
- **Fail fast, escalate early** — machine-unsolvable problems should reach the human quickly

### 4. Independent and Strict Evaluator

**Why not let the Generator check its own work?**

Anthropic's direct observation:
> *"agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre"*

Benefits of separation:
- Evaluator can be independently tuned toward strictness
- Generator receives genuine external pressure, improving its responses to feedback
- Mirrors GAN-style adversarial dynamics — Generator and Evaluator push each other toward better outcomes

### 5. Specs Stay High-Level

**Why doesn't the Planner specify implementation details?**

Anthropic learned this the hard way:
> *"if the planner tried to specify granular technical details upfront and got something wrong, the errors in the spec would cascade into the downstream implementation"*

The spec defines **what** to build, not **how** to code it. Implementation details are the Generator's domain.

### 6. Modular and Skippable Phases

**Why is every phase toggleable?**

Anthropic's most important lesson:
> *"every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing"*

- The 4.5 era required sprint decomposition → 4.6 no longer needed it
- The 4.5 era required context resets → 4.6 no longer needed them
- Today's essential component may be tomorrow's dead weight

Every phase can be skipped via flags (`--no-spec`, `--no-review`), making it straightforward to simplify the harness as models improve.

## Target Users

1. **Solo Developers** — Working alone but wanting code review and quality assurance
2. **Small Teams** — Using agents to fill missing roles (PM for specs, senior engineer for reviews)
3. **Learners** — Learning best practices through agent-generated specs and reviews

## Use Cases

| Scenario | Command | Phases |
|----------|---------|--------|
| Bug fix | `/super-harness "Fix null check in auth.ts" --no-spec` | Code → Review |
| New feature | `/super-harness "Add JWT authentication"` | Spec → Code → Review |
| Major refactor | `/super-harness "Refactor payment module to microservice" --sprint multi` | Spec → Multi-Sprint Code → Review |
| Design only | `/super-harness "Design caching layer" --spec-only` | Spec only |
| Rapid prototype | `/super-harness "Build a todo app" --no-review` | Spec → Code |

## Roadmap

| Version | Feature | Status |
|---------|---------|--------|
| V1 | Spec → Code → Review base pipeline | ✅ Current |
| V2 | Automated test agent (run tests, not just read code) | 🔧 Planned |
| V3 | Playwright UI verification (frontend tasks) | 🔧 Planned |
| V4 | Dynamic agent selection (best agent per task type) | 💭 Exploring |
| V5 | Sprint contracts (Generator & Evaluator negotiate completion criteria before coding) | 💭 Exploring |

## References

- [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Theoretical foundation for the three-agent architecture
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — *"find the simplest solution possible"*
- [Claude Code Source Architecture](https://github.com/instructkr/claude-code) — Production patterns from coordinator/, AgentTool, TeamCreateTool
- [OpenClaw gh-issues Skill](https://github.com/openclaw/openclaw) — Reference implementation for sub-agent orchestration patterns
