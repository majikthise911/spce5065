# -*- coding: utf-8 -*-
"""Single source of truth for the vacuum / cold-welding presentation.

Both build_html.py and build_pptx.py import SLIDES and REFERENCES from here,
so the deck and the PowerPoint never drift apart. `notes` on each slide is the
spoken narration (also written into PPTX speaker notes and the script file).

Style rules enforced elsewhere: no em/en dashes anywhere; no mention of the
instructor; AIAA references numbered by first appearance in the talk body.
"""

TITLE = "Cold Welding in the Vacuum Environment"
SUBTITLE = "When spacecraft parts fuse themselves together"
PRESENTER = "Jordan Clayton"
COURSE = "SPCE 5065"
DATE = "July 2026"

SLIDES = [
    {
        "kind": "title",
        "title": TITLE,
        "subtitle": SUBTITLE,
        "meta": f"{PRESENTER}   |   {COURSE}   |   {DATE}",
        "hero": "img/iss_orbit.jpg",
        "credit": "Image: NASA",
        "notes": (
            "Hi, I'm Jordan Clayton. My current-events topic is the vacuum "
            "environment, and I want to look at it through one specific and "
            "slightly strange effect: cold welding, where spacecraft parts can "
            "fuse themselves together in orbit with no heat at all."
        ),
    },
    {
        "kind": "bullets",
        "title": "A weld with no heat, 400 km up",
        "bullets": [
            "In November 2024 an experiment called ASTROBEAT reached the ISS to "
            "test cold welding as a way to repair debris damage to a spacecraft "
            "hull [1][2]",
            "It runs on a phenomenon engineers usually spend careers trying to "
            "prevent",
            "That same physics once jammed a NASA spacecraft's antenna shut",
            "The question for today: how do two metal parts weld together in "
            "orbit with no heat and no welder?",
        ],
        "image": "img/iss_orbit2.jpg",
        "credit": "Image: NASA",
        "notes": (
            "Here is the hook. In November 2024, an experiment called ASTROBEAT "
            "went up to the International Space Station. Its goal is to use cold "
            "welding on purpose, as a way to patch holes punched in a hull by "
            "debris. What is interesting is that cold welding is normally a "
            "failure mode, something designers fight to avoid, and the same "
            "physics once jammed a famous NASA antenna shut. So the question I "
            "want to answer is simple: how can two metal parts weld together in "
            "orbit, with no heat and no welder?"
        ),
    },
    {
        "kind": "figure",
        "title": "Space is not just empty",
        "bullets": [
            "Pressure falls about 13 orders of magnitude from sea level to low "
            "Earth orbit",
            "At ISS altitude it is around 1e-8 Torr, harder than most vacuum "
            "chambers on the ground",
            "The key consequence: almost no oxygen to re-grow the oxide films "
            "that normally protect metal surfaces",
        ],
        "figure": "fig1_pressure_vs_altitude.png",
        "notes": (
            "First, what the vacuum environment actually is. Pressure drops "
            "about thirteen orders of magnitude from the ground to low Earth "
            "orbit. At the Space Station's altitude it is around ten to the "
            "minus eight Torr, which is a harder vacuum than most chambers we "
            "can build on the ground. The consequence that matters for us is "
            "this: there is essentially no oxygen up there to re-grow the oxide "
            "films that normally protect a metal surface."
        ),
    },
    {
        "kind": "figure",
        "title": "Why clean metal is sticky",
        "bullets": [
            "On Earth every metal instantly grows an oxide layer plus adsorbed "
            "gas; those films keep parts from bonding",
            "From our surface-interaction lectures: a truly clean surface has a "
            "high sticking coefficient and bonds readily",
            "In vacuum, once that film is scrubbed off it does not come back",
            "Bare metal on bare metal forms real metallic bonds; the atoms "
            "cannot tell which part they came from [3]",
        ],
        "figure": "fig2_coldweld_schematic.png",
        "notes": (
            "So why is clean metal sticky? On Earth, every metal instantly "
            "grows an oxide layer plus a film of adsorbed gas, and those films "
            "are what keep two parts from bonding when they touch. This ties "
            "straight back to our surface-interaction lectures: a truly clean "
            "surface has a high sticking coefficient and wants to bond. In "
            "vacuum, once that protective film is scrubbed away, it does not "
            "grow back. Now you have bare metal touching bare metal, and the "
            "atoms form real metallic bonds across the joint. The two parts "
            "effectively become one crystal, because the atoms cannot tell "
            "which original piece they belong to. No heat, no melting."
        ),
    },
    {
        "kind": "figure",
        "title": "Static contact is not the danger. Motion is.",
        "bullets": [
            "Flat parts just resting together rarely weld; real surfaces are "
            "rough and the oxide usually survives",
            "The real driver is fretting: tiny vibration during launch, plus "
            "impact, which scrub the film off and press fresh metal together [4]",
            "Worst pairs: soft metals like aluminum and copper, and any metal "
            "against an identical metal",
            "Even dissimilar metals adhere once the surface film is breached [5]",
        ],
        "figure": "fig3_material_pairs.png",
        "notes": (
            "Here is the nuance that separates hype from engineering. Pure "
            "static contact, two flat parts just resting together, rarely welds, "
            "because real surfaces are rough and the oxide usually survives. The "
            "real danger is fretting: tiny oscillating motion, like launch "
            "vibration, and impact. That motion scrubs the film off and presses "
            "fresh metal together, which is essentially a friction weld. The "
            "worst material pairs are soft metals like aluminum and copper, and "
            "any metal against an identical metal. But as this ESA test data "
            "shows, even dissimilar metals adhere with real force once the film "
            "is breached."
        ),
    },
    {
        "kind": "bullets",
        "title": "Case 1: Galileo's antenna, told honestly",
        "bullets": [
            "1991: Galileo's umbrella high-gain antenna stalled with 3 of 18 "
            "ribs stuck [6]",
            "Root cause was loss of the dry MoS2 lubricant, worn away by "
            "vibration over cross-country truck transport, plus pin-and-socket "
            "friction",
            "The antenna never received a thermal-vacuum test before launch",
            "Bare-metal cold welding was a contributor once the lubricant was "
            "gone, not a spontaneous static weld [7]",
        ],
        "image": "img/galileo_a.jpg",
        "credit": "Image: NASA/JPL (Galileo; furled high-gain antenna at top)",
        "notes": (
            "Case one is the classic story, and I want to tell it honestly, "
            "because it is often oversimplified. In 1991, Galileo's umbrella-"
            "style high-gain antenna tried to open and stalled, with three of "
            "its eighteen ribs stuck. NASA's investigation found the main cause "
            "was loss of the dry molybdenum-disulfide lubricant on the rib pins, "
            "worn away by vibration during several cross-country truck trips, "
            "combined with friction in the pin-and-socket joints. It also never "
            "got a thermal-vacuum test before launch. Cold welding of the now-"
            "bare metal was a contributor once the lubricant was gone, but it "
            "was not a spontaneous static weld. Lubricant loss and fretting came "
            "first."
        ),
    },
    {
        "kind": "bullets",
        "title": "Real, but often over-blamed",
        "bullets": [
            "Confirmed and current: ESA testing shows repeated bending of wire "
            "harnesses in vacuum can cold-weld individual strands, stiffening "
            "or even breaking them [7]",
            "The counter-example: NASA's Lucy solar array stuck about 92 percent "
            "open in 2021",
            "Widely blamed online on vacuum sticking, but NASA traced it to a "
            "deployment lanyard that lost tension [8]",
            "Lesson: cold welding is real, but diagnosis matters; not every "
            "stuck deployable is a weld",
        ],
        "image": "img/lucy.jpg",
        "credit": "Image: NASA/KSC (Lucy spacecraft and its solar array)",
        "notes": (
            "Cold welding is real, but it is also one of the most over-cited "
            "facts on the internet, so let me show both sides. On the confirmed "
            "and current side, recent ESA testing shows that repeatedly bending "
            "a wire harness in vacuum can cold-weld the individual strands "
            "together, stiffening the harness or even breaking wires. On the "
            "over-blamed side, NASA's Lucy mission had a solar array stick about "
            "ninety-two percent open in 2021. A lot of people online blamed "
            "vacuum sticking, but NASA actually traced it to a deployment "
            "lanyard that lost tension. The lesson is that cold welding is real, "
            "but careful diagnosis matters. Not every stuck deployable is a weld."
        ),
    },
    {
        "kind": "bullets",
        "title": "Turning the failure mode into a tool",
        "bullets": [
            "ASTROBEAT flips the problem: use cold welding on purpose to patch "
            "hull damage from hypervelocity debris [1]",
            "A technology-readiness-level 6 demonstrator, run on the ISS by a "
            "team led out of Malta",
            "The same adhesion that threatens deployables becomes an in-space "
            "repair method",
            "Why now: growing mega-constellations and debris make on-orbit "
            "repair increasingly worth the effort",
        ],
        "image": "img/hvi2.jpg",
        "credit": "Image: NASA/WSTF (hypervelocity impact test; the damage ASTROBEAT aims to repair)",
        "notes": (
            "Which brings us back to ASTROBEAT. It flips the whole problem "
            "around: instead of preventing cold welding, it uses it on purpose "
            "to patch hull damage from hypervelocity debris impacts. It is a "
            "fairly mature demonstrator, technology-readiness-level six, run on "
            "the Space Station by a team led out of Malta. The same adhesion "
            "that threatens hinges and antennas becomes a repair method. And the "
            "timing makes sense: with mega-constellations and a growing debris "
            "population, being able to repair a spacecraft in orbit is worth "
            "more than ever."
        ),
    },
    {
        "kind": "bullets",
        "title": "How designers fight cold welding",
        "bullets": [
            "Material choice: avoid soft, identical metal pairs in separable "
            "contacts; pair hard against soft",
            "Coatings and dry lubricants like MoS2 help, but ESA found they are "
            "not a guarantee; adhesion returned after about 20 fretting cycles "
            "[9]",
            "Limit fretting with preload and stiff hold-downs, and add redundant "
            "actuators",
            "Protect the lubricant during ground handling, and qualify "
            "deployment in a thermal-vacuum chamber",
        ],
        "image": "img/tvac.jpg",
        "credit": "Image: NASA (thermal-vacuum Chamber A, Johnson Space Center)",
        "notes": (
            "So how do designers actually fight this? Four levers. First, "
            "material choice: avoid soft, identical metal pairs in any contact "
            "that has to separate later, and pair a hard material against a soft "
            "one. Second, coatings and dry lubricants like molybdenum disulfide "
            "help, but ESA testing found they are not a guarantee. Adhesion came "
            "back after only about twenty fretting cycles. Third, limit fretting "
            "itself with preload and stiff hold-downs, and add redundant "
            "actuators so one stuck joint is not fatal. And fourth, protect the "
            "lubricant during ground handling, which is exactly where Galileo "
            "failed, and qualify the deployment in a thermal-vacuum chamber "
            "before flight."
        ),
    },
    {
        "kind": "bullets",
        "title": "Takeaways",
        "bullets": [
            "The vacuum environment is active by absence: no oxide re-growth "
            "means bare metal bonds",
            "Fretting and impact, not static contact, drive real cold-welding "
            "failures",
            "The effect is real but frequently over-cited; the Lucy case shows "
            "why diagnosis matters",
            "Engineers are now using it deliberately, as ASTROBEAT is testing on "
            "the ISS right now",
        ],
        "notes": (
            "To wrap up, four takeaways. The vacuum environment is dangerous by "
            "absence: with no oxide to re-grow, bare metal bonds. Fretting and "
            "impact, not static contact, are what actually drive cold-welding "
            "failures. The effect is real but frequently over-cited, and the "
            "Lucy case shows why you have to diagnose carefully. And finally, "
            "engineers are now turning it into a tool, which is exactly what "
            "ASTROBEAT is testing on the Space Station right now. Thank you."
        ),
    },
    {
        "kind": "references",
        "title": "References",
        "notes": "",
    },
]

# AIAA style, numbered by first appearance in the talk body.
REFERENCES = [
    'ISS National Laboratory, "ISS National Lab-Sponsored Research to Test '
    'Cold Welding for Spacecraft Repairs," ISS National Laboratory, Nov. 2024, '
    "https://issnationallab.org/press-releases/spacex-crs31-mcast-astrobeat-welding/ "
    "[retrieved 21 July 2026].",

    'Malta College of Arts, Science and Technology, "ASTROBEAT," MCAST, 2024, '
    "https://mcast.edu.mt/astrobeat/ [retrieved 21 July 2026].",

    'Merstallinger, A., "Cold Welding: An Underestimated Problem in Space '
    'Engineering," Aerospace and Advanced Composites GmbH, 23 Oct. 2023, '
    "https://www.aac-research.at/cold-welding-an-underestimated-problem-in-space-engineering/ "
    "[retrieved 21 July 2026].",

    "Merstallinger, A., Sales, M., Semerad, E., and Dunn, B. D., "
    '"Assessment of Cold Welding between Separable Contact Surfaces due to '
    'Impact and Fretting under Vacuum," STM-279, European Space Agency, ESTEC, '
    "Noordwijk, The Netherlands, 2009.",

    'Merstallinger, A., et al., "Cold Welding in Hold-Down Points of Space '
    'Mechanisms Due to Fretting When Omitting Grease," Lubricants, Vol. 9, '
    "No. 8, 2021, Art. 72. doi:10.3390/lubricants9080072.",

    '"Galileo High Gain Antenna (HGA) Deployment Failure," Lesson No. 0492, '
    "NASA Lessons Learned Information System, https://llis.nasa.gov/lesson/492 "
    "[retrieved 21 July 2026].",

    "Holzbauer, R., Merstallinger, A., Gaillard, L., and Bamsey, N., "
    '"Cold Welding under Space and Launch Conditions," Proceedings of the 47th '
    "Aerospace Mechanisms Symposium (ESMATS 2024), Paper 519, 2024, "
    "https://www.esmats.eu/amspapers/pastpapers/pdfs/2024/holzbauer.pdf "
    "[retrieved 21 July 2026].",

    '"NASA Suspends Efforts to Fully Deploy Lucy Solar Array," SpaceNews, '
    "20 Dec. 2022, "
    "https://spacenews.com/nasa-suspends-efforts-to-fully-deploy-lucy-solar-array/ "
    "[retrieved 21 July 2026].",

    '"Temperature-Dependent Friction, Wear, and Life of MoS2 Dry-Film '
    'Lubricants for Space Mechanisms: A Comprehensive Review," Lubricants, '
    "2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12316733/ "
    "[retrieved 21 July 2026].",
]
