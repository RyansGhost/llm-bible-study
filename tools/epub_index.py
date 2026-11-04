#!/usr/bin/env python3
"""Index EPUB books so their material can be used to write the Bible book notes.

Standard library only. EPUBs and indexes are git-ignored: never commit them.

    python3 tools/epub_index.py index epubs/*.epub        # build or refresh the index
    python3 tools/epub_index.py list                      # indexed works
    python3 tools/epub_index.py toc WORK                  # a work's sections
    python3 tools/epub_index.py book genesis              # where each work covers a Bible book
    python3 tools/epub_index.py search "scarlet cord"     # full-text search
    python3 tools/epub_index.py show WORK:SECTION         # print one section

The index lives in .epub-index/ (change with --index DIR). Each work gets a
folder with meta.json, sections.jsonl (one section per line, with its text) and
refs.json (Bible book -> sections that cite it, with the references found).
"""

import argparse
import hashlib
import html
import json
import posixpath
import re
import sys
import textwrap
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree as ET

DEFAULT_INDEX = ".epub-index"
MAX_SECTION_WORDS = 2500  # long sections are split into parts of about this size

# --------------------------------------------------------------------------
# Bible books: (number, slug used by plugin/skills/bible-study/books, names)
# Names are matched case-insensitively; abbreviations may end in a full stop.
# --------------------------------------------------------------------------
BOOKS = [
    (1, "genesis", ["Genesis", "Gen", "Gn"]),
    (2, "exodus", ["Exodus", "Exod", "Exo", "Ex"]),
    (3, "leviticus", ["Leviticus", "Lev", "Lv"]),
    (4, "numbers", ["Numbers", "Num", "Nm", "Nb", "Nu"]),
    (5, "deuteronomy", ["Deuteronomy", "Deut", "Dt"]),
    (6, "joshua", ["Joshua", "Josh", "Jos", "Jsh"]),
    (7, "judges", ["Judges", "Judg", "Jdg", "Jg", "Jgs"]),
    (8, "ruth", ["Ruth", "Rth", "Ru"]),
    (9, "1-samuel", ["1 Samuel", "1 Sam", "1 Sa", "1Sam", "1Sa", "I Samuel", "I Sam", "First Samuel", "1Sm", "1 Sm"]),
    (10, "2-samuel", ["2 Samuel", "2 Sam", "2 Sa", "2Sam", "2Sa", "II Samuel", "II Sam", "Second Samuel", "2Sm", "2 Sm"]),
    (11, "1-kings", ["1 Kings", "1 Kgs", "1 Ki", "1Kgs", "1Ki", "I Kings", "I Kgs", "First Kings"]),
    (12, "2-kings", ["2 Kings", "2 Kgs", "2 Ki", "2Kgs", "2Ki", "II Kings", "II Kgs", "Second Kings"]),
    (13, "1-chronicles", ["1 Chronicles", "1 Chron", "1 Chr", "1Chr", "I Chronicles", "I Chron", "I Chr", "First Chronicles", "1Ch"]),
    (14, "2-chronicles", ["2 Chronicles", "2 Chron", "2 Chr", "2Chr", "II Chronicles", "II Chron", "II Chr", "Second Chronicles", "2Ch"]),
    (15, "ezra", ["Ezra", "Ezr"]),
    (16, "nehemiah", ["Nehemiah", "Neh", "Ne"]),
    (17, "esther", ["Esther", "Esth", "Est"]),
    (18, "job", ["Job", "Jb"]),
    (19, "psalms", ["Psalms", "Psalm", "Pss", "Psa", "Ps"]),
    (20, "proverbs", ["Proverbs", "Prov", "Prv", "Pr"]),
    (21, "ecclesiastes", ["Ecclesiastes", "Eccles", "Eccl", "Ecc", "Qoh", "Ec"]),
    (22, "song-of-songs", ["Song of Songs", "Song of Solomon", "Canticles", "Song", "Cant", "SS", "Sg"]),
    (23, "isaiah", ["Isaiah", "Isa", "Is"]),
    (24, "jeremiah", ["Jeremiah", "Jer"]),
    (25, "lamentations", ["Lamentations", "Lam", "Lm"]),
    (26, "ezekiel", ["Ezekiel", "Ezek", "Eze", "Ezk"]),
    (27, "daniel", ["Daniel", "Dan", "Dn"]),
    (28, "hosea", ["Hosea", "Hos"]),
    (29, "joel", ["Joel", "Jl"]),
    (30, "amos", ["Amos", "Am"]),
    (31, "obadiah", ["Obadiah", "Obad", "Ob"]),
    (32, "jonah", ["Jonah", "Jon", "Jnh"]),
    (33, "micah", ["Micah", "Mic", "Mi"]),
    (34, "nahum", ["Nahum", "Nah", "Na"]),
    (35, "habakkuk", ["Habakkuk", "Hab"]),
    (36, "zephaniah", ["Zephaniah", "Zeph", "Zep"]),
    (37, "haggai", ["Haggai", "Hag", "Hg"]),
    (38, "zechariah", ["Zechariah", "Zech", "Zec"]),
    (39, "malachi", ["Malachi", "Mal"]),
    (40, "matthew", ["Matthew", "Matt", "Mt"]),
    (41, "mark", ["Mark", "Mk", "Mrk"]),
    (42, "luke", ["Luke", "Lk"]),
    (43, "john", ["John", "Jn", "Jhn"]),
    (44, "acts", ["Acts", "Act", "Ac"]),
    (45, "romans", ["Romans", "Rom", "Rm"]),
    (46, "1-corinthians", ["1 Corinthians", "1 Cor", "1Cor", "I Corinthians", "I Cor", "First Corinthians", "1Co", "1 Co"]),
    (47, "2-corinthians", ["2 Corinthians", "2 Cor", "2Cor", "II Corinthians", "II Cor", "Second Corinthians", "2Co", "2 Co"]),
    (48, "galatians", ["Galatians", "Gal"]),
    (49, "ephesians", ["Ephesians", "Eph"]),
    (50, "philippians", ["Philippians", "Phil", "Php"]),
    (51, "colossians", ["Colossians", "Col"]),
    (52, "1-thessalonians", ["1 Thessalonians", "1 Thess", "1 Th", "1Thess", "I Thessalonians", "I Thess", "First Thessalonians", "1Th", "1Thes"]),
    (53, "2-thessalonians", ["2 Thessalonians", "2 Thess", "2 Th", "2Thess", "II Thessalonians", "II Thess", "Second Thessalonians", "2Th", "2Thes"]),
    (54, "1-timothy", ["1 Timothy", "1 Tim", "1Tim", "I Timothy", "I Tim", "First Timothy", "1Tm", "1 Tm"]),
    (55, "2-timothy", ["2 Timothy", "2 Tim", "2Tim", "II Timothy", "II Tim", "Second Timothy", "2Tm", "2 Tm"]),
    (56, "titus", ["Titus", "Tit", "Ti"]),
    (57, "philemon", ["Philemon", "Philem", "Phlm", "Phm"]),
    (58, "hebrews", ["Hebrews", "Heb"]),
    (59, "james", ["James", "Jas", "Jms"]),
    (60, "1-peter", ["1 Peter", "1 Pet", "1 Pt", "1Pet", "I Peter", "I Pet", "First Peter", "1Pt"]),
    (61, "2-peter", ["2 Peter", "2 Pet", "2 Pt", "2Pet", "II Peter", "II Pet", "Second Peter", "2Pt"]),
    (62, "1-john", ["1 John", "1 Jn", "1Jn", "I John", "I Jn", "First John"]),
    (63, "2-john", ["2 John", "2 Jn", "2Jn", "II John", "II Jn", "Second John"]),
    (64, "3-john", ["3 John", "3 Jn", "3Jn", "III John", "III Jn", "Third John"]),
    (65, "jude", ["Jude", "Jud"]),
    (66, "revelation", ["Revelation", "Rev", "Apocalypse", "Apoc", "Rv"]),
]
BOOK_BY_SLUG = {slug: (num, names) for num, slug, names in BOOKS}
BOOK_FILE = {slug: f"{num:02d}-{slug}.md" for num, slug, _ in BOOKS}


def _name_pattern(name):
    # "1 Samuel" also matches "1Samuel" and "1. Samuel"; abbreviations allow a trailing full stop.
    parts = [re.escape(p) for p in name.split(" ")]
    return r"\.?\s*".join(parts) + r"\.?"


# Longest names first so "1 John" wins over "John" and "Song of Songs" over "Song".
_ALL_NAMES = sorted(((n, slug) for _, slug, names in BOOKS for n in names), key=lambda x: -len(x[0]))

# A reference is a capitalised book name followed by a chapter, optionally a
# verse and a range: "Gen. 3:15", "1 Sam 17", "Ps 23:1-4", "John 3.16", and the
# older "Gen. iii. 15" with lowercase roman chapters. Requiring a chapter keeps
# "Mark", "Job" and "Acts" in ordinary prose from counting; matching is
# case-sensitive so "is 3" isn't Isaiah. One- and two-letter abbreviations
# ("Is", "Am", "Mt") also need a verse (see find_refs).
_CHAPTER = r"(\d{1,3}|[ivxlc]{1,8}(?=\.))"
_VERSE = r"(?:\.?\s*[:.]\s*(\d{1,3})(?:\s*[-\u2013]\s*\d{1,3})?)?"
REF_RE = re.compile(
    r"(?<![\w])(" + "|".join(_name_pattern(n) for n, _ in _ALL_NAMES) + r")"
    r"\s+" + _CHAPTER + _VERSE + r"(?![\w])"
)
_ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}


def roman_to_int(s):
    total, prev = 0, 0
    for ch in reversed(s.lower()):
        v = _ROMAN.get(ch, 0)
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total


# A heading that names a book, e.g. "Introduction to Genesis", "THE BOOK OF JOSHUA",
# "1 Samuel", "Commentary on Galatians". Only full names count here.
_FULL_NAMES = sorted(
    [(names[0], slug) for _, slug, names in BOOKS]
    + [(n, slug) for _, slug, names in BOOKS for n in names if n.startswith(("I ", "II ", "III ", "First", "Second", "Third", "Song of"))],
    key=lambda x: -len(x[0]),
)
HEADING_BOOK_RE = re.compile(
    r"(?<![\w])(" + "|".join(_name_pattern(n) for n, _ in _FULL_NAMES) + r")(?![\w])",
    re.IGNORECASE,
)


def slug_for_name(name):
    key = re.sub(r"[\s.]+", "", name).lower()
    for n, slug in _ALL_NAMES:
        if re.sub(r"[\s.]+", "", n).lower() == key:
            return slug
    return None


def find_refs(text):
    """Return {slug: ["3:15", "17", ...]} for every Bible reference in the text."""
    found = {}
    for m in REF_RE.finditer(text):
        name, ch, vs = m.group(1), m.group(2), m.group(3)
        slug = slug_for_name(name)
        if not slug:
            continue
        if len(re.sub(r"[\s.]", "", name)) <= 2 and not vs:
            continue  # "Is 6" or "Am 5" alone is too likely to be prose
        if not ch.isdigit():
            ch = str(roman_to_int(ch))
        found.setdefault(slug, []).append(f"{ch}:{vs}" if vs else ch)
    return found


# "The First Epistle of John", "The Second Book of the Kings",
# "The First Epistle General of Peter", "II Epistle of Paul to the Corinthians"
ORDINAL_HEADING_RE = re.compile(
    r"\b(First|Second|Third|1st|2nd|3rd|III|II|I)\s+(?:General\s+)?(?:Book|Epistle|Letter)\s+"
    r"(?:General\s+)?(?:of\s+)?(?:Paul\s+(?:the\s+Apostle\s+)?)?(?:to\s+the\s+|of\s+the\s+|to\s+|the\s+)?"
    r"(Samuel|Kings|Chronicles|Corinthians|Thessalonians|Timothy|Peter|John)\b",
    re.IGNORECASE,
)
_ORDINAL = {"first": 1, "1st": 1, "i": 1, "second": 2, "2nd": 2, "ii": 2, "third": 3, "3rd": 3, "iii": 3}


# "1–2 Samuel", "1-3 John": one chapter covering several numbered books
RANGE_HEADING_RE = re.compile(
    r"(?<![\w])([123])\s*[\u2013-]\s*([23])\s+(Samuel|Kings|Chronicles|Corinthians|Thessalonians|Timothy|Peter|John)\b",
    re.IGNORECASE,
)
TWELVE_RE = re.compile(r"^\s*(The\s+(Book\s+of\s+the\s+)?Twelve|The\s+Minor\s+Prophets|Minor\s+Prophets)\s*$", re.IGNORECASE)
TWELVE = [slug for num, slug, _ in BOOKS if 28 <= num <= 39]


def books_in_heading(heading):
    out = []
    heading = heading or ""
    for part in heading.split(" / "):
        if TWELVE_RE.match(part):
            out.extend(b for b in TWELVE if b not in out)

    def book_range(m):
        for n in range(int(m.group(1)), int(m.group(2)) + 1):
            slug = f"{n}-{m.group(3).lower()}"
            if slug in BOOK_BY_SLUG and slug not in out:
                out.append(slug)
        return " "

    heading = RANGE_HEADING_RE.sub(book_range, heading)

    def ordinal(m):
        slug = f"{_ORDINAL[m.group(1).lower()]}-{m.group(2).lower()}"
        if slug in BOOK_BY_SLUG and slug not in out:
            out.append(slug)
        return " "

    heading = ORDINAL_HEADING_RE.sub(ordinal, heading)
    for m in HEADING_BOOK_RE.finditer(heading):
        slug = slug_for_name(m.group(1))
        if slug and slug not in out:
            out.append(slug)
    return out


# --------------------------------------------------------------------------
# EPUB reading
# --------------------------------------------------------------------------
class DRMError(Exception):
    pass


NS = {
    "c": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "ncx": "http://www.daisy.org/z3986/2005/ncx/",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "enc": "http://www.w3.org/2001/04/xmlenc#",
}
FONT_OBFUSCATION = {"http://www.idpf.org/2008/embedding", "http://ns.adobe.com/pdf/enc#RC"}


def check_drm(zf):
    names = set(zf.namelist())
    if "META-INF/rights.xml" in names:
        raise DRMError("Adobe DRM (META-INF/rights.xml)")
    if "META-INF/sinf.xml" in names or any(n.endswith(".sinf") for n in names):
        raise DRMError("Apple FairPlay DRM")
    if "META-INF/encryption.xml" in names:
        root = ET.fromstring(zf.read("META-INF/encryption.xml"))
        for data in root.iter(f"{{{NS['enc']}}}EncryptedData"):
            method = data.find(f"{{{NS['enc']}}}EncryptionMethod")
            algo = method.get("Algorithm") if method is not None else ""
            ref = data.find(f".//{{{NS['enc']}}}CipherReference")
            uri = ref.get("URI", "") if ref is not None else ""
            # Font obfuscation is not DRM; anything else encrypted is.
            if algo not in FONT_OBFUSCATION and not re.search(r"\.(otf|ttf|woff2?)$", uri, re.I):
                raise DRMError(f"encrypted content ({uri or 'unknown file'})")


def _text(el):
    return (el.text or "").strip() if el is not None else ""


def read_package(zf):
    container = ET.fromstring(zf.read("META-INF/container.xml"))
    rootfile = container.find(".//c:rootfile", NS)
    opf_path = rootfile.get("full-path")
    opf_dir = posixpath.dirname(opf_path)
    opf = ET.fromstring(zf.read(opf_path))

    meta_el = opf.find("opf:metadata", NS)
    meta = {
        "title": _text(meta_el.find("dc:title", NS)),
        "creators": [_text(e) for e in meta_el.findall("dc:creator", NS) if _text(e)],
        "publisher": _text(meta_el.find("dc:publisher", NS)),
        "date": _text(meta_el.find("dc:date", NS)),
        "language": _text(meta_el.find("dc:language", NS)),
        "rights": _text(meta_el.find("dc:rights", NS)),
        "identifier": _text(meta_el.find("dc:identifier", NS)),
    }

    manifest = {}
    nav_href = None
    for item in opf.find("opf:manifest", NS):
        href = posixpath.normpath(posixpath.join(opf_dir, unquote(item.get("href", ""))))
        manifest[item.get("id")] = {"href": href, "type": item.get("media-type", ""), "props": item.get("properties", "")}
        if "nav" in (item.get("properties") or "").split():
            nav_href = href

    spine_el = opf.find("opf:spine", NS)
    spine = []
    for ref in spine_el.findall("opf:itemref", NS):
        item = manifest.get(ref.get("idref"))
        if item and ("html" in item["type"] or item["href"].endswith((".xhtml", ".html", ".htm"))):
            spine.append(item["href"])

    toc = {}
    ncx_id = spine_el.get("toc")
    if nav_href:
        toc = read_nav(zf, nav_href)
    elif ncx_id and ncx_id in manifest:
        toc = read_ncx(zf, manifest[ncx_id]["href"])
    return meta, spine, toc


def read_nav(zf, nav_href):
    """EPUB 3 nav document: {file href: first title that points into it}."""
    toc = {}
    base = posixpath.dirname(nav_href)
    try:
        root = ET.fromstring(zf.read(nav_href))
    except ET.ParseError:
        return toc
    for a in root.iter(f"{{{NS['xhtml']}}}a"):
        href = a.get("href", "")
        if not href:
            continue
        path = posixpath.normpath(posixpath.join(base, unquote(href.split("#")[0])))
        title = " ".join("".join(a.itertext()).split())
        if title:
            toc.setdefault(path, title)
    return toc


def read_ncx(zf, ncx_href):
    """EPUB 2 NCX table of contents: {file href: first title that points into it}."""
    toc = {}
    base = posixpath.dirname(ncx_href)
    try:
        root = ET.fromstring(zf.read(ncx_href))
    except ET.ParseError:
        return toc
    for point in root.iter(f"{{{NS['ncx']}}}navPoint"):
        label = point.find("ncx:navLabel/ncx:text", NS)
        content = point.find("ncx:content", NS)
        if content is None:
            continue
        path = posixpath.normpath(posixpath.join(base, unquote(content.get("src", "").split("#")[0])))
        if _text(label):
            toc.setdefault(path, _text(label))
    return toc


# Many publishers mark headings with a class on <p> or <div> instead of <h1>-<h6>.
# Level 1 is a book or chapter title; deeper levels are sub-headings.
HEADING_CLASSES = {
    # Crossway (e.g. Van Pelt, Kruger)
    "chtit": 1, "fbtit": 1, "fbtit1": 1, "head1": 2, "head2": 2, "head3": 3, "head3n": 3, "head4": 4, "head5": 5,
    # Concordia (The Lutheran Study Bible)
    "ct": 1, "pt": 1, "cn": 2, "ah": 2, "ahaft": 3, "sbh": 3, "sbah": 4,
    # Common generic names
    "chapter-title": 1, "chaptertitle": 1, "chapter-head": 1, "title": 1, "subtitle": 2,
    "h1": 1, "h2": 2, "h3": 3, "h4": 4, "a-head": 2, "b-head": 3, "c-head": 4,
}


def heading_level(attrs):
    classes = (dict(attrs).get("class") or "").lower().split()
    levels = [HEADING_CLASSES[c] for c in classes if c in HEADING_CLASSES]
    return min(levels) if levels else None


class _Extractor(HTMLParser):
    """Turn an XHTML chapter into [(heading level, heading, paragraphs)] blocks."""

    BLOCK = {"p", "div", "li", "blockquote", "br", "tr", "dd", "dt", "section", "article", "aside", "pre", "figcaption"}
    SKIP = {"script", "style", "head", "title"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = [[0, "", []]]  # level, heading, paragraphs
        self.buf = []
        self.heading = None  # level while inside a heading
        self.heading_tag = None  # (tag, open count) that closes a class-marked heading
        self.open = {}
        self.skip = 0

    def _flush(self):
        text = " ".join("".join(self.buf).split())
        self.buf = []
        if text:
            self.blocks[-1][2].append(text)

    def handle_starttag(self, tag, attrs):
        self.open[tag] = self.open.get(tag, 0) + 1
        if tag in self.SKIP:
            self.skip += 1
        elif self.heading:
            return  # markup inside a heading
        elif re.fullmatch(r"h[1-6]", tag):
            self._flush()
            self.heading = int(tag[1])
            self.heading_tag = (tag, self.open[tag])
        elif tag in ("p", "div") and heading_level(attrs):
            self._flush()
            self.heading = heading_level(attrs)
            self.heading_tag = (tag, self.open[tag])
        elif tag in self.BLOCK:
            self._flush()

    def _end_heading(self):
        title = " ".join("".join(self.buf).split())
        self.buf = []
        if title:
            self.blocks.append([self.heading, title, []])
        self.heading = None
        self.heading_tag = None

    def handle_endtag(self, tag):
        closing_heading = self.heading and self.heading_tag == (tag, self.open.get(tag, 0))
        self.open[tag] = max(0, self.open.get(tag, 0) - 1)
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif closing_heading:
            self._end_heading()
        elif tag in self.BLOCK and not self.heading:
            self._flush()

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)

    def close(self):
        super().close()
        self._flush()
        return [b for b in self.blocks if b[1] or b[2]]


def extract_blocks(raw):
    parser = _Extractor()
    parser.feed(raw.decode("utf-8", errors="replace"))
    return parser.close()


def _split_long(paragraphs, limit=MAX_SECTION_WORDS):
    parts, cur, n = [], [], 0
    for p in paragraphs:
        w = len(p.split())
        if cur and n + w > limit:
            parts.append(cur)
            cur, n = [], 0
        cur.append(p)
        n += w
    if cur:
        parts.append(cur)
    return parts or [[]]


def build_sections(zf, spine, toc):
    sections = []
    path = []  # heading trail: [(level, title)]
    for spine_idx, href in enumerate(spine):
        try:
            raw = zf.read(href)
        except KeyError:
            continue
        blocks = extract_blocks(raw)
        if toc.get(href):
            # A new chapter in the table of contents: start the heading trail afresh.
            # Strip a chapter number glued to the title ("1Genesis" -> "Genesis").
            path = [(1, re.sub(r"^\d+(?=[A-Za-z])", "", toc[href]))]
        for level, heading, paragraphs in blocks:
            if heading:
                path = [(lv, t) for lv, t in path if lv < level] + [(level, heading)]
            if not paragraphs and heading:
                continue  # a heading with no body text; it still shapes the trail
            title = path[-1][1] if path else (toc.get(href) or posixpath.basename(href))
            parts = _split_long(paragraphs)
            for i, part in enumerate(parts):
                text = "\n\n".join(part)
                if not text.strip():
                    continue
                sections.append({
                    "id": len(sections) + 1,
                    "spine": spine_idx,
                    "href": href,
                    "heading": title + (f" (part {i + 1} of {len(parts)})" if len(parts) > 1 else ""),
                    "path": [t for _, t in path],
                    "words": len(text.split()),
                    "text": text,
                })
    return sections


# --------------------------------------------------------------------------
# Index commands
# --------------------------------------------------------------------------
_STOP = {"the", "a", "an", "of", "on", "to", "and", "in", "for", "with", "by", "upon", "from"}


def work_slug(meta, filename):
    """Short, citable id: author surname + up to four title words, e.g. luther-commentary-epistle-galatians."""
    title = meta.get("title") or Path(filename).stem
    creator = (meta.get("creators") or [""])[0]
    if "," in creator:
        surname = creator.split(",")[0]
    else:
        parts = creator.split() or [""]
        surname = parts[-1]
        # Keep particles: "Miles V. Van Pelt" -> "Van Pelt", "Ludwig von Mises" -> "von Mises"
        if len(parts) > 2 and parts[-2].lower() in {"van", "von", "de", "der", "den", "du", "da", "di", "le", "la", "st.", "ten", "ter"}:
            surname = f"{parts[-2]} {parts[-1]}"
    words = [w for w in re.findall(r"[a-z0-9]+", title.lower()) if w not in _STOP][:4]
    s = "-".join([w for w in re.findall(r"[a-z0-9]+", surname.lower())] + words)
    return s[:60].strip("-") or "work"


def index_epub(epub_path, index_dir):
    epub_path = Path(epub_path)
    data = epub_path.read_bytes()
    with zipfile.ZipFile(epub_path) as zf:
        check_drm(zf)
        meta, spine, toc = read_package(zf)
        sections = build_sections(zf, spine, toc)

    slug = work_slug(meta, epub_path.name)
    out = Path(index_dir) / slug
    out.mkdir(parents=True, exist_ok=True)

    refs = {}
    for s in sections:
        found = find_refs(s["text"])
        for b in books_in_heading(" / ".join(s["path"])):
            refs.setdefault(b, {"heading_sections": [], "cited_in": {}})["heading_sections"].append(s["id"])
        for b, rs in found.items():
            refs.setdefault(b, {"heading_sections": [], "cited_in": {}})["cited_in"][str(s["id"])] = rs

    meta.update({
        "work": slug,
        "file": epub_path.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "spine_documents": len(spine),
        "sections": len(sections),
        "words": sum(s["words"] for s in sections),
    })
    (out / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    (out / "refs.json").write_text(json.dumps(refs, indent=1, ensure_ascii=False))
    with open(out / "sections.jsonl", "w", encoding="utf-8") as f:
        for s in sections:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    return meta


def load_works(index_dir):
    works = {}
    for meta_file in sorted(Path(index_dir).glob("*/meta.json")):
        meta = json.loads(meta_file.read_text())
        works[meta["work"]] = meta
    return works


def load_sections(index_dir, work):
    path = Path(index_dir) / work / "sections.jsonl"
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def resolve_work(index_dir, name):
    works = load_works(index_dir)
    if name in works:
        return name
    matches = [w for w in works if name.lower() in w]
    if len(matches) == 1:
        return matches[0]
    sys.exit(f"No single work matches '{name}'. Indexed works: {', '.join(works) or 'none'}")


def cmd_index(args):
    ok = 0
    for p in args.epubs:
        try:
            meta = index_epub(p, args.index)
        except DRMError as e:
            print(f"SKIPPED {p}: DRM-protected ({e}). Only DRM-free EPUBs can be indexed.", file=sys.stderr)
            continue
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
            print(f"SKIPPED {p}: not a readable EPUB ({e})", file=sys.stderr)
            continue
        ok += 1
        who = ", ".join(meta["creators"]) or "unknown author"
        print(f"indexed {meta['work']}: {meta['title']} ({who}) - {meta['sections']} sections, {meta['words']:,} words")
    if not ok:
        sys.exit(1)


def cmd_list(args):
    works = load_works(args.index)
    if not works:
        print(f"No works indexed in {args.index}/ yet. Run: python3 tools/epub_index.py index FILE.epub")
        return
    for w, m in works.items():
        who = ", ".join(m["creators"]) or "unknown author"
        extra = ", ".join(x for x in [m.get("publisher"), m.get("date", "")[:4]] if x)
        print(f"{w}\n    {m['title']} - {who}{f' ({extra})' if extra else ''}\n    {m['sections']} sections, {m['words']:,} words, from {m['file']}")


def cmd_toc(args):
    work = resolve_work(args.index, args.work)
    for s in load_sections(args.index, work):
        part = re.search(r" \(part \d+ of \d+\)$", s["heading"])
        trail = " > ".join(s["path"][-3:]) or s["heading"]
        print(f"{s['id']:>5}  {trail}{part.group(0) if part and part.group(0) not in trail else ''}  ({s['words']} words)")


def cmd_book(args):
    slug = slug_for_name(args.book) or args.book.lower().replace(" ", "-")
    if slug not in BOOK_BY_SLUG:
        sys.exit(f"Unknown Bible book '{args.book}'. Use a name like 'Genesis', '1 Samuel' or a slug like 1-samuel.")
    works = load_works(args.index)
    print(f"{BOOK_BY_SLUG[slug][1][0]}  (notes file: plugin/skills/bible-study/books/{BOOK_FILE[slug]})\n")
    for w in works:
        refs = json.loads((Path(args.index) / w / "refs.json").read_text()).get(slug)
        if not refs:
            continue
        secs = {s["id"]: s for s in load_sections(args.index, w)}
        print(f"== {w}")
        hs = refs["heading_sections"]
        if hs and len(hs) >= 0.6 * len(secs):
            print(f"   The whole work is about this book: {len(hs)} of its {len(secs)} sections. Use: toc {w}")
        elif hs:
            print(f"   Sections about this book (by heading), {len(hs)} in all:")
            for sid in hs[: args.limit]:
                s = secs[sid]
                print(f"   {w}:{sid:<6} {' > '.join(s['path'][-2:])}  ({s['words']} words)")
        cited = sorted(refs["cited_in"].items(), key=lambda kv: -len(kv[1]))
        if cited:
            total = sum(len(v) for _, v in cited)
            print(f"   Cites it {total} times in {len(cited)} sections; most often in:")
            for sid, rs in cited[: args.limit]:
                s = secs[int(sid)]
                shown = ", ".join(sorted(set(rs), key=rs.index)[:8])
                print(f"   {w}:{sid:<6} {s['heading'][:60]}  [{shown}{'...' if len(set(rs)) > 8 else ''}]")
        print()


def cmd_search(args):
    pattern = re.compile(args.query if args.regex else re.escape(args.query), re.IGNORECASE)
    works = [resolve_work(args.index, args.work)] if args.work else list(load_works(args.index))
    shown = 0
    for w in works:
        for s in load_sections(args.index, w):
            for m in pattern.finditer(s["text"]):
                a, b = max(0, m.start() - 160), min(len(s["text"]), m.end() + 160)
                snippet = " ".join(s["text"][a:b].split())
                print(f"{w}:{s['id']}  {s['heading'][:70]}\n    ...{snippet}...\n")
                shown += 1
                if shown >= args.limit:
                    print(f"(stopped at {args.limit} hits; use --limit for more)")
                    return
    if not shown:
        print("No matches.")


def cmd_show(args):
    work, _, sid = args.ref.partition(":")
    work = resolve_work(args.index, work)
    secs = {s["id"]: s for s in load_sections(args.index, work)}
    s = secs.get(int(sid)) if sid.isdigit() else None
    if not s:
        sys.exit(f"No section {sid} in {work}. See: python3 tools/epub_index.py toc {work}")
    meta = load_works(args.index)[work]
    print(f"# {meta['title']} - {', '.join(meta['creators'])}")
    print(f"# {' > '.join(s['path'])}  [{work}:{s['id']}, {s['words']} words]\n")
    for para in s["text"].split("\n\n"):
        print(textwrap.fill(html.unescape(para), width=100) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--index", default=DEFAULT_INDEX, help=f"index folder (default {DEFAULT_INDEX})")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("index", help="index one or more DRM-free EPUB files")
    p.add_argument("epubs", nargs="+")
    p.set_defaults(func=cmd_index)
    sub.add_parser("list", help="list indexed works").set_defaults(func=cmd_list)
    p = sub.add_parser("toc", help="list a work's sections")
    p.add_argument("work")
    p.set_defaults(func=cmd_toc)
    p = sub.add_parser("book", help="find each work's material on a Bible book")
    p.add_argument("book")
    p.add_argument("--limit", type=int, default=12)
    p.set_defaults(func=cmd_book)
    p = sub.add_parser("search", help="full-text search across works")
    p.add_argument("query")
    p.add_argument("--work")
    p.add_argument("--regex", action="store_true")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_search)
    p = sub.add_parser("show", help="print one section, e.g. show calvin-commentaries:42")
    p.add_argument("ref")
    p.set_defaults(func=cmd_show)
    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
