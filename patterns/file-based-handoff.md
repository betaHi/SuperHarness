# Pattern: File-Based Handoff Protocol

## Problem
Agents lose context across sessions. Conversational handoffs are lossy, untraceable, and break on context resets.

## Solution
All inter-agent communication flows through structured Markdown files in a shared directory. Each file follows a defined schema.

## Handoff Directory

```
.harness/handoff/
├── task.md # Original task + metadata
├── spec.md # Structured specification
├── implementation.md # What was built, decisions made, known limitations
├── review.md # Verdict (PASS/FAIL) + specific issues
└── sprint-N-brief.md # Per-sprint scope (multi-sprint only)
```

## Why Files, Not Conversation
- **Traceable** — Every decision is inspectable after the fact
- **Persistent** — Survives context resets, agent restarts, session timeouts
- **Structured** — More precise than natural language conversation
- **Debuggable** — When something breaks, read the files to find which phase went wrong

## References
- Anthropic: *"Communication was handled via files: one agent would write a file, another agent would read it and respond"*
- Claude Code architecture: coordinator/ uses file-based agent communication
