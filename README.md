# The Periodic Table of the Human Elements

*Your AI already has a definition of a human being. It just never showed it to you.*

This repository holds the canonical definitions of the **Periodic Table of the Human Elements**: the words that define what a human being is, drawn from the classical tradition — Aristotle, Boethius, Aquinas, Kant — with contemporary voices such as *Magnifica Humanitas* admitted as a second, clearly marked layer.

These definitions stand or fall by reason; none asks to be believed on authority. But they are not traditionless. In their selection and synthesis, they reflect the Judeo-Christian understanding of the human being, in conversation with classical philosophy: a creature endowed with inviolable dignity and ordered toward truth, goodness, and love.

Each element is defined twice: once for the human reader, and once **for the AI** — an operative form meant to change how an AI regards and treats the person before it. Assembled in order, the definitions form a *personality file* a visitor can download and give to their own AI.

The website is here: https://caggio.github.io/Human-elements — it is built from the definitions in this repository on every push.

## The table

Columns are families; the number is the order of dependence. Read down a column, then across: an element may build on anything above it in its own column, or anything in columns to its left.

| Foundations | Constitution | Finitude | Transcendentals | Powers | Relationship | Action | Ends |
|---|---|---|---|---|---|---|---|
| 100 Nature | 200 Person | 300 Limit | 400 Truth | 500 Reason | 600 Relationship | 700 Vocation | 800 Destiny |
| 101 Substance | 201 Creature | 301 Need | 401 Goodness | 501 Heart | 601 Love | 701 Work | 801 Happiness |
| 102 Individual | 202 Dignity | 302 Vulnerability | 402 Beauty | 502 Freedom | 602 Communion | | 802 Mystery |
| | 203 Soul | 303 Mortality | | 503 Desire | | | |
| | 204 Body | | | | | | |

God is not an element of this table: He is named as Creator in the framing — its source, not one of its members.

## Repository structure

- `definitions/` — one file per element (`200-person.md`), the single source of truth. Frontmatter carries number, symbol, group, status, what the entry is built from, and its bonds; the body follows the house template: short definition, the definition unfolded, what it is not, *For the AI*, bonds, sources.
- `personalities/` — named assemblies of the definitions. `basic.md` is the starting personality: the whole table, in order. Future personalities may select or override, but never rewrite the canon in place.

## Editorial model

This table has an editor. The definitions are self-consistent by design: every load-bearing term used inside a definition is itself defined in the table, in one sense, everywhere; known exceptions (such as Person's forward reference to Reason) are declared inside the entry, never hidden.

Suggestions are made one way: as **pull requests** against a definition file — a diff is the clearest suggestion there is. Nothing merges without the editor's hand. Each element page on the website links straight to its definition file, so a reader can go from reading a definition to proposing a change in a few clicks.

A suggestion with a checkable source carries the most weight; every citation in the table is verified before it stands.

## Status

The first five elements are drafted; the remaining elements are in preparation, each carrying its provisional gloss. The website's downloadable file is generated from this repository's definitions.

## License

The definitions, the personalities, and the website text are © 2026 Francesco Caggioni, Marco Caggioni, Lorenzo Caggioni, Paolo Caggioni, Alessandra Negrini and are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)** — full text in [LICENSE](LICENSE), summary at https://creativecommons.org/licenses/by-sa/4.0/. Share them, adapt them, give them to your AI — with attribution, and with adaptations shared under the same terms.

The site builder in `site/` is code, and is licensed under the **MIT License** — see [LICENSE-MIT](LICENSE-MIT).

By opening a pull request, you agree that your contribution is licensed under the same terms as the part of the project it touches.
