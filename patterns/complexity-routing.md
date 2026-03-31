# Pattern: Complexity-Based Routing

## Problem
Running every task through the full five-layer pipeline wastes resources on simple tasks and under-serves complex ones.

## Solution
Assess task complexity upfront and route through the appropriate subset of layers.

## Routing Table
| Complexity | Signal | Pipeline |
|------------|--------|----------|
| **Simple** | Bug fix, typo, <50 lines | Execution → Evaluation |
| **Medium** | New feature, refactor | Spec → Execution → Evaluation |
| **Complex** | New module, architecture change | Spec → Plan (multi-sprint) → Execution → Evaluation per sprint |

## Assessment Heuristics
- Number of files likely touched
- Whether new architecture decisions are needed
- Whether existing tests cover the change area
- Ambiguity in the task description

## Key Rule
When in doubt, route one level up. Under-routing (treating complex as simple) causes more damage than over-routing (treating simple as medium).
