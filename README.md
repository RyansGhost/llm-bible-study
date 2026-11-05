# LLM Bible Study

**Learn the Bible by talking it through with an AI tutor, one book at a time.**

This project helps ordinary Christians (laymen, not scholars) have a structured, well-grounded conversation with a language model. The model teaches them the Bible: its books, its major themes and people, and its morals and lessons.

On its own, an AI's answers about the Bible can be vague, can drift from the text, or can mix up which story belongs to which book. This repo gives the AI two things:

- **A structure.** The *bible-study* skill runs each session the same way. It asks what you already know, rates it 0–10, corrects mistakes plainly, and teaches the book's people, events, themes, and how it points to Christ. It lets you choose where to go deeper, then quizzes you and records an honest rating.
- **A foundation.** Notes for all 66 books, written in our own words, with citations, from trusted sources of the Reformation and the Reformed tradition. In order: Scripture, the Reformed confessions and catechisms, the Reformation Study Bible and the Reformation Heritage KJV Study Bible, and teachers such as Calvin, Luther, Matthew Henry, the Puritans, Joel Beeke, Spurgeon and R.C. Sproul. The full list is in [`sources.md`](plugin/skills/bible-study/sources.md), also published at [/sources/](https://llm-bible-study.ryanfleck.ca/sources/). The AI is told to say when a point is its own opinion rather than the text or a source.

Sessions work spoken aloud as well as typed, so you can study on a commute.

The same notes are published at **<https://llm-bible-study.ryanfleck.ca>**, with a plain markdown copy of every page and an [`llms.txt`](https://llm-bible-study.ryanfleck.ca/llms.txt) index for AI tools.

## Start studying

### Claude app (web, desktop, mobile)

1. Download [`bible-study.zip`](https://github.com/RyansGhost/llm-bible-study/releases/latest/download/bible-study.zip) from the latest release. Don't use GitHub's "Source code" zip.
2. In Claude, go to **Customize → Skills**, click **+**, then **Create skill → Upload a skill**, and choose the zip. Code execution must be turned on.
3. Start a chat and say "Let's study Genesis."

On Team and Enterprise plans, an owner can also upload the plugin for the whole organisation under the organisation's plugin settings ([help article](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization)).

### Claude Code

```
/plugin marketplace add RyansGhost/llm-bible-study
/plugin install bible-study@llm-bible-study
```

Or copy `plugin/skills/bible-study/` to `~/.claude/skills/bible-study/` to install the skill by hand.

### Any other AI assistant

The most reliable way is the [home page](https://llm-bible-study.ryanfleck.ca/#start): choose a book and press **Copy Study Guide**. That copies the tutor's instructions and the book's full notes, so the assistant needs no web access. (Some assistants, Claude among them, will only open links you paste yourself, not links inside a page they've opened.)

If your assistant can search the web and open links, you can instead paste this prompt at the start of a new conversation. It's the same prompt as at the [bottom of the home page](https://llm-bible-study.ryanfleck.ca/#prompt). It points the AI to [`llms.txt`](https://llm-bible-study.ryanfleck.ca/llms.txt), which holds the notes and the teaching method.

```text
Act as my warm but rigorous Bible study tutor. First read https://llm-bible-study.ryanfleck.ca/llms.txt and follow its instructions for tutors, then read the notes for the book I choose. If you can't open a link, tell me; don't guess.

Ask which book I want to study and what I already remember of it. Teach the story and its key people first, one at a time: use leading questions to help me recall and connect what I know, then fill in the gaps and correct mistakes plainly but kindly. Quiz me on the story before moving on to its setting and timeline, then its themes and how it points to Jesus Christ.

Put Scripture first, teach from the notes, and say when something is your own view or from a web search. Finish with a quiz from the book's Q&A, a 0–10 rating, and an update to my progress tracker.

I'm preparing for seminary, evangelism and ministry, so don't flatter me or mistake familiarity for understanding. Encourage me when I've earned it.
```

### Keeping a progress tracker

The skill can log each book to a tracker doc: your starting rating, what you knew, what you learned, and your quiz result. Give Claude the doc's link in the chat, in project instructions, or in memory, and it will update the doc after each book. To start a new tracker, use [`tracker-template.md`](plugin/skills/bible-study/tracker-template.md), or ask Claude to set one up.

## How the repo is laid out

The book notes are written once, inside the skill, and the website reads the same files.

```
.claude-plugin/marketplace.json      Claude Code marketplace "llm-bible-study"
plugin/
  .claude-plugin/plugin.json         the "bible-study" plugin
  skills/bible-study/                the skill; this folder alone is the release zip
    SKILL.md                         session steps, rating scale, rules, book index
    sources.md                       approved sources and their abbreviations
    books/01-genesis.md … 66-revelation.md
site/                                Hugo site; mounts the books folder above as content/books;
                                     llms.txt quotes SKILL.md's method (steps to tracker)
.github/workflows/release.yml        on a v* tag, zips the skill and attaches it to a release
```

The top of `llms.txt` links to `SKILL.md` and copies its session steps, rating scale, rules and tracker sections word for word at build time. Edit them in `SKILL.md`, and the site follows. Keep those sections free of relative links other than `sources.md` and `tracker-template.md`, or the build stops with an error.

The site also publishes the skill's `SKILL.md` and `tracker-template.md` at its root (`/SKILL.md`, `/tracker-template.md`), with `SKILL.md`'s links rewritten to absolute site URLs. These are the links `llms.txt` and the study guides use: some AI fetch tools won't open raw.githubusercontent.com. If a link in `SKILL.md` can't be resolved, the build stops with an error.

## Writing a book's notes

Every book file uses the same headings: Summary, Setting, Structure, Chapter by chapter, Key people, Key events, Themes, How it points to Christ, Common mix-ups, Going deeper, Q&A, Sources, and Changelog. That way the AI can find the same thing in any book. `06-joshua.md` is the worked example. Follow the citation rules in [`AGENTS.md`](AGENTS.md); `CLAUDE.md` imports it for Claude Code.

- Write in your own words. Don't copy study Bible introductions or notes: that text is copyrighted.
- Cite every source by section: the study Bible introduction and its section headings, a commentary's chapter, a Ligonier URL, or chapter and verse. Page numbers aren't needed.
- Cite the five main works by italic abbreviation with a footnote: *BTO*, *BTN*, *LSB*, *RSB* and *RH* (key in [`sources.md`](plugin/skills/bible-study/sources.md)). Write `*RSB*[^rsb]` in the text, or put the footnote on the chapter author for BTO and BTN (`Timmer[^bto]`). Under Sources, define each footnote with a bold key: `[^rsb]: **RSB**: *The Reformation Study Bible* (Reformation Trust, 2015), introduction to …`. The site shows these footnotes under the Sources heading. Other sources stay as a plain list.
- Flag any non-Reformed source by name.
- Mark your own applications as yours.
- Write each Q&A item as a numbered `**Q:**` line with its `**A:**` indented under it, and give the answer a chapter and verse. The site styles these as question cards; the markdown stays plain.
- Set `status` in the front matter as the notes progress: `draft` (written, awaiting human review; shown as "Human review pending") or `complete`. The site and the skill both use it.
- Add a line to the book's Changelog whenever the notes change, e.g. `2. 2026-11-20: Human review; checked the citations against the sources`.

To draft notes from commentaries or study Bibles you own as DRM-free EPUBs, use the indexer in [`tools/`](tools/README.md). It finds each book's material across your sources. The EPUBs themselves are never committed.

## Building the site

Install [Hugo extended](https://gohugo.io/installation/) 0.168.0 or newer, then run either:

```
hugo server --source site
```

```
hugo --source site --minify
```

`hugo server` previews the site at http://localhost:1313. `hugo --minify` builds it into `site/public/`.

The live site is built by Cloudflare Pages from `master`, with these settings:

- Build command: `bash build.sh`
- Output directory: `site/public`

`build.sh` downloads the pinned Hugo version (0.168.0, or `HUGO_VERSION` if set) and builds with it. Don't use Cloudflare's built-in `hugo`: it's too old for this site and the build fails.

## Releasing the skill

1. Bump `version` in `plugin/.claude-plugin/plugin.json`, e.g. to `0.2.0`, and merge to `master`.
2. Either push a matching tag (`git tag v0.2.0 && git push origin v0.2.0`), or open **Actions → Release skill zip → Run workflow** on `master` and enter `v0.2.0`.

The workflow checks the version matches `plugin.json`, builds `bible-study.zip`, and publishes the release. The "latest release" download link above always points to the newest one.

## Licence

The book notes, the skill text and the site's written content are licensed under [CC BY 4.0](LICENSE). The site templates, styles and workflows are licensed under the [MIT licence](LICENSE-CODE).
