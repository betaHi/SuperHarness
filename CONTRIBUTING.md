# Contributing to Super Harness

Thanks for your interest in contributing! Here's how to get started.

## Areas of Contribution

### High Priority
- **Real-world testing** — Run Super Harness on actual projects and report results
- **Evaluator tuning** — Improve review prompts for stricter, more useful feedback
- **Edge case handling** — Git conflicts, timeout recovery, partial completions

### Medium Priority
- **New coding agent integrations** — Beyond Claude Code and Codex
- **Sprint decomposition heuristics** — Better complexity assessment
- **Cost tracking** — Token usage reporting per phase

### Nice to Have
- **Documentation improvements** — Examples, tutorials, case studies
- **Visualization** — Pipeline progress visualization
- **Benchmarks** — Comparing solo vs harness outcomes across task types

## Development Setup

1. Clone the repo
2. Set up an agent orchestration platform (e.g., OpenClaw) or run phases manually
3. Install a coding agent (Claude Code or Codex)
4. Run `/super-harness` on a test project

## Pull Request Process

1. Fork the repo
2. Create a feature branch (`feat/your-feature`)
3. Make your changes
4. Test on at least one real coding task
5. Submit PR with description of what and why

## Code of Conduct

Be respectful. Be constructive. Ship good code.
