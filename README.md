# SPCE 5065 — Space Environment Interactions (Summer 2026)

Coursework, homework, and design-project material for **SPCE 5065: Space Environment Interactions**, a graduate course in the Department of Mechanical and Aerospace Engineering at the University of Colorado Colorado Springs (UCCS).

- **Instructor:** Dr. Lynnane George
- **Term:** Summer 2026 (8 weeks, 6/15 – 8/9), fully online
- **Student:** Jordan Clayton

## What the course is about

Space is a place, and like going anywhere, you have to prepare for it. This course covers the properties and effects of the environment that spacecraft and astronauts have to survive, with intensive coverage of the Earth–Sun–Lunar system. The goal is to understand how the harsh space environment damages spacecraft and harms humans so that missions can be designed to be robust against it.

The material is organized into roughly six parts:

1. The vacuum environment
2. Neutral atmospheric particles
3. Charged particle and plasma interactions
4. The radiation environment
5. Orbital debris (micrometeoroids and MMOD)
6. Human effects (bioastronautics)

Topics span the ionosphere, atmospheric chemistry, radiation belts, magnetosphere, aurora, geomagnetic storms, the celestial background, and bio-astronautic effects. References must follow **AIAA format**.

### Grade weighting

| Assessment | Weight |
|---|---|
| Homework | 25% |
| Final Project | 25% |
| Test 1 | 15% |
| Test 2 | 15% |
| Project Milestones | 15% |
| Current Event Presentation | 5% |

### Schedule at a glance

| Wk | Dates | Content | Due |
|---|---|---|---|
| 1 | 6/15 – 6/21 | The Space Environment; Planet–Sun Relationships | — |
| 2 | 6/22 – 6/28 | Neutral Environment | **HW1** |
| 3 | 6/29 – 7/5 | Bioastronautics | HW2 |
| 4 | 7/6 – 7/12 | Plasma Environment | HW3, **Milestone 1**, Quiz 1 |
| 5 | 7/13 – 7/19 | Micrometeoroids & Orbital Debris | HW4 |
| 6 | 7/20 – 7/26 | Vacuum Environment | HW5 |
| 7 | 7/27 – 8/2 | Radiation Environment | HW6, **Milestone 2** |
| 8 | 8/3 – 8/9 | Review | HW7, **Final Project**, Quiz 2 |

> Note: Milestone 1 is listed as due **3 July 2026** in the project handout (the schedule shows it alongside Week 4 deliverables — check Canvas for the authoritative date).

## Homework 1 (complete — scored 96/100)

HW1 covered space-environment anomalies plus two-body orbital mechanics and solar irradiance. Eight problems:

1. **Spacecraft anomaly** — case study of the *Galaxy 15* "zombiesat" (GEO charging / ESD failure) and the fixes that followed.
2. **Circular-orbit velocity & period vs. altitude** — derive `v = √(μ/(R_E+h))` and `T = 2π√((R_E+h)³/μ)`, plot both.
3. **800 km orbital lifetime vs. solar-cycle phase** — why launch timing barely matters at that altitude.
4. **Hazards for a 350 km optical EO spacecraft** — full Lesson 1 sweep (drag, atomic oxygen, charging, radiation/SAA, debris, contamination, UV, thermal cycling) with mitigations.
5. **Earth's magnetic field** — why it drifts, how we know it reverses, and when the next reversal might come.
6. **Solar irradiance** — `S(r) = S_e (au/r)²` vs. eccentricity, day-of-year, and per planet (log scale).
7. **Mass of Saturn from Titan's orbit** — Kepler's third law, ~4% off and why.
8. **Mass of an asteroid** — vis-viva from a single state vector.

**Result:** 96/100. Both deductions were AIAA **reference-formatting** issues, not physics — number references by first appearance in the body, and cite every external value inline at its point of use. (See `memory/feedback_references.md`.)

Files: `wk01/hw/Clayton_spce_5065_hw1_submission.md` (submission), `wk01/hw/spce_5065_hw1_solution.py` (runnable script that regenerates every figure and number), plus the walkthrough and by-hand worksheet.

## Main assignments

### Current Event Presentation (5%)

- **Topic:** The **vacuum environment** (assigned).
- **Format:** 5–10 minute current-event presentation tied to the week's material.
- **Delivery:** either send a recorded video by **Wednesday 7/22**, or present live on the class Zoom between **6:30–7:00 PM on Thursday 7/23**. (Live is recommended so other students can ask questions.)
- Working notes: `presentation/topic.txt`.

### Design Project — Space Tug and Repair Servicing Satellite (25% final + 15% milestones)

**Selected mission (#1): Space Tug and Repair Servicing Satellite.** Design a servicing satellite that can dock with a cooperative satellite, control its orientation, and provide fuel so it can continue its mission — in the spirit of Northrop Grumman's Mission Extension Vehicle (MEV-1/MEV-2).

Individual project. Standing constraints: **mission duration ≥ 5 years**, **total budget $100M**. The final report must describe the mission purpose, design selections, and the rationale for each, with all supporting calculations. AIAA-format references throughout.

Deliverables:

- **Milestone 1** (due 3 July 2026) — name the system and set mission objectives; summarize the Sun–Earth system and hazards at two of GEO/MEO/LEO; summarize space weather and its impact on a comms downlink; justify why vacuum testing is advisable; **choose an orbit**; include a visual orbit simulation (STK or FreeFlyer); and predict orbital lifetime without stationkeeping.
- **Milestone 2** (Week 7) — refined design.
- **Final Report** (last day of class, Week 8) — complete design with full rationale and calculations.

Working notes: `design_project/topic.txt`.

## Repository layout

```
spce5065/
├── wk01/                 Week 1 — course material (syllabus, schedule) + HW1
│   ├── course_material/
│   └── hw/               HW1 submission, solution script, figures, hand calcs
├── wk02/                 Week 2 — Neutral Environment readings + HW2
├── wk03/                 Week 3 — Bioastronautics + HW3
├── presentation/         Current Event Presentation (vacuum environment)
├── design_project/       Space Tug design project
├── memory/               Project memory / context (synced via git — see CLAUDE.md)
├── prompts/              Workflow prompt scaffolding
└── CLAUDE.md             Project conventions and submission requirements
```

## Conventions

Submission, grading, and file-naming conventions live in `CLAUDE.md`. In short: number AIAA references by first appearance, cite every external value inline, and follow the `spce_5065_<hwN|exN>_*` naming scheme. Accumulated grading feedback and voice calibration are in `memory/`.
