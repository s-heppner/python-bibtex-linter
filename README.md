# python-bibtex-linter
A Python tool to parse BibTeX entries and a set of self-defined invariants (constraints) on them.

> [!warning]
> This tool is a **Work in Progress**.

## Motivation
I've always assumed that I just needed to take care that my `references.bib` file was in order, that as many of the
fields of the entries in there were filled, and then I could easily use them to create standard-conforming citations in
my LaTeX documents. 
As it turns out, a lot of different citation styles omit various fields, and it's an overall mess. 
Therefore, I created this tool (in Python, since that's what I know best), that can parse the entries and then performs
arbitrary (self-defined) invariant checks on them.

In my field the most used citation style is IEEEtran so this is how I've defined the invariants in the script.
However, I tried to make it easy to define others if the need arises.

## How to use:
First we need to install the tool, I recommend to use [pipx](https://github.com/pypa/pipx) for that:
```commandline
pipx install .
```

Then you can call the script the following way:
```commandline
bibtex_linter path/to/refs.bib
```

The script will parse the file, perform the verifications and print out the results. 

## Definition of used Terms

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

## IEEE Citations
Here's my observations on the different entry types with the standard `IEEEtran.cls` style template. 
You can find maximal examples (e.g. of all the available fields) [here](./test/test_template/maximal_example_refs.bib).
This file can also be used to generate a test bibliography to check how entries are rendered with your citation style
and template.

> [!note]
> This is not the full list of possible entry types, just the ones I deemed most important.
> The full list can be found in the 
> [offical template documentation](https://ctan.net/macros/latex/contrib/IEEEtran/bibtex/IEEEtran_bst_HOWTO.pdf).

### Article
A typical journal article.

Rendered fields:
- author
- title
- journal
- volume
- pages
- month
- year
- note

Not rendered fields:
- language
- number
- url

### InProceedings/Conference
A typical conference paper.

Rendered fields:
- author
- title
- booktitle
- editor
- volume
- series
- address
- pages
- organization
- publisher
- month
- year
- note

Not rendered fields:
- intype
- language
- number
- paper
- type
- url

### Online/Electronic
A reference on the internet.

Rendered fields:
- author
- title
- howpublished
- month
- year
- note

> [!warning]
> It is especially surprising (to me), that the `online` type does not render the URL field.
> After some research I found out that it is suggested to put the URL into the `note` field instead: 
> `note = {{Available: \url{...}, Accessed 2025-01-01}},`.

Not rendered fields
- language
- organization
- address
- url

### Book
Referencing a whole book.

Rendered fields:
- author
- title
- volume
- series
- address
- publisher
- edition
- month
- year
- note

Not rendered fields:
- editor
- language
- volume
- number
- url

### InBook
Referencing a part of a book (chapters or pages).

Rendered fields:
- author
- title 
- volume
- series
- type
- chapter
- pages
- address
- publisher
- edition
- month
- year
- note

Not rendered fields:
- editor
- language
- number
- url

### InCollection
Referencing a part of a book that has its own name.

Rendered fields:
- author
- title
- booktitle
- editor
- volume
- series
- type
- chapter
- pages
- address
- publisher
- edition
- month
- year
- note

Not rendered fields:
- language
- number
- url

### Standard
Used for proposed or formally published standards.

Rendered fields:
- author
- title
- howpublished
- month
- year
- note

Not rendered fields:
- language
- organization
- institution
- type
- number
- revision
- address
- url

### TechReport
Used for technical reports, or reports about standards. Not to be confused with 
[standard](#standard).

Rendered fields:
- author
- title 
- type
- number
- institution
- address
- month
- year
- note

> [!warning]
> I advise against using the `techreport` entry type, as it omits the `howpublished` field, which I would 
> consider mandatory. 

Not rendered fields:
- language
- howpublished
- url

### Misc
Anything else that does not fit the above.

Rendered fields:
- author
- title
- howpublished
- month
- year
- note

Not rendered fields:
- language
- organization
- address
- pages
- url
