# SPCE 5065 — HW1 By-Hand Calculation Worksheet

These are the four problems worth doing on paper: **Q7** and **Q8** are clean
single-equation plug-ins (do the whole thing by hand with confidence), and
**Q2 / Q6** are worth a hand pass for the *derivation* plus a spot-check or two
(let the script handle the full curves).

Every step carries units. The **target** line is what the solution script
prints — cover it, work the problem, then check.

**Constants used (all given in the assignment):**

| Symbol | Value | Units |
|---|---|---|
| $\mu_\oplus = GM_\oplus$ | $398{,}600.5$ | km³/s² |
| $R_E$ | $6378.0$ | km |
| $G$ | $6.6743\times10^{-11}$ | N·m²/kg² |
| $S_e$ (irradiance at 1 AU) | $1366.1$ | W/m² |
| $e_\oplus$ (Earth eccentricity) | $0.016710$ | — |
| 1 day | $86{,}400$ | s |

---

## Q2 — Circular orbital velocity & period

### Derivation (do this part by hand — it's the point of the problem)

Set gravitational pull equal to the centripetal requirement for a circular orbit
of radius $r = R_E + h$:

$$\frac{GM_\oplus m}{r^2} = \frac{m v^2}{r}
\;\;\Longrightarrow\;\; \boxed{v = \sqrt{\frac{\mu}{R_E + h}}}$$

Period is just circumference over speed, $T = 2\pi r / v$, which simplifies to:

$$T = \frac{2\pi r}{\sqrt{\mu/r}} = 2\pi\sqrt{\frac{r^3}{\mu}}
\;\;\Longrightarrow\;\; \boxed{T = 2\pi\sqrt{\frac{(R_E+h)^3}{\mu}}}$$

### Spot-check #1 — surface velocity ($h = 0$)

| Step | Work |
|---|---|
| 1. Radius | $r = R_E + h = 6378 + 0 = 6378\ \text{km}$ |
| 2. Ratio | $\dfrac{\mu}{r} = \dfrac{398600.5}{6378} = 62.496\ \text{km}^2/\text{s}^2$ |
| 3. Root | $v = \sqrt{62.496} = 7.9055\ \text{km/s}$ |

$$\boxed{v_{\text{surface}} = 7.9055\ \text{km/s}}$$

> **Target:** `7.9055 km/s`. This is the classic "first cosmic velocity" (~7.9 km/s) — if it didn't land near 7.9 I'd know I fumbled the radius or a unit.

### Spot-check #2 — GEO period ($h = 35{,}786$ km)

| Step | Work |
|---|---|
| 1. Radius | $r = 6378 + 35786 = 42{,}164\ \text{km}$ |
| 2. Cube | $r^3 = 42164^3 = 7.4959\times10^{13}\ \text{km}^3$ |
| 3. Divide | $\dfrac{r^3}{\mu} = \dfrac{7.4959\times10^{13}}{398600.5} = 1.8806\times10^{8}\ \text{s}^2$ |
| 4. Root | $\sqrt{1.8806\times10^{8}} = 13{,}713\ \text{s}$ |
| 5. $\times 2\pi$ | $T = 2\pi(13713) = 86{,}164\ \text{s}$ |

$$\boxed{T_{\text{GEO}} = 86{,}164\ \text{s} = 23.93\ \text{h}}$$

> **Target:** `86163.56 s`, i.e. one **sidereal day** (86,164 s) to −0.001%. This is the cleanest sanity check in the whole assignment — a geostationary orbit *must* match Earth's rotation period, so matching the sidereal day confirms both the formula and the arithmetic at once.

> **Leave to the script:** the two full curves (v-vs-altitude, T-vs-altitude). Hand-plotting 600 points is not a good use of paper.

---

## Q6 — Solar irradiance extremes (perihelion / aphelion)

Inverse-square law with the orbit at its closest ($r = a(1-e)$) and farthest
($r = a(1+e)$), with $a = 1$ AU so the AU's cancel:

$$S = S_e\left(\frac{1\,\text{AU}}{r}\right)^2,\qquad
S_{\max} = \frac{S_e}{(1-e)^2},\qquad
S_{\min} = \frac{S_e}{(1+e)^2}$$

### Perihelion (max)

| Step | Work |
|---|---|
| 1. $(1-e)$ | $1 - 0.016710 = 0.98329$ |
| 2. Square | $0.98329^2 = 0.96686$ |
| 3. Divide | $S_{\max} = \dfrac{1366.1}{0.96686} = 1412.9\ \text{W/m}^2$ |

$$\boxed{S_{\max} = 1412.9\ \text{W/m}^2}$$

### Aphelion (min)

| Step | Work |
|---|---|
| 1. $(1+e)$ | $1 + 0.016710 = 1.01671$ |
| 2. Square | $1.01671^2 = 1.03370$ |
| 3. Divide | $S_{\min} = \dfrac{1366.1}{1.03370} = 1321.6\ \text{W/m}^2$ |

$$\boxed{S_{\min} = 1321.6\ \text{W/m}^2}$$

> **Targets:** `1412.9` and `1321.6 W/m²`. Sanity check: both straddle the mean $S_e = 1366.1$, and the spread is about $\pm 3.4\%$ — roughly $4e \approx 4(0.0167) = 6.7\%$ peak-to-peak, exactly what a small eccentricity predicts.

> **Leave to the script:** the day-of-year curve. That one needs Kepler's equation $M = E - e\sin E$ solved by Newton–Raphson — iterative, miserable by hand.

---

## Q7 — Mass of Saturn from Titan (Kepler III) — *fully by hand*

Invert Kepler's third law for the central mass. **Work entirely in SI (m, s, kg).**

$$M = \frac{4\pi^2 a^3}{G\,T^2}$$

**Given:** Titan period $T = 14.1$ d, semi-major axis $a = 1{,}110{,}781{,}765$ m.

| Step | Work |
|---|---|
| 1. Period → s | $T = 14.1 \times 86400 = 1{,}218{,}240\ \text{s}$ |
| 2. $T^2$ | $T^2 = (1.21824\times10^6)^2 = 1.4841\times10^{12}\ \text{s}^2$ |
| 3. $a^3$ | $a = 1.110782\times10^9\ \text{m} \Rightarrow a^3 = 1.3705\times10^{27}\ \text{m}^3$ |
| 4. Numerator | $4\pi^2 a^3 = 39.478 \times 1.3705\times10^{27} = 5.4106\times10^{28}$ |
| 5. Denominator | $G\,T^2 = 6.6743\times10^{-11} \times 1.4841\times10^{12} = 99.06$ |
| 6. Divide | $M = \dfrac{5.4106\times10^{28}}{99.06} = 5.4622\times10^{26}\ \text{kg}$ |

$$\boxed{M_{\text{Saturn}} = 5.46\times10^{26}\ \text{kg}}$$

> **Target:** `5.4623e26 kg`. Published value $5.6834\times10^{26}$ kg → **−3.9%**. That error is the *given data* (period rounded to 14.1 d), not your method — a true two-body fit of Titan's real elements lands right on the published mass.

---

## Q8 — Mass of an asteroid from vis-viva — *fully by hand*

One measured state vector (range $r$, speed $v$) plus the semi-major axis $a$ gives
$\mu$, then divide by $G$. **Work in SI.**

$$v^2 = \mu\left(\frac{2}{r} - \frac{1}{a}\right)
\;\;\Longrightarrow\;\;
\mu = \frac{v^2}{\dfrac{2}{r} - \dfrac{1}{a}},\qquad M = \frac{\mu}{G}$$

**Given:** $a = 1.0\times10^6$ m, $r = 1.5\times10^6$ m, $v = 10$ m/s.

| Step | Work |
|---|---|
| 1. $2/r$ | $\dfrac{2}{1.5\times10^6} = 1.3333\times10^{-6}\ \text{m}^{-1}$ |
| 2. $1/a$ | $\dfrac{1}{1.0\times10^6} = 1.0000\times10^{-6}\ \text{m}^{-1}$ |
| 3. Difference | $1.3333\times10^{-6} - 1.0000\times10^{-6} = 3.333\times10^{-7}\ \text{m}^{-1}$ |
| 4. $\mu$ | $\dfrac{v^2}{\;\cdot\;} = \dfrac{10^2}{3.333\times10^{-7}} = 3.000\times10^{8}\ \text{m}^3/\text{s}^2$ |
| 5. Divide by $G$ | $M = \dfrac{3.000\times10^{8}}{6.6743\times10^{-11}} = 4.4949\times10^{18}\ \text{kg}$ |

$$\boxed{M_{\text{asteroid}} = 4.49\times10^{18}\ \text{kg}}$$

> **Target:** `4.4949e18 kg`. The intermediate $\mu = 3.0\times10^8$ comes out suspiciously round — that's by design in the problem, and it's a nice tell that your $2/r - 1/a$ step is right before you ever touch $G$.

---

## Quick answer key (cover until you've worked them)

| Problem | Quantity | By-hand answer | Script target |
|---|---|---|---|
| Q2 | $v$ at surface | $7.9055$ km/s | `7.9055 km/s` |
| Q2 | $T$ at GEO | $86{,}164$ s (sidereal day) | `86163.56 s` |
| Q6 | $S_{\max}$ (perihelion) | $1412.9$ W/m² | `1412.9 W/m²` |
| Q6 | $S_{\min}$ (aphelion) | $1321.6$ W/m² | `1321.6 W/m²` |
| Q7 | Mass of Saturn | $5.46\times10^{26}$ kg | `5.4623e26 kg` (−3.9%) |
| Q8 | Mass of asteroid | $4.49\times10^{18}$ kg | `4.4949e18 kg` |

**Unit discipline reminder:** Q2/Q6 stay in **km and km³/s²** (μ is given in those
units); Q7/Q8 must convert everything to **m, s, kg** because they use $G$ in SI.
Mixing the two is the single most likely way to blow one of these.
