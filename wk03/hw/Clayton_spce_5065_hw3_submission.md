# SPCE 5065: Homework 3
**Bioastronautics, human factors, and the SHELL model for Mars and Ceres**
**Author:** Jordan Clayton
**Date:** July 6, 2026

---

### Approach Overview

1. **These are conceptual, so I anchored every answer to Lesson 3.** Where the lecture gave a hard number (habitable volume tiers, EVA suit pressures, the roadmap colors) I used it and cited it; where it did not (astronaut calorie count, planetary environment data) I pulled the number from a NASA source and cited that instead.
2. **Q4, Q5, Q7 all hinge on the same idea:** a mission gets harder as it gets longer and as gravity gets weaker, so I ran that thread through the volume recommendation, the Ceres roadmap, and the three EVA suits.
3. **Q8 is a real weighted trade study,** not a vibe. I scored all eight options against five criteria, let the math pick the top three, and kept the two runners-up in the writeup so the tradeoff is visible.
4. **Q6 and Q9 both use the SHELL model,** so I drew it once (Figure 2) and reused it. Apollo 13 for the single case, Challenger versus Columbia for the comparison, because that pair is the cleanest illustration of the same organizational failure repeating.

---

## Problem 1: Current-Events Presentations (2 July)

> *For the current events presentations on Thursday 2 July: (a) Summarize the presentation, (b) Describe something you learned from it, (c) Write one question you have left about the presentation.*

There were two presentations, so I summarized both.

**(a) Summaries.**

**Shelby Schreckenberg, "Bioastronautics overview" [1].** This was a broad survey of the field: bioastronautics is the study of how living things exist and behave in space, a blend of biology and astrodynamics, and it took off as a research area after Apollo 11. She walked through the standard microgravity medical problems (bone-density loss like accelerated osteoporosis, muscle atrophy, fluid shift causing facial puffiness and congestion, cardiovascular changes, a suppressed immune system, space motion sickness in the first few days, and balance/orientation problems on return) and then the countermeasures the ISS actually flies: onboard exercise machines, ultrasound and even MRI capability, light therapy plus melatonin for circadian control, radiation sensors, and closed-loop air and water recycling. She closed on the "what's next": more research, longer-duration missions, and astronauts self-documenting their own adaptation.

**Grace Burns, "AVATAR on Artemis II" [2].** This one was a genuine current event. AVATAR (Virtual Astronaut Tissue Analog Response) is an organ-on-a-chip experiment flying on Artemis II to measure how radiation and microgravity damage human tissue. The trick is that each chip is patient-specific: for every tissue type there are two identical chips, one stays on Earth and one flies, and after the mission you compare the pair for DNA damage, cell growth, and immune response, cross-checked against the astronaut's own pre- and post-flight blood. Each chip is about the size of a USB drive and is built from bone-marrow stem cells (which can become red cells, white cells, and platelets, so the chips can mimic heart, brain, liver, and immune tissue). The company Emulate isolates those stem cells from the leftovers of an ordinary platelet donation using magnetic beads, and Space Tango built the automated, battery-powered, self-contained payload [2].

**(b) Something I learned.** From Burns: the stem cells for the organ chips come from the *waste* fraction of a normal platelet donation at a clinic, pulled out with magnetic beads, rather than from any invasive marrow biopsy of the astronaut [2]. That is a clever, non-invasive sourcing trick I had no idea about. From Schreckenberg: the ISS carries ultrasound and MRI, and crew with only general medical training run the scans and downlink the data [1]. I had assumed anything beyond first aid waited for return.

**(c) Question I have left.** For AVATAR: an organ-on-a-chip is a tiny, actively-perfused system with its own micro-environment, so how much of the radiation and fluid-behavior response actually transfers to a whole 70 kg human? A chip has none of the body's systemic regulation (hormones, a real immune system, an actual skeleton absorbing dose), so I want to know what the validation plan is for showing the chip response predicts crew-level outcomes and not just chip-level artifacts [2]. (Separately, the lecture's own open thread fits here: the professor is having students model whether anyone could even survive the radiation dose of a crewed Ceres mission, which is exactly the kind of question AVATAR-type data would inform [3].)

---

## Problem 2: Altered Vestibular Function and Its Symptoms

> *What is meant by "altered vestibular functions" and what are its symptoms?*

**What it means.** The vestibular system is the balance apparatus in the inner ear: the otolith organs (utricle and saccule) sense linear acceleration and, on the ground, which way gravity points, and the three semicircular canals sense rotation [3]. On Earth those signals agree with what your eyes and your muscles/joints are telling you, and your brain fuses them into a solid sense of up and down. In free fall the otoliths stop getting the steady gravity pull, so that channel goes silent while vision and the canals keep reporting. "Altered vestibular function" is that sensory conflict: the professor put it as "your ability to sense what's up and down interferes with your inner ear, and that keeps you off balance," with astronauts floating oriented every which way and no consistent sense of down [3].

**Symptoms.** The lecture grouped these as Space Adaptation Syndrome, "the equivalent of car sick in that environment" [3]:

- **Space motion sickness in the first few days:** nausea, vomiting, malaise, headache, sweating, and loss of appetite while the brain reweights its inputs [1], [3].
- **Spatial disorientation and visual illusions:** a wrong sense of self-motion or of the vehicle tumbling, and difficulty telling floor from ceiling.
- **Degraded eye-head coordination and gaze stabilization,** which makes reading instruments and tracking targets harder right when tasks are most critical.
- **Post-landing readaptation problems back in gravity:** balance, posture, gait, and orientation all suffer, usually clearing in a few days to a few weeks depending on how long the crew was up [1], [3]. The professor's vivid version: Nick Hague and others "pretty much have to be carried out of their landing capsule" to reorient to 1 g [3].

A few things worth flagging: susceptibility is hard to predict crew-to-crew, and men have shown up as *more* susceptible than women [3]. The Mars punchline the lecture kept returning to is that nobody is standing on Mars to carry a wobbly crew out of the lander, so on the Bioastronautics Roadmap this is still a risk without a mature countermeasure [3], [4]. That "who catches them on arrival" problem is the whole reason it stays yellow-to-red for exploration missions.

---

## Problem 3: Astronaut Caloric Intake and Two Free-Fall Nutritional Requirements

> *What are approximate caloric intake requirements for astronauts? Describe two unique nutritional requirements driven by the free-fall environment.*

**Caloric intake.** Energy demand in orbit is close to the ground demand, because the crew still does hours of hard resistive exercise every day. NASA sizes intake from the WHO energy equations scaled by an activity factor, which lands most crew members in the range below [5]:

$$\boxed{\text{Astronaut energy intake} \approx 2{,}500 \text{ to } 3{,}000\ \text{kcal/day, about } 2{,}700\ \text{kcal/day for a typical crew member} \; [5]}$$

That tracks with the lecture's mass-balance framing, where a typical astronaut moves roughly 5 kg per day in and out, of which about 3.5 kg is potable water [3]. Now two requirements that free fall specifically drives:

**1. Vitamin D supplementation, tied to bone and calcium management.** Weight-bearing bone demineralizes at roughly 1 to 1.5% per month in free fall, dumping calcium into the blood and urine [5]. There is no sunlight exposure through the hull, so the skin makes essentially no vitamin D, and vitamin D is what lets the gut absorb calcium and keep bone turnover in check. So NASA supplements vitamin D directly (crews get a routine of vitamins and calcium) and pairs it with the daily loading exercise [3], [5]. The lecture's memorable version of why this matters: early station toilets kept clogging because nobody planned for how much calcium the crews were shedding [3].

**2. Electrolyte and mineral rebalancing, specifically lower sodium and lower iron.** Both cut against microgravity physiology. High dietary sodium accelerates bone resorption and calcium loss and pushes renal-stone risk up, so NASA reformulated space food to be lower in sodium [5]. Iron is the subtler one: red-cell mass drops in free fall ("space anemia") because the body needs less circulating volume, so surplus dietary iron is not going into hemoglobin and instead promotes oxidative stress and adds to the stone-forming load, so NASA holds iron intake down rather than up [5].

Both requirements run against ground intuition, where you would happily load up on salt and iron. In free fall you hold sodium and iron down, and you lean on supplemental vitamin D plus targeted calcium to fight the bone loss (crews do take calcium to replace what the bones shed [3]), rather than just eating more of everything.

---

## Problem 4: Recommended Habitable Volume for a Mars Mission

> *For a Mars mission, what habitable volume would you recommend for the crew quarters on the (a) flight there, (b) surface, (c) return flight? Explain your rationale.*

**Assumptions:** crew of 4, long-stay conjunction-class profile, so roughly a 6 to 7 month (about 210 day) transit each way and about a 500 day surface stay. "Habitable volume" here is usable pressurized volume per crew member, not gross internal volume.

The lecture gave the two anchor numbers: about **5 m³ per person is tolerable** (survivable, miserable) and about **17 m³ per person is optimal** [3]. That matches the classic Celentano habitability curve, where per-person volume needs rise with mission duration and level off around 18 to 20 m³ once you are past a few months [6]. Every Mars phase is a long-duration phase, so my recommendations all sit at or above that optimal asymptote, nudged by what makes each phase hard. **Figure 1** shows the curve with my three picks marked.

![Figure 1: Habitable volume per crew member vs. mission duration with recommended Mars-phase volumes](figures/fig1_habitable_volume.png)

**Table 1:** Recommended habitable volume per crew member by mission phase.

| Phase | Duration | Recommended volume | Driving factor |
|:---|:---|---:|:---|
| (a) Outbound transit | ~210 days | 20 m³/person | Long confinement in 0 g, no outside, isolation still building |
| (b) Surface | ~500 days | 25 m³/person | Longest phase, heavy EVA/science workload, but 0.38 g helps |
| (c) Return transit | ~210 days | 22 m³/person | Deconditioned crew, morale sag on the "we already did it" leg |

$$\boxed{\text{(a) } 20\ \text{m}^3/\text{person} \quad\text{(b) } 25\ \text{m}^3/\text{person} \quad\text{(c) } 22\ \text{m}^3/\text{person}}$$

**Rationale.**

- **(a) Outbound, 20 m³:** at the optimal asymptote. It is a half-year of 0 g in a can with no external environment to escape into, and the crew is still forming as a team, so I want them at the "optimal," not "performance," tier from day one [3], [6]. Cutting volume here to save mass is the kind of decision that shows up later as a Liveware-Liveware problem.
- **(b) Surface, 25 m³ (a bit above optimal):** this is the longest and most operationally intense phase, with EVA prep, sample handling, and science stacking on top of daily living, so people need workspace as well as living space. The one thing working in my favor is 0.38 g, which restores some sense of up/down and lets you stack and store, so the extra volume is easier to build with landed or inflatable habitats than it would be in transit [6].
- **(c) Return, 22 m³:** I keep it slightly above the outbound number even though the phase length is the same. The crew comes home physically deconditioned and, per the Mars 500 "third-quarter" finding, motivation tends to dip on the homeward leg once the big goal is behind them [3], [4]. Squeezing the habitat right when morale is most fragile is exactly wrong, so I trade a little return mass for volume.

Across all three, the SHELL angle matters: private crew quarters (part of the volume budget) are a Liveware-Liveware mitigation, giving each person somewhere to decompress, which the psychology block flagged as central to long-duration crews [3]. Below about 10 m³ per person you are in the "performance" band where people function but degrade, and 5 m³ is bare survival [3], [6]. Nothing about a two-plus-year Mars mission belongs in either.

---

## Problem 5: Bioastronautics Roadmap, Extended to Ceres

> *NASA's Bioastronautics Roadmap provides overall ratings for a human Mars mission. (a) Complete the columns for a Ceres mission. (b) Choose three specific areas and discuss them more thoroughly: how would the risk be different for Ceres, and what might be a mitigation strategy?*

**Assumptions for the Ceres profile:** Ceres sits at 2.77 AU in the asteroid belt, so a crewed mission is a multi-year round trip (several years even with a Mars gravity assist), the surface gravity is only about 0.029 g, essentially still free fall, and one-way communication runs up to roughly half an hour [3], [7]. Those three facts (longer, more radiation, weaker gravity) drive almost every rating up.

**(a) Completed table.** I carried over NASA's Mars ratings from the roadmap and rated Ceres by the same red/yellow/green scheme, where red means no mitigation exists, yellow means partial mitigation, and green means well mitigated [4].

**Table 2:** Bioastronautics Roadmap ratings, Mars (per NASA) and Ceres (my ratings). R = red, Y = yellow, G = green.

| Risk | Mars op. | Mars long | Ceres op. | Ceres long |
|:---|:---:|:---:|:---:|:---:|
| Adverse Cognitive/Behavioral Conditions & Psychiatric Disorders | R | Y | R | R |
| Adverse Health/Performance Effects of Celestial Dust Exposure | R | R | R | R |
| Adverse Health Effects Due to Host-Microorganism Interactions | Y | Y | R | R |
| Adverse Health Event Due to Altered Immune Response | Y | Y | R | R |
| Adverse Health Outcomes from Medical Conditions (in-mission & long-term) | R | R | R | R |
| Adverse Outcomes from Inadequate Human Systems Integration | R | N/A | R | N/A |
| Altered Sensorimotor/Vestibular Function | Y | G | R | Y |
| Bone Fracture from Spaceflight-Induced Bone Changes | R | Y | R | R |
| Cardiovascular Adaptations | R | Y | R | R |
| Reduced Muscle Size, Strength, Endurance | Y | G | R | Y |
| Ineffective or Toxic Medications | R | R | R | R |
| Injury & Compromised Performance from EVA Operations | R | Y | R | R |
| Injury from Dynamic Loads | R | N/A | R | N/A |
| Behavioral Health Decrements from Inadequate Team Cooperation | R | N/A | R | N/A |
| Crew Illness from Inadequate Food and Nutrition | R | R | R | R |
| Sleep Loss, Circadian Desynchronization, Work Overload | Y | Y | R | R |
| Radiation Carcinogenesis | G | Y | R | R |
| Reduced Aerobic Capacity | Y | G | R | Y |
| Renal Stone Formation | R | R | R | R |
| Spaceflight-Associated Neuro-ocular Syndrome (SANS) | R | R | R | R |

The pattern is that Ceres pushes nearly everything toward red. The three levers are the same every time: the mission is years longer so exposures accumulate, cumulative galactic-cosmic-ray dose climbs with time, and the ~0.03 g surface means the "surface" phase gives essentially none of the gravitational reloading that lets several Mars risks (muscle, aerobic, vestibular) sit green long-term [3], [4], [7].

**(b) Three areas in depth.**

**1. Radiation Carcinogenesis (Mars G/Y, Ceres R/R).** This is the biggest jump. For a Mars mission NASA rates in-mission carcinogenesis green and long-term yellow because the ~2.5 year exposure stays within managed limits [4]. A Ceres mission is a multi-year cruise through deep space, so cumulative GCR dose runs well past career limits, which is exactly why the judges at the professor's conference argued nobody could survive the trip [3], [7]. *Mitigation:* use Ceres itself. It is a water-ice-rich body, so you shield with mass you do not have to launch: bank water and regolith around a dedicated storm-shelter sleep station, park the surface habitat under regolith, and add pharmacological radioprotectants and aggressive dosimetry with a hard "get to the shelter" protocol during solar events. Shortening the transit with a higher-energy trajectory also directly cuts the integrated dose.

**2. Altered Sensorimotor/Vestibular Function (Mars Y/G, Ceres R/Y).** On Mars the long-term rating is green because 0.38 g reloads the balance system once the crew lands, so they readapt [4]. Ceres has almost no surface gravity, so the "surface" is really just more free fall, and the crew never gets that reloading during a years-long stay. That turns a Mars in-mission annoyance into a chronic, mission-length problem, and the "who carries them out on arrival" issue from Problem 2 has no gravity to resolve it [3]. *Mitigation:* supply the gravity the destination will not. A rotating habitat or a short-arm centrifuge for scheduled artificial-gravity loading is the real fix, backed by the daily resistive/vestibular exercise program and pre-mission adaptability training. This is the one Ceres risk where the answer is essentially "build the artificial gravity you skipped for Mars."

**3. Adverse Cognitive/Behavioral Conditions and Psychiatric Disorders (Mars R/Y, Ceres R/R).** Already red in-mission for Mars, and I push the long-term to red for Ceres. The stressors the psychology block named all get worse: the isolation runs years instead of months, the comm delay stretches toward half an hour each way so the crew is fully autonomous, and Earth shrinks to a dim dot instead of a visible planet [3], [7]. The Mars 500 study already showed circadian disruption and a third-quarter motivation slump over 520 simulated days, and Ceres is several times longer [3]. *Mitigation:* front-load it, because 80% of a flight psychologist's work happens before launch [3]. Select and train for autonomy and cohesion together, guarantee private crew quarters (tie back to Problem 4's volume), build in structured routines, exercise, family contact, and give the crew real onboard behavioral-health tools and autonomy since they cannot phone a therapist in real time. Prevention beats treatment here because there is no evacuation.

---

## Problem 6: Apollo 13 Breakdowns and the SHELL Model

> *Describe the major breakdowns and disconnects that occurred during the Apollo 13 mission. Which elements of the SHELL model were involved?*

**The breakdowns.** On 13 April 1970, about 56 hours into the flight, oxygen tank 2 in the service module exploded during a routine cryogenic stir [8]. The chain behind it is a stack of disconnects:

- **A documentation/design disconnect that had been latent for years.** The tank's internal heater used thermostatic switches still rated for the old 28 V ground supply, but the spec was never updated when the command module moved to 65 V. On a pre-flight detank the switches welded shut, the heater cooked the Teflon insulation off the nearby fan wiring, and nobody caught it [8].
- **A routine crew action triggered the latent fault.** When the crew ran the standard "stir the cryo tanks" procedure, the fan motor energized the exposed wiring, it arced, the insulation ignited in the pure-oxygen tank, and the tank blew, taking out a line to tank 1 as well [8].
- **Cascading system loss.** The explosion vented both oxygen tanks and killed two of the three fuel cells, so the command module lost most of its power, water, and oxygen. That is when the crew radioed "Houston, we've had a problem," and the mission goal instantly collapsed from "land on the Moon" to "get everyone home alive" [8].
- **A hardware-interface mismatch under stress.** With the crew living in the lunar module lifeboat, its CO2 scrubbers overloaded, and the command module's square lithium-hydroxide canisters did not fit the LM's round receptacles. Ground engineers had to invent the "mailbox" adapter out of onboard parts and read the procedure up to the crew [8].

**SHELL elements involved.** All five, which is exactly the lecture's point that disasters come from interactions, not a single cause [3]. **Figure 2** is the model I use for both this problem and Problem 9.

![Figure 2: SHELL human-factors model, human at center](figures/fig2_shell_model.png)

- **Hardware (H):** the mis-specified thermostat switches, the damaged wiring, the ruptured tank, and the LiOH canister that would not fit [8].
- **Software (S), meaning procedures and documentation:** the voltage spec that never propagated to the switch rating, the stir procedure that unknowingly triggered the fault, and the improvised scrubber procedure that had to be written on the fly [8].
- **Environment (E):** deep space with finite consumables, a freezing powered-down cabin, and rationed water, which is what turned an equipment failure into a survival problem.
- **Liveware (L), the crew:** flying a crippled ship, executing the manual PC+2 free-return burn by hand, and holding it together cold and dehydrated.
- **Liveware-Liveware (L-L):** the crew-to-Mission-Control coordination that actually saved them. The professor's framing was that the single unmistakable goal ("get everyone home") unified every decision on both sides and cut confusion, which is the human-factors success buried inside the hardware failure [3].

The clean lesson is that the fatal-looking hardware breakdown was seeded by a paperwork breakdown years earlier, and it was recovered by the L-L interface working the way it should. Same model, opposite outcomes, at two different interfaces.

---

## Problem 7: EVA Suit Requirements for the Moon, Mars, and Ceres

> *Propose requirements for an EVA suit for a human mission to the (a) Moon, (b) Mars, (c) Ceres. Include a discussion of the unique aspects of the destination.*

Every suit has to do the same core job the lecture stressed: carry everything a human needs, so oxygen, CO2 removal, water, comms, thermal control, and pressure, all self-contained [3]. The shared design baseline from the lecture is in **Table 3**; then each destination adds its own hard problem.

**Table 3:** EVA design baseline from Lesson 3 (U.S. values, with Russian figures for contrast) [3].

| Parameter | U.S. | Russia |
|:---|:---:|:---:|
| Suit operating pressure | 29.6 kPa | 39.2 kPa |
| Pre-breathe (N2 washout) | 100% O2, ~1 hr | ~30 min |
| Target bends ratio R (habitat N2 / suit N2) | ~1.5 ideal | ~1.5 ideal |
| Max EVA duration | ~8 hr | ~7 hr |
| Life-support pack mass | ~55 kg | ~120 kg |

Every suit keeps R (the ratio of nitrogen partial pressure in the cabin to that in the suit) near 1.5 to keep decompression sickness off the table, since supersaturated nitrogen coming out of solution is what forms the bubbles that cause the bends [3].

**(a) Moon.** Unique aspects: 1/6 g, hard vacuum, a ~14-day day/night cycle swinging from roughly +120°C in sunlight to below -130°C in shadow (colder in polar permanent shadow), and abrasive, electrostatically-charged regolith with no weathering to round it off [9]. That dust is the killer; it chewed through Apollo suit seals and bearings in three days.
- Dust-tolerant bearings and sealing surfaces, plus a suitport or dust-off protocol so regolith never comes inside.
- Wide thermal range with active heating and cooling for both the lunar day and shadowed work.
- High lower-body and glove mobility for surface tasks in partial gravity.
- Multi-EVA durability and radiation shielding for extended surface campaigns.

**(b) Mars.** Unique aspects: 0.38 g, a thin ~0.6 kPa mostly-CO2 atmosphere (near-vacuum but not vacuum, so there is a little convective heat exchange), global dust storms, fine perchlorate-laden toxic dust, and temperatures from about -125°C to +20°C [10]. The mission also runs hundreds of EVAs over a ~500 day stay with no resupply, and, per Problem 2, no ground crew to catch a wobbly astronaut on arrival [3].
- Reusable and field-maintainable for hundreds of cycles, because you cannot ship spares.
- Perchlorate/dust mitigation and airlock design that keeps the toxic fines out of the habitat.
- Regenerable life support sized for the CO2 atmosphere, with thermal control tuned for convection plus radiation.
- Because it operates in real gravity, suit mass and center of gravity actually matter here, unlike free-fall EVA, so keep it light and mobile.

**(c) Ceres.** Unique aspects: ~0.03 g (basically an orbital EVA even while "standing" on the surface), 2.77 AU from the Sun so very low solar flux and extreme cold, a tenuous water-vapor exosphere near vacuum, and high cumulative GCR from the deep-space environment [3], [7].
- Microgravity-EVA architecture: handholds, tethers, and a jetpack (SAFER-style) for translation, because there is no meaningful gravity to walk in.
- Heavy insulation and active heating for cryogenic surface temperatures far from the Sun.
- Maximum practical radiation shielding and strict EVA dose budgeting, since this is the flagship red risk from Problem 5.
- Very long service life and in-situ repair, plus tolerance for icy/salty regolith, for a years-long mission.

The through-line: the Moon suit fights dust and thermal swing, the Mars suit fights durability and toxic fines in partial gravity, and the Ceres suit is really a deep-space orbital suit that has to survive cold and radiation for years. Gravity drops and distance grows as you go down the list, and the suit problem shifts from "surface mobility" toward "keep a human alive in deep space" the whole way.

---

## Problem 8: Weighted Trade Study, 1,500 kg Mars Crew-Health Allocation

> *NASA has allocated an additional 1,500 kg of launch mass for improving crew health during a 900-day Mars mission. Invest the mass in only three of: radiation shielding, exercise equipment, food variety, medical equipment, private crew quarters, water reserves, artificial gravity demonstration hardware, additional scientific equipment. Develop a weighted trade study with objectives, evaluation criteria, weighting factors, trade matrix, and final recommendation.*

**Assumptions:** the baseline vehicle already carries minimal exercise gear, standard food, and basic meds, so the 1,500 kg is an augmentation on top of that. Crew of 4, no realistic abort or evacuation once en route.

**Objective.** Spend the 1,500 kg to maximize crew health, safety, and mission-effective performance across 900 days, prioritizing the risks that are life-threatening and currently unmitigated (the red rows from Problem 5) [4].

**Evaluation criteria and weights.** I weighted survival highest, then the two big long-duration health domains, then coverage and mass efficiency:

- **C1 Crew survival / acute life-threat reduction (0.30)**
- **C2 Chronic physiological health: bone, muscle, cardiovascular, aerobic (0.20)**
- **C3 Behavioral and psychological health / morale (0.20)**
- **C4 Coverage of an unmitigated (red) roadmap risk (0.15)**
- **C5 Mass efficiency, health benefit per kg over 900 days (0.15)**

**Trade matrix.** Each option scored 1 (poor) to 5 (excellent); the weighted total is the dot product with the weights. **Figure 3** plots the results.

**Table 4:** Weighted trade matrix. Bold = selected top three.

| Option | C1 (.30) | C2 (.20) | C3 (.20) | C4 (.15) | C5 (.15) | **Total** |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Exercise equipment** | 3 | 5 | 4 | 3 | 4 | **3.75** |
| **Medical equipment** | 5 | 2 | 2 | 5 | 3 | **3.50** |
| **Radiation shielding** | 5 | 1 | 2 | 5 | 2 | **3.15** |
| Food variety | 2 | 2 | 5 | 3 | 4 | 3.05 |
| Private crew quarters | 2 | 1 | 5 | 4 | 3 | 2.85 |
| Water reserves | 3 | 1 | 1 | 2 | 2 | 1.90 |
| Artificial-gravity demo hardware | 2 | 3 | 1 | 2 | 1 | 1.85 |
| Additional science equipment | 1 | 1 | 2 | 1 | 2 | 1.35 |

![Figure 3: Weighted trade-study scores for the eight options](figures/fig3_trade_study.png)

**Final recommendation.**

$$\boxed{\text{Invest the 1,500 kg in exercise equipment, medical equipment, and radiation shielding}}$$

A defensible split: ~300 kg to advanced resistive and cardio exercise hardware, ~400 kg to a real diagnostic/surgical/pharmacy medical kit with telemedicine, and ~800 kg to a water-and-polyethylene storm-shelter augmentation around the sleep station.

**Why these three.**
- **Exercise equipment (3.75)** wins because without it the deconditioning is near-certain and mission-ending: bone, muscle, and cardiovascular loss over 900 days would leave the crew unable to work on arrival, and it is a well-understood, high-benefit-per-kg countermeasure that also helps morale [3], [4].
- **Medical equipment (3.50)** covers the "medical conditions in-mission" red row, which is life-or-death with no evacuation. One appendicitis or one bad injury with no kit is a dead crew member [4].
- **Radiation shielding (3.15)** is the flagship red risk. It scored a notch lower only because 1,500 kg buys just a partial storm shelter, not full-mission shielding, so its benefit-per-kg is the weakest of the three. It is too dangerous to skip, so it takes the third slot [4].

**The honest tradeoff.** Food variety (3.05) missed the cut by one line, and it is the one I would revisit: over 900 days, morale and appetite really do drive performance (the Mars 500 and Schirra stories both make that point), so if the medical or shielding masses came in lighter than budgeted, food variety is where I would spend the leftover [3]. Private crew quarters (2.85) is strong on psychology but overlaps with the volume I already recommended in Problem 4, so I did not double-buy it. Artificial-gravity *demonstration* hardware (1.85) scored low on purpose: a demo protects future crews, not this one, and 1,500 kg is nowhere near enough for mission-effective artificial gravity. Additional science (1.35) is not a crew-health investment at all, which is the objective here.

---

## Problem 9: SHELL Comparison of Two Accidents (Challenger and Columbia)

> *Using the SHELL model, compare two human-spaceflight accidents. Evaluate as applicable: common failure modes (in the SHELL context), organizational influences, design deficiencies, operational decisions, and lessons that remain relevant for Artemis or Mars.*

I picked Challenger (1986) and Columbia (2003) because they are the same organization making the same mistake seventeen years apart, which is the clearest possible demonstration of the SHELL point that accidents live at the interfaces, not in one broken part [3]. Figure 2 (Problem 6) is the model.

**Table 5:** SHELL comparison of Challenger and Columbia.

| SHELL interface | Challenger (STS-51-L) | Columbia (STS-107) |
|:---|:---|:---|
| Hardware (H) | Solid-rocket-booster O-ring lost resilience in the cold and failed to seal, letting hot gas burn through [11] | Foam from the external tank struck and breached the wing's reinforced-carbon-carbon thermal protection [12] |
| Software (S) = procedures | O-ring erosion had been seen on prior flights and accepted via waivers instead of grounding the fleet [11] | Foam shedding had happened repeatedly and was reclassified as an accepted "in-family" event, not a safety-of-flight issue [12] |
| Environment (E) | Record-cold launch morning, below the O-ring's qualified range [11] | Deep-space/entry environment plus no on-orbit inspection or rescue capability planned [12] |
| Liveware-Liveware (L-L) | Management overrode the engineers who recommended against launching in the cold [11] | Management dismissed engineers' requests for on-orbit imaging of the wing [12] |
| Liveware (L) = crew | No survivable abort mode at that flight phase | No way to inspect or repair the wing from orbit; the damage was already done at launch |

**Common failure modes.** Both are textbook **normalization of deviance**: an anomaly (O-ring erosion, foam strikes) recurs without immediate consequence, so it gets quietly reclassified as acceptable until it kills a crew [11], [12]. In SHELL terms the fatal interface in both is **Liveware-Liveware**, engineering-versus-management, where the people closest to the hardware were overruled by the people closest to the schedule.

**Organizational influences.** Schedule and budget pressure sat behind both. Challenger flew under pressure to keep an aggressive launch cadence; Columbia flew in a program pressured to hit Space Station assembly milestones. In both, the safety organization lacked the independent authority to stop the line, so the S interface (the rules that were supposed to catch these) had been eroded by the culture that wrote the waivers [11], [12].

**Design deficiencies and operational decisions.** Challenger's design deficiency was a joint that leaked when cold, and the operational decision was launching anyway on the coldest morning [11]. Columbia's was a debris-shedding tank plus a thermal-protection system with no on-orbit inspection or repair option, and the operational decision was to wave off the imaging that might have caught it in time [12].

**Lessons that remain relevant for Artemis and Mars.**
- **Do not normalize anomalies.** A recurring off-nominal event is a warning, not a new baseline. This is the single lesson both accidents teach and it applies directly to Artemis hardware maturing under schedule pressure.
- **Protect dissent and independent technical authority.** The engineers were right both times and got overruled both times. A Mars crew is far past any rescue, so the L-L interface between crew, ground, and management has to be built to hear the minority technical voice, which is exactly the coordination the professor credited for saving Apollo 13 [3].
- **Design for inspection and abort.** Columbia had neither. Any Mars-class vehicle needs in-situ damage detection and repair because there is no ground crew and no ride home, which ties straight back to the Problem 5 medical and EVA red risks [4].

The uncomfortable takeaway is that neither accident was a surprise in hindsight, and both had the same root at the same interface. If NASA re-learned it between 1986 and 2003, the standing risk for Artemis and Mars is re-learning it a third time.

---

## Sources Cited

[1] Schreckenberg, S., "Bioastronautics: An Overview of Space Medicine and Human Health," current-events presentation, SPCE 5065, University of Colorado Colorado Springs, 2 July 2026.

[2] Burns, G., "AVATAR: Virtual Astronaut Tissue Analog Response on Artemis II," current-events presentation, SPCE 5065, University of Colorado Colorado Springs, 2 July 2026.

[3] George, L., "Bioastronautics and Human Factors: Lesson 3," SPCE 5065 lecture video and slides, University of Colorado Colorado Springs, 2026.

[4] NASA Human Research Program, "Human Research Roadmap: A Risk Reduction Strategy for Human Space Exploration," NASA, https://humanresearchroadmap.nasa.gov/ [retrieved 6 July 2026].

[5] Smith, S. M., Zwart, S. R., and Heer, M., *Human Adaptation to Spaceflight: The Role of Food and Nutrition*, 2nd ed., NP-2021-08-0021-JSC, NASA Johnson Space Center, Houston, TX, 2021.

[6] Celentano, J. T., Amorelli, D., and Freeman, G. G., "Establishing a Habitability Index for Space Stations and Planetary Bases," AIAA Paper 63-139, 1963.

[7] NASA Science, "Ceres: Facts," NASA Solar System Exploration, https://science.nasa.gov/dwarf-planets/ceres/facts/ [retrieved 6 July 2026].

[8] Cortright, E. M. (chair), "Report of the Apollo 13 Review Board," NASA, Washington, DC, 15 June 1970.

[9] Williams, D. R., "Moon Fact Sheet," NASA Goddard Space Flight Center / NSSDCA, https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html [retrieved 6 July 2026].

[10] Williams, D. R., "Mars Fact Sheet," NASA Goddard Space Flight Center / NSSDCA, https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html [retrieved 6 July 2026].

[11] Rogers, W. P. (chair), "Report of the Presidential Commission on the Space Shuttle Challenger Accident," U.S. Government Printing Office, Washington, DC, 6 June 1986.

[12] Columbia Accident Investigation Board, "Columbia Accident Investigation Board Report, Volume I," NASA and U.S. Government Printing Office, Washington, DC, Aug. 2003.

---

## Appendix: Figure-Generation Script

The three figures were generated by `spce_5065_hw3_solution.py` (in this folder). It is a plain matplotlib script (no physics; this is a conceptual assignment), producing `figures/fig1_habitable_volume.png`, `figures/fig2_shell_model.png`, and `figures/fig3_trade_study.png`. Running `python spce_5065_hw3_solution.py` regenerates all three.
