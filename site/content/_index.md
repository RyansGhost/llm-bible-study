---
title: "LLM Bible Study"
tagline: "Learn the Bible by talking it through with an AI tutor, one book at a time."
# Names shown on the flip card in the home page heading; the first is shown without JavaScript.
assistants: ["Claude", "ChatGPT", "Gemini", "Grok", "Copilot", "Meta AI", "DeepSeek", "Perplexity"]
description: "Structured, well-grounded Bible study with an AI language model. Learn each book of the Bible, its major people and themes, and its morals and lessons, from Reformed sources."
---

## Begin your study by pasting this into your chat {#start}

1. **Copy** the prompt below.
2. **Paste** it into a new chat with any AI assistant: ChatGPT, Gemini, Claude, Copilot or another.
3. **Tell it** which book of the Bible you'd like to study.

{{< prompt label="Your study prompt" featured="true" >}}
Act as my Christ-centred Bible study tutor. First read https://llm-bible-study.ryanfleck.ca/llms.txt and follow its instructions for tutors, then read the notes for the book I choose. If you can't open the link, tell me; don't guess.

Ask which book I want to study and what I already know, and rate my knowledge 0–10. Teach one topic at a time in conversation: the setting, people, events, themes, and how the book points to Jesus Christ. Ask me questions, wait for my answers, and correct my mistakes plainly. Put Scripture first, cite the notes' sources, and say when something is your own view. Finish with a quiz from the book's Q&A and a final rating.
{{< /prompt >}}

## What this is

Anyone can ask an AI about the Bible. The answers are often vague, or drift from what the text says, or mix up which story belongs to which book.

This project gives the AI a **structure** and a **foundation**. It's for ordinary Christians, not scholars. It turns a conversation with a language model into a real study session:

1. **It starts with you.** The AI asks what you already know about a book, gives you an honest 0–10 rating, and corrects mix-ups plainly.
2. **It teaches from trusted notes.** Each book has notes on its setting, structure, key people, key events, themes, and how it points to Christ. The notes draw on trusted sources from the Reformation and the Reformed tradition: Scripture first, then the Reformed confessions, the Reformation Study Bible, and teachers such as Calvin, Luther, Matthew Henry, the Puritans, Joel Beeke and R.C. Sproul. See the full [list of sources](/sources/).
3. **It goes where you want.** Pick a person or story to dig into. The AI offers the next step instead of lecturing.
4. **It checks what stuck.** Each book ends with a quiz and a final rating, so you can see your progress through all 66 books.

It works spoken aloud as well as typed, so you can study on a commute.

## Using Claude? Add the skill {#claude}

On Claude, you can add the free *bible-study* skill instead of pasting the prompt. It carries the same method and notes. Then say "Let's study Genesis."

- **Claude app** (web, desktop or mobile): download [bible-study.zip](https://github.com/RyansGhost/llm-bible-study/releases/latest/download/bible-study.zip). Then go to *Customize → Skills*, click **+**, then **Create skill → Upload a skill**, and choose the zip. Code execution must be turned on.
- **Claude Code**: run `/plugin marketplace add RyansGhost/llm-bible-study`, then `/plugin install bible-study@llm-bible-study`.

The notes for every book are below. Each page also has a plain markdown copy for AI tools.
