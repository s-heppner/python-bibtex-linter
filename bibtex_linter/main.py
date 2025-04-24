from typing import List
import argparse
import importlib.util
import sys

from bibtex_linter.verification import verify
from bibtex_linter.parser import BibTeXEntry, parse_bibtex_file


def import_from_path(file_path: str) -> None:
    """
    Import a given module using its path.
    """
    # (2025-04-24, s-heppner)
    # This is taken directly from the importlib documentation:
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    # It seems a bit cursed, but I guess as long as it works and really only used on known and safe `rules.py`...
    module_name: str = "ruleset"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not import ruleset from '{file_path}'.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a .bib file using a set of defined rules.")
    parser.add_argument("filepath", type=str, help="Path to the .bib file to verify")
    parser.add_argument("ruleset",
                        type=str,
                        nargs="?",
                        default=None,
                        help="Path to the rules.py that define the rules. If left empty, the default ruleset is used. "
                             "WARNING: Executes the Python code inside rules.py, so be sure that it's safe!")

    args = parser.parse_args()

    # Try to import the ruleset
    if args.ruleset is None:
        import bibtex_linter.default_rules
        print("Using the default ruleset.")
    else:
        print(f"Importing rules from {args.ruleset}.")
        import_from_path(args.ruleset)

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

    print(f"\n\nFound {total_number_of_violations} invariant violation(s) in {len(entries)} entries.")

    if not had_violations:
        print("All entries passed verification.")
        sys.exit(0)  # Exit as success

    sys.exit(1)  # Exit as failure


if __name__ == "__main__":
    main()
