# The Periodic Table of the Human Elements

*Your AI already has a definition of a human being. It just never showed it to you.*

This repository holds the canonical definitions of the **Periodic Table of the Human Elements**: twenty-two words that define what a human being is, drawn from the classical tradition — Aristotle, Boethius, Aquinas, Kant — with contemporary voices such as *Magnifica Humanitas* admitted as a second, clearly marked layer.

Each element is defined twice: once for the human reader, and once **for the AI** — an operative form meant to change how an AI regards and treats the person before it. Assembled in order, the definitions form a *personality file* a visitor can download and give to their own AI.

The companion website is here: https://muse.ai/s/the-periodic-table-of-the-human-xdf6z0pmxgfo9

## The table

Columns are families; the number is the order of dependence. Read down a column, then across: an element may build on anything above it in its own column, or anything in columns to its left.

| Foundations | Constitution | Transcendentals | Powers | Relationship | Action | Ends |
|---|---|---|---|---|---|---|
| 1 Nature | 4 Person | 9 Truth | 12 Reason | 16 Relationship | 19 Vocation | 21 Destiny |
| 2 Substance | 5 Creature | 10 Goodness | 13 Heart | 17 Love | 20 Work | 22 Mystery |
| 3 Individual | 6 Dignity | 11 Beauty | 14 Freedom | 18 Communion | | |
| | 7 Soul | | 15 Desire | | | |
| | 8 Body | | | | | |

God is not an element of this table: He is named as Creator in the framing — its source, not one of its members.

## Repository structure

- `definitions/` — one file per element (`04-person.md`), the single source of truth. Frontmatter carries number, symbol, group, status, what the entry is built from, and its bonds; the body follows the house template: short definition, the definition unfolded, what it is not, *For the AI*, bonds, sources.
- `personalities/` — named assemblies of the definitions. `basic.md` is the starting personality: the whole table, in order. Future personalities may select or override, but never rewrite the canon in place.

## Editorial model

This table has an editor. The definitions are self-consistent by design: every load-bearing term used inside a definition is itself defined in the table, in one sense, everywhere; known exceptions (such as Person's forward reference to Reason) are declared inside the entry, never hidden.

Suggestions are welcome two ways:

- **Pull requests** against a definition file — a diff is the clearest suggestion there is. Nothing merges without the editor's hand.
- **The suggestion box** on the website, for readers without a GitHub account.

A suggestion with a checkable source carries the most weight; every citation in the table is verified before it stands.

## Status

Elements 1–5 are drafted; 6–22 are in preparation, each carrying its provisional gloss. The website's downloadable file is generated from this repository's definitions.
