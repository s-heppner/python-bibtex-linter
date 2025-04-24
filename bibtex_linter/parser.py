from typing import List, Dict
import dataclasses
import enum
import re


class EntryType(enum.Enum):
    """
    A collection of entry types that the LaTeX `IEEEtran` offers. Note that these only include what I
    need at the moment. The full list can be found at:
    https://ctan.net/macros/latex/contrib/IEEEtran/bibtex/IEEEtran_bst_HOWTO.pdf
    """
    ARTICLE = "ARTICLE"  # A typical journal article
    CONFERENCE = "CONFERENCE"  # A typical conference paper. Alias to: `IN_PROCEEDINGS`
    ONLINE = "ONLINE"  # A reference on the internet. Alias to: `ELECTRONIC`
    BOOK = "BOOK"  # Referencing a whole book
    IN_BOOK = "IN_BOOK"  # Referencing a part of a book (chapters or pages)
    IN_COLLECTION = "IN_COLLECTION"  # Referencing a part of a book that has its own name
    STANDARD = "STANDARD"  # Used for proposed or formally published standards
    TECH_REPORT = "TECH_REPORT"  # Used for technical reports, or reports about standards. Compare to `STANDARD`!
    MISC = "MISC"  # Anything else that does not fit the above

    @classmethod
    def from_string(cls, s: str) -> 'EntryType':
        """
        Get the `EntryType` from the string. Can deal with common aliases.

        :raises: KeyError, if the given string does not correspond to one of the entry types
        """
        s = s.upper()
        str_to_entry_type_map: Dict[str, "EntryType"] = {
            "ARTICLE": EntryType.ARTICLE,
            "CONFERENCE": EntryType.CONFERENCE,
            "INPROCEEDINGS": EntryType.CONFERENCE,

            "BOOK": EntryType.BOOK,
            "INBOOK": EntryType.IN_BOOK,
            "INCOLLECTION": EntryType.IN_COLLECTION,
            "STANDARD": EntryType.STANDARD,
            "TECHREPORT": EntryType.TECH_REPORT,

            "ONLINE": EntryType.ONLINE,
            "ELECTRONIC": EntryType.ONLINE,

            "MISC": EntryType.MISC,
        }
        return str_to_entry_type_map[s]


@dataclasses.dataclass
class BibTeXEntry:
    """
    An entry in a BibTeX file

    :ivar entry_type: Type of the entry (e.g. `@misc`). See `EntryType` for details
    :ivar name: Name or ID of the entry. So basically what is here: `@misc{Name_or_ID,`
    :ivar fields: Fields of the entry, as a Dict mapping the field key (e.g. `author`) to its cleaned up value.

    Note:
      The field's key is transformed via `.lower()`, so you can always expect non-capitalized characters.

    Note:
       When parsing multi-line field values, the additional white spaces are removed, but the new line characters are
       kept. For example, this:
       ```
       @misc{multiline_field,
         note = {This value
                 spans multiple
                 lines}
       }
       ```
       will be parsed to: `{"note": "This value\nspans multiple\nlines"}`. For the implementation details, check out
       the `BibTeXEntry._parse_field_value` static method.
    """
    entry_type: EntryType
    name: str
    fields: Dict[str, str]

    @classmethod
    def from_string(cls, entry_string: str) -> "BibTeXEntry":
        entry_type_string: str = entry_string.split("{")[0].lstrip("@")
        entry_type = EntryType.from_string(entry_type_string)

        name: str = entry_string.split("{")[1].split(",")[0]
        raw_fields = cls._split_fields(entry_string)
        fields: Dict[str, str] = {}
        for raw_field in raw_fields:
            raw_key, raw_value = raw_field.split("=")
            # Clean up key and value
            key = raw_key.strip(" ").lower()
            value = cls._parse_field_value(raw_value)
            fields[key] = value

        return BibTeXEntry(
            entry_type=entry_type,
            name=name,
            fields=fields,
        )

    @staticmethod
    def _split_fields(entry_string: str) -> List[str]:
        """
        Extract the list of fields from the entry_string (same input as into `from_string`)
        """
        entry_string = entry_string.strip()

        # Validate the entry starts with something like @type{ID,
        if not re.match(r"^@\w+\s*{", entry_string):
            raise KeyError(f"Invalid BibTeX entry format:\n\n{entry_string}\n\n")

        # Clean up trailing junk
        entry_string = entry_string.rstrip("}").rstrip(",\n")

        # Find the first `{` after entry type and extract what's inside
        start = entry_string.find('{')
        if start == -1:
            raise KeyError(f"Could not split the fields of the entry:\n\n{entry_string}\n\n")

        entry_string = entry_string[start + 1:]

        # Normalize comma-space-newline to comma-newline
        # It is possible to have trailing white spaces on the line `author = {{John Doe}}, \n`,
        # which we need to remove before we can split the entry into each field.
        entry_string = re.sub(r",\s*\n", ",\n", entry_string)

        raw_fields = entry_string.split(",\n")
        if raw_fields:
            raw_fields.pop(0)  # remove entry ID

        return raw_fields

    @staticmethod
    def _parse_field_value(raw_value: str) -> str:
        """
        Parse and normalize a field value.

        This will remove brackets `{}`, double brackets `{{}}`, quotation marks `"` and all additional stuff like
        commas `,` and white spaces from the field value, while leaving the value itself intact.

        Note:
          This does not change the `\\url{}` or `\\href{}{}` constructs, if they exist in the value.

        :param raw_value: The raw string of the value
        :return: The normalized value
        """
        # First we remove the trailing comma, and any spaces before and after it.
        raw_value = raw_value.strip().rstrip(',').strip()

        # If the value is in double brackets `{{`, we remove them
        if raw_value.startswith('{{') and raw_value.endswith('}}'):
            return raw_value[2:-2].strip()

        # If the value is in single brackets `{`, we remove them
        if (raw_value.startswith('{') and raw_value.endswith('}')) or \
                (raw_value.startswith('"') and raw_value.endswith('"')):
            return raw_value[1:-1].strip()

        return raw_value


def split_entries(raw_content: str) -> List[str]:
    """
    Split a file containing one or more entries into substrings containing each only one entry to prepare them for
    further parsing

    :param raw_content: Single string with one or more entries
    :return: List of substrings containing one entry each
    """
    entries = []
    brace_count = 0
    current_entry = []
    inside_entry = False

    for line in raw_content.splitlines():
        line = line.strip()
        if line.startswith('@'):
            inside_entry = True
            brace_count = 0
            current_entry = [line]
            brace_count += line.count('{') - line.count('}')
        elif inside_entry:
            current_entry.append(line)
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0:
                entries.append('\n'.join(current_entry))
                inside_entry = False

    return entries


def parse_bibtex_file(filename: str) -> List[BibTeXEntry]:
    """
    Parse a BibTeX file and return the list of parsed `BibTeXEntry`s
    """
    with open(filename, "r") as file:
        raw_entries: List[str] = split_entries(file.read())
        entries: List[BibTeXEntry] = []
        for raw_entry_string in raw_entries:
            entries.append(BibTeXEntry.from_string(raw_entry_string))
    return entries
