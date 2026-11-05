{{- /* books/<book>/index-for-copy.md: what the book page's copy button copies.
     The home page's study prompt, read from the {{< prompt >}} shortcode in
     content/_index.md so it has one source, goes in <instructions>, with links to
     llms.txt and the skill and the skill's teaching method (the same essentials
     llms.txt quotes, via skill-essentials.txt), so a pasted guide is complete
     without any web access. The notes, the same text as index.md
     (page.markdown.md), go in <notes>. */ -}}
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

<notes>
{{ .RawContent | strings.TrimSpace | safeHTML }}

---

Source: {{ .Permalink }}
</notes>
