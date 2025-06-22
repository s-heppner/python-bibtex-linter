# python-bibtex-linter
A Python tool to parse BibTeX entries and run (custom) checks on them.

```commandline
> bibtex_linter refs.bib

Entry 'SomeBook' of type 'BOOK' failed verification:
  ❌ Invariant Violations:
    - Entry 'SomeBook' misses the following required fields: [publisher]
    - Entry 'SomeBook' has fields present that would be omitted in the compiled document: [url]. This could lead to a loss of information.
    
Found 2 invariant violations in 17 entries.
```

## Motivation
I've always assumed that I just needed to take care that my `references.bib` file was in order, that as many of the
fields of the entries in there were filled, and then I could easily use them to create standard-conforming citations in
my LaTeX documents. 
As it turns out, a lot of different citation styles omit various fields, and it's an overall mess. 
Therefore, I created this tool (in Python, since that's what I know best), that can parse the entries and then performs
arbitrary (self-defined) invariant checks on them.

In my field the most used citation style is `ieeetr` so this is how I've defined the default rules of the script.
I've written down the observations on which the rules are based [here](test/test_template/IEEEtr_observations.md).
These should not be confused with the LaTeX built-in `IEEEtran` citation style, for which I also developed rules.

It is however relatively easy to define your own [custom ruleset](#advanced-custom-rulesets), should the need arise.

## How to use:
First we need to install the tool, I recommend to use [pipx](https://github.com/pypa/pipx) for that:
```commandline
pipx install bibtex_linter
```

You can find the package on PyPI [here](https://pypi.org/project/bibtex-linter/).

### Basic Usage
Then you can call the script the following way:
```commandline
bibtex_linter path/to/refs.bib
```

The script will parse the file, perform the checks and print out the results. 

> [!note]
> As the `bibtex_linter` returns exit code `0`, if all checks have passed and `1`, if violations were found, 
> you could also use it in the CI of your LaTeX projects. 

### Defined Rulesets
Currently, the following rulesets are shipped with the `bibtex_linter`:

- `bibtex_linter path/to/refs.bib ieeetr` (default): Citation style of some IEEE conferences (needs `IEEEtran.cls`)
- `bibtex_linter path/to/refs.bib IEEEtran`: LaTeX built-in IEEE citation style (via `\bibliographystyle{IEEEtran}`)

If you want to define your own rules, see the next section on how to do this:

### Advanced: Custom Rulesets

It is also possible to define your own rules inside a Python file.

> [!warning]
> Custom rulesets are plain Python code and will be executed on your machine.
> If you wouldn't trust running `python3 my_rules.py`, you shouldn't use it with `bibtex_linter`.
> **Only use rulesets from sources you trust!**

Let's call our custom rule file `my_own_rules.py`.
Creating your own rule is as simple as:

```Python
from typing import List

from bibtex_linter.parser import BibTeXEntry
from bibtex_linter.verification import linter_rule


@linter_rule(entry_type="article")
def check_article(entry: BibTeXEntry) -> List[str]:
    """
    Check that a `BibTeXEntry` has a nonempty `author` field.

    :param entry: The BibTeXEntry
    :return: A list of string descriptions of rule violations for this entry.
    """
    if not entry.fields.get("author"):
        return [f"Entry '{entry.name}' misses the required field author!"]
    return []
```

As you can see, we created a method and designated that it is a linter rule by using the `@linter_rule` decorator.
The method needs to have a specific interface: 
It needs to take the `BibTeXEntry` to be checked as input argument, and it needs to return a List of strings explaining
the rule violations for that `BibTeXEntry`. 
If there are no rule violations, it should return an empty list.

This rule only gets executed for entries of the `article` type, as specified by the decorator argument.
If we left the `entry_type` argument empty, this check would be executed on all entries.
Read section [Entry Type](#entry-type) for some notes on how the `entry_type` is parsed to string.

For more inspiration on what you could define as your custom rules, have a look into `bibtex_linter/default_rules.py`.
After defining the rules in `my_own_rules.py`, we can execute them on a BibTeX file like this: 

```commandline
bibtex_linter path/to/refs.bib path/to/my_own_rules.py
```

Let's reiterate the warning from beforehand:

> [!warning]
> Custom rulesets are plain Python code and will be executed on your machine.
> If you wouldn't trust running `python3 my_rules.py`, you shouldn't use it with `bibtex_linter`.
> **Only use rulesets from sources you trust!**


## Definition of used Terms
If you're unfamiliar with BibTex, here's a short list of terms, so that you can better understand the output of the
`bibtex_linter`.

### Entry
An entry to the BibTeX file:
```LaTeX
@article{basic_case,
  author = {Test author},
  title = {Standard field format},
  year = {2020}
}
```

### Field
A field inside an entry, consists of a `key` and a `value`:
```LaTeX
author = {Test author},
```
In this case, `"author"` would be the `key` and `"Test author"` the `value`. 

> [!note]
> There are many different ways of wrapping the value text, from `{}` via `{{}}` or `""`.
> This tool removes these wrapping characters and only considers the text inside of them as `value`.

### Entry Type
The entry type specifies the available fields and is written behind the `@` and in front of the first `{` of an entry:
```LaTeX
@article{...}
@conference{...}
@online{...}
```

> [!note]
> Our convention is to use small letter entry types.
> This means, the [parser](bibtex_linter/parser.py) will automatically parse `@ARTICLE` to
> `BibTeXEntry.entry_type = "article"`.
> Furthermore, the parser converts some well-known aliases of `entry_types` into a standard form.
> Check the `RESOLVE_ENTRY_TYPE_ALIAS` `Dict` in the [parser.py](bibtex_linter/parser.py).
