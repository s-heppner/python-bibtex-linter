# Best Practices for the `IEEEtran` Citation Style
This document is meant as a cheatsheet for how to set up your `refs.bib` file when using the `IEEEtran` citation style.

> [!warning]
> Do not confuse the LaTeX built-in IEEE citation style (via `\bibliographystyle{IEEEtran}`) with the `ieeetr` style
> from the conference paper template `IEEEtran.cls`.

## Choosing an Entry Type
- [`@article`](#article): Referencing an article in a journal.
- [`@conference`](#conference): Referencing a conference paper.
- [`@online`](#online): Referencing something on the internet.
- [`@book`](#book): Referencing a whole book.
- [`@inbook`](#inbook): Referencing a part of a book (chapters or pages).
- [`@incollection`](#incollection): Referencing a part of a book that has its own name.
- [`@standard`](#standard): Referencing proposed or formally published standards.
- [`@misc`](#misc): Anything else that does not fit the above.

## Article
- Entry name: `@article`
- Usage: Referencing an article in a journal.
- Mandatory fields:
  - `author`: The author(s) of the article
  - `title`: The title of the article
  - `journal`: The journal where the article is published
  - `year`: The year of publication
- Optional fields:
  - `volume`: Groups all issues published in a year.
  - `number`: (sometimes called "Issue"), specific issue within a volume.
  - `pages`: On which pages is the article inside the journal
  - `month`: The month of publication
  - `note`: See special rule below
- Disallowed fields:
  - `url`: See special rule below
- Special rules:
  - `note` and `url` convention: Do not use `url`, rather format the `note` in the following pattern:
    `[ONLINE]. Available: \url{...}, Accessed: YYYY-mmm-dd`

## Conference
- Entry names: `@conference`, `@inproceedings`
- Usage: Referencing a conference paper.
- Mandatory fields:
  - `author`: The author(s) of the conference paper
  - `title`: The title of the conference paper
  - `booktitle`: The **name of the conference**
  - `publisher`: The entity publishing the proceedings (e.g., `IEEE IES`)
  - `year`: The year of publication
  - `type`: The paper type (e.g., `"Conference Paper"`)
- Optional fields:
  - `series`: For conferences published in a recurring series (e.g., "Lecture Notes in Computer Science")
  - `editor`: The people who compiled/edited the proceedings volume.
  - `volume`: If part of a multi-volume proceedings, uncommon
  - `number`: Usually the issue number in a journal. Rarely needed for conference proceedings.
  - `organization`: The body hosting the conference (e.g., `IEEE IES`), see rule below.
  - `address`: The address of the publishing entity, uncommon.
  - `month`: The month of publication
  - `pages`: The pages in the proceedings where the paper is located
  - `note`: See special rule below
- Disallowed fields:
  - `paper`: Seems to be not standard, so avoid using it
  - `url`: See special rule below
- Special rules:
  - `note` and `url` convention: Do not use `url`, rather format the `note` in the following pattern:
    `[ONLINE]. Available: \url{...}, Accessed: YYYY-mmm-dd`
  - If both `organization` and `publisher` have the exact same value, only use `publisher`.

## Online
- Entry names: `@online`, `@electronic`
- Usage: Referencing something on the internet.
- Mandatory fields
  - `author`: The author(s) of the online resource
  - `year`: The year of publication
  - `title`: The title of the online resource
  - `howpublished`: (Something like: "White paper", "Blog post", "GitHub Repository", etc.)
- Optional fields:
  - `month`: The month of publication
  - `organization`: The publishing organization, see rule below
  - `address`: The address of the `organization`, uncommon.
  - `note`: See special rule below
- Disallowed fields:
  - `url`: See special rule below
- Special rules:
  - `note` and `url` convention: Do not use `url`, rather format the `note` in the following pattern:
    `[ONLINE]. Available: \url{...}, Accessed: YYYY-mmm-dd`
  - If `organization` and `author` are the same, only use `author`

## Book
- Entry name: `@book`
- Usage: Referencing a whole book.
- Mandatory fields:
  - `author`: The author(s) of the book
  - `title`: The title of the book
  - `publisher`: The publisher of the book
  - `year`: The year of publication
- Optional fields:
  - `edition`: Edition of the book
  - `series`: Name of the series, if the book is part of one
  - `editor`: Editor of the book
  - `address`: Address of the `publisher`, uncommon
  - `month`:  Month of publication
  - `volume`: Volume if part of a book series, if existing
  - `number`: Number/Issue of the book series, if existing
  - `note`: See special rule below
- Disallowed fields:
  - `url`: See special rule below
- Special rules:
  - `note` and `url` convention: Do not use `url`, rather format the `note` in the following pattern:
    `[ONLINE]. Available: \url{...}, Accessed: YYYY-mmm-dd`
  - If `editor` and `publisher` are the same, only use `publisher`.

## InBook
- Entry name: `@inbook`
- Usage: Referencing a part of a book (chapters or pages).
- Mandatory fields:
  - `author`: Author(s) of the referred part of the book
  - `title`: Title of the book
  - `publisher`: Publisher of the book
  - `year`: Year of publication
- Optional fields:
  - `edition`: Edition of the book
  - `series`: Series of the book, if existing
  - `address`: Address of the publisher, uncommon
  - `month`: Month of publciation
  - `volume`: Volume, if the book is part of a series
  - `number`: Number/Issue, if the book is part of a series
  - `type`: Should be one of: "Chapter", "Section", "Appendix", "Part" or similar
  - `chapter`: Chapter number of the referenced part of the book, if applicable
  - `pages`: Pages of the referenced part in the book, if applicable
  - `note`: See special rule below
- Disallowed fields:
  - `url`: See special rule below
  - `editor`: Field is not rendered
- Special rules:
  - `note` and `url` convention: Do not use `url`, rather format the `note` in the following pattern:
    `[ONLINE]. Available: \url{...}, Accessed: YYYY-mmm-dd`

## InCollection
- Entry name: `@incollection`
- Usage: Referencing a part of a book that has its own name.
- Mandatory fields:
  - `author`: Author(s) of the referenced part
  - `title`:  Title of the referenced part
  - `booktitle`: Title of the book/collection the referenced part is a part of
  - `publisher`: Publisher of the book/collection the referenced part is a part of
  - `year`: Year of publication
- Optional fields:
  - `edition`: Edition of the book/collection the referenced part is a part of
  - `series`: Series of the book/collection the referenced part is a part of, if existing
  - `editor`: Editor of the book/collection the referenced part is a part of, if existing
  - `address`: Address of the `publisher`
  - `month`: Month of publication
  - `chapter`: Chapter of the referenced part in the book/collection, if applicable
  - `pages`: Pages of the referenced part in the book/collection, if applicable
  - `note`: See special rule below
- Disallowed fields:
  - `url`: See special rule below
  - `type`: Disallowed, since if it was set to (Article, Paper, etc.), we should use the proper entry type instead.)
- Special rules:
  - `note` and `url` convention: Do not use `url`, rather format the `note` in the following pattern:
    `[ONLINE]. Available: \url{...}, Accessed: YYYY-mmm-dd`
  - If `editor` and `publisher` are the same, use `publisher`.

## Standard
- Entry name: `@standard`
- Usage: Referencing proposed or formally published standards.
- Mandatory fields:
  - `title`: Title of the standard
  - `organization`: The issuing body or standards organization
  - `type`: One of: Standard, Technical Report, Recommendation, Specification, Guideline, Draft Standard, etc.
  - `number`: Number of the standard
  - `year`: Year of publication
- Optional fields:
  - `author`: Author(s) of the standard, only if differing from `organization`, see below
  - `howpublished`:  (how the standard is delivered or accessed "Online", "Print", "PDF", "Available from IEEE Xplore")
  - `revision`: Revision of the standard
  - `month`: Month of publication
  - `note`: See special rule bewlo
- Disallowed fields:
  - `url`: See special rule below
- Special rules:
  - `note` and `url` convention: Do not use `url`, rather format the `note` in the following pattern:
    `[ONLINE]. Available: \url{...}, Accessed: YYYY-mmm-dd`
  - If `author` and `organization` are the same, use `organization`

> [!note]
> I advise against using `techreport`. Rather use `standard` instead.

## Misc
- Entry name: `@misc`
- Usage: Anything else that does not fit the above.
- Mandatory fields:
  - `author`: Author(s) of the referenced object
  - `title`: Title of the referenced object
  - `howpublished`: How the referenced object is published
  - `year`: Year of publication
- Optional fields:
  - `organization`: Publishing organization, only use if not equal to `author`
  - `address`: Address of the publishing organization, uncommon 
  - `pages`: Pages, seems nonsensible to use
  - `month`: Month of publication
  - `note`: See special rule below
- Disallowed fields:
  - `url`: See special rule below
- Special rules:
  - `note` and `url` convention: Do not use `url`, rather format the `note` in the following pattern:
    `[ONLINE]. Available: \url{...}, Accessed: YYYY-mmm-dd`

> [!note]
> Try using the other entry types instead of this one, if possible.

