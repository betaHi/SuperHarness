# Implementation Notes

## Files Created
- `quotes.py` — Main CLI utility (80 lines)
- `test_quotes.py` — 8 unit tests

## Key Decisions
- Single file design for simplicity (no package structure needed)
- 20 quotes across 4 categories (motivation, wisdom, humor, leadership)
- `argparse` for CLI parsing — stdlib, no deps
- `random.sample()` for count > 1 to avoid duplicates
- Error handling: invalid category exits with helpful message

## How to Test
```bash
python quotes.py                      # Random quote
python quotes.py -c wisdom            # Filtered
python quotes.py -j                   # JSON output
python quotes.py -n 3                 # Multiple
python test_quotes.py                 # Run tests
```

## Known Limitations
- Quote database is hardcoded (V2: load from file/API)
- No deduplication across multiple runs
- No i18n support
