from typing import List, Set
import argparse

from bibtex_linter.verification import invariant, verify
from bibtex_linter.parser import BibTeXEntry, EntryType, parse_bibtex_file


def _check_required_fields(entry: BibTeXEntry, fields: Set[str]) -> List[str]:
    """
    Internal function to check the existence of a set of required fields for the given entry.
    """
    existing_fields: Set[str] = set(entry.fields.keys())
    if not fields.issubset(entry.fields):
        missing = fields - existing_fields
        return [f"Entry '{entry.name}' misses the following required fields: [{', '.join(sorted(missing))}]"]
    return []


def _check_omitted_fields(entry: BibTeXEntry, fields: Set[str]) -> List[str]:
    """
    Internal function to check the existence of a set of omitted fields for the given entry.
    """
    existing_fields: Set[str] = set(entry.fields.keys())
    omitted_fields_present = fields & existing_fields

    if omitted_fields_present:
        return [f"Entry '{entry.name}' has fields present that would be omitted in the compiled document: "
                f"[{', '.join(sorted(omitted_fields_present))}]. This could lead to a loss of information."]
    return []

@invariant(entry_type=EntryType.ARTICLE)
def check_article(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.ARTICLE` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
        "number",
        "url",
    }
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@invariant(entry_type=EntryType.CONFERENCE)
def check_conference(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.CONFERENCE` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@invariant(entry_type=EntryType.ONLINE)
def check_online(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.ONLINE` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
    if not "note" in entry.fields.keys():
        invariant_violations.append(f"Entry '{entry.name}' is of type 'online' and needs a field 'note' with the URL.")
        # Todo: In the future, we could actually check that it contains an URL
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@invariant(entry_type=EntryType.BOOK)
def check_book(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.BOOK` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@invariant(entry_type=EntryType.IN_BOOK)
def check_in_book(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.IN_BOOK` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
    if not "chapter" in entry.fields.keys() or not "pages" in entry.fields.keys():
        invariant_violations.append(f"Entry {entry.name} needs to contain one of the "
                                    f"following fields: [chapter, pages].")
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@invariant(entry_type=EntryType.IN_COLLECTION)
def check_in_collection(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.IN_COLLECTION` are there and that there are no fields present, that
    would be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@invariant(entry_type=EntryType.STANDARD)
def check_standard(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.STANDARD` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@invariant(entry_type=EntryType.TECH_REPORT)
def check_tech_report(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.TECH_REPORT` are there and that there are no fields present, that
    would be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


@invariant(entry_type=EntryType.MISC)
def check_misc(entry: BibTeXEntry) -> List[str]:
    """
    Check that the required fields for `EntryType.MISC` are there and that there are no fields present, that would
    be omitted in the final compiled LaTeX documents.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of violations of the invariant.
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
    invariant_violations.extend(_check_required_fields(entry, required_fields))
    invariant_violations.extend(_check_omitted_fields(entry, omitted_fields))
    return invariant_violations


def main():
    parser = argparse.ArgumentParser(description="Verify a .bib file for consistency.")
    parser.add_argument("filepath", type=str, help="Path to the .bib file to verify")

    args = parser.parse_args()

    entries: List[BibTeXEntry] = parse_bibtex_file(args.filepath)
    had_violations = False
    total_number_of_violations: int = 0

    for entry in entries:
        violations: List[str] = verify(entry)
        total_number_of_violations += len(violations)
        if violations:
            had_violations = True
            print(f"\nEntry '{entry.name}' of type '{entry.entry_type.name}' failed verification:")
            print("  ❌ Invariant Violations:")
            for issue in violations:
                print(f"    - {issue}")

    print(f"\n\nFound {total_number_of_violations} invariant violations in {len(entries)} entries.")

    if not had_violations:
        print("All entries passed verification.")

if __name__ == "__main__":
    main()
