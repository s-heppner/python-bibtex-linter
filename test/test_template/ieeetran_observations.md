# IEEEtran Citation Style
Here are my observations using the `ieeetran` citation style.
The following snippet was used and compiled with `lualatex`:

```latex
\bibliographystyle{IEEEtran}
\bibliography{maximal_example_refs.bib}              
\nocite{*}
```

# Special Rules
- if an `url`-field is present, we raise an error. We rather expect to use a note field with the following schema: 
  `[ONLINE]. Available: \url{}, Accessed: YYYY-mm-dd`.


# Article
An article in a journal.

Volume vs number:
- `volume`: Groups all issues published in a year.
- `number`: (or Issue) – Specific issue within a volume.
- some journals don’t use issue numbers, only volumes.
- Online-only or open access journals may skip both .

Based on the observations below, we define the following rules:
- Mandatory fields
  - author
  - title
  - journal
  - year
- Optional fields
  - volume
  - number
  - pages
  - month
- Disallowed fields:
  - url
- Special rules (see above)
  - `note` and `url` (see above)

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
- url

Not rendered fields
- language

# Conference/InProceedings
A conference article

Based on the observations below, we define the following rules:
- Mandatory fields:
  - author
  - title
  - booktitle
  - publisher
  - year
  - type
- Optional fields:
  - series
  - editor
  - volume
  - number
  - organization
  - address
  - month
  - pages
  - note
- Not allowed fields:
  - paper
  - url
- Special Rules:
  - If both `organization` and `publisher` have the exact same value, only use `publisher`.
  - `note` and `url` (see above)

Rendered fields
- author
- title
- intype (Not really standard, avoid using)
- booktitle (Name of the conference)
- series (For conferences published in a recurring series (e.g., Lecture Notes in Computer Science), optional)
- editor (The people who compiled/edited the proceedings volume. Optional)
- volume (If part of a multi-volume proceedings (e.g., Volume 2 of a conference series), uncommon, optional.)
- number (Usually the issue number in a journal. Rarely needed for conference proceedings, optional)
- organization (The body hosting the conference)
- address (The people who compiled/edited the proceedings volume, optional.)
- publisher (The company that published the proceedings (e.g., IEEE Press, Springer).)
- month
- year
- type (Describes the type of report/publication (e.g., “Conference Paper”))
- paper (Not standard, avoid using)
- pages
- note
- url

Not rendered fields
- language

# Online/Electronic
A reference on the internet.

Based on the observations below, we define the following rules:
- Mandatory fields
  - author
  - year
  - title
  - howpublished (Something like: "White paper", "Blog post", "GitHub Repository", etc.)
- Optional fields:
  - month
  - organization
  - address
  - note
- Disallowed fields:
  - url
- Special rules:
  - `note` and `url` (see above)
  - If `organization` and `author` are the same, only use `author`

Rendered fields
- author
- year
- month
- title
- howpublished
- organization
- address
- note
- url

Not rendered fields
- language

# Book
Referencing a whole book.

Based on the observations below, we define the following rules:
- Mandatory fields:
  - author
  - title
  - publisher
  - year
- Optional fields:
  - edition
  - series
  - editor
  - address
  - month
  - volume
  - number
  - note
- Disallowed fields:
  - url
- Special rules:
  - `note` and `url` (see above)
  - If `editor` and `publisher` are the same, only use `publisher`.

Rendered fields
- author
- title
- edition
- series
- editor
- address
- publisher
- month
- year
- volume
- number
- note
- url

Not rendered fields
- language

# InBook
Referencing a part of a book (chapters or pages).

Based on the observations below, we define the following rules:
- Mandatory fields:
  - author
  - title (of the book)
  - publisher
  - year
- Optional fields:
  - edition
  - series
  - address
  - month
  - volume
  - number
  - type (One of: "Chapter", "Section", "Appendix", "Part")
  - chapter
  - pages
  - note
- Disallowed fields:
  - url
  - editor (not rendered)
- Special rules:
  - `note` and `url` (see above)

Rendered fields
- author
- title
- edition
- series
- address
- publisher
- month
- year
- volume
- number
- type
- chapter
- pages
- note
- url

Not rendered fields
- editor
- language

# InCollection
Referencing a part of a book that has its own name.

Based on the observations below, we define the following rules:
- Mandatory fields:
  - author
  - title
  - booktitle
  - publisher
  - year
- Optional fields:
  - edition
  - series
  - editor
  - address
  - month
  - chapter
  - pages
  - note
- Disallowed fields:
  - url
  - type (Since if it was set to (Article, Paper, Essay etc.), we should use ARTICLE or CONFERENCE instead.)
- Special rules:
  - `note` and `url` (see above)
  - If `editor` and `publisher` are the same, use `publisher`.

Rendered fields
- author
- title
- booktitle
- edition
- series
- editor
- address
- publisher
- month
- year
- volume
- number
- type
- chapter
- pages
- note
- url

Not rendered fields
- language

# Standard
Used for proposed or formally published standards.

Based on the observations below, we define the following rules:
- Mandatory fields:
  - title
  - organization (The issuing body or standards organization)
  - type (Standard, Technical Report, Recommendation, Specification, Guideline, Draft Standard)
  - number
  - year
- Optional fields:
  - author
  - howpublished (how the standard is delivered or accessed "Online", "Print", "PDF", "Available from IEEE Xplore")
  - revision
  - month
  - note
- Disallowed fields:
  - url
- Special rules:
  - `note` and `url` (see above)
  - If `author` and `organization` are the same, use `organization`

Rendered fields
- author
- title
- howpublished
- organization
- type
- number
- revision
- month
- year
- note
- url

Not rendered fields
- language
- institution
- address

# TechReport
Used for technical reports, or reports about standards. Not to be confused with 
[standard](#standard).

> [!note]
> I advise against using `techreport`. Rather use `standard` instead.

Rendered fields
- author
- title
- howpublished
- institution
- address
- type
- number
- month
- year
- note
- url

Not rendered fields
- language

# Misc
Anything else that does not fit the above.

Based on the observations below, we define the following rules:
- Mandatory fields:
  - author
  - title
  - howpublished
  - year
- Optional fields:
  - organization
  - address
  - pages
  - month
  - note
- Disallowed fields:
  - url
- Special rules:
  - `note` and `url` (see above)

> [!note]
> Try using the other entry types instead of this one, if possible.

Rendered fields
- author
- title
- howpublished
- organization
- address
- pages
- month
- year
- note
- url

Not rendered fields
- language
