# The Periodic Table of the Human Elements

*Your AI already has a definition of a human being. It just never showed it to you.*

This repository holds the canonical definitions of the **Periodic Table of the Human Elements**: the words that define what a human being is, drawn from the classical tradition — Aristotle, Boethius, Aquinas, Kant — with contemporary voices such as *Magnifica Humanitas* admitted as a second, clearly marked layer.

Each element is defined twice: once for the human reader, and once **for the AI** — an operative form meant to change how an AI regards and treats the person before it. Assembled in order, the definitions form a *personality file* a visitor can download and give to their own AI.

The website is here: https://caggio.github.io/Human-elements — it is built from the definitions in this repository on every push.

## The table

Columns are families; the number is the order of dependence. Read down a column, then across: an element may build on anything above it in its own column, or anything in columns to its left.

| Foundations | Constitution | Finitude | Transcendentals | Powers | Relationship | Action | Ends |
|---|---|---|---|---|---|---|---|
| 1 Nature | 4 Person | 9 Limit | 13 Truth | 16 Reason | 20 Relationship | 23 Vocation | 25 Destiny |
| 2 Substance | 5 Creature | 10 Need | 14 Goodness | 17 Heart | 21 Love | 24 Work | 26 Mystery |
| 3 Individual | 6 Dignity | 11 Vulnerability | 15 Beauty | 18 Freedom | 22 Communion | | |
| | 7 Soul | 12 Mortality | | 19 Desire | | | |
| | 8 Body | | | | | | |

God is not an element of this table: He is named as Creator in the framing — its source, not one of its members.

## Repository structure

- `definitions/` — one file per element (`04-person.md`), the single source of truth. Frontmatter carries number, symbol, group, status, what the entry is built from, and its bonds; the body follows the house template: short definition, the definition unfolded, what it is not, *For the AI*, bonds, sources.
- `personalities/` — named assemblies of the definitions. `basic.md` is the starting personality: the whole table, in order. Future personalities may select or override, but never rewrite the canon in place.

## Editorial model

This table has an editor. The definitions are self-consistent by design: every load-bearing term used inside a definition is itself defined in the table, in one sense, everywhere; known exceptions (such as Person's forward reference to Reason) are declared inside the entry, never hidden.

Suggestions are made one way: as **pull requests** against a definition file — a diff is the clearest suggestion there is. Nothing merges without the editor's hand. Each element page on the website links straight to its definition file, so a reader can go from reading a definition to proposing a change in a few clicks.

A suggestion with a checkable source carries the most weight; every citation in the table is verified before it stands.

## Status

The first five elements are drafted; the remaining elements are in preparation, each carrying its provisional gloss. The website's downloadable file is generated from this repository's definitions.

## License

The definitions, the personalities, and the website text are © 2026 Francesco Caggioni and are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)** — full text in [LICENSE](LICENSE), summary at https://creativecommons.org/licenses/by-sa/4.0/. Share them, adapt them, give them to your AI — with attribution, and with adaptations shared under the same terms.

The site builder in `site/` is code, and is licensed under the **MIT License** — see [LICENSE-MIT](LICENSE-MIT).

By opening a pull request, you agree that your contribution is licensed under the same terms as the part of the project it touches.
