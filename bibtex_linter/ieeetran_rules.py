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


# LaTeX escapes of special characters that can appear in a DOI, mapped to the character they represent
_LATEX_ESCAPES = {
    r"\textasciitilde{}": "~",
    r"\textasciitilde": "~",
    r"\~{}": "~",
    r"\_": "_",
    r"\#": "#",
    r"\%": "%",
    r"\&": "&",
    r"\$": "$",
}
_LATEX_ESCAPE_PATTERN = re.compile("|".join(re.escape(escape) for escape in _LATEX_ESCAPES))


def _unescape_latex(text: str) -> str:
    """
    Replace the LaTeX escapes of special characters (e.g. `\\_`) in the given text with the characters themselves.

    :param text: The text to unescape
    :return: The text with all escaped special characters unescaped
    """
    return _LATEX_ESCAPE_PATTERN.sub(lambda match: _LATEX_ESCAPES[match.group(0)], text)


@linter_rule(entry_type=None)
def check_url_field(entry: BibTeXEntry) -> List[str]:
    """
    Check that the `url` and `doi` fields are not set, since `IEEEtran.bst` does not render them properly.
    Additionally, if the `note` field is set, check that it conforms to one of the following schemas:

    ```
    [ONLINE]. Available: \\url{...}, Accessed: YYYY-MM-DD
    doi: \\href{https://doi.org/10.xxxx/yyy}{10.xxxx/yyy}
    ```
    Note, that the backslash had to be escaped here and is only meant to be a single one.
    In the DOI form, the shown DOI must be the same as the DOI in the URL. Special characters in the shown DOI may be
    escaped (e.g. `10.1007/11574620\\_45`), since the shown DOI is typeset as normal text. Since a DOI is persistent,
    it has no access date.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    invariant_violations: List[str] = []
    for field in ("url", "doi"):
        if field in entry.fields.keys():
            invariant_violations.append(
                f"Contains the non-allowed field: [{field}]. "
                "Move the content of the field into the [note] field."
            )
    if "note" in entry.fields.keys():
        note_content: str = entry.fields["note"]
        online_pattern = r"^\[ONLINE\]\. Available: \\url\{(.+?)\}, Accessed: (\d{4}-\d{2}-\d{2})$"
        doi_pattern = r"^doi: \\href\{https://doi\.org/(10\.\d{4,9}/\S+)\}\{(\S+)\}$"
        doi_match = re.match(doi_pattern, note_content)
        is_valid_doi = doi_match is not None and doi_match.group(1) == _unescape_latex(doi_match.group(2))
        if not (re.match(online_pattern, note_content) or is_valid_doi):
            invariant_violations.append(
                "Contains a malformed field [note]. "
                "Make sure the [note] field follows one of the following patterns: "
                "'[ONLINE]. Available: \\url{...}, Accessed: YYYY-MM-DD' or "
                "'doi: \\href{https://doi.org/10.xxxx/yyy}{10.xxxx/yyy}'"
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
            "Fields [organization] and [publisher] are the same. Remove field [organization]."
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
            "Fields [organization] and [author] are the same. Remove field [organization]."
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
            "Fields [publisher] and [editor] are the same. Remove field [editor]."
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
            "Fields [editor] and [publisher] are the same. Remove field [editor]."
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
            "Fields [author] and [organization] are the same. Remove field [author]."
        )
    return invariant_violations


@linter_rule(entry_type="techreport")
def check_tech_report(entry: BibTeXEntry) -> List[str]:
    """
    Disallow the use of the techreport entry type.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    return ["Is of type 'TECHREPORT'. Please use a different entry type, such as 'STANDARD'."]


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
