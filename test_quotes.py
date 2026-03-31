#!/usr/bin/env python3
"""Tests for quotes.py"""

import json
import subprocess
import sys
import unittest


class TestQuotes(unittest.TestCase):
    def run_cmd(self, *args):
        result = subprocess.run(
            [sys.executable, "quotes.py", *args],
            capture_output=True, text=True
        )
        return result

    def test_basic_output(self):
        """Test: python quotes.py prints a quote with author"""
        result = self.run_cmd()
        self.assertEqual(result.returncode, 0)
        self.assertIn("—", result.stdout)  # Author attribution
        self.assertIn('"', result.stdout)   # Quote marks

    def test_category_filter(self):
        """Test: --category filters correctly"""
        result = self.run_cmd("--category", "wisdom")
        self.assertEqual(result.returncode, 0)
        self.assertIn("[wisdom]", result.stdout)

    def test_json_output(self):
        """Test: --json outputs valid JSON"""
        result = self.run_cmd("--json")
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("text", data)
        self.assertIn("author", data)
        self.assertIn("category", data)

    def test_count(self):
        """Test: --count returns multiple quotes"""
        result = self.run_cmd("--count", "3")
        self.assertEqual(result.returncode, 0)
        # Should have multiple "—" for multiple quotes
        self.assertGreaterEqual(result.stdout.count("—"), 3)

    def test_invalid_category(self):
        """Test: invalid category shows error"""
        result = self.run_cmd("--category", "nonexistent")
        self.assertNotEqual(result.returncode, 0)

    def test_list_categories(self):
        """Test: --list-categories shows all categories"""
        result = self.run_cmd("--list-categories")
        self.assertEqual(result.returncode, 0)
        for cat in ["humor", "leadership", "motivation", "wisdom"]:
            self.assertIn(cat, result.stdout)

    def test_minimum_quotes(self):
        """Test: at least 20 quotes exist"""
        from quotes import QUOTES
        self.assertGreaterEqual(len(QUOTES), 20)

    def test_four_categories(self):
        """Test: at least 4 categories exist"""
        from quotes import CATEGORIES
        self.assertGreaterEqual(len(CATEGORIES), 4)


if __name__ == "__main__":
    unittest.main()
