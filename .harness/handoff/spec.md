# Spec: Random Quote Generator

## Overview
A Python CLI utility that generates random inspiring quotes with proper author attribution. Lightweight, no external dependencies, easily extensible quote database.

## Scope
**In scope:**
- CLI tool with `python quotes.py` invocation
- Built-in quote database (20+ quotes)
- Random quote selection
- Author attribution display
- Category filtering (optional flag)
- JSON output mode (optional flag)

**Out of scope:**
- Web UI
- External API integration
- Database storage

## Technical Design
- Single Python file (`quotes.py`) for simplicity
- Quote data stored as list of dicts: `{"text": "...", "author": "...", "category": "..."}`
- `argparse` for CLI argument parsing
- `random.choice()` for selection
- Categories: motivation, wisdom, humor, leadership

## Files to Create
- `quotes.py` — Main utility
- `test_quotes.py` — Basic tests

## Acceptance Criteria
1. `python quotes.py` prints a random quote with author
2. `python quotes.py --category wisdom` filters by category
3. `python quotes.py --json` outputs JSON format
4. `python quotes.py --count 3` shows multiple quotes
5. Contains at least 20 quotes across 4 categories
6. `python test_quotes.py` passes all tests
