{{- /* books/<book>/index-for-copy.md: what the book page's copy button copies.
     The home page's study prompt, read from the {{< prompt >}} shortcode in
     content/_index.md so it has one source, goes in <instructions>, with links to
     llms.txt and the skill and the skill's teaching method (the same essentials
     llms.txt quotes, via skill-essentials.txt), so a pasted guide is complete
     without any web access. <memory> places the session in the whole-Bible plan
     (pointing to llms.txt) and asks for a progress tracker, pointing to the skill's
     tracker template. The notes, the same text as
     index.md (page.markdown.md), go in <notes>. */ -}}
{{- $prompt := "" -}}
{{- with findRE `(?s)\{\{< prompt [^>]*>\}\}.*?\{\{< /prompt >\}\}` site.Home.RawContent 1 -}}
  {{- $prompt = replaceRE `(?s)^\{\{< prompt [^>]*>\}\}\s*|\s*\{\{< /prompt >\}\}$` "" (index . 0) -}}
{{- end -}}
{{- if not $prompt }}{{ errorf "page.copy.md: no {{< prompt >}} block found in content/_index.md" }}{{ end -}}
<instructions>
{{ $prompt | safeHTML }}

We're studying {{ .Title }}. Its notes are in the <notes> block below, so don't ask which book; start by asking what I remember of it. If you can open the links below, read their instructions for tutors as well.

- Full site index and instructions for tutors: {{ "llms.txt" | absURL }}
- The complete teaching method (bible-study skill): {{ site.Params.skillURL }}

The essentials of that teaching method follow, so you can begin even if you can't open those links.

{{/* the Tracker section is left out here: <memory> asks for the tracker */ -}}
{{ replaceRE `(?s)\n*\*\*Tracker:\*\*.*$` "" (partial "skill-essentials.txt" .) | safeHTML }}
</instructions>

<memory>
This session is one part of a larger plan to study all 66 books of the Bible, one at a time; the full instructions are at {{ "llms.txt" | absURL }}. Keep a progress tracker for me (in my notes, or your memory or project): one checkbox per book with my starting and final scores, plus a short entry per book, as in the tracker template at {{ replace site.Params.skillURL "SKILL.md" "tracker-template.md" }}. When we finish {{ .Title }}, update it; if you can't save it, give me the update at the end.
</memory>

<notes>
{{ .RawContent | strings.TrimSpace | safeHTML }}

---

Source: {{ .Permalink }}
</notes>
