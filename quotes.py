#!/usr/bin/env python3
"""Random Quote Generator — Super Harness Demo"""

import argparse
import json
import random
import sys

QUOTES = [
    # Motivation
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "motivation"},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "category": "motivation"},
    {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "category": "motivation"},
    {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "motivation"},
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "category": "motivation"},
    # Wisdom
    {"text": "The only true wisdom is in knowing you know nothing.", "author": "Socrates", "category": "wisdom"},
    {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "category": "wisdom"},
    {"text": "Knowledge speaks, but wisdom listens.", "author": "Jimi Hendrix", "category": "wisdom"},
    {"text": "The unexamined life is not worth living.", "author": "Socrates", "category": "wisdom"},
    {"text": "Turn your wounds into wisdom.", "author": "Oprah Winfrey", "category": "wisdom"},
    # Humor
    {"text": "I'm not superstitious, but I am a little stitious.", "author": "Michael Scott", "category": "humor"},
    {"text": "Behind every great man is a woman rolling her eyes.", "author": "Jim Carrey", "category": "humor"},
    {"text": "I used to think I was indecisive. But now I'm not so sure.", "author": "Tommy Cooper", "category": "humor"},
    {"text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb", "category": "humor"},
    {"text": "I have not failed. I've just found 10,000 ways that won't work.", "author": "Thomas Edison", "category": "humor"},
    # Leadership
    {"text": "A leader is one who knows the way, goes the way, and shows the way.", "author": "John C. Maxwell", "category": "leadership"},
    {"text": "The greatest leader is not the one who does the greatest things, but the one who gets people to do the greatest things.", "author": "Ronald Reagan", "category": "leadership"},
    {"text": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs", "category": "leadership"},
    {"text": "Before you are a leader, success is all about growing yourself. When you become a leader, success is all about growing others.", "author": "Jack Welch", "category": "leadership"},
    {"text": "Management is doing things right; leadership is doing the right things.", "author": "Peter Drucker", "category": "leadership"},
]

CATEGORIES = sorted(set(q["category"] for q in QUOTES))


def get_quotes(category=None, count=1):
    """Get random quotes, optionally filtered by category."""
    pool = QUOTES
    if category:
        pool = [q for q in QUOTES if q["category"] == category]
        if not pool:
            print(f"Error: Unknown category '{category}'. Available: {', '.join(CATEGORIES)}", file=sys.stderr)
            sys.exit(1)
    
    count = min(count, len(pool))
    return random.sample(pool, count)


def format_quote(quote, as_json=False):
    """Format a single quote for display."""
    if as_json:
        return json.dumps(quote, ensure_ascii=False, indent=2)
    return f'"{quote["text"]}"\n  — {quote["author"]} [{quote["category"]}]'


def main():
    parser = argparse.ArgumentParser(description="Random Quote Generator 🔱")
    parser.add_argument("--category", "-c", choices=CATEGORIES, help="Filter by category")
    parser.add_argument("--count", "-n", type=int, default=1, help="Number of quotes (default: 1)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--list-categories", "-l", action="store_true", help="List available categories")
    args = parser.parse_args()

    if args.list_categories:
        print("Available categories:", ", ".join(CATEGORIES))
        return

    quotes = get_quotes(category=args.category, count=args.count)

    if args.json:
        if len(quotes) == 1:
            print(format_quote(quotes[0], as_json=True))
        else:
            print(json.dumps(quotes, ensure_ascii=False, indent=2))
    else:
        for i, q in enumerate(quotes):
            if i > 0:
                print()
            print(format_quote(q))


if __name__ == "__main__":
    main()
