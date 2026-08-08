# SPCE 5065 -- Final Exam
**Author:** Jordan Clayton
**Date:** August 8, 2026

*I completed this assignment using only authorized references: the textbook, my personal notes, material on the course Canvas page, and a calculator.*

---

## Problem 1: True / False

**a.** High emissivity gives a lower equilibrium temperature. $\boxed{\textbf{TRUE}}$
$T = (Q_{in}/\varepsilon\sigma A)^{1/4}$, so $\varepsilon$ is in the denominator: more emissivity, more heat shed, cooler vehicle [1].

**b.** Safe mode is often used to recover from an MMOD impact. $\boxed{\textbf{TRUE}}$
Safe mode is on the MMOD design-implications list with redundancy and isolation [2]. An impact shows up as an EMI transient or bus fault, and safing buys time to diagnose.

**c.** Free fall and zero gravity are the same. $\boxed{\textbf{FALSE}}$
LEO still has ~91% of surface gravity [3]. Free fall removes the contact forces, not gravity, hence microgravity.

**d.** A large positive bias is best at GEO. $\boxed{\textbf{FALSE}}$
Electrons are ~43x faster than protons, so a positive bias pulls in a huge electron current and worsens differential charging [4]. Standard practice is slightly negative on a common conductive ground.

**e.** REMs and RADs are equivalent in the Van Allen belts. $\boxed{\textbf{FALSE}}$
REM = RAD x RBE, and RBE is 5 to 7 in the belts [5]. They only match where RBE = 1.

**f.** The neutral environment is the same as the vacuum environment. $\boxed{\textbf{FALSE}}$
Vacuum is the absence of matter (radiative-only heat transfer, outgassing, cold welding) [1]; neutral is the residual atmosphere that is still there (drag, atomic oxygen, sputtering, glow) [6].

**g.** Class 10,000 is the most common cleanliness level and equals ISO 7. $\boxed{\textbf{TRUE}}$
Fed-Std-209 class 10,000 maps to ISO Class 7, the standard spacecraft high-bay level [1].

**h.** GCRs are higher-energy than SPE particles. $\boxed{\textbf{TRUE}}$
GCRs run to GeV/nucleon; SPE protons are tens to hundreds of MeV [5]. SPEs win on flux, not energy.

**i.** An SEU permanently damages a device. $\boxed{\textbf{FALSE}}$
An SEU is a soft bit flip that clears on rewrite or reset [5]. Latch-up and burnout are the destructive ones.

**j.** A 1 mm particle in LEO is too small to matter. $\boxed{\textbf{FALSE}}$
The damage table puts 0.1 mm at surface erosion and 1 mm at serious damage [2]. At ~10 km/s it is in the untrackable-but-lethal band.

---

## Problem 2: Multiple Choice

**I. Single-event latch-up.** $\boxed{\textbf{a}}$
A parasitic thyristor turns on, so the part draws excessive current and needs a power cycle; if the current is not interrupted it burns out [5]. (c) overstates it, (b) assumes fault tolerance always works, (d) describes TID.

**II. Outgassing mechanisms (select all).** $\boxed{\textbf{b, d, e}}$
Desorption (surface water, fast), diffusion (bulk, the long tail), decomposition (material breakdown) [1]. Decantation is liquid separation and deflagration is combustion.

**III. Solar UV alters which ratio.** $\boxed{\textbf{c. absorptivity to emissivity}}$
UV darkens coatings, raising $\alpha$ faster than $\varepsilon$, and $\Delta T \cong \frac{T}{4}\frac{\Delta(\alpha/\varepsilon)}{(\alpha/\varepsilon)}$ [1].

**IV. Whipple bumper purpose.** $\boxed{\textbf{b. Vaporize or fragment the projectile}}$
The bumper is deliberately thin: it shocks the particle into a debris cloud, and the standoff lets the cloud spread so the rear wall takes a distributed load [2].

**V. Half-value layer.** $\boxed{\textbf{Reduce the photon flux by one-half}}$
$\Phi/\Phi_0 = (1/2)^{x/\text{HVL}}$, defined on flux, not energy [5]. (Two options are labelled "d," so I am naming the text.)

---

## Problem 3: GEO Sensor at 215 THz

$$\boxed{\textbf{No. Plasma is a non-issue, but 1.394 } \mu\textbf{m sits in a water-vapor absorption band.}}$$

**Wavelength:** $\lambda = c/f = (2.998\times10^8)/(2.15\times10^{14}) = 1.394\ \mu$m, short-wave IR.

**Plasma check.** $f_p = 8.98\sqrt{n_e}$ Hz [4]. Worst case on the path is the day/solar-max F2 peak, which reads off the density profile at roughly $5\times10^{12}$ m$^{-3}$:

$$f_{p,max} = 8.98\sqrt{5\times10^{12}} \approx 20\ \text{MHz}$$

The sensor is ~$10^7$ times higher, and the $1/f^2$ effects (delay, excess range, Faraday rotation) scale away to nothing. The ionosphere is transparent here.

**Atmosphere check.** On the transmittance chart the sea-level curve drops to essentially zero from ~1.35 to 1.45 $\mu$m, a deep H$_2$O band [6]. At 1.394 $\mu$m the sensor is at the bottom of that notch, so it sees water vapor instead of the target.

**Fix:** move into an adjacent window, 1.55 to 1.75 $\mu$m (~175 to 195 THz) or 2.0 to 2.4 $\mu$m; 0.4 to 0.9 $\mu$m also works if the target has a visible or NIR signature. A ~15% shift recovers the link.

---

## Problem 4: Charged-Particle Flux vs Solar Activity

**Table 1:** Flux density correlated with solar activity.

| | Solar Min | Solar Max |
|:---|:---:|:---:|
| **Trapped radiation** | ----- | ----- |
| &nbsp;&nbsp;- electrons | **lower** | **higher** |
| &nbsp;&nbsp;- protons | **higher** | **lower** |
| **Galactic Cosmic Rays** | **higher** | **lower** |
| **Solar Particle Events** | **lower** | **higher** |

- **Electrons:** injected by storms and substorms, which track solar activity [5].
- **Protons:** the only anti-correlated row. Their CRAND source is GCR-fed (suppressed at solar max) and the puffed-up solar-max thermosphere increases the loss rate [7]. Both effects push the same way.
- **GCRs:** the strong solar-max heliospheric field deflects them, so they peak at solar min [5].
- **SPEs:** flares and CMEs cluster within a year or two of sunspot maximum [5].

---

## Problem 5: Severing the N-O Bond

Taking NO as nitric oxide (nitrous oxide is N$_2$O), 1.67 eV is the N-O bond energy.

**(a)** A single photon must carry the full bond energy, so [1]:

$$\lambda_{max} = \frac{hc}{E_{bond}} = \frac{1239.84\ \text{eV}\cdot\text{nm}}{1.67\ \text{eV}} = 742.4\ \text{nm}$$

$$\boxed{\lambda_{max} = 742\ \text{nm} = 0.742\ \mu\text{m}\quad (f_{min} = 404\ \text{THz})}$$

Shorter wavelengths carry more energy and break the bond; longer ones cannot, at any intensity.

**(b)** $\boxed{\textbf{Yes.}}$ 742 nm is at the red edge of the visible, so everything that qualifies is the whole visible band plus all the UV. On the irradiance chart that covers the peak near 500 nm and everything left of it, clearly more than half the area [6]. 1.67 eV is a weak bond (a C-C single bond is 3.47 eV), so the threshold falls out of the UV and into where the Sun puts most of its energy.

---

## Problem 6: Plasma Frequencies at 1000 km

Reading the four curves at the 1000 km row of the given density profile, the spread is about one decade: roughly $10^{10}$ m$^{-3}$ at the low end (night, solar min) to roughly $10^{11}$ m$^{-3}$ at the high end (day, solar max). I am carrying one significant figure because that is all a log plot supports by eye.

$$f_p = \frac{1}{2\pi}\sqrt{\frac{n_e e^2}{\varepsilon_0 m_e}} = 8.98\sqrt{n_e}\ \text{Hz} \quad (n_e \text{ in m}^{-3})\ \text{[4]}$$

$$f_p(10^{10}) = 8.98\sqrt{10^{10}} = 8.98\times10^5 = 0.90\ \text{MHz}$$
$$f_p(10^{11}) = 8.98\sqrt{10^{11}} = 2.84\times10^6 = 2.8\ \text{MHz}$$

$$\boxed{f_p \approx 0.9\ \text{to}\ 2.8\ \text{MHz, call it 1 to 3 MHz}}$$

The square root is why a full decade of density becomes only a $\sqrt{10} = 3.2$x spread in frequency.

**Why we care:**
- It is a hard cutoff, not attenuation. Below $f_p$ the signal reflects and no link margin recovers it.
- A ground link must also clear the F2 peak *beneath* the orbit, ~20 MHz at day/solar max. That is the real gate.
- Above cutoff you still pay the $1/f^2$ costs: group delay, excess range, Faraday rotation (Problem 8).
- It moves by ~3x with local time and solar cycle, plus storms and SIDs, so the link budget carries the worst case.

That is why satellite comms live at hundreds of MHz to tens of GHz.

---

## Problem 7: Three Hazards for a 550 km CubeSat

Ranked by which hazard most certainly breaks a stated requirement over the full 5 years.

**1. Radiation (TID and single-event effects on COTS parts).** Sun-synchronous is polar, so the vehicle crosses the auroral horns every revolution and cuts the SAA repeatedly [5]. Dose accumulates for 5 years with no recovery, and COTS parts have no rad-hard guarantee. This threatens "reliable communications" directly.
- *Mitigation:* spot-shield only the most sensitive devices, add current-limiting latch-up protection on every COTS rail, run EDAC memory behind a watchdog.
- *Tradeoff:* it buys reliability with availability, since every watchdog reset is a comm outage and a data gap. Shielding also spends the binding mass constraint.

**2. Neutral environment (atomic oxygen, drag as a budget item).** Certain and continuous but degrading, not fatal. With $BC = m/C_dA \approx 4/(2.2 \times 0.03) = 61$ kg/m$^2$ [6], integrating $\dot R = -(\rho/BC)\sqrt{\mu R}$ from 550 km loses only ~40 km over 5 years, and that decay helps post-mission disposal. AO is the sharper half: it erodes exposed polyimide hinges, tape, and array adhesives.
- *Mitigation:* AO-resistant externals (germanium-coated black Kapton or SiO$_x$ over polyimide) and a low-frontal-area attitude.
- *Tradeoff:* the overcoats shift $\alpha/\varepsilon$, so the AO fix perturbs the thermal design; the minimum-drag attitude fights payload, array, and antenna pointing.

**3. Plasma (auroral charging and ESD).** Dangerous but episodic, and the cheapest to fix, so it earns the least mass. The polar orbit crosses the auroral oval twice per revolution; the failure mode is the arc, not the potential, and the EMI corrupts the link [4].
- *Mitigation:* partially conductive exterior surfaces (ITO coverglass, conductive paint) bonded to a single chassis ground.
- *Tradeoff:* ITO costs more and shaves array output on a power-starved bus; bonding straps add harness mass and labor.

MMOD is an honorable mention: 550 km is the densest debris shell, but a 3U cross-section makes 5-year collision probability low and there is no mass to shield it.

---

## Problem 8: Worst-Case Excess Range and Delay, 500 km, K-band

**Assumptions:** $f = 18$ GHz, the bottom of K-band, since $\Delta R \propto 1/f^2$ makes the lowest frequency worst; TEC $= 10^{18}$ e/m$^2$ (day, solar max, equatorial anomaly, disturbed), conservative because a 500 km satellite is above the F2 peak so part of the ionosphere is out of the path; obliquity factor 3 for a horizon-grazing pass.

$$\Delta R = \frac{40.31\,\text{TEC}}{f^2} = \frac{40.31 \times 10^{18}}{(1.8\times10^{10})^2} = \frac{4.031\times10^{19}}{3.24\times10^{20}} = 0.1244\ \text{m}$$

$$\Delta t = \frac{\Delta R}{c} = \frac{0.1244}{2.998\times10^8} = 4.15\times10^{-10}\ \text{s}$$

**Table 3:** Worst-case ionospheric error at K-band.

| Case | $f$ | $\Delta R$ | $\Delta t$ |
|:---|---:|---:|---:|
| Vertical, band edge | 18 GHz | 12.44 cm | 0.415 ns |
| Vertical, top of band | 26.5 GHz | 5.74 cm | 0.191 ns |
| Slant (obliquity 3) | 18 GHz | 37.3 cm | 1.24 ns |

$$\boxed{\Delta R \approx 12\ \text{cm},\ \Delta t \approx 0.42\ \text{ns vertical; } 37\ \text{cm and } 1.2\ \text{ns at low elevation}}$$

**Check:** the same TEC at GPS L1 (1.575 GHz) gives 16.2 m and 54 ns, a ratio of 130, matching $(18/1.575)^2 = 130.5$ [4]. Sub-nanosecond means a single-frequency K-band system barely needs an ionospheric correction.

---

## Problem 9: Thermal Design of a Black Cube at 300 km

**Assumptions:** isothermal cube at steady state; one face takes solar, one face takes albedo and Earth IR, and all six radiate since all six are painted; sun and nadir incidence 0$^\circ$; Earth fluxes 1367, 465, and 237 W/m$^2$ with the albedo and IR terms carrying $\sin^2\rho$ and written with $\alpha$ per the course form of Eq. 11-25 [1]; 100 W runs continuously; no solar or albedo term in eclipse.

### (a) Equilibrium temperatures

$$\sin\rho = \frac{6378}{6678} = 0.9551,\qquad \sin^2\!\rho = 0.9122$$

$$Q_{solar} = 0.975(1)(1367) = 1332.8\ \text{W}$$
$$Q_{albedo} = 0.975(1)(0.9122)(465) = 413.6\ \text{W}$$
$$Q_{IR} = 0.975(1)(0.9122)(237) = 210.8\ \text{W}$$

**Table 4:** Energy balance.

| Term | Sunlit (W) | Eclipse (W) |
|:---|---:|---:|
| $Q_{solar}$ | 1332.8 | 0 |
| $Q_{albedo}$ | 413.6 | 0 |
| $Q_{IR}$ | 210.8 | 210.8 |
| $Q_{internal}$ | 100.0 | 100.0 |
| **Total in** | **2057.2** | **310.8** |

With $\varepsilon A_{total} = 0.874(6) = 5.244$ m$^2$:

$$T_{sun} = \left(\frac{2057.2}{0.874(5.67\times10^{-8})(6)}\right)^{1/4} = (6.919\times10^9)^{1/4} = 288.4\ \text{K}$$

$$\boxed{T_{sun} = 288.4\ \text{K} = 15.3\ ^\circ\text{C} \qquad T_{eclipse} = 179.8\ \text{K} = -93.3\ ^\circ\text{C}}$$

### (b) Adequate?

$\boxed{\textbf{No.}}$ Sunlit is 0.3 $^\circ$C past the 15 $^\circ$C ceiling with zero margin before end-of-life UV darkening. Eclipse is 93 $^\circ$C below the operational floor and 83 $^\circ$C below the $-10\ ^\circ$C survival limit [8], every orbit. 100 W cannot hold 6 m$^2$ of high-emissivity surface warm without the Sun.

### (c) Recommended solution

Two constraints bound what the four sides can do:
- Sunlit at 15 $^\circ$C needs $\varepsilon_4 = 0.879$; the catalogue tops out at black paint, 0.874, so the baseline is already the best available hot case.
- Eclipse at 0 $^\circ$C needs $\varepsilon A \le 0.985$ m$^2$, but the two *fixed* black faces alone are 1.748 m$^2$. Heaters are mandatory regardless of coating.

So the hot case wants high emissivity and the cold case wants low, from the same four faces: that calls for variable emissivity.

**Table 5:** Four-side trade at \$25,000/kg, heaters sized to hold 0 $^\circ$C in eclipse [1].

| Option | $T_{sun}$ | $T_{ecl}$ raw | Heater | Mass | Cost |
|:---|---:|---:|---:|---:|---:|
| Black paint (no change) | 15.3 $^\circ$C | $-93.3$ | 1344 W | 33.6 kg | \$840,000 |
| White paint | 16.6 $^\circ$C | $-92.5$ | 1314 W | 32.9 kg | \$821,000 |
| Radiators, $\varepsilon = 0.8$ | 19.5 $^\circ$C | $-90.7$ | 1251 W | 33.7 kg | \$842,000 |
| MLI, $\varepsilon = 0.05$ | 96.3 $^\circ$C | $-42.8$ | 304 W | 8.8 kg | \$220,000 |
| **Louvers, 0.05 to 0.8** | **19.5 $^\circ$C** | $-42.8$ | **304 W** | **16.8 kg** | **\$420,000** |

MLI is cheapest and cooks the vehicle at 96 $^\circ$C. Every fixed high-$\varepsilon$ option needs over 1250 W of heaters, more than twelve times the internal power on a satellite with no arrays.

**Recommendation: louvered radiators on the four side faces plus 304 W of Kapton heaters.** Louvers 4 m$^2$ x 2.1 = 8.40 kg, four controllers 0.80 kg, heaters 304 W x 0.025 = 7.60 kg, total 16.80 kg.

$$\boxed{T_{sun} = 19.5\ ^\circ\text{C (open)} \qquad T_{eclipse} = 0.0\ ^\circ\text{C (closed, heaters on)} \qquad \text{Cost} = \$420{,}000}$$

Sunlit runs 4.5 $^\circ$C over the operational ceiling but stays inside the $-10$ to 25 $^\circ$C survival band [8], and no coating beats the 15.3 $^\circ$C baseline anyway. If the two fixed faces were on the table, the real fix is a low-$\alpha$ finish on the sun face plus MLI elsewhere, cutting the hot input and the cold losses at once for far less mass.

---

## Problem 10: Three Ways to Survive MMOD Impacts

MMOD splits by size: above ~10 cm you track and dodge, below ~1 cm you shield, and the 1 to 10 cm band is neither trackable nor shieldable [2]. The three approaches map onto those regimes.

**1. Whipple shielding, for the sub-centimetre band.** A thin sacrificial bumper at a standoff shocks the particle into a debris cloud; the standoff lets the cloud spread so the rear wall takes a distributed impulse instead of a point punch [2]. Bumper thickness, standoff distance, and rear-wall thickness are sized against a ballistic limit for the design particle; stuffed variants (Nextel and Kevlar in the gap) buy more protection per kilogram. Apply it only where a hole is fatal: pressurized volumes, propellant and pressurant tanks, batteries. *Cost:* mass and packaging volume.

**2. Configuration: reduce, relocate, compartmentalize.** Debris flux peaks on the RAM face, so fly the smallest cross-section into the velocity vector and keep arrays and radiators edge-on. Put avionics, batteries, and harness behind the tanks and primary structure, since existing mass shields for free. Internal bulkheads confine a penetration and its spall cone to one bay. *Cost:* fights the pointing, thermal, and field-of-view layouts the payload wants.

**3. Tolerate the hit: redundancy, isolation, safe mode.** Cross-strapped redundant strings, *physically separated* so one debris cloud cannot take both. Fast current limiters and isolation valves cut a shorted bus or leaking line loose before it propagates. Autonomous safe mode puts the vehicle in a stable, power-positive, ground-commandable state while the anomaly is diagnosed. Backstop with conjunction screening and post-mission disposal. *Cost:* redundancy is mass and power; safing costs availability on every false trip.

The three layers are complementary: configuration is nearly free and should be spent first, Whipple shields cover the small stuff on the few critical components, and fault tolerance catches the rest.

---

## Problem 11 (Bonus): Altitude Rate from an Applied $\Delta V$

Energy method, same path as the drag derivation [6].

**Step 1.** Circular orbit, $a = R$: $\;E = -\dfrac{\mu m}{2R}$

**Step 2.** Differentiate: $\;\dfrac{dE}{dt} = \dfrac{\mu m}{2R^2}\dot R$

**Step 3.** A tangential force does work at $P = Fv$. With $\dot V \equiv F/m$ and $v = \sqrt{\mu/R}$:

$$\frac{dE}{dt} = m\,\dot V\sqrt{\frac{\mu}{R}}$$

**Step 4.** Equate; the mass divides out:

$$\frac{\mu m}{2R^2}\dot R = m\,\dot V\sqrt{\frac{\mu}{R}} \qquad\Longrightarrow\qquad \dot R = \frac{2R^2}{\mu}\dot V\sqrt{\frac{\mu}{R}}$$

$$\boxed{\dot R = 2\,\dot V\sqrt{\frac{R^3}{\mu}} = \frac{2\dot V}{n} = \frac{2R\,\dot V}{v}}$$

Prograde raises, retrograde lowers, and sensitivity grows as $R^{3/2}$.

**Check:** substituting a drag deceleration $\dot V = -\rho v^2/2BC = -\rho\mu/(2\,BC\,R)$ gives

$$\dot R = 2\sqrt{\frac{R^3}{\mu}}\left(-\frac{\rho\mu}{2\,BC\,R}\right) = -\frac{\rho}{BC}\sqrt{\mu R}$$

the drag decay result exactly [6].

---

## Sources Cited

[1] SPCE 5065 Lesson 6 notes and slides, Vacuum Environment Parts 1 and 2 (Canvas), UCCS, Summer 2026.

[2] SPCE 5065 Lesson 5 notes and slides, Micrometeoroids and Orbital Debris Parts 1 to 3 (Canvas), UCCS, Summer 2026.

[3] SPCE 5065 Lesson 3 notes and slides, Bioastronautics (Canvas), UCCS, Summer 2026.

[4] SPCE 5065 Lesson 4 notes and slides, The Plasma Environment Parts 1 to 3 (Canvas), UCCS, Summer 2026.

[5] SPCE 5065 Lesson 7 notes and slides, The Radiation Environment Parts 1 to 3 (Canvas), UCCS, Summer 2026.

[6] SPCE 5065 Lesson 2 notes and slides, The Neutral Environment Parts 1 and 2 (Canvas), UCCS, Summer 2026.

[7] Tribble, A. C., *The Space Environment: Implications for Spacecraft Design*, rev. ed., Princeton Univ. Press, 2003.

[8] Larson, W. J., and Wertz, J. R. (eds.), *Space Mission Analysis and Design*, 3rd ed., Microcosm/Kluwer (Canvas): Table 11.43 component temperature limits, Table 11.49 thermal component masses.
