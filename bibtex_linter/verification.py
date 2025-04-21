"""
This module implements verification of constraints or invariants.

When using the decorators, they automatically load the method below them into the `_constraint_functions` list at time
of import.

To use this, you can define your own rules:

```Python
from bibtex_linter.verification import invariant, invariant_for
from bibtex_linter.parser import BibTeXEntry, EntryType

@invariant(EntryType.ONLINE)
def online_must_have_url(entry: BibTeXEntry) -> List[str]:
    if "url" in entry.fields:
        return []
    return ["ONLINE entries must include a URL"]
```

As you can see, the parameter should always be the entry to check, the output should always be a `List[str]`, where
each string is descriptive explanation of a found issue. If no issues are found, the check should return an empty list.
"""
from typing import Callable, Tuple, List, Optional

from bibtex_linter.parser import BibTeXEntry, EntryType

_invariants: List[Callable] = []

def invariant(entry_type: Optional[EntryType] = None) -> Callable:
    """
    Decorator to mark a constraint for a specific entry type.

    If `entry_type` is `None`, we assume it is valid for all types.
    """
    def wrapper(func: Callable[[BibTeXEntry], List[Tuple[bool, str]]]) -> Callable:
        setattr(func, "_is_invariant", True)
        setattr(func, "_entry_type", entry_type)
        _invariants.append(func)
        return func
    return wrapper


def verify(entry: BibTeXEntry) -> List[str]:
    errors = []

    for check in _invariants:
        entry_type = getattr(check, "_entry_type", None)
        if entry_type is None or entry_type == entry.entry_type:
            errors.extend(check(entry))

    return errors
