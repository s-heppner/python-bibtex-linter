## IEEEtr Style
Here's my observations on the different entry types with the standard `IEEEtran.cls` style template used in some
IEEE conferences.

> [!warning]
> This is not to be confused with the built-in LaTeX `ieeetran` style

This snippet used together with the `IEEEtran.cls` file to create the citations for the observations:

```latex
\bibliographystyle{ieeetr}
\bibliography{maximal_example_refs.bib}
\nocite{*}
```

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
