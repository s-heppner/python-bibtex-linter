import unittest
from typing import List, Set

from bibtex_linter.verification import check_required_fields, check_omitted_fields, verify, linter_rule
from bibtex_linter.parser import BibTeXEntry


@linter_rule(entry_type="test_entry_type")
def example_linter_rule(entry: BibTeXEntry) -> List[str]:
    violations = []
    required_fields: Set[str] = {"author", "title", "howpublished", "year"}
    omitted_fields: Set[str] = {"language", "organization", "address", "pages", "url"}
    violations.extend(check_required_fields(entry, required_fields))
    violations.extend(check_omitted_fields(entry, omitted_fields))
    return violations


class TestVerification(unittest.TestCase):
    def test_check_required_fields_missing(self) -> None:
        entry = BibTeXEntry(
            entry_type="test_entry_type",
            name="missing_fields",
            fields={"author": "Jane"}
        )
        expected = ["Entry 'missing_fields' misses the following required fields: [howpublished, title, year]"]
        actual = check_required_fields(entry, {"author", "title", "howpublished", "year"})
        self.assertEqual(expected, actual)

    def test_check_required_fields_complete(self) -> None:
        entry = BibTeXEntry(
            entry_type="test_entry_type",
            name="complete",
            fields={"author": "Jane", "title": "Work", "howpublished": "Online", "year": "2020"}
        )
        self.assertEqual([], check_required_fields(entry, {"author", "title", "howpublished", "year"}))

    def test_check_omitted_fields_present(self) -> None:
        entry = BibTeXEntry(
            entry_type="test_entry_type",
            name="omit_test",
            fields={"author": "Jane", "language": "en", "url": "example.com"}
        )
        expected = [
            "Entry 'omit_test' has fields present that would be omitted in the compiled document: "
            "[language, url]. This could lead to a loss of information."
        ]
        actual = check_omitted_fields(entry, {"language", "organization", "address", "pages", "url"})
        self.assertEqual(expected, actual)

    def test_check_omitted_fields_absent(self) -> None:
        entry = BibTeXEntry(
            entry_type="test_entry_type",
            name="omit_ok",
            fields={"author": "Jane", "title": "Work"}
        )
        self.assertEqual([], check_omitted_fields(entry, {"url"}))

    def test_verify_combined_rule(self) -> None:
        entry = BibTeXEntry(
            entry_type="test_entry_type",
            name="bad_entry",
            fields={"author": "Jane", "url": "http://example.org"}
        )
        expected = [
            "Entry 'bad_entry' misses the following required fields: [howpublished, title, year]",
            "Entry 'bad_entry' has fields present that would be omitted in the compiled document: [url]. "
            "This could lead to a loss of information."
        ]
        actual = verify(entry)
        self.assertEqual(expected, actual)

    def test_verify_skips_different_entry_type(self) -> None:
        entry = BibTeXEntry(
            entry_type="unrelated_type",  # does not match the rule's "test_entry_type"
            name="skipped_entry",
            fields={"author": "Someone", "url": "http://example.org"}
        )
        actual = verify(entry)
        expected: List[str] = []  # No rules should apply
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
