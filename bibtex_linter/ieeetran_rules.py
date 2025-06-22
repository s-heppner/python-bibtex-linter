from typing import List, Set
import re

from bibtex_linter.parser import BibTeXEntry
from bibtex_linter.verification import (
    linter_rule,
    check_required_fields,
    check_required_field,
    check_omitted_fields,
    check_disallowed_field,
)


@linter_rule(entry_type=None)
def check_url_field(entry: BibTeXEntry) -> List[str]:
    """
    Check that the `url` field is not set.
    Additionally, if the `note` field is set, check that it conforms to the following schema:

    ```
    [ONLINE]. Available: \\url{...}, Accessed: YYYY-mmm-dd
    ```
    Note, that the backslash had to be escaped here and is only meant to be a single one.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    if "url" in entry.fields.keys():
        invariant_violations.append(
            f"Entry '{entry.name}' contains the non-allowed field: [url]. "
            f"Move the content of the field into the [note] field."
        )
    if "note" in entry.fields.keys():
        note_content: str = entry.fields["note"]
        pattern = r"^\[ONLINE\]\. Available: \\url\{(.+?)\}, Accessed: (\d{4}-\d{2}-\d{2})$"
        match = re.match(pattern, note_content)
        if not match:
            invariant_violations.append(
                f"Entry '{entry.name}' contains a malformed field [note]. "
                "Make sure the [note] field follows the following pattern: '[ONLINE]. Available: \\url{...}, "
                "Accessed: YYYY-mmm-dd'"
            )
    return invariant_violations


@linter_rule(entry_type="article")
def check_article(entry: BibTeXEntry) -> List[str]:
    """
    Check that the article entry type contains the required fields.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    invariant_violations.extend(check_required_fields(
        entry,
        fields={
            "author",
            "title",
            "journal",
            "year"
        }
    ))
    return invariant_violations


@linter_rule(entry_type="conference")
def check_conference(entry: BibTeXEntry) -> List[str]:
    """
    Check that conference entry type contains all required fields.
    Additionally, check that 'publisher' and 'organization' are not duplicates of each other.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    invariant_violations.extend(check_required_fields(
        entry,
        fields={
            "author",
            "title",
            "booktitle",
            "publisher",
            "year",
            "type",
        }
    ))
    invariant_violations.extend(check_required_field(
        entry,
        field="booktitle",
        explanation="This should be the name of the conference.",
    ))
    invariant_violations.extend(check_required_field(
        entry,
        field="publisher",
        explanation="This should be the company that published the proceedings.",
    ))
    invariant_violations.extend(check_required_field(
        entry,
        field="type",
        explanation="This should describe the type of report/publication (e.g., “Conference Paper”).",
    ))
    if entry.fields.get("organization") == entry.fields.get("publisher"):
        invariant_violations.append(
            f"Entry '{entry.name}' fields [organization] and [publisher] are the same. Remove field [organization]."
        )
    return invariant_violations


@linter_rule(entry_type="online")
def check_online(entry: BibTeXEntry) -> List[str]:
    """
    Check that online entry type contains all required fields.
    Additionally, check that 'author' and 'organization' are not duplicates of each other.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    invariant_violations.extend(check_required_fields(
        entry,
        fields={
            "author",
            "title",
            "year",
            "howpublished",
        }
    ))
    invariant_violations.extend(check_required_field(
        entry,
        field="howpublished",
        explanation="This should be something like: 'White paper', 'Blog post', 'GitHub repository', etc.",
    ))
    if entry.fields.get("organization") == entry.fields.get("author"):
        invariant_violations.append(
            f"Entry '{entry.name}' fields [organization] and [author] are the same. Remove field [organization]."
        )
    return invariant_violations


@linter_rule(entry_type="book")
def check_book(entry: BibTeXEntry) -> List[str]:
    """
    Check that book entry type contains all required fields.
    Additionally, check that 'publisher' and 'editor' are not duplicates of each other.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    invariant_violations.extend(check_required_fields(
        entry,
        fields={
            "author",
            "title",
            "year",
            "publisher",
        }
    ))
    if entry.fields.get("publisher") == entry.fields.get("editor"):
        invariant_violations.append(
            f"Entry '{entry.name}' fields [publisher] and [editor] are the same. Remove field [editor]."
        )
    return invariant_violations


@linter_rule(entry_type="inbook")
def check_in_book(entry: BibTeXEntry) -> List[str]:
    """
    Check that inbook entry type contains all required fields.
    Additionally check that the field `editor` is not present.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    invariant_violations.extend(check_required_fields(
        entry,
        fields={
            "author",
            "title",
            "year",
            "publisher",
        }
    ))
    invariant_violations.extend(check_required_field(
        entry,
        field="title",
        explanation="This should be the title of the book.",
    ))
    invariant_violations.extend(check_disallowed_field(
        entry,
        field="editor",
        explanation="This field is not rendered in IEEEtran-style.",
    ))
    return invariant_violations


@linter_rule(entry_type="incollection")
def check_in_collection(entry: BibTeXEntry) -> List[str]:
    """
    Check that incollection entry type contains all required fields.
    Additionally, check that the field `type` is not set.
    Furthermore, check that 'editor' and 'publisher' are not duplicates of each other.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    invariant_violations.extend(check_required_fields(
        entry,
        fields={
            "author",
            "title",
            "year",
            "booktitle",
            "publisher",
        }
    ))
    invariant_violations.extend(check_disallowed_field(
        entry,
        field="type",
        explanation="If this field is set to (Article, Paper, Essay etc.), you should use a different entry type."
    ))
    if entry.fields.get("editor") == entry.fields.get("publisher"):
        invariant_violations.append(
            f"Entry '{entry.name}' fields [editor] and [publisher] are the same. Remove field [editor]."
        )
    return invariant_violations


@linter_rule(entry_type="standard")
def check_standard(entry: BibTeXEntry) -> List[str]:
    """
    Check that standard entry type contains all required fields.
    Furthermore, check that 'author' and 'organization' are not duplicates of each other.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    invariant_violations.extend(check_required_fields(
        entry,
        fields={
            "title",
            "organization",
            "type",
            "number",
            "year",
        }
    ))
    invariant_violations.extend(check_required_field(
        entry,
        field="organization",
        explanation="This should be the issuing body or standards organization.",
    ))
    invariant_violations.extend(check_required_field(
        entry,
        field="type",
        explanation="This should be something like "
                    "(Standard, Technical Report, Recommendation, Specification, Guideline, Draft Standard).",
    ))
    if entry.fields.get("author") == entry.fields.get("organization"):
        invariant_violations.append(
            f"Entry '{entry.name}' fields [author] and [organization] are the same. Remove field [author]."
        )
    return invariant_violations


@linter_rule(entry_type="techreport")
def check_tech_report(entry: BibTeXEntry) -> List[str]:
    """
    Disallow the use of the techreport entry type.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    return [f"Entry '{entry.name}' is of type 'TECHREPORT'. Please use a different entry type, such as 'STANDARD'."]


@linter_rule(entry_type="misc")
def check_misc(entry: BibTeXEntry) -> List[str]:
    """
    Check that misc entry type contains all required fields.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    invariant_violations.extend(check_required_fields(
        entry,
        fields={
            "author",
            "title",
            "howpublished",
            "year",
        }
    ))
    return invariant_violations
