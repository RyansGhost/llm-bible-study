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
2. **It teaches from trusted notes.** Each book has notes on its setting, structure, key people, key events, themes, and how it points to Christ. The notes draw on Reformed sources such as the Reformation Study Bible, Ligonier, R.C. Sproul and Matthew Henry.
3. **It goes where you want.** Pick a person or story to dig into. The AI offers the next step instead of lecturing.
4. **It checks what stuck.** Each book ends with a quiz and a final rating, so you can see your progress through all 66 books.

It works spoken aloud as well as typed, so you can study on a commute.

## How to start

**With Claude** (recommended): add the free *bible-study* skill, then say "Let's study Genesis."

- **Claude app** (web, desktop or mobile): download [bible-study.zip](https://github.com/RyansGhost/llm-bible-study/releases/latest/download/bible-study.zip). Then go to *Customize → Skills*, click **+**, then **Create skill → Upload a skill**, and choose the zip. Code execution must be turned on.
- **Claude Code**: run `/plugin marketplace add RyansGhost/llm-bible-study`, then `/plugin install bible-study@llm-bible-study`.

**With any other AI assistant**: paste this at the start of a conversation.

> Be my Bible study tutor. Use the notes at https://llm-bible-study.ryanfleck.ca/llms.txt and the book pages they link to. Teach me one book at a time from Reformed sources: first ask what I already know and rate it 0–10, then teach the book's key people, events, themes, and how it points to Christ, then quiz me. Correct my mistakes plainly, and tell me when something is your own opinion rather than the text or a source.

The notes for every book are below. Each page also has a plain markdown copy for AI tools.
