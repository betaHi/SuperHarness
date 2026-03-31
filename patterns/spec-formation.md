# Pattern: Spec Formation

## Problem
Agents jump from raw intent to code, producing output that technically runs but doesn't match what the human actually wanted. Decisions go undocumented, requirements stay implicit, acceptance criteria don't exist.

## Solution
Transform ambiguous intent into a structured spec before any code is written. The spec captures goals, constraints, boundaries, and acceptance criteria — becoming the contract between human intent and agent execution.

## How It Works
1. **Elicit** — Surface hidden assumptions through guided conversation
2. **Structure** — Organize into goals, scope (in/out), technical approach, acceptance criteria
3. **Validate** — Human reviews spec before execution begins
4. **Reference** — Spec becomes the source of truth for downstream agents

## Key Rules
- Spec defines **what** to build, not **how** to code it
- Keep it high-level — granular implementation details cause error cascading
- Acceptance criteria must be concrete and testable
- Spec is a living artifact — update it when scope changes

## When to Skip
- Bug fixes with clear reproduction steps
- One-line changes with obvious intent
- Tasks where the "spec" is a failing test case

## References
- Superpowers: *"it doesn't just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do."*
- Kiro: *"From single prompt to requirements → Technical design → Implement tasks"*
- Anthropic: *"if the planner tried to specify granular technical details upfront and got something wrong, the errors would cascade"*
