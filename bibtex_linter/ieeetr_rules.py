from typing import List, Set

from bibtex_linter.parser import BibTeXEntry
from bibtex_linter.verification import (
    linter_rule,
    check_required_fields,
    check_omitted_fields,
)


@linter_rule(entry_type="article")
def check_article(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.ARTICLE` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "journal",
        "year",
    }
    omitted_fields: Set[str] = {
        "language",
        "url",
    }
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@linter_rule(entry_type="conference")
def check_conference(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.CONFERENCE` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "booktitle",
        "publisher",
        "year",
    }
    omitted_fields: Set[str] = {
        "intype",
        "language",
        "number",
        "paper",
        "type",
        "url",
    }
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@linter_rule(entry_type="online")
def check_online(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.ONLINE` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "howpublished",
        "year",
        "note",
    }
    omitted_fields: Set[str] = {
        "language",
        "organization",
        "address",
        "url",
    }
    if "note" not in entry.fields.keys():
        invariant_violations.append(f"Entry '{entry.name}' is of type 'online' and needs a field 'note' with the URL.")
        # Todo: In the future, we could actually check that it contains an URL
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@linter_rule(entry_type="book")
def check_book(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.BOOK` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "publisher",
        "year",
    }
    omitted_fields: Set[str] = {
        "editor",
        "language",
        "volume",
        "number",
        "url",
    }
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@linter_rule(entry_type="inbook")
def check_in_book(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.IN_BOOK` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "publisher",
        "year",
    }
    omitted_fields: Set[str] = {
        "editor",
        "language",
        "number",
        "url",
    }
    if "chapter" not in entry.fields.keys() or "pages" not in entry.fields.keys():
        invariant_violations.append(f"Entry {entry.name} needs to contain one of the "
                                    f"following fields: [chapter, pages].")
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@linter_rule(entry_type="incollection")
def check_in_collection(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.IN_COLLECTION` are there and that there are no fields present, that
    would be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "booktitle",
        "publisher",
        "year",
    }
    omitted_fields: Set[str] = {
        "language",
        "number",
        "url",
    }
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@linter_rule(entry_type="standard")
def check_standard(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.STANDARD` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "howpublished",
        "year",
        "note",
    }
    omitted_fields: Set[str] = {
        "language",
        "organization",
        "institution",
        "type",
        "number",
        "revision",
        "address",
        "url",
    }
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@linter_rule(entry_type="techreport")
def check_tech_report(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.TECH_REPORT` are there and that there are no fields present, that
    would be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "institution",
        "year",
    }
    omitted_fields: Set[str] = {
        "language",
        "howpublished",
        "url",
    }
    if "howpublished" in entry.fields.keys():
        invariant_violations.append(f"Entry {entry.name} is of type 'techreport', which does not render field "
                                    f"'howpublished'. Either use field 'institution' instead, or switch to a different "
                                    f"entry type completely.")
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@linter_rule(entry_type="misc")
def check_misc(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.MISC` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    required_fields: Set[str] = {
        "author",
        "title",
        "howpublished",
        "year",
    }
    omitted_fields: Set[str] = {
        "language",
        "organization",
        "address",
        "pages",
        "url",
    }
    invariant_violations.extend(check_required_fields(entry, required_fields))
    invariant_violations.extend(check_omitted_fields(entry, omitted_fields))
    return invariant_violations
