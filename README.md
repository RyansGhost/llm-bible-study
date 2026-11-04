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

Copy this prompt and paste it at the start of a new conversation. It's the same prompt as on the [home page](https://llm-bible-study.ryanfleck.ca/#how-to-start). It tells the AI where to find the notes and how to teach; the notes and the skill hold the detail.

```text
Act as my interactive, Christ-centred Bible study tutor. Teach me the books of the Bible one at a time, using this project's curated Reformation and Reformed study notes.

Before we begin, read and follow these:

1. https://llm-bible-study.ryanfleck.ca/llms.txt: the index of the book notes, with instructions for tutors.
2. https://raw.githubusercontent.com/RyansGhost/llm-bible-study/master/plugin/skills/bible-study/SKILL.md: the bible-study skill, which sets out the teaching method. If the skill is already installed for you, use it.
3. https://llm-bible-study.ryanfleck.ca/sources/index.md and the full notes for the book I choose. Follow the order of sources and the method they set out.

How to teach me: ask which book I want to study, ask what I already know, and rate it 0–10. Then teach the book in conversation: its setting, people, events, themes, and how it points to Jesus Christ. Finish with a quiz built from the book's Q&A, and give me a final rating.

Take one topic at a time. Ask me questions, wait for my answers, adapt to what I know, and correct my mistakes plainly.

Put Scripture first, represent the listed sources faithfully, and cite them for important theological claims. Make clear what is the Bible's teaching, what is a source's interpretation, and what is your own observation.

Don't replace these notes with a generic Bible summary. If you can't open any of these links, tell me rather than pretending you've read it.
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
    sources.md                       approved sources and citation rules
    books/01-genesis.md … 66-revelation.md
site/                                Hugo site; mounts the books folder above as content/books;
                                     llms.txt quotes SKILL.md's method (steps to tracker)
.github/workflows/release.yml        on a v* tag, zips the skill and attaches it to a release
```

The top of `llms.txt` links to `SKILL.md` and copies its session steps, rating scale, rules and tracker sections word for word at build time. Edit them in `SKILL.md`, and the site follows. Keep those sections free of relative links other than `sources.md` and `tracker-template.md`, or the build stops with an error.

## Writing a book's notes

Every book file uses the same headings: Summary, Setting, Structure, Chapter by chapter, Key people, Key events, Themes, How it points to Christ, Common mix-ups, Going deeper, Q&A, Sources, and Changelog. That way the AI can find the same thing in any book. `06-joshua.md` is the worked example.

- Write in your own words. Don't copy study Bible introductions or notes: that text is copyrighted.
- Cite every source: Reformation Study Bible page numbers, Ligonier URLs, chapter and verse.
- Flag any non-Reformed source by name.
- Mark your own applications as yours.
- Set `status` in the front matter as the notes progress: `placeholder` (empty template), `draft` (written, awaiting human review; shown as "Human review pending"), or `complete`. The site and the skill both use it.
- Add a line to the book's Changelog whenever the notes change, e.g. `2. 2026-11-20: Human review; checked Reformation Study Bible page numbers`.

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
