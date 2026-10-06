# Vector- en functieruimten — slides

Quarto sources for the course slides, in `slides/H*.qmd`. The same sources render two ways:

- **Website**: HTML pages in `docs/`, published via GitHub Pages. Configured in `_quarto.yml`.
- **Presentations**: reveal.js decks in `_presentations/` (not committed). Configured in the
  Quarto profile `_quarto-revealjs.yml`.

The `.qmd` front matter has no `format:` block, so it never needs editing to switch between the two.
The LaTeX macros shared by all chapters live in `slides/_macros.qmd`, which every chapter includes.

## Usage

```bash
make site                         # website into docs/
make revealjs                     # all chapters as reveal.js decks
make revealjs CH=H3               # one chapter (CH="H3 H4" for several)
make revealjs CH=H3 THEME=night   # another reveal.js theme
make preview CH=H3                # live preview in the browser
make clean                        # remove _presentations/ (keeps the KaTeX cache)
```

Requires `quarto` on the `PATH`, or `make ... QUARTO=/path/to/quarto`.

Implementation notes are in the comments of the `Makefile`, `_quarto-revealjs.yml` and `tools/`.
