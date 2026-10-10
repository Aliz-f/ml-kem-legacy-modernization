#!/usr/bin/env python3
"""Build the consolidated technical-document PDF from its Markdown chapters."""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "technical-document"
OUTPUT = DOCS / "technical-document.pdf"
CHAPTERS = sorted(DOCS.glob("[0-9][0-9]-*.md"))
TITLE = (
    "Gateway-Based Post-Quantum Modernization of a Legacy Edge–Cloud System: "
    "Security Operations and Residual Risks"
)
MEMBERS = ("Alireza Fadaei", "Roope Paananen", "Armin Shalchian", "Masoud Abrishami", "Dorsa Abdolmaleki")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TABLE_DIVIDER = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
IMAGE = re.compile(r"^!\[([^]]*)\]\(([^)]+)\)\s*$")
EXISTING_TABLE_CAPTION = re.compile(r"^\*\*Table\s+\d+\.\d+:\s*(.*?)\*\*$")
NUMBERED_LANGUAGES = {"python", "bash", "docker", "dockerfile"}
APPENDIX_REFERENCE = re.compile(r"\bAppendix\s+([A-F](?:\.\d+)*)\b")
RENDERED_TABLE = re.compile(
    r'(<table>.*?)(</table>)\s*<div class="table-caption">(.*?)</div>', re.DOTALL
)
RENDERED_CODE = re.compile(
    r'(<div class="code-caption">.*?</div>)\s*(<pre.*?</pre>)', re.DOTALL
)


def slugify(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def section_label(text: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\s+", "", text).strip()


def image_label(alt: str) -> str:
    name = Path(alt).stem.replace("_", " ")
    return re.sub(r"^chapter\s+\d+\s*-\s*", "", name, flags=re.I) or "System diagram"


def heading_label(text: str) -> str:
    """Remove Markdown emphasis markers from headings rendered as raw HTML."""
    return text.replace("**", "").replace("__", "")


def numbered_code(lines: list[str], language: str) -> str:
    """Return a code block with visual line numbers for executable examples."""
    numbered_lines = "".join(
        f'<span class="code-line"><span class="line-number">{number}</span>{html.escape(line)}</span>\n'
        for number, line in enumerate(lines, start=1)
    )
    return f'<pre class="numbered-code"><code class="language-{language}">{numbered_lines}</code></pre>'


def appendix_targets() -> dict[str, str]:
    """Map every Chapter 8 appendix heading to its generated fragment id."""
    targets: dict[str, str] = {}
    for line in CHAPTERS[-1].read_text(encoding="utf-8").splitlines():
        match = HEADING.match(line)
        if not match:
            continue
        title = heading_label(match.group(2))
        appendix = re.match(r"Appendix\s+([A-F])(?:\s|:)", title)
        subsection = re.match(r"([A-F](?:\.\d+)+)\b", title)
        reference = f"Appendix {appendix.group(1)}" if appendix else (
            f"Appendix {subsection.group(1)}" if subsection else None
        )
        if reference:
            targets[reference] = slugify(title)
    return targets


def link_appendix_references(line: str, targets: dict[str, str]) -> str:
    """Convert prose Appendix references to same-document PDF links."""
    def replacement(match: re.Match[str]) -> str:
        reference = f"Appendix {match.group(1)}"
        target = targets.get(reference)
        if not target:
            return match.group(0)
        return f'<a class="appendix-reference" href="#{target}">{reference}</a>'

    return APPENDIX_REFERENCE.sub(replacement, line)


def preprocess(source: Path, chapter: int, targets: dict[str, str]) -> tuple[str, list[tuple[int, str, str]]]:
    """Add rendering-only anchors and sequential caption blocks."""
    lines = source.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    contents: list[tuple[int, str, str]] = []
    identifiers: set[str] = set()
    section = f"Chapter {chapter}"
    figures = tables = listings = 0
    index = 0
    fence = ""
    while index < len(lines):
        line = lines[index]
        if fence:
            out.append(line)
            if line.startswith(fence):
                fence = ""
            index += 1
            continue
        if line.startswith(("```", "~~~")):
            listings += 1
            language = line[3:].strip() or "text"
            language = "plaintext" if language == "text" else language
            out += [
                f'<div class="code-caption">Code Listing {chapter}.{listings} — {html.escape(section_label(section))} ({html.escape(language)})</div>',
            ]
            if language in NUMBERED_LANGUAGES:
                fence_marker = line[:3]
                code_start = index + 1
                code_end = code_start
                while code_end < len(lines) and not lines[code_end].startswith(fence_marker):
                    code_end += 1
                if code_end == len(lines):
                    raise ValueError(f"Unclosed {fence_marker} code fence in {source}")
                out.append(numbered_code(lines[code_start:code_end], language))
                index = code_end + 1
                continue
            fence = line[:3]
            out.append(line)
            index += 1
            continue
        match = HEADING.match(line)
        if match:
            level, title = len(match.group(1)), heading_label(match.group(2))
            identifier = slugify(title)
            duplicate = 2
            while identifier in identifiers:
                identifier = f"{slugify(title)}-{duplicate}"
                duplicate += 1
            identifiers.add(identifier)
            section = title
            contents.append((level, title, identifier))
            out += [f'<h{level} id="{identifier}">{html.escape(title)}</h{level}>', ""]
            index += 1
            continue
        match = IMAGE.match(line)
        if match:
            figures += 1
            alt, src = match.groups()
            out += [
                '<figure class="figure">',
                f'<figcaption>Figure {chapter}.{figures} — {html.escape(image_label(alt))}</figcaption>',
                f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}">',
                "</figure>", "",
            ]
            index += 1
            continue
        if index + 1 < len(lines) and "|" in line and TABLE_DIVIDER.match(lines[index + 1]):
            tables += 1
            caption = section_label(section)
            previous = next((item for item in reversed(out) if item.strip()), "")
            old_caption = EXISTING_TABLE_CAPTION.match(previous)
            if old_caption:
                caption = old_caption.group(1)
                out.remove(previous)
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                out.append(lines[index])
                index += 1
            out += ["", f'<div class="table-caption">Table {chapter}.{tables} — {html.escape(caption)}</div>', ""]
            continue
        out.append(link_appendix_references(line, targets))
        index += 1
    return "\n".join(out), contents


def toc(entries: list[tuple[int, str, str]]) -> str:
    return "\n".join(
        f'<li class="toc-level-{min(level, 4)}"><a href="#{identifier}">{html.escape(title)}</a></li>'
        for level, title, identifier in entries
    )


def build_html() -> tuple[str, tuple[int, int, int]]:
    rendered_chapters: list[str] = []
    entries: list[tuple[int, str, str]] = []
    targets = appendix_targets()
    for number, source in enumerate(CHAPTERS, start=1):
        chapter, chapter_entries = preprocess(source, number, targets)
        rendered = markdown.markdown(chapter, extensions=["extra", "sane_lists"])
        rendered = RENDERED_TABLE.sub(r'\1<caption class="table-caption">\3</caption>\2', rendered)
        rendered = RENDERED_CODE.sub(r'<div class="code-figure">\1\2</div>', rendered)
        if number == 8:
            appendix_links = [entry for entry in chapter_entries if entry[0] == 2 and entry[1].startswith("Appendix ")]
            navigation = '<nav class="appendix-links"><strong>Appendix navigation</strong><ul>' + "".join(
                f'<li><a href="#{identifier}">{html.escape(title)}</a></li>'
                for _, title, identifier in appendix_links
            ) + "</ul></nav>"
            rendered = rendered.replace("</h1>", "</h1>" + navigation, 1)
        rendered_chapters.append('<section class="chapter">' + rendered + "</section>")
        entries.extend(chapter_entries)
    body = "\n".join(rendered_chapters)
    document = TEMPLATE.format(
        title=html.escape(TITLE),
        members=html.escape(", ".join(MEMBERS)),
        toc=toc(entries),
        body=body,
    )
    return document, (body.count('class="figure"'), body.count('class="table-caption"'), body.count('class="code-caption"'))


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>
@page {{ size: A4; margin: 21mm 18mm 20mm; @bottom-center {{ content: counter(page); font: 9pt serif; }} }}
* {{ box-sizing: border-box; }}
body {{ color: #17212b; font-family: Georgia, 'Times New Roman', serif; font-size: 10pt; line-height: 1.35; }}
.title-page {{ background: linear-gradient(145deg, #f3f8fa, #ffffff 62%); border-bottom: 3mm solid #0b3954; border-top: 8mm solid #0b3954; display: flex; flex-direction: column; justify-content: center; min-height: 246mm; padding: 14mm; position: relative; text-align: center; page-break-after: always; }}
.title-page h1 {{ color: #0b3954; font-size: 25pt; line-height: 1.25; margin: 0 auto 20mm; max-width: 155mm; }}
.title-page h2 {{ color: #0b3954; font-size: 16pt; letter-spacing: 0.4pt; margin: 0 0 6mm; }} .title-page p {{ font-size: 11pt; margin: 2mm 0; }} .title-page .cover-details {{ background: #ffffff; border: 0.4pt solid #b7c8d2; border-radius: 2mm; box-shadow: 0 1mm 3mm #d5e0e5; margin: 0 auto; max-width: 145mm; padding: 7mm 10mm; }} .title-page .members {{ font-size: 8.5pt; line-height: 1.45; margin: 0 auto; max-width: 135mm; white-space: nowrap; }} .title-page a {{ color: #0b3954; }}
.toc {{ page-break-after: always; }} .toc h1 {{ color: #0b3954; font-size: 21pt; }} .toc ul {{ list-style: none; margin: 0; padding: 0; }} .toc li {{ margin: 2.2mm 0; }} .toc a {{ color: #0b3954; text-decoration: none; }}
.toc-level-1 {{ font-size: 12pt; font-weight: bold; margin-top: 4mm !important; }} .toc-level-2 {{ margin-left: 7mm !important; }} .toc-level-3 {{ margin-left: 14mm !important; font-size: 9.4pt; }} .toc-level-4 {{ margin-left: 21mm !important; font-size: 9pt; }}
.chapter {{ break-before: page; page-break-before: always; }} .chapter:first-of-type {{ break-before: auto; page-break-before: auto; }}
h1, h2, h3, h4, h5, h6 {{ color: #0b3954; page-break-after: avoid; }} h1 {{ font-size: 20pt; border-bottom: 1px solid #89a9bc; padding-bottom: 2mm; }} h2 {{ font-size: 15pt; margin-top: 6mm; }} h3 {{ font-size: 12pt; margin-top: 4mm; }} h4 {{ font-size: 10.5pt; margin-top: 3mm; }}
p, li {{ orphans: 3; widows: 3; }} figure, .code-figure {{ break-inside: avoid; page-break-inside: avoid; }} figure {{ margin: 4mm auto; max-width: 100%; text-align: center; }} figcaption, .code-caption {{ color: #0b3954; font-family: Arial, sans-serif; font-size: 9pt; font-weight: bold; margin-bottom: 2mm; text-align: center; }} figure img {{ display: block; margin: 0 auto; max-height: 178mm; max-width: 100%; object-fit: contain; }}
table {{ border-collapse: collapse; font-family: Arial, sans-serif; font-size: 8pt; margin: 3mm auto 5mm; max-width: 100%; width: 100%; }} th, td {{ border: 0.3pt solid #8fa6b5; padding: 1.4mm; vertical-align: top; }} th {{ background: #dce9ef; color: #0b3954; }} .table-caption {{ caption-side: bottom; color: #0b3954; font-family: Arial, sans-serif; font-size: 9pt; font-style: italic; margin-top: 1.5mm; text-align: center; }}
pre {{ background: #f3f6f8; border: 0.4pt solid #b7c8d2; border-left: 3pt solid #2d6a8c; font-size: 7.4pt; line-height: 1; margin: 0; overflow-wrap: anywhere; padding: 2mm; white-space: pre-wrap; }} code {{ font-family: 'DejaVu Sans Mono', 'Liberation Mono', monospace; }} p code, li code, td code {{ background: #f0f3f5; padding: 0.2mm 0.6mm; }} .code-caption {{ margin: 4mm 0 1.5mm; }} .code-line {{ display: block; line-height: 1; }} .line-number {{ color: #607080; display: inline-block; margin-right: 2mm; text-align: right; user-select: none; width: 7mm; }} .appendix-links {{ background: #f3f6f8; border-left: 3pt solid #2d6a8c; margin: 5mm 0; padding: 3mm 5mm; }} .appendix-links ul {{ columns: 2; margin: 2mm 0 0; }} .appendix-links a {{ color: #0b3954; }} blockquote {{ border-left: 2pt solid #89a9bc; margin-left: 0; padding-left: 4mm; }}
</style></head><body>
<section class="title-page"><h1>{title}</h1><div class="cover-details"><h2>Group 20</h2><p><strong>Institution:</strong> University of Oulu</p><p><strong>Course:</strong> Software Development, Maintenance &amp; Operations</p><p><strong>Repository:</strong> <a href="https://github.com/Aliz-f/ml-kem-legacy-modernization">github.com/Aliz-f/ml-kem-legacy-modernization</a></p><h2>Members</h2><p class="members">{members}</p></div></section>
<nav class="toc"><h1>Contents</h1><ul>{toc}</ul></nav>
{body}
</body></html>"""


def main() -> int:
    if not CHAPTERS:
        raise SystemExit(f"No numbered Markdown chapters found in {DOCS}")
    document, counts = build_html()
    with tempfile.TemporaryDirectory(prefix="technical-document-") as temporary:
        # The HTML needs to sit next to the Markdown assets while Chromium
        # resolves their relative image paths.  Keep its generated filename
        # unique, then remove it immediately after rendering.
        source = DOCS / f".technical-document-render-{Path(temporary).name}.html"
        source.write_text(document, encoding="utf-8")
        try:
            subprocess.run(["chromium", "--headless", "--no-sandbox", "--disable-gpu", f"--print-to-pdf={OUTPUT}", "--no-pdf-header-footer", source.as_uri()], check=True)
        finally:
            source.unlink(missing_ok=True)
    if not OUTPUT.is_file() or not OUTPUT.stat().st_size:
        raise SystemExit("Chromium did not produce a non-empty PDF")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(f"Captioned {counts[0]} figures, {counts[1]} tables, and {counts[2]} code listings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
