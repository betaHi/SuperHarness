# Protocol: Handoff Schema

## Overview
All inter-agent communication uses structured Markdown files. This document defines the schema for each file type.

## task.md

```markdown
# Task
[Natural language task description]

## Metadata
- Complexity: [Simple | Medium | Complex]
- Sprint Mode: [single | multi]
- Base Branch: [git branch name]
- Base Commit: [git commit hash]
- Timestamp: [ISO 8601]
```

## spec.md

```markdown
# Spec: [Title]

## Overview
[What we're building and why — 2-3 sentences]

## Scope
**In scope:** [bullet list]
**Out of scope:** [bullet list]

## Technical Design
[High-level approach — WHAT not HOW]

## Files to Create/Modify
[Expected file changes]

## Acceptance Criteria
[Numbered list of concrete, testable criteria]

## Sprint Plan (if multi-sprint)
[Ordered list of sprints with deliverables]
```

## implementation.md

```markdown
# Implementation Notes

## Files Changed
[List with brief description of each change]

## Key Decisions
[Decisions made during implementation and why]

## How to Test
[Commands or steps to verify the implementation]

## Known Limitations
[Anything incomplete, deferred, or potentially fragile]
```

## review.md

```markdown
# Code Review

## Verdict: [PASS | FAIL]

## Issues Found
[Each issue with severity: Must Fix / Should Fix / Nit]

## What's Good
[Brief — keep it short]

## Required Changes (if FAIL)
[Specific, actionable changes needed to pass]

## Acceptance Criteria Check
[Each criterion from spec: or with notes]
```
