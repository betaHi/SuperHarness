# Pattern: Review-Fix Loop with Escalation

## Problem
Automated review without a fix path is just a report. But unlimited fix loops burn tokens without convergence.

## Solution
When review fails, route feedback back to the builder for a fix. Cap at 2 rounds, then escalate to human with full context.

## Flow

```
Build → Review → PASS → Done
 FAIL → Fix (round 1) → Review → PASS → Done
 FAIL → Fix (round 2) → Review → PASS → Done
 FAIL → ESCALATE
```

## Why Max 2 Rounds
- Anthropic's data: improvement plateaus after 2-3 iterations
- If 2 rounds can't fix it, the problem likely exceeds the agent's capability
- Human judgment at this point is worth more than another $50 in tokens

## Escalation Protocol
When escalating, provide:
1. Original task and spec
2. What was built (implementation.md)
3. All review feedback (review.md)
4. What was attempted in each fix round
5. Evaluator's assessment of remaining issues
