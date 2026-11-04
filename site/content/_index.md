---
title: "LLM Bible Study"
tagline: "Learn the Bible by talking it through with an AI tutor, one book at a time."
# Names shown on the flip card in the home page heading; the first is shown without JavaScript.
assistants: ["Claude", "ChatGPT", "Gemini", "Grok", "Copilot", "Meta AI", "DeepSeek", "Perplexity"]
description: "Structured, well-grounded Bible study with an AI language model. Learn each book of the Bible, its major people and themes, and its morals and lessons, from Reformed sources."
---

## What this is

Anyone can ask an AI about the Bible. The answers are often vague, or drift from what the text says, or mix up which story belongs to which book.

This project gives the AI a **structure** and a **foundation**. It's for ordinary Christians, not scholars. It turns a conversation with a language model into a real study session:

1. **It starts with you.** The AI asks what you already know about a book, gives you an honest 0–10 rating, and corrects mix-ups plainly.
2. **It teaches from trusted notes.** Each book has notes on its setting, structure, key people, key events, themes, and how it points to Christ. The notes draw on trusted sources from the Reformation and the Reformed tradition: Scripture first, then the Reformed confessions, the Reformation Study Bible, and teachers such as Calvin, Luther, Matthew Henry, the Puritans, Joel Beeke and R.C. Sproul. See the full [list of sources](/sources/).
3. **It goes where you want.** Pick a person or story to dig into. The AI offers the next step instead of lecturing.
4. **It checks what stuck.** Each book ends with a quiz and a final rating, so you can see your progress through all 66 books.

It works spoken aloud as well as typed, so you can study on a commute.

## How to start

**With Claude** (recommended): add the free *bible-study* skill, then say "Let's study Genesis."

- **Claude app** (web, desktop or mobile): download [bible-study.zip](https://github.com/RyansGhost/llm-bible-study/releases/latest/download/bible-study.zip). Then go to *Customize → Skills*, click **+**, then **Create skill → Upload a skill**, and choose the zip. Code execution must be turned on.
- **Claude Code**: run `/plugin marketplace add RyansGhost/llm-bible-study`, then `/plugin install bible-study@llm-bible-study`.

**With any other AI assistant**: copy this prompt and paste it at the start of a new conversation. It tells the AI where to find the notes and how to teach; the notes and the skill hold the detail.

{{< prompt label="Prompt for any AI" >}}
Act as my interactive, Christ-centred Bible study tutor. Teach me the books of the Bible one at a time, using this project's curated Reformation and Reformed study notes.

Before we begin, read and follow these:

1. https://llm-bible-study.ryanfleck.ca/llms.txt: the index of the book notes, with instructions for tutors.
2. https://raw.githubusercontent.com/RyansGhost/llm-bible-study/master/plugin/skills/bible-study/SKILL.md: the bible-study skill, which sets out the teaching method. If the skill is already installed for you, use it.
3. https://llm-bible-study.ryanfleck.ca/sources/index.md and the full notes for the book I choose. Follow the order of sources and the method they set out.

How to teach me: ask which book I want to study, ask what I already know, and rate it 0–10. Then teach the book in conversation: its setting, people, events, themes, and how it points to Jesus Christ. Finish with a quiz built from the book's Q&A, and give me a final rating.

Take one topic at a time. Ask me questions, wait for my answers, adapt to what I know, and correct my mistakes plainly.

Put Scripture first, represent the listed sources faithfully, and cite them for important theological claims. Make clear what is the Bible's teaching, what is a source's interpretation, and what is your own observation.

Don't replace these notes with a generic Bible summary. If you can't open any of these links, tell me rather than pretending you've read it.
{{< /prompt >}}

The notes for every book are below. Each page also has a plain markdown copy for AI tools.
