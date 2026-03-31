# Pattern: Harness Evolution

## Problem
Harness components encode assumptions about model limitations. As models improve, these assumptions go stale, and the harness becomes unnecessary overhead.

## Solution
Periodically re-examine each harness component. Strip away what's no longer load-bearing. Add new components for capabilities that are now within reach.

## Anthropic's Example
- **Opus 4.5**: Required sprint decomposition + context resets
- **Opus 4.6**: Neither needed — model handled long tasks natively

> *"Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing."*

## Practice
1. List every component in your harness
2. For each: "What model limitation does this compensate for?"
3. Test: remove it, run the same task, compare quality
4. If quality holds: remove it permanently
5. If quality drops: keep it, but flag for re-evaluation on next model upgrade

## Design Implication
Every phase in Super Harness is toggleable (`--no-spec`, `--no-review`, `--sprint single`). This isn't just convenience — it's a structural commitment to evolution.
