# APA Citation Style
Here are my observations using the `apalike` citation style.
The following snippet was used and compiled with `lualatex`:

```latex
\bibliographystyle{apalike}
\bibliography{maximal_example_refs.bib}              
\nocite{*}
```

# Article
Rendered fields
- author
- year
- title
- journal
- volume
- number
- pages
- note

Not rendered fields
- language
- month
- url

# Conference/InProceedings
Rendered fields
- author
- year
- title
- editor
- booktitle
- volume
- series
- pages
- address
- organization
- publisher
- note

Not rendered fields
- intype
- language
- number
- month
- paper
- type
- url

# Online
Rendered fields
- author
- year
- title
- howpublished
- note

Not rendered fields
- language
- organization
- address
- url
- month

# Book
Rendered fields
- author
- year
- title
- volume
- series
- publisher
- address
- organization
- publisher
- note

Not rendered fields
- editor
- language
- edition
- month
- number
- url

# InBook
Rendered fields
- author
- year
- title
- volume
- series
- type
- chapter
- pages
- publisher
- address
- edition
- note

Not rendered fields
- editor
- language
- month
- number
- url

# InCollection
Rendered fields
- author
- year
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
- note

Not rendered fields
- language
- month
- number
- chapter
- url

# Standard
Rendered fields
- author
- year
- title
- howpublished
- note

Not rendered fields
- language
- institution
- address
- number
- type
- month
- url

# TechReport
Rendered fields
- author
- year
- title
- type
- number
- institution
- address 
- note

Not rendered fields
- language
- howpublished
- month
- url

# Misc
Rendered fields
- author
- year
- title
- howpublished
- note

Not rendered fields
- language
- organization
- address
- pages
- month
- url
