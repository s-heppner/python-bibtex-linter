import unittest
import os
from typing import Dict, List

from bibtex_linter.parser import BibTeXEntry, split_entries, parse_bibtex_file


class TestBibTeXEntry(unittest.TestCase):
    def test_parse_field_value(self) -> None:
        test_cases = [
            ("{John Doe}", "John Doe"),
            ("{{John Doe}}", "John Doe"),
            ('"John Doe"', "John Doe"),
            ("{{Industrial Digital Twin Association e. V.}}", "Industrial Digital Twin Association e. V."),
            ("{\\LaTeX}", "\\LaTeX"),
            ("{\\url{https://example.com}}", "\\url{https://example.com}"),
            ("   {Example Title}   ,", "Example Title"),
            ("{Multiple     Spaces}", "Multiple     Spaces"),
            ("{  Trimmed   }", "Trimmed"),
            ('"Surrounded by quotes" ,', "Surrounded by quotes"),
            ("   2020   ,", "2020"),
            ("{12345}", "12345"),
            ("{This is a {nested} value}", "This is a {nested} value"),
            ("{{This is a {{nested}} value}}", "This is a {{nested}} value"),
            ("Some plain text", "Some plain text"),
            ('"\\textit{Italicized}"', "\\textit{Italicized}"),
            ("{This value, has, commas}", "This value, has, commas"),
            ('"Quoted, with, commas"', "Quoted, with, commas"),
            ("{\\href{https://a.com}{A}}", "\\href{https://a.com}{A}"),
            ("{{\\href{https://a.com}{A}}}", "\\href{https://a.com}{A}"),
        ]

        for raw_value, expected in test_cases:
            with self.subTest(raw_value=raw_value):
                result = BibTeXEntry._parse_field_value(raw_value)
                self.assertEqual(expected, result)

    def test_split_fields_basic(self) -> None:
        entry = """@article{doe2020,
  author = {John Doe},
  title = {A Study},
  year = {2020}
}"""
        expected = [
            "  author = {John Doe}",
            "  title = {A Study}",
            "  year = {2020}"
        ]
        result = BibTeXEntry._split_fields(entry)
        self.assertEqual(expected, result)

    def test_split_fields_with_trailing_comma_and_newline(self) -> None:
        entry = """@book{smith2021,
  author = {Jane Smith},
  title = {The Book of Testing},
  year = {2021},
}"""
        expected = [
            "  author = {Jane Smith}",
            "  title = {The Book of Testing}",
            "  year = {2021}"
        ]
        result = BibTeXEntry._split_fields(entry)
        self.assertEqual(expected, result)

    def test_split_fields_multiline_values(self) -> None:
        entry = """@misc{nested2022,
  author = {{Industrial Digital Twin Association e. V.}},
  url = {https://example.com},
  note = {Line 1
          Line 2}
}"""
        expected = [
            "  author = {{Industrial Digital Twin Association e. V.}}",
            "  url = {https://example.com}",
            "  note = {Line 1\n          Line 2}"
        ]
        result = BibTeXEntry._split_fields(entry)
        self.assertEqual(expected, result)

    def test_split_fields_with_extra_whitespace(self) -> None:
        entry = ("@misc{id123,  \n    "
                 "author    =    {Someone}  , \n    "
                 "title=   {  Extra Spaces   }   , \n    "
                 "year= {2023}    }")
        expected = [
            "    author    =    {Someone}  ",
            "    title=   {  Extra Spaces   }   ",
            "    year= {2023}    "
        ]
        result = BibTeXEntry._split_fields(entry)
        self.assertEqual(expected, result)

    def test_split_fields_with_linebreak_after_entry_type(self) -> None:
        entry = """@misc
{
id456,
  author = {Spaced Out},
  title = {Linebreak test}
}"""
        expected = [
            "  author = {Spaced Out}",
            "  title = {Linebreak test}"
        ]
        result = BibTeXEntry._split_fields(entry)
        self.assertEqual(expected, result)

    def test_split_fields_missing_open_brace(self) -> None:
        entry = "article, author = {John Doe}, title = {Oops}"
        with self.assertRaises(KeyError):
            BibTeXEntry._split_fields(entry)

    def test_field_with_equals_in_value(self) -> None:
        bibtex_string = """@misc{test_entry,
          note = {This URL has equals: https://example.com/?id=123&lang=en},
        }"""
        entry = BibTeXEntry.from_string(bibtex_string)
        actual = entry.fields.get("note")
        expected = "This URL has equals: https://example.com/?id=123&lang=en"
        self.assertEqual(expected, actual)

    def test_double_braces(self) -> None:
        bibtex_string = """@misc{test_entry,
          title = {{Title with {{extra}} braces}},
        }"""
        entry = BibTeXEntry.from_string(bibtex_string)
        actual = entry.fields.get("title")
        expected = "Title with {{extra}} braces"
        self.assertEqual(expected, actual)

    def test_quoted_field(self) -> None:
        bibtex_string = """@misc{test_entry,
          author = "Jane Doe",
        }"""
        entry = BibTeXEntry.from_string(bibtex_string)
        actual = entry.fields.get("author")
        expected = "Jane Doe"
        self.assertEqual(expected, actual)

    def test_multiline_field(self) -> None:
        bibtex_string = """@misc{test_entry,
          note = {This is a
                  multi-line
                  note.},
        }"""
        entry = BibTeXEntry.from_string(bibtex_string)
        actual = entry.fields.get("note")
        expected = "This is a\n                  multi-line\n                  note."
        self.assertEqual(expected, actual)

    def test_field_with_url_and_brackets(self) -> None:
        bibtex_string = """@misc{test_entry,
          howpublished = {\\url{https://example.org/query?x=1&y=2}},
        }"""
        entry = BibTeXEntry.from_string(bibtex_string)
        actual = entry.fields.get("howpublished")
        expected = "\\url{https://example.org/query?x=1&y=2}"
        self.assertEqual(expected, actual)

    def test_empty_field_value(self) -> None:
        bibtex_string = """@misc{test_entry,
          note = ,
        }"""
        entry = BibTeXEntry.from_string(bibtex_string)
        actual = entry.fields.get("note")
        expected = ""
        self.assertEqual(expected, actual)

        bibtex_string = """@misc{test_entry,
                  note = {},
                }"""
        entry = BibTeXEntry.from_string(bibtex_string)
        actual = entry.fields.get("note")
        expected = ""
        self.assertEqual(expected, actual)

        bibtex_string = """@misc{test_entry,
                  note = {{}},
                }"""
        entry = BibTeXEntry.from_string(bibtex_string)
        actual = entry.fields.get("note")
        expected = ""
        self.assertEqual(expected, actual)


class TestSplitEntries(unittest.TestCase):
    def test_single_entry(self) -> None:
        raw = """@article{key1,
  author = {John Doe},
  title = {Example},
  year = {2020}
}"""
        entries = split_entries(raw)
        self.assertEqual(1, len(entries))
        self.assertIn("key1", entries[0])

    def test_multiple_entries(self) -> None:
        raw = """@article{key1,
  author = {John Doe},
  title = {Example 1},
  year = {2020}
}

@book{key2,
  author = {Jane Doe},
  title = {Example 2},
  year = {2021}
}"""
        entries = split_entries(raw)
        self.assertEqual(2, len(entries))
        self.assertIn("key1", entries[0])
        self.assertIn("key2", entries[1])

    def test_entry_with_nested_braces(self) -> None:
        raw = """@misc{key3,
  note = {Something with {nested} braces}
}"""
        entries = split_entries(raw)
        self.assertEqual(1, len(entries))
        self.assertIn("nested", entries[0])

    def test_entry_with_line_breaks(self) -> None:
        raw = """@online{key4,
  author = {Someone},
  title = {Line
Break},
  year = {2022}
}"""
        entries = split_entries(raw)
        self.assertEqual(1, len(entries))
        self.assertIn("Line\nBreak", entries[0])

    def test_incomplete_entry(self) -> None:
        raw = """@article{key5,
  title = {Missing closing brace}
"""
        entries = split_entries(raw)
        self.assertEqual(len(entries), 0)


class TestParseBibtexFile(unittest.TestCase):
    def test_parse_all_entries(self) -> None:
        bib_path = os.path.join(os.path.dirname(__file__), "test_refs.bib")
        entries = parse_bibtex_file(bib_path)
        self.assertEqual(17, len(entries))

        expected_types = {
            "article": 1,
            "conference": 1,
            "online": 1,
            "techreport": 1,
            "book": 1,
            "misc": 9,
            "standard": 1,
            "inbook": 1,
            "incollection": 1,
        }

        for entry_type, expected_count in expected_types.items():
            with self.subTest(entry_type=entry_type):
                actual_count = sum(1 for e in entries if e.entry_type == entry_type)
                self.assertEqual(expected_count, actual_count)

    def test_entry_fields_and_values(self) -> None:
        expected_entries: List[Dict[str, str | Dict[str, str]]] = [
            {
                "type": "article",
                "fields": {
                    "author": "Tests basic article",
                    "title": "Standard field format",
                    "year": "2020"
                }
            },
            {
                "type": "conference",
                "fields": {
                    "author": "Should map to CONFERENCE",
                    "title": "Using alias INPROCEEDINGS",
                    "year": "2021"
                }
            },
            {
                "type": "online",
                "fields": {
                    "author": "Should map to ONLINE",
                    "url": "https://example.com"
                }
            },
            {
                "type": "techreport",
                "fields": {
                    "author": "Should map to TECH_REPORT",
                    "title": "Tech report via alias"
                }
            },
            {
                "type": "book",
                "fields": {
                    "author": "Extra spaces around field and value",
                    "title": "Trimmed Title",
                    "year": "2023"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "note": "This has nested braces inside",
                    "comment": "But only outermost braces should be stripped"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "author": "Double brace test",
                    "title": "Another level of nesting"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "author": "Quoted Author",
                    "title": "Simple quoted title"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "note": "This value\nspans multiple\nlines"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "howpublished": r"\url{https://wrapped-url.com}"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "title": r"\LaTeX command in value"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "author": "Trailing Comma",
                    "title": "Should be OK"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "author": "No Trailing Comma"
                }
            },
            {
                "type": "misc",
                "fields": {
                    "author": "Newlines and spacing\neverywhere",
                    "title": "Still valid"
                }
            },
            {
                "type": "standard",
                "fields": {
                    "author": "Tests EntryType.STANDARD",
                    "title": "Formal standard ref"
                }
            },
            {
                "type": "inbook",
                "fields": {
                    "author": "Part of a book",
                    "title": "Chapter Title",
                    "booktitle": "Whole Book Title"
                }
            },
            {
                "type": "incollection",
                "fields": {
                    "author": "Self-contained part of a collection",
                    "title": "In Collection Title",
                    "booktitle": "Collection Name"
                }
            },
        ]

        bib_path = os.path.join(os.path.dirname(__file__), "test_refs.bib")
        parsed_entries = parse_bibtex_file(bib_path)

        for expected in expected_entries:
            with self.subTest(expected=expected["fields"]):
                # (2025-04-24, s-heppner)
                # We can safely ignore the mypy warning here, since we wrote the `expected_entries` this way just above.
                expected_fields: Dict[str, str] = expected["fields"]  # type: ignore
                match = next(
                    (e for e in parsed_entries if all(e.fields.get(k) == v for k, v in expected_fields.items())),
                    None
                )
                all_field_sets = [e.fields for e in parsed_entries]
                self.assertIsNotNone(
                    match,
                    f"Missing or incorrect entry for:\nExpected Fields: {expected['fields']}\n"
                    f"Parsed Entries:\n{all_field_sets}"
                )
                # (2025-04-24, s-heppner)
                # We can safely ignore the mypy warning here, since we already asserted that `match` is not `None` in
                # the line above.
                self.assertEqual(expected["type"], match.entry_type)  # type: ignore


if __name__ == "__main__":
    unittest.main()
