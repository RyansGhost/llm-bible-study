# Tracker template

Use this to start a new tracker, or to match the format of an existing one. It has a checklist of all 66 books, grouped by testament and section, with a short entry below for each finished book. The tracker can live anywhere the user can read and Claude can edit: a doc, a note, an artifact, or a markdown file. If the user's existing tracker uses a different layout, keep theirs and add entries in its style.

Rules for entries:

- Add one entry per book, newest first, when the book's quiz is done. If a session ends mid-book, add the entry as "In progress" and finish it next time.
- Be plain and harsh, not kind. Write what the user actually knew and didn't know, not encouragement. "Thought Jericho was in Judges" is useful; "Great effort!" is not.
- Ratings use the 0–10 scale in SKILL.md. Always give both the starting and final rating.
- Keep each entry short enough to read aloud in under a minute.
- When a book is done, tick its box, fill in its start and final ratings and the date, and update the "Covered" count. A book started but not finished gets "(in progress)" after its name.

## The template

Copy everything below the line into the new tracker.

---

```markdown
# Books of the Bible Tracker

Covered: 0 of 66 books

## Progress

### Old Testament

**Law**

- [ ] Genesis: start _/10, final _/10, finished _
- [ ] Exodus: start _/10, final _/10, finished _
- [ ] Leviticus: start _/10, final _/10, finished _
- [ ] Numbers: start _/10, final _/10, finished _
- [ ] Deuteronomy: start _/10, final _/10, finished _

**History**

- [ ] Joshua: start _/10, final _/10, finished _
- [ ] Judges: start _/10, final _/10, finished _
- [ ] Ruth: start _/10, final _/10, finished _
- [ ] 1 Samuel: start _/10, final _/10, finished _
- [ ] 2 Samuel: start _/10, final _/10, finished _
- [ ] 1 Kings: start _/10, final _/10, finished _
- [ ] 2 Kings: start _/10, final _/10, finished _
- [ ] 1 Chronicles: start _/10, final _/10, finished _
- [ ] 2 Chronicles: start _/10, final _/10, finished _
- [ ] Ezra: start _/10, final _/10, finished _
- [ ] Nehemiah: start _/10, final _/10, finished _
- [ ] Esther: start _/10, final _/10, finished _

**Wisdom and Poetry**

- [ ] Job: start _/10, final _/10, finished _
- [ ] Psalms: start _/10, final _/10, finished _
- [ ] Proverbs: start _/10, final _/10, finished _
- [ ] Ecclesiastes: start _/10, final _/10, finished _
- [ ] Song of Solomon: start _/10, final _/10, finished _

**Major Prophets**

- [ ] Isaiah: start _/10, final _/10, finished _
- [ ] Jeremiah: start _/10, final _/10, finished _
- [ ] Lamentations: start _/10, final _/10, finished _
- [ ] Ezekiel: start _/10, final _/10, finished _
- [ ] Daniel: start _/10, final _/10, finished _

**Minor Prophets**

- [ ] Hosea: start _/10, final _/10, finished _
- [ ] Joel: start _/10, final _/10, finished _
- [ ] Amos: start _/10, final _/10, finished _
- [ ] Obadiah: start _/10, final _/10, finished _
- [ ] Jonah: start _/10, final _/10, finished _
- [ ] Micah: start _/10, final _/10, finished _
- [ ] Nahum: start _/10, final _/10, finished _
- [ ] Habakkuk: start _/10, final _/10, finished _
- [ ] Zephaniah: start _/10, final _/10, finished _
- [ ] Haggai: start _/10, final _/10, finished _
- [ ] Zechariah: start _/10, final _/10, finished _
- [ ] Malachi: start _/10, final _/10, finished _

### New Testament

**Gospels**

- [ ] Matthew: start _/10, final _/10, finished _
- [ ] Mark: start _/10, final _/10, finished _
- [ ] Luke: start _/10, final _/10, finished _
- [ ] John: start _/10, final _/10, finished _

**History**

- [ ] Acts: start _/10, final _/10, finished _

**Pauline Epistles**

- [ ] Romans: start _/10, final _/10, finished _
- [ ] 1 Corinthians: start _/10, final _/10, finished _
- [ ] 2 Corinthians: start _/10, final _/10, finished _
- [ ] Galatians: start _/10, final _/10, finished _
- [ ] Ephesians: start _/10, final _/10, finished _
- [ ] Philippians: start _/10, final _/10, finished _
- [ ] Colossians: start _/10, final _/10, finished _
- [ ] 1 Thessalonians: start _/10, final _/10, finished _
- [ ] 2 Thessalonians: start _/10, final _/10, finished _
- [ ] 1 Timothy: start _/10, final _/10, finished _
- [ ] 2 Timothy: start _/10, final _/10, finished _
- [ ] Titus: start _/10, final _/10, finished _
- [ ] Philemon: start _/10, final _/10, finished _

**General Epistles**

- [ ] Hebrews: start _/10, final _/10, finished _
- [ ] James: start _/10, final _/10, finished _
- [ ] 1 Peter: start _/10, final _/10, finished _
- [ ] 2 Peter: start _/10, final _/10, finished _
- [ ] 1 John: start _/10, final _/10, finished _
- [ ] 2 John: start _/10, final _/10, finished _
- [ ] 3 John: start _/10, final _/10, finished _
- [ ] Jude: start _/10, final _/10, finished _

**Prophecy**

- [ ] Revelation: start _/10, final _/10, finished _

## Entries

### <Book>: <start>/10 → <final>/10

- **Initial impression:** One or two blunt sentences on where the user started.
- **Already knew:** What they got right before any teaching.
- **Got wrong or missed:** Errors and gaps, including stories placed in the wrong book.
- **Learned:** The key people, events, themes and lessons covered this time.
- **Quiz:** Score (e.g. 4/5) and which questions they missed.
- **Next time:** What to review before moving on, or "nothing, move on".
```

## Example

An example only; not a real record. The book's line in the checklist, once it's done:

```markdown
- [x] Joshua: start 3/10, final 7/10, finished 2026-11-04
```

And its entry:

```markdown
### Joshua: 3/10 → 7/10

- **Initial impression:** Knew Jericho and not much else. Vague on how Joshua connects to Moses.
- **Already knew:** Walls of Jericho fell; Joshua led Israel after Moses.
- **Got wrong or missed:** Put Moses' death in Joshua (it's Deuteronomy). Had never heard of Achan, Ai or the Gibeonites. Thought the conquest was finished.
- **Learned:** Rahab and the scarlet cord, crossing the Jordan, Achan's sin and the defeat at Ai, the Gibeonite treaty, the sun standing still, Caleb at 85, "as for me and my house" (24:15). Joshua and Jesus share a name; Hebrews 4 on the greater rest.
- **Quiz:** 4/5. Missed how the Gibeonites tricked Israel.
- **Next time:** Re-tell the Gibeonite story from memory before starting Judges.
```
