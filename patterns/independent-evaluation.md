# Pattern: Independent Evaluation

## Problem
Agents asked to evaluate their own output are systematically biased toward approval. They identify real issues, then rationalize them away.

## Solution
The agent that builds code must never be the agent that reviews it. Evaluation is performed by an independent agent with strict criteria and a skeptical posture.

## Why This Is the Highest-Leverage Pattern
Anthropic's controlled experiments demonstrated:
- Solo agent ($9, 20min): core functionality **broken**
- With independent evaluator ($125, 4hr): core functionality **working**

> *"Agents tend to respond by confidently praising the work — even when, to a human observer, the quality is obviously mediocre."*

Separating evaluation from generation was the single most impactful intervention.

## Review Dimensions (Priority Order)
1. **Correctness** — Does it work? Does it match the spec?
2. **Security** — Vulnerabilities, secrets, injection risks
3. **Design** — Architecture soundness, code smells
4. **Edge Cases** — What could break? Missing error handling?
5. **Style** — Consistency, naming, formatting

## Calibration
Out-of-the-box LLMs are poor evaluators. Calibration requires:
- Few-shot examples of good vs bad reviews
- Explicit instruction to be skeptical, not supportive
- Concrete grading criteria (not "is this good?" but "does this meet criteria X?")
