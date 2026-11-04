"""Tests for epub_index.py. Run: python3 -m unittest discover -s tools"""

import io
import json
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import epub_index as ei  # noqa: E402

CONTAINER = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""

OPF = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>A Test Commentary on Joshua</dc:title>
    <dc:creator>Henry, Matthew</dc:creator>
    <dc:language>en</dc:language>
    <dc:identifier id="id">test-1</dc:identifier>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="c1" href="text/ch%201.xhtml" media-type="application/xhtml+xml"/>
    <item id="c2" href="text/ch2.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine toc="ncx"><itemref idref="c1"/><itemref idref="c2"/></spine>
</package>"""

NCX = """<?xml version="1.0"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <navMap>
    <navPoint id="n1"><navLabel><text>Introduction to Joshua</text></navLabel><content src="text/ch%201.xhtml"/></navPoint>
    <navPoint id="n2"><navLabel><text>Chapter Two</text></navLabel><content src="text/ch2.xhtml"/></navPoint>
  </navMap>
</ncx>"""

CH1 = """<html xmlns="http://www.w3.org/1999/xhtml"><head><title>x</title><style>p{}</style></head><body>
<p>Joshua succeeds Moses (Deut. 34:9). Compare Heb. iv. 8 and Heb 11:31.</p>
<p>There is 1 lesson here and I am 5 times more sure of it.</p>
</body></html>"""

CH2 = """<html xmlns="http://www.w3.org/1999/xhtml"><body>
<h2>Rahab and the spies</h2><p>Rahab hid the spies and hung the scarlet cord (Josh. 2:18).</p>
<h3>The cord</h3><p>The scarlet cord recalls the Passover blood (Ex. 12:13).</p>
</body></html>"""


def make_epub(path, extra=None, drop=()):
    files = {
        "mimetype": "application/epub+zip",
        "META-INF/container.xml": CONTAINER,
        "OEBPS/content.opf": OPF,
        "OEBPS/toc.ncx": NCX,
        "OEBPS/text/ch 1.xhtml": CH1,
        "OEBPS/text/ch2.xhtml": CH2,
    }
    files.update(extra or {})
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in files.items():
            if name not in drop:
                zf.writestr(name, data)
    return path


def encryption_xml(algorithm, uri):
    return f"""<encryption xmlns="urn:oasis:names:tc:opendocument:xmlns:container"
      xmlns:enc="http://www.w3.org/2001/04/xmlenc#">
      <enc:EncryptedData><enc:EncryptionMethod Algorithm="{algorithm}"/>
      <enc:CipherData><enc:CipherReference URI="{uri}"/></enc:CipherData></enc:EncryptedData>
    </encryption>"""


class RefTests(unittest.TestCase):
    def test_references(self):
        refs = ei.find_refs("Gen. 3:15; 1 Sam 17; Ps 23:1-4; John 3.16; Rom. viii. 28; Heb. 11, 2 Cor 5:17")
        self.assertEqual(refs, {
            "genesis": ["3:15"], "1-samuel": ["17"], "psalms": ["23:1"], "john": ["3:16"],
            "romans": ["8:28"], "hebrews": ["11"], "2-corinthians": ["5:17"],
        })

    def test_prose_is_not_a_reference(self):
        self.assertEqual(ei.find_refs("There is 1 thing; I am 5; a job 3; mark 4 times; Is 6 alone"), {})
        self.assertEqual(ei.find_refs("Is 6:3 and Am 5:24"), {"isaiah": ["6:3"], "amos": ["5:24"]})

    def test_numbered_books_beat_plain_names(self):
        self.assertEqual(ei.find_refs("1 John 4:8 and John 4:8"), {"1-john": ["4:8"], "john": ["4:8"]})

    def test_publisher_abbreviations(self):
        self.assertEqual(ei.find_refs("Cf Dt 1:6; Jsh 24:2; 1Sm 17:45; Rv 21:4; Ac 2:38; Ac 2"), {
            "deuteronomy": ["1:6"], "joshua": ["24:2"], "1-samuel": ["17:45"], "revelation": ["21:4"], "acts": ["2:38"],
        })

    def test_combined_book_headings(self):
        self.assertEqual(ei.books_in_heading("1\u20132 Samuel"), ["1-samuel", "2-samuel"])
        self.assertEqual(ei.books_in_heading("1\u20133 John"), ["1-john", "2-john", "3-john"])
        self.assertEqual(ei.books_in_heading("Ezra\u2013Nehemiah"), ["ezra", "nehemiah"])
        self.assertEqual(ei.books_in_heading("1 and 2 Samuel"), ["1-samuel", "2-samuel"])
        self.assertEqual(len(ei.books_in_heading("The Twelve")), 12)

    def test_headings(self):
        self.assertEqual(ei.books_in_heading("The First Epistle of John"), ["1-john"])
        self.assertEqual(ei.books_in_heading("The Second Book of the Kings"), ["2-kings"])
        self.assertEqual(ei.books_in_heading("THE BOOK OF GENESIS"), ["genesis"])
        self.assertEqual(ei.books_in_heading("Introduction to Joshua"), ["joshua"])
        self.assertEqual(ei.books_in_heading("Preface"), [])


class EpubTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.index = self.tmp / "index"

    def test_index_search_and_book(self):
        meta = ei.index_epub(make_epub(self.tmp / "t.epub"), self.index)
        self.assertEqual(meta["work"], "henry-test-commentary-joshua")
        self.assertEqual(meta["creators"], ["Henry, Matthew"])
        work = self.index / meta["work"]
        sections = [json.loads(line) for line in (work / "sections.jsonl").read_text().splitlines()]
        # The first chapter has no heading, so it takes its title from the NCX.
        self.assertEqual(sections[0]["path"], ["Introduction to Joshua"])
        # Each file starts from its own table-of-contents entry.
        self.assertEqual(sections[-1]["path"], ["Chapter Two", "Rahab and the spies", "The cord"])
        self.assertNotIn("p{}", sections[0]["text"])  # <style> is skipped
        refs = json.loads((work / "refs.json").read_text())
        self.assertIn("1", refs["deuteronomy"]["cited_in"])
        self.assertEqual(refs["hebrews"]["cited_in"]["1"], ["4:8", "11:31"])
        self.assertEqual(refs["exodus"]["cited_in"][str(sections[-1]["id"])], ["12:13"])
        self.assertTrue(refs["joshua"]["heading_sections"])
        self.assertNotIn("isaiah", refs)
        self.assertNotIn("amos", refs)

        out = io.StringIO()
        with redirect_stdout(out):
            ei.main(["--index", str(self.index), "search", "scarlet cord"])
        self.assertIn("henry-test-commentary-joshua:", out.getvalue())
        out = io.StringIO()
        with redirect_stdout(out):
            ei.main(["--index", str(self.index), "book", "Exodus"])
        self.assertIn("12:13", out.getvalue())

    def test_class_marked_headings(self):
        ch = """<html xmlns="http://www.w3.org/1999/xhtml"><body>
        <p class="chtit">Genesis</p><p class="head2">The <i>Fall</i></p><p class="indent">Text about Gen. 3:15.</p>
        <div class="ct">Genesis Study Notes</div><p class="cn">Genesis 3</p><p class="fn">3:15 First gospel.</p>
        </body></html>"""
        meta = ei.index_epub(make_epub(self.tmp / "cls.epub", {"OEBPS/text/ch2.xhtml": ch}), self.index)
        lines = (self.index / meta["work"] / "sections.jsonl").read_text().splitlines()
        sections = [json.loads(line) for line in lines]
        self.assertEqual(sections[-2]["path"], ["Genesis", "The Fall"])
        self.assertEqual(sections[-1]["path"], ["Genesis Study Notes", "Genesis 3"])
        refs = json.loads((self.index / meta["work"] / "refs.json").read_text())
        self.assertEqual(len(refs["genesis"]["heading_sections"]), 2)

    def test_adobe_drm_is_refused(self):
        epub = make_epub(self.tmp / "drm.epub", {"META-INF/rights.xml": "<rights/>"})
        with self.assertRaises(ei.DRMError):
            ei.index_epub(epub, self.index)

    def test_encrypted_content_is_refused(self):
        enc = encryption_xml("http://www.w3.org/2001/04/xmlenc#aes128-cbc", "OEBPS/text/ch2.xhtml")
        epub = make_epub(self.tmp / "enc.epub", {"META-INF/encryption.xml": enc})
        with self.assertRaises(ei.DRMError):
            ei.index_epub(epub, self.index)

    def test_font_obfuscation_is_allowed(self):
        enc = encryption_xml("http://www.idpf.org/2008/embedding", "OEBPS/fonts/a.otf")
        meta = ei.index_epub(make_epub(self.tmp / "font.epub", {"META-INF/encryption.xml": enc}), self.index)
        self.assertGreater(meta["sections"], 0)


if __name__ == "__main__":
    unittest.main()
