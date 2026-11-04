# Drafting book notes from EPUB sources

`epub_index.py` indexes DRM-free EPUB books, such as commentaries, study Bibles and catechisms, so their material can be found by Bible book and used to write the notes in `plugin/skills/bible-study/books/`. It uses only the Python standard library.

**Never commit the EPUBs or the index.** Most of these books are copyrighted. `epubs/`, `*.epub` and `.epub-index/` are git-ignored.

## 1. Add and index the books

Put DRM-free EPUBs in `epubs/`. In a Claude session, attach the files and ask Claude to index them. Then build the index:

```bash
python3 tools/epub_index.py index epubs/*.epub
```

The indexer refuses DRM-protected files (Adobe, Apple FairPlay, or encrypted content). It never tries to remove DRM. Font obfuscation isn't DRM, so files that use it are fine.

Check what's indexed:

```bash
python3 tools/epub_index.py list
```

Each work gets a short ID, the author's surname plus up to four title words (e.g. `luther-commentary-epistle-galatians`). Sections are numbered in reading order, so `luther-commentary-epistle-galatians:18` is one citable section.

## 2. Find the material for a Bible book

```bash
python3 tools/epub_index.py book joshua
```

For every indexed work this shows:

- **Sections about the book**, found from headings like "Introduction to Joshua" or "The Second Book of the Kings". When a whole work is about the book, it says so.
- **Where the book is cited**, ranked by how many references to it each section contains, e.g. `Josh. 2:18`, `Heb 11:31`, or old-style `Gen. iii. 15`.

Then read and search:

```bash
python3 tools/epub_index.py digest joshua
```

`digest` prints each work's introduction to the book (background, structure, theology, and a study Bible's overview and outline) without the Scripture text, so it can be read in one pass.

```bash
python3 tools/epub_index.py toc WORK
```

```bash
python3 tools/epub_index.py show WORK:SECTION
```

```bash
python3 tools/epub_index.py search "scarlet cord"
```

`toc` lists a work's sections, `show` prints one section, and `search` searches every work. Add `--work WORK` to search one work, or `--regex` to use a regular expression.

## 3. Write the note

Fill in the book file's template headings: Summary, Setting, Structure, Chapter by chapter, Key people, Key events, Themes, How it points to Christ, Common mix-ups, Going deeper, Q&A, and Sources. Follow `plugin/skills/bible-study/sources.md`:

- **Own words.** Summarise; never copy study Bible introductions or notes. Quote only short phrases, in quotation marks, with the author named.
- **Source order.** Scripture first, then the confessions, study Bibles, and commentaries. Every key event and theme gets chapter and verse.
- **Cite what you used** in the book's Sources section, by author, work and chapter or section heading, e.g. *Calvin, Commentary on Joshua, on chapter 2*. EPUBs rarely carry print page numbers, so mark page numbers needed for print editions as "p. ___ (to verify)".
- **Flag differences.** Where Luther or Spurgeon differ from the Reformed confessions, say so as `sources.md` describes.
- **Set `status: draft`** in the front matter. Change it to `complete` only after the citations have been checked against the books.

## Tests

```bash
python3 -m unittest discover -s tools
```

The tests build small synthetic EPUBs, so they need no real books.
