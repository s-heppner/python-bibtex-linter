# Plain (Numbered) Citation Style
Here are my observations using the `plain` citation style.
The following snippet was used and compiled with `lualatex`:

```latex
\bibliographystyle{plain}
\bibliography{maximal_example_refs.bib}              
\nocite{*}
```

> [!note]
> The following observations are also valid for the `alpha` and `abbrv` styles.
> They should also be valid for `unsrt` style.

# Article
Rendered fields
- author
- title
- journal
- volume
- number
- pages
- month
- year
- note

Not rendered fields
- language
- url

# Conference/InProceedings
Based on the observations below, I'd suggest to use
- `editor` as name of the conference
- `organization` as the organization e.g IEEE IES
- `publisher` as the publisher, but only one of the two if both are the same

Rendered fields
- author
- title
- editor (as "In")
- booktitle
- volume
- series
- pages
- address
- month
- year
- organization
- publisher
- note

Not rendered fields
- intype
- booktitle
- language
- number
- paper
- type
- url

# Online
Rendered fields
- author
- title
- howpublished
- month
- year
- note

Not rendered fields
- language
- organization
- address
- url

# Book
Rendered fields
- author
- title
- volume
- series
- publisher
- address
- edition
- month
- year
- note

Not rendered fields
- editor
- language
- number
- url

# InBook
Rendered fields
- author
- title
- volume
- series
- type
- chapter
- pages
- publisher
- address
- edition
- month
- year
- note

Not rendered fields
- editor
- language
- number
- url

# InCollection
Rendered fields
- author
- title
- editor
- booktitle
- volume
- series
- type
- chapter
- pages
- publisher
- address
- edition
- month
- year
- note

Not rendered fields
- language
- number
- url

# Standard
Rendered fields
- author
- title
- howpublished
- month
- year
- note

Not rendered fields
- language
- organization
- institution
- type
- number
- revision
- address
- url

# TechReport
Rendered fields
- author
- title
- type
- number
- institution
- address
- month
- year
- note

Not rendered fields
- language
- howpublished
- address
- url

# Misc
Rendered fields
- author
- title
- howpublished
- month
- year
- note

Not rendered fields
- language
- organization
- address
- pages
- url
