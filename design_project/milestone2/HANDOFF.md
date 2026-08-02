# HANDOFF: SPCE 5065 Milestone 2, STK simulation task

**Written:** 2 Aug 2026, at the end of a macOS session.
**For:** a fresh Claude Code session on Jordan's **Windows** machine.
**Why the machine change:** STK desktop is Windows x86-64 only. The previous session ran on
an Apple Silicon M4, where STK cannot be installed.

Read this whole file before doing anything.

---

## 1. TL;DR for the new session

Milestone 2 of the SPCE 5065 design project is **written, verified, and complete except for
one thing**: the graduate-requirement STK simulation. Everything else (report, figures,
analysis script, docx) is finished and pushed to GitHub.

**Your job:** build the MESA scenario in STK, produce three stills plus the scenario file,
and wire them into Section 12 of the report as Figures 9 through 11.

**Do not rewrite the report.** It has been through a full verification pass. Only add the
STK content and touch the specific lines called out in Section 7 below.

---

## 2. Course and project context

- **Course:** SPCE 5065, Space Environment Interactions, UCCS, Summer 2026
- **Project:** semester-long design project, three deliverables (Milestone 1, Milestone 2,
  Final Report). Each is **cumulative**: MS2 contains a corrected MS1 plus new work, and the
  final report will contain a corrected MS2 plus more.
- **The mission:** **MESA (Mission Extension and Servicing Asset)**, a ~2,000 kg
  geostationary satellite-servicing tug patterned on Northrop Grumman's Mission Extension
  Vehicle. It docks with client comsats at GEO, takes over their stationkeeping, refuels
  them, and tows them to and from the graveyard orbit. Five-year life, $100M budget.
- **Milestone 2 is late.** The sheet said 29 July; it is now 2 August. Getting it submitted
  matters more than polishing it further.

### Milestone 1 was graded 92/100

This drives most of Milestone 2's structure. The deductions and the grader's handwritten
margin comments:

| Item | Score | Comment |
|:---|:---|:---|
| Sun-Earth risks (§2) | 9/10 | "write in paragraph form" (the risk lists were bullets) |
| Space weather (§3) | 13/15 | "describe more" (bracketed on the monitoring paragraph) |
| **Visual simulation (§6)** | **3/5** | **"Do you have a 3D source? If not, I can recommend a few."** |
| Grammar | 7/10 | "TOC set up incorrectly", "spell out numbers ≤10", "use better transitions between sections" |
| Everything else | full marks | including "I like the analogy" on the MESA name |

The graded PDFs are in `design_project/milestone1/graded/`.

**The §6 comment is why you are doing this task.** A 2D matplotlib plot did not satisfy
"visual simulation." The MS2 grad requirement is written in STK's own menu language, and
the MS1 assignment sheet says STK is "available through UCCS IT and is highly recommended."
So STK is what she wants.

---

## 3. Getting the repo on Windows

Everything is committed and pushed to `git@github.com:majikthise911/spce5065.git`, branch
`main`.

```bash
git clone git@github.com:majikthise911/spce5065.git
cd spce5065
git pull            # if already cloned
```

**Note:** the repo is ~880 MB (429 MB of `.git`, mostly committed Canvas course PDFs and
PPTX). The clone will take a few minutes. This is also why cloud/remote agent sessions fail
on this repo with "repo too large to teleport."

**Read `CLAUDE.md` at the repo root first.** It defines project conventions. Critically:
**project memory lives in `./memory/` inside the repo**, not in the machine-local
`~/.claude/projects/.../memory/` folder, precisely so it survives a machine change like this
one. Read `./memory/MEMORY.md` (the index) and then the relevant files.

---

## 4. Where Milestone 2 stands

Everything lives in `design_project/milestone2/submission/`.

| File | Status |
|:---|:---|
| `Clayton_spce5065_ms2_submission.md` | **Complete.** ~8,700 words, 13 sections, cumulative |
| `Clayton_spce5065_ms2_submission.docx` | **Complete.** Built with pandoc, 9 images, Word TOC field |
| `spce5065_ms2_figs.py` | **Complete.** Computes every number in the report, writes Figures 2 and 4 to 8 |
| `figures/` | fig0 through fig8, all current |
| `STK_MESA_scenario_guide.md` | **The build guide for your task.** Read it |
| `stk/` | Empty. Put the scenario and stills here |

### The report's section structure

Sections 1 to 7 are the corrected Milestone 1. Sections 8 to 13 are new:

- **§8** Vehicle definition + thermal control (equilibrium temps in sun and eclipse)
- **§9** Plasma (risks, mitigations, subsystem impact)
- **§10** Radiation (risks, mitigations, subsystem impact)
- **§11** ADACS (four disturbance torques, actuator sizing)
- **§12** Simulations (power, torque, mission life) **← your work goes here**
- **§13** Conclusions

### Verification already done, do not redo

- Citations run **strictly ascending 1 to 17 by first appearance**, none uncited. This is an
  AIAA rule the grader has docked points for before. **If you add a reference, it must go at
  the position of first appearance and everything after renumbers.**
- **Zero em dashes and en dashes** in the entire document. Hard user rule. Verify with
  `grep -c $'\u2014\|\u2013'` before delivering anything.
- **Zero mentions of the professor/instructor.** Course material is cited by lesson name, never
  by a person's name. Another hard user rule.
- All 35 headline numbers cross-checked against the script's console output.

---

## 5. THE TASK: build the MESA scenario in STK

The graduate requirement, verbatim from `design_project/milestone2/Milestone_2_2026.pdf`:

> Modify the default satellite model in STK to one closer to your design and analyze its
> power and drag characteristics.
> - Right click on the satellite name to pull up the "Properties" menu, then go to 3D
>   graphics/model. Try a few different model styles to find one closest to your proposed design.
> - Go to utilities on the top menu and select component browser. Go to Power Sources and
>   modify them to fit your scenario.
> - Use the "Solar Panel" and "Lifetime" functions under the "Satellite" menu. Plot the
>   satellite's power output over a one-day period and estimate its mission life

**`STK_MESA_scenario_guide.md` has the full step-by-step with every value pre-filled.** Use it.

### The MESA parameter card

Every number STK needs. These all come from the report, so the scenario and the write-up
agree. Do not invent different values.

| Parameter | Value | Report reference |
|:---|---:|:---|
| Scenario epoch | 20 Mar 2027 00:00:00 UTCG | vernal equinox, worst-case eclipse |
| Duration | exactly 1 day | grad requirement |
| Semi-major axis | 42,164.137 km | Eq. (1) |
| Eccentricity | 0.0 | Eq. (1) |
| Inclination | 0.0 deg | Eq. (1) |
| Subsatellite longitude | 105 deg W | §6 |
| Propagator | Two-Body | Astrogator is a paid module, not needed |
| Wet mass | 2,000 kg | Table 3 |
| Bus envelope | 1.8 x 1.8 x 3.5 m | Table 3 |
| Solar array area | 10.24 m² (2 wings) | Table 3 |
| Drag area | 16.54 m² | Table 3 |
| Drag coefficient | 2.2 | §7 |
| Cell efficiency BOL | 30%, packing 0.90, temp derate 0.90 | §12.1 |
| Array output BOL | 3,387 W | Eq. (12) |
| Array output EOL (5 yr) | 2,984 W | Eq. (12) |
| Peak load | 1,773 W | Table 7 |
| Orbit-average load | 1,200 W | Table 7 |
| **Eclipse duration at equinox** | **69.4 min** | Eq. (11) |

### Can Claude actually drive STK? Yes, with caveats to verify first

STK 12 ships a **Python API** and a **Connect** command interface, so the scenario can be
built programmatically rather than by clicking. Approach:

```python
from agi.stk12.stkdesktop import STKDesktop
stk = STKDesktop.StartApplication(visible=True, userControl=True)
root = stk.Root
root.NewScenario("MESA_MS2")
root.ExecuteCommand('...')      # Connect commands
```

The API wheel ships **inside the STK install**, typically:
`C:\Program Files\AGI\STK 12\bin\AgPythonAPI\agi.stk12-*.whl`
Install it into a venv with `pip install <that wheel>`.

**Verify these three things on the machine before committing to the scripted path:**

1. **Does the license tier expose the automation API?** STK Free may gate Connect/API
   access. If it does, fall back to the GUI walkthrough in `STK_MESA_scenario_guide.md`.
2. **Are the Solar Panel and Lifetime tools available and API-accessible?** They may be
   GUI-only depending on tier.
3. **Exact Connect syntax for a 3D window snapshot.** Check the local STK help
   (Help → Connect Command Library) rather than guessing. Guessed Connect syntax fails silently.

Being straight about confidence: the overall approach (Python API + Connect) is solid and
well documented. The exact snapshot command and the license gating are the parts that need
checking against the installed docs. If scripting stalls for more than a short while, **just
do it in the GUI** and move on. Three screenshots are the deliverable, not elegant automation.

### Expect this result, it is not a bug

**STK's Lifetime tool will report that the orbit does not decay.** That is physically
correct at GEO and it is exactly what report §7 concludes (drag-decay timescale of 10⁵ to
10⁶ years). Screenshot it and say so in the write-up. A tool that confirms the analysis is
a better result than one that just prints a number.

Optional and strong: re-run Lifetime with the same vehicle at **400 km** and compare against
the 298 days in Table 2. If STK is in the same ballpark, §7's model is independently validated.

---

## 6. What to produce

Into `design_project/milestone2/submission/stk/`:

| File | Content |
|:---|:---|
| `MESA_MS2/` (whole folder, zipped) | The scenario. STK scenarios are folders, not single files |
| `fig9_stk_3d.png` | 3D view: MESA + Earth + orbit trail |
| `fig10_stk_power.png` | Solar panel power over one day (should show the eclipse notch) |
| `fig11_stk_lifetime.png` | Lifetime tool report |

---

## 7. Wiring the results into the report

This is the **only** part of `Clayton_spce5065_ms2_submission.md` you should edit.

1. **Add a §12.3 "STK scenario verification"** after §12.2, containing Figures 9, 10, 11
   with captions, and a sentence stating the scenario file is submitted alongside the report.
2. **Record the three cross-checks** against the Python model, honestly:

   | Quantity | Python model | STK | Where |
   |:---|---:|:---|:---|
   | Eclipse duration at equinox | 69.4 min | *(from STK)* | Eq. (11) |
   | Array power BOL | 3,387 W | *(from STK)* | Eq. (12) |
   | GEO orbital decay | none, 10⁵ to 10⁶ yr | expect "does not decay" | Eq. (3) |

3. **If STK disagrees by more than a few percent, do not paper over it.** Say so in the
   report and work out which model is wrong. Fabricating agreement in an academic submission
   is not acceptable.
4. **Update the Revision Log item 1**, which currently says the 3D fix was done in matplotlib.
   Once STK is in, it should say the visual simulation is now an STK scenario, with the
   matplotlib 3D view retained as the reproducible analysis.
5. **Rebuild the docx** and re-verify (Section 9 below).

**Do not write STK results into the report before STK has produced them.**

---

## 8. Standing user rules (these are hard)

From `./memory/` in the repo. Read those files; the highlights:

- **Zero em dashes (—) and en dashes (–).** Anywhere. Use a colon, comma, parentheses,
  semicolon, or split the sentence. Grep to verify before delivering.
- **Never mention the professor, instructor, or lecturer** in the submission, and never frame
  a result as "matching" what they said. Cite course material by lesson name only.
- **Number references by first appearance in the body** (AIAA), and **inline-cite every
  external value at its point of use**. HW1 lost 4 points on exactly this.
- **Spell out numbers ≤10** in running text (a MS1 grammar deduction). Keep numerals for
  measured quantities with units, table entries, and section/figure/reference numbers.
- **Match HW1 density.** Sanity checks are one to two sentences, no labeled justification
  paragraphs. Conceptual answers stay substantive.
- **First-person voice**, boxed final answers via `$$\boxed{...}$$`.

---

## 9. Verification before calling it done

```bash
cd design_project/milestone2/submission

# 1. Analysis script still runs clean
python spce5065_ms2_figs.py

# 2. Rebuild the docx
pandoc Clayton_spce5065_ms2_submission.md -o Clayton_spce5065_ms2_submission.docx

# 3. Image count must equal the figure count INCLUDING the cover
python -c "import zipfile; z=zipfile.ZipFile('Clayton_spce5065_ms2_submission.docx'); print(len([n for n in z.namelist() if n.startswith('word/media/')]))"
```

**The image count is a real trap.** Pandoc silently drops the cover image if it is written as
a raw HTML `<img>` tag, and the build still exits 0. The cover currently uses a markdown
image inside the styled div specifically to avoid this. It is worth 5 rubric points
("cover page includes a conceptual figure"). Currently the count is **9**; after adding
Figures 9 to 11 it must be **12**. See `./memory/feedback_docx_cover_image.md`.

Also verify:
- `grep -c $'\u2014\|\u2013'` returns 0
- `grep -ic 'professor\|instructor\|lecturer'` returns 0
- Citation markers still ascend 1..N by first appearance with none uncited

---

## 10. Known gotchas

- **Pandoc drops raw HTML in docx.** Affects the cover image and the HTML table of contents.
  The document uses a `` ```{=openxml} `` block to inject a real Word TOC field (page numbers
  and hyperlinks, which fixes a MS1 grammar deduction) and a `` ```{=html} `` block for the
  markdown-rendered TOC. Each format gets exactly one TOC. Do not "simplify" this.
- **The Word TOC field shows placeholder text until Word updates it.** It carries
  `w:dirty="true"` so Word populates it on open. If it looks empty, select it and press F9.
- **Wheel mass and power:** the course's own table (Week 7 Radiation Part 2, slide 11)
  disagrees with SMAD Table 11.12. The report uses the **course** table. Keep it that way.
- **The eclipse only appears at an equinox epoch.** Wrong epoch means STK shows no eclipse
  and silently contradicts Eq. (11).

---

## 11. If STK turns out to be a dead end

Fallback: Jordan has an `orbital-vis` skill on his openclaw bot at
`~/.openclaw/workspace/skills/orbital-vis/` (macOS machine, not Windows). Its `scripts/style.py`
provides `kepler_orbit_eci`, `kepler_state_at_nu`, `earth_sphere`, `ecef_rotation_matrix`,
`save_gif`, and `save_mp4`, so an animated GEO orbit is close to a drop-in. That produces a
moving simulation rather than a static plot, which is a partial answer to the grader's note.

STK is still the better answer, because it is what she named and recommended.

---

## 12. Open question for Jordan

Confirm whether an STK scenario file is actually accepted as a submitted artifact alongside
the docx, or whether she wants only the stills embedded. The report currently plans to
reference the scenario as a separate submission. Worth a quick email to her.
