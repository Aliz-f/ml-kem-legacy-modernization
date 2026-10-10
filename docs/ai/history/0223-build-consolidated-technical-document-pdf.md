# AI Task 0223 — Build consolidated technical-document PDF

**Status:** Complete

**Created:** 2026-10-10T15:15:56+03:00

**Updated:** 2026-10-10T16:11:21+03:00

**Agent:** Codex

---

# Task

Create one PDF from docs/technical-document Markdown chapters with the supplied title page, linked index, and chapter-scoped sequential figure, table, and code captions. Add only the renderer and generated PDF artifacts required for this documentation deliverable; do not change application or protocol behavior.

---

# Prompt

I want to create a single pdf file from these md files. the files should follow these rules: 1- first page should have teams name, project title and group number members: Alireza Fadaei, Roope Paananen, Armin Shalchian, Masoud Abrishami, Dorsa Abdolmaleki projec title: Gateway-Based Post-Quantum Modernization of a Legacy Edge–Cloud System: Security Operations and Residual Risks group number: 20 2- index that should have active link to each chapter and subsections 3- table captions with sequencial ordering (with chapter number) at the bottom of the table 4- figure caption above the figure which equencial ordering (with chapter number) 5- code caption above the code box with sequencial ordersing includes chapter

---

# AI Implementation — Initial

## LLM Output

Added a reproducible Markdown-to-PDF renderer and generated the consolidated technical document with the supplied Group 20 cover page, linked contents, and chapter-scoped figure, table, and code-listing captions.

## Files Created

- docs/ai/history/0223-build-consolidated-technical-document-pdf.md
- docs/technical-document/technical-document.pdf
- scripts/build_technical_document.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- python scripts/build_technical_document.py; UV_CACHE_DIR=/tmp/ml-kem-doc-uv-cache uv run ruff check scripts/build_technical_document.py; qpdf --check docs/technical-document/technical-document.pdf; pdftohtml -f 2 -l 2 -xml -hidden docs/technical-document/technical-document.pdf /tmp/technical-document.xml

### Results

- Generated a 99-page A4 PDF (16,801,141 bytes) with 14 figures, 25 tables, and 57 code listings captioned. Ruff and qpdf passed; the extracted contents page has 32 active PDF link annotations.

## AI Notes

Chromium Snap rendering requires normal system runtime permissions in this environment. The renderer leaves the Markdown chapters unchanged and removes its temporary HTML after rendering.

---

# Human Review — Round 1

## Problems Found

Table 1.3 caption appeared on the following page. The cover page lacked the institution, course, report link, and list-form member names. Captions were not centered. Appendix navigation needed explicit hyperlinks. Python, Bash, and Docker listings lacked line numbers. The PDF needs an audit for literal bold asterisks, denser page flow, and plaintext instead of text in code captions.

## Decision

Modified

## Requested Modifications

Keep every table caption with its table; add the requested cover-page fields and member list; center captions; add appendix hyperlinks; add line numbers to Python, Bash, and Docker code listings; remove literal Markdown bold markers outside code; reduce unused whitespace while permitting block splitting; and rename text code-caption languages to plaintext.

---

# AI Revision — Round 1

## Revision Summary

Revised the PDF renderer and regenerated the technical document: table captions are internal bottom table captions; the cover now includes the requested University, course, report link, and member list; captions are centered; appendix quick links are included; Python/Bash/Docker listings have line numbers; text labels are plaintext; heading emphasis markers are removed; and forced chapter page breaks were removed to reduce whitespace.

## Files Created

- docs/ai/history/0223-build-consolidated-technical-document-pdf.md
- docs/technical-document/technical-document.pdf
- scripts/build_technical_document.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- python scripts/build_technical_document.py; UV_CACHE_DIR=/tmp/ml-kem-doc-uv-cache uv run ruff check scripts/build_technical_document.py; qpdf --check docs/technical-document/technical-document.pdf; pdftotext -layout docs/technical-document/technical-document.pdf /tmp/technical-document-final.txt; pdftohtml -xml -hidden docs/technical-document/technical-document.pdf /tmp/final-links.xml

### Results

- Generated a 90-page A4 PDF (17,017,688 bytes). Ruff and qpdf passed. It contains 14 figure captions, 25 in-table bottom captions, 57 code captions, 11 plaintext labels, line numbers on Python/Bash/Docker listings, a linked report URL, and linked appendix entries. The only literal double asterisk is valid Python **fields syntax in a code listing.

## AI Notes

Chromium Snap rendering requires normal system runtime permissions in this environment. The renderer removes its temporary HTML after rendering.

---

# Human Review — Round 2

## Problems Found

The cover members must be displayed on one comma-separated line, the report label must be Repository, the cover needs stronger visual presentation, captions above figures and code blocks must remain on the same page as the block, and code-block line spacing must be tighter.

## Decision

Modified

## Requested Modifications

Display the member names in one comma-separated line; change Report to Repository; improve the cover-page visual design; keep above-block captions with their figures/code blocks during pagination; and minimize code-block line spacing.

---

# AI Revision — Round 2

## Revision Summary

Completed the second requested PDF revision: the cover has a one-line comma-separated member list, a Repository link, and enhanced visual styling; top captions are kept with figures and code blocks; and code listings use compact line spacing.

## Files Created

- docs/ai/history/0223-build-consolidated-technical-document-pdf.md
- docs/technical-document/technical-document.pdf
- scripts/build_technical_document.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- python scripts/build_technical_document.py; UV_CACHE_DIR=/tmp/ml-kem-doc-uv-cache uv run ruff check scripts/build_technical_document.py; qpdf --check docs/technical-document/technical-document.pdf; pdftotext -layout docs/technical-document/technical-document.pdf /tmp/technical-document-second-revision.txt

### Results

- Generated a valid 90-page A4 PDF (17,027,073 bytes). Ruff and qpdf passed. Visual inspection confirmed the one-line cover member list, Repository label/link, caption-plus-block pagination, and compact numbered Python listing spacing.

## AI Notes

Chromium Snap rendering requires normal system runtime permissions in this environment. The renderer removes its temporary HTML after rendering.

---

# Human Review — Round 3

## Problems Found

Chapters need to begin on fresh pages, and Appendix references in the report prose need active links to their corresponding Chapter 8 sections.

## Decision

Modified

## Requested Modifications

Restore a fresh-page start for each chapter and make Appendix A–F/subsection references in the text active internal links to the matching Appendix targets in Chapter 8.

---

# AI Revision — Round 3

## Revision Summary

Restored a fresh-page start for every chapter and added same-document hyperlinks for Appendix A–F and subsection references in prose, targeting the corresponding Chapter 8 headings.

## Files Created

- docs/ai/history/0223-build-consolidated-technical-document-pdf.md
- docs/technical-document/technical-document.pdf
- scripts/build_technical_document.py

## Files Modified

- docs/ai/.state.json

## Files Deleted

- None

## AI-Executed Verification

### Commands

- python scripts/build_technical_document.py; UV_CACHE_DIR=/tmp/ml-kem-doc-uv-cache uv run ruff check scripts/build_technical_document.py; qpdf --check docs/technical-document/technical-document.pdf; pdftotext -layout docs/technical-document/technical-document.pdf /tmp/technical-document-final.txt; qpdf --qdf --object-streams=disable docs/technical-document/technical-document.pdf /tmp/technical-document-qdf.pdf

### Results

- Generated a valid 95-page A4 PDF (17,045,898 bytes). Ruff and qpdf passed. Chapter starts were verified on pages 7, 12, 22, 28, 36, 51, 62, and 69. The generated HTML contains 13 Appendix-reference anchors and the PDF has 197 link annotations.

## AI Notes

Chromium Snap rendering requires normal system runtime permissions in this environment. The renderer removes its temporary HTML after rendering.

---

# Human Review — Round 4

## Problems Found

No problems found during human review.

## Decision

Accepted

---

# Final Verification

## AI-Executed Verification

- qpdf validation, Ruff, generated link, pagination, caption, and visual checks were completed before human verification.

## Human-Confirmed Verification

User stated: i verify it

---

# Final Outcome

**Status:** Complete
