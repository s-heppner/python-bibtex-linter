import unittest
from unittest import mock
from typing import List, Set

from bibtex_linter import verification
from bibtex_linter.verification import check_required_fields, check_omitted_fields, verify, linter_rule
from bibtex_linter.parser import BibTeXEntry
from bibtex_linter.ieeetran_rules import check_url_field


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
        expected = ["Misses the following required fields: [howpublished, title, year]"]
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
            "Has fields present that would be omitted in the compiled document: "
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
            "Misses the following required fields: [howpublished, title, year]",
            "Has fields present that would be omitted in the compiled document: [url]. "
            "This could lead to a loss of information."
        ]
        # Only check the rule defined here, not the ones registered by importing a ruleset
        with mock.patch.object(verification, "_rules", [example_linter_rule]):
            actual = verify(entry)
        self.assertEqual(expected, actual)

    def test_verify_skips_different_entry_type(self) -> None:
        entry = BibTeXEntry(
            entry_type="unrelated_type",  # does not match the rule's "test_entry_type"
            name="skipped_entry",
            fields={"author": "Someone", "url": "http://example.org"}
        )
        with mock.patch.object(verification, "_rules", [example_linter_rule]):
            actual = verify(entry)
        expected: List[str] = []  # No rules should apply
        self.assertEqual(expected, actual)


class TestIEEEtranUrlField(unittest.TestCase):
    MALFORMED_NOTE = (
        "Contains a malformed field [note]. "
        "Make sure the [note] field follows one of the following patterns: "
        "'[ONLINE]. Available: \\url{...}, Accessed: YYYY-MM-DD' or "
        "'doi: \\href{https://doi.org/10.xxxx/yyy}{10.xxxx/yyy}'"
    )

    def test_online_note_valid(self) -> None:
        entry = BibTeXEntry(
            entry_type="misc",
            name="online_note",
            fields={"note": "[ONLINE]. Available: \\url{https://example.com}, Accessed: 2025-01-01"}
        )
        self.assertEqual([], check_url_field(entry))

    def test_doi_note_valid(self) -> None:
        entry = BibTeXEntry(
            entry_type="article",
            name="doi_note",
            fields={"note": "doi: \\href{https://doi.org/10.1109/TPAMI.2008.12}{10.1109/TPAMI.2008.12}"}
        )
        self.assertEqual([], check_url_field(entry))

    def test_doi_note_mismatching_doi(self) -> None:
        entry = BibTeXEntry(
            entry_type="article",
            name="doi_mismatch",
            fields={"note": "doi: \\href{https://doi.org/10.1109/TPAMI.2008.12}{10.1109/TPAMI.2008.13}"}
        )
        self.assertEqual([self.MALFORMED_NOTE], check_url_field(entry))

    def test_doi_note_unescaped_underscore(self) -> None:
        entry = BibTeXEntry(
            entry_type="incollection",
            name="doi_underscore",
            fields={"note": "doi: \\href{https://doi.org/10.1007/11574620_45}{10.1007/11574620_45}"}
        )
        self.assertEqual([], check_url_field(entry))

    def test_doi_note_escaped_special_characters(self) -> None:
        for url_doi, shown_doi in (
            ("10.1007/11574620_45", "10.1007/11574620\\_45"),
            ("10.1007/978-3-642-25073-6_18", "10.1007/978-3-642-25073-6\\_18"),
            ("10.1234/a#b%c&d$e", "10.1234/a\\#b\\%c\\&d\\$e"),
            ("10.1234/a~b", "10.1234/a\\textasciitilde{}b"),
            ("10.1234/a~b", "10.1234/a\\~{}b"),
        ):
            with self.subTest(shown_doi=shown_doi):
                entry = BibTeXEntry(
                    entry_type="incollection",
                    name="doi_escaped",
                    fields={"note": f"doi: \\href{{https://doi.org/{url_doi}}}{{{shown_doi}}}"}
                )
                self.assertEqual([], check_url_field(entry))

    def test_doi_note_escaped_mismatching_doi(self) -> None:
        entry = BibTeXEntry(
            entry_type="incollection",
            name="doi_escaped_mismatch",
            fields={"note": "doi: \\href{https://doi.org/10.1007/11574620_45}{10.1007/11574620\\_46}"}
        )
        self.assertEqual([self.MALFORMED_NOTE], check_url_field(entry))

    def test_doi_note_with_access_date(self) -> None:
        entry = BibTeXEntry(
            entry_type="article",
            name="doi_accessed",
            fields={"note": "doi: \\href{https://doi.org/10.1109/TPAMI.2008.12}{10.1109/TPAMI.2008.12}, "
                            "Accessed: 2025-01-01"}
        )
        self.assertEqual([self.MALFORMED_NOTE], check_url_field(entry))

    def test_doi_field_disallowed(self) -> None:
        entry = BibTeXEntry(
            entry_type="article",
            name="doi_field",
            fields={"doi": "10.1109/TPAMI.2008.12"}
        )
        expected = ["Contains the non-allowed field: [doi]. Move the content of the field into the [note] field."]
        self.assertEqual(expected, check_url_field(entry))


if __name__ == "__main__":
    unittest.main()
