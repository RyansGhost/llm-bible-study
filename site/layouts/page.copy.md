{{- /* books/<book>/index-for-copy.md: what the book page's copy button copies.
     The home page's study prompt, read from the {{< prompt >}} shortcode in
     content/_index.md so it has one source, goes in <instructions>, with links to
     llms.txt and the skill and the skill's teaching method (the same essentials
     llms.txt quotes, via skill-essentials.txt), so a pasted guide is complete
     without any web access. <memory> places the session in the whole-Bible plan
     (pointing to llms.txt) and asks for a progress tracker with one checkbox per
     book, generated from the site's 66 book pages. The notes, the same text as
     index.md (page.markdown.md), go in <notes>. */ -}}
{{- $prompt := "" -}}
{{- with findRE `(?s)\{\{< prompt [^>]*>\}\}.*?\{\{< /prompt >\}\}` site.Home.RawContent 1 -}}
  {{- $prompt = replaceRE `(?s)^\{\{< prompt [^>]*>\}\}\s*|\s*\{\{< /prompt >\}\}$` "" (index . 0) -}}
{{- end -}}
{{- if not $prompt }}{{ errorf "page.copy.md: no {{< prompt >}} block found in content/_index.md" }}{{ end -}}
<instructions>
{{ $prompt | safeHTML }}

We're studying {{ .Title }}. Its notes are in the <notes> block below, so don't ask which book; start by asking what I already know. Teach from these notes, and if you can open the links below, read their instructions for tutors as well.

- Full site index and instructions for tutors: {{ "llms.txt" | absURL }}
- The complete teaching method (bible-study skill): {{ site.Params.skillURL }}

The essentials of that teaching method follow, so you can begin even if you can't open those links.

{{ partial "skill-essentials.txt" . }}
</instructions>

<memory>
This session is one part of a larger plan to study all 66 books of the Bible, one book at a time. The full instructions for tutors, with the teaching method and links to every book's notes, are at {{ "llms.txt" | absURL }}.

Keep a progress tracker for me: a document, note or file wherever I keep my notes, or in your memory or project if you have one. Save this block there too, so future sessions follow the same plan. The tracker has one checkbox per book, in the order below. When we finish {{ .Title }}, tick it and fill in my starting score, my final score (both out of 10) and the date. If I have no tracker yet, offer to start one from this list. If you can't save documents, give me the updated list at the end of the session so I can keep it myself.

{{ range (where site.RegularPages "Section" "books").ByWeight -}}
- [ ] {{ .Title }} (start: _/10, final: _/10, date: _)
{{ end -}}
</memory>

<notes>
{{ .RawContent | strings.TrimSpace | safeHTML }}

---

Source: {{ .Permalink }}
</notes>
