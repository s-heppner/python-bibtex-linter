"""
This module implements verification of constraints or invariants.

When using the decorators, they automatically load the method below them into the `_rules` list at time
of import.
"""
from typing import Callable, TypeVar, List, Optional, Set

from bibtex_linter.parser import BibTeXEntry

# The dynamic list of known rules.
# This list gets updated when a method with the `@linter_rule` decorator gets imported.
_rules: List[Callable[[BibTeXEntry], List[str]]] = []

# For the type annotations, we define a `LINTER_RULE_TYPE` variable, which describes the type of the methods that
# define the linter rules.
LINTER_RULE_TYPE = TypeVar("LINTER_RULE_TYPE", bound=Callable[[BibTeXEntry], List[str]])


def linter_rule(entry_type: Optional[str] = None) -> Callable[[LINTER_RULE_TYPE], LINTER_RULE_TYPE]:
    """
    Decorator to mark a method defines rules to be checked by the linter for a specific entry type.

    If `entry_type` is `None`, we assume it is valid for all types.
    """
    def wrapper(func: LINTER_RULE_TYPE) -> LINTER_RULE_TYPE:
        setattr(func, "_is_invariant", True)
        setattr(func, "_entry_type", entry_type)
        _rules.append(func)
        return func
    return wrapper


def check_required_fields(entry: BibTeXEntry, fields: Set[str]) -> List[str]:
    """
    Helper function to check the existence of a set of required fields for the given entry.
    """
    existing_fields: Set[str] = set(entry.fields.keys())
    if not fields.issubset(entry.fields):
        missing = fields - existing_fields
        return [f"Entry '{entry.name}' misses the following required fields: [{', '.join(sorted(missing))}]"]
    return []


def check_required_field(entry: BibTeXEntry, field: str, explanation: str) -> List[str]:
    """
    Helper function to check the existence of one field for the given entry.
    If it does not exist, include the explanation sentence in the invariant violation text to help the user fill
    out the required field.
    """
    if field not in entry.fields.keys():
        return [f"Entry '{entry.name}' misses required field [{field}]. {explanation}"]
    return []


def check_omitted_fields(entry: BibTeXEntry, fields: Set[str]) -> List[str]:
    """
    Helper function to check the existence of a set of omitted fields for the given entry.
    """
    existing_fields: Set[str] = set(entry.fields.keys())
    omitted_fields_present = fields & existing_fields

    if omitted_fields_present:
        return [f"Entry '{entry.name}' has fields present that would be omitted in the compiled document: "
                f"[{', '.join(sorted(omitted_fields_present))}]. This could lead to a loss of information."]
    return []


def check_disallowed_fields(entry: BibTeXEntry, fields: Set[str]) -> List[str]:
    """
    Helper function to check that no disallowed fields are existing in the given entry.
    """
    existing_fields: Set[str] = set(entry.fields.keys())
    disallowed_fields_present = fields & existing_fields

    if disallowed_fields_present:
        return [f"Entry '{entry.name}' has fields present that would be omitted in the compiled document: "
                f"[{', '.join(sorted(disallowed_fields_present))}]."]
    return []


def check_disallowed_field(entry: BibTeXEntry, field: str, explanation: str) -> List[str]:
    """
    Helper function to check the existence of a disallowed one field for the given entry.
    If it does exist, include the explanation sentence in the invariant violation text to help the user understand
    why it is disallowed.
    """
    if field not in entry.fields.keys():
        return [f"Entry '{entry.name}' contains disallowed field [{field}]. {explanation}"]
    return []


def verify(entry: BibTeXEntry) -> List[str]:
    """
    Call this function to execute all imported methods that have the `invariant` decorator.

    Warning: This is basically remote code execution, so be sure to know what methods are imported!
    """
    errors = []

    for check in _rules:
        entry_type = getattr(check, "_entry_type", None)
        if entry_type is None or entry_type == entry.entry_type:
            errors.extend(check(entry))

    return errors
