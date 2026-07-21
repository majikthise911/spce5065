---
name: project_presentation_pipeline
description: Current-event presentation format (5-10 min video) and the reusable slide-build pipeline in presentation/
metadata:
  type: project
---

**Current-event presentations (SPCE 5065):** each student gives a 5 to 10 minute talk on a current event tied to the week's material (syllabus, 5% of grade). Delivered either as a video sent to the instructor OR live on the class Zoom. Two grader-visible example decks live in `wk05/course_material/` (Ron Smetek China debris; Claire Wadman MMOD); both follow the arc hook current event -> physics -> design/mitigation -> AIAA references. Topic assignment is in `presentation/topic.txt`.

**First one done (July 2026): the vacuum environment**, angled on **cold welding of deployable mechanisms**. Anchor current event = **ASTROBEAT** (Nov 2024 ISS experiment using cold welding on purpose to repair debris damage). Told Galileo HGA honestly (primary cause was MoS2 lubricant loss + fretting from truck transport, cold welding secondary; it never got a TVAC test) and used NASA Lucy (lanyard, NOT cold welding) as the anti-hype counterexample. Course tie-in: Chapter 6 "atomically clean surface" (oxide/adsorbed monolayers stripped in vacuum -> bare metal bonds).

**Reusable build pipeline** (in `presentation/`, all Python):
- `deck_content.py` = single source of truth: `SLIDES` (title/kind/bullets/figure/notes) + `REFERENCES` (AIAA, numbered by first appearance). `notes` field is the spoken narration, reused as PPTX speaker notes.
- `make_figures.py` -> matplotlib figures into `figures/`, dark theme (surface #1a1a19, blue accent #3987e5), single-hue magnitude so no CVD issues.
- `build_html.py` -> single self-contained `.html` deck (figures base64-inlined, arrow-key nav, F for fullscreen). Verified via headless Chrome screenshot.
- `build_pptx.py` -> editable 16:9 `.pptx` via python-pptx (installed --user). Verified by converting to PDF with `/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf` then reading the PDF.
- Standalone timed reading script: `spce_5065_vacuum_environment_script.md`.

**Real photos:** sourced public-domain NASA imagery via the images-api.nasa.gov search+asset endpoints (curl/urllib), saved to `presentation/img/`, each one VISUALLY INSPECTED before use (several API results were mislabeled: an "ISS" hit was a ground truss, an "HVI test" hit was an astronaut portrait). Slides carry an on-slide `credit` ("Image: NASA/..."). Builders support `image`+`credit` on bullet slides (split layout) and a `hero`+`credit` on the title (right-panel in PPTX, full-bleed with left dark gradient in HTML). Vacuum deck uses: ISS in-orbit (title+hook), Galileo furled HGA, Lucy solar array, WSTF hypervelocity impact plate, JSC thermal-vacuum Chamber A.

**3D animations:** not feasible cleanly in a .pptx / static deck and licensed clips are a copyright risk, so use real stills instead.

**QA before delivery:** grep every deliverable for em/en dashes (hard rule [[feedback_no_em_dashes]]) and instructor mentions [[feedback_no_professor_mentions]]; renumber AIAA refs by first appearance [[feedback_references]]. To reuse for the next presentation, edit `deck_content.py` + `make_figures.py` and re-run the two builders.
