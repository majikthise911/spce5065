# SPCE 5065 - HW2 By-Hand Calculation Worksheet

These are the problems worth doing on paper. **P2, P3, P4a, and P6b** are clean
plug-ins (do the whole thing by hand with confidence). **P1** is worth a hand
pass for the *derivation* plus one spot-check of the decay rate; the actual
223.7-day lifetime comes from a numerical integral, so let the script own that
number. **P4b** and **P6a** are written answers (no arithmetic).

Every step carries units. The **target** line is what the solution script
prints: cover it, work the problem, then check.

**Watch the units.** Two different systems show up in this homework:
- **P1, P2, P4a, P6b** work in **SI (m, s, kg, Pa)**.
- **P3** works in **CGS (cm, atoms/cm³, cm³/atom)** because the erosion yield and
  the atomic-oxygen densities are given in CGS. Convert the ram speed to **cm/s**.
- The **density formula takes altitude in km** but returns **kg/m³**:
  $\rho(h) = 1.020\times10^{7}\,h^{-7.172}$, valid above 150 km.

**Constants and given values:**

| Symbol | Value | Units |
|---|---|---|
| $\mu_\oplus$ | $3.986004418\times10^{14}$ | m³/s² |
| $R_E$ | $6.378137\times10^{6}$ | m |
| $C_D A / m$ (ballistic term) | $2.2\times1/100 = 0.0220$ | m²/kg |
| $I_{sp}$ | $200$ | s |
| $g_0$ | $9.80665$ | m/s² |
| 1 year | $3.156\times10^{7}$ ($365.25\times86400$) | s |
| $E_{\text{Kapton}}$ (erosion yield) | $3.0\times10^{-24}$ | cm³/atom |
| $R$ (universal gas) | $8.314$ | J/(mol·K) |
| $M_{O_2}$ | $0.0319988$ (32.0 g/mol) | kg/mol |
| 1 psia | $6894.757$ | Pa |

---

## P1 - Drag lifetime, 400 km to 150 km

### Derivation (do this by hand: it is the point of the problem)

A circular orbit of radius $a$ has specific energy $\varepsilon = -\mu/(2a)$.
Drag dissipates specific energy at $\dot\varepsilon = -\tfrac12\rho\,(C_DA/m)\,v^3$,
and for a circular orbit $v^2 = \mu/a$. Convert "energy per second" into
"radius per second" with $\dot a = \dot\varepsilon / (d\varepsilon/da)$, where
$d\varepsilon/da = \mu/(2a^2)$:

$$\dot a = \frac{-\tfrac12\rho\,(C_DA/m)\,v^3}{\mu/(2a^2)}
= -\rho\,(C_DA/m)\,a^2\,\frac{v^3}{\mu},
\qquad v^3 = \left(\frac{\mu}{a}\right)^{3/2}$$

$$\boxed{\;\dot a = -\rho\,(C_DA/m)\,\sqrt{\mu\,a}\;}$$

Lifetime is the reciprocal integrated over the fall (deorbit at 150 km):

$$\boxed{\;t = \int_{a_f}^{a_0}\frac{da}{\rho(h)\,(C_DA/m)\,\sqrt{\mu\,a}},
\qquad h = \frac{a - R_E}{1000}\ \text{km}\;}$$

Because $\rho(h)$ sits inside the integral and swings ~3 orders of magnitude from
400 to 150 km, this is a **numerical** integral. That is exactly what "do not
assume an average R" means: R is not frozen.

### Spot-check - initial decay rate at 400 km (do this by hand)

This confirms the months-long lifetime is the right order of magnitude.

| Step | Work |
|---|---|
| 1. Radius | $a = R_E + 400\ \text{km} = 6.378137\times10^{6} + 4.00\times10^{5} = 6.778\times10^{6}\ \text{m}$ |
| 2. Density | $\rho(400) = 1.020\times10^{7}\,(400)^{-7.172} = 2.221\times10^{-12}\ \text{kg/m}^3$ |
| 3. $\sqrt{\mu a}$ | $\sqrt{(3.986\times10^{14})(6.778\times10^{6})} = \sqrt{2.702\times10^{21}} = 5.198\times10^{10}\ \text{m}^2/\text{s}$ |
| 4. $\dot a$ | $-(2.221\times10^{-12})(0.0220)(5.198\times10^{10}) = -2.54\times10^{-3}\ \text{m/s}$ |
| 5. Per day | $\dot a \times 86400 = -219\ \text{m/day} \approx -0.22\ \text{km/day}$ |

$$\boxed{\;\dot a\big|_{400\,\text{km}} \approx -0.22\ \text{km/day}\;}$$

> **Target:** initial decay ~0.2 km/day. At that starting rate the satellite has
> hundreds of km to lose, so a lifetime of *months* is exactly right. The decay
> accelerates hard near the end (density runs away), which is why the final
> number is 223.7 days rather than $250/0.22 \approx 1140$ days.

> **Leave to the script:** the full integral (`223.7 days`) and the P5 sweep.
> Integrating a 3-orders-of-magnitude density by hand is not a paper job.

---

## P2 - Drag-makeup fuel for one year - *fully by hand*

Hold the 400 km orbit: thrust cancels a constant drag deceleration, so
$\Delta v = a_D\,t$, then the rocket equation gives the propellant. Use
$\rho(400) = 2.221\times10^{-12}$ kg/m³ (from P1) and $v = 7668.6$ m/s.

$$a_D = \tfrac12\rho v^2\,(C_DA/m),\qquad
\Delta v = a_D\,t,\qquad
\Delta m = m\left(1 - e^{-\Delta v/(I_{sp}g_0)}\right)$$

| Step | Work |
|---|---|
| 1. $v^2$ | $7668.6^2 = 5.881\times10^{7}\ \text{m}^2/\text{s}^2$ |
| 2. $a_D$ | $\tfrac12(2.221\times10^{-12})(5.881\times10^{7})(0.0220) = 1.437\times10^{-6}\ \text{m/s}^2$ |
| 3. $\Delta v$ | $(1.437\times10^{-6})(3.156\times10^{7}) = 45.35\ \text{m/s}$ |
| 4. Exhaust vel. | $I_{sp}g_0 = 200\times9.80665 = 1961.3\ \text{m/s}$ |
| 5. Ratio | $\Delta v/(I_{sp}g_0) = 45.35/1961.3 = 0.02312$ |
| 6. Exponential | $1 - e^{-0.02312} = 1 - 0.97714 = 0.02286$ |
| 7. Fuel | $\Delta m = 100\times0.02286 = 2.29\ \text{kg}$ |

$$\boxed{\;\Delta m \approx 2.29\ \text{kg of monopropellant}\;}$$

> **Target:** `2.29 kg` (linear approx $m\,\Delta v/(I_{sp}g_0) = 2.31$ kg, within
> 1%, since 45 m/s is tiny next to the 1961 m/s exhaust velocity). About 2% of
> the satellite mass per year: a sensible reboost budget at 400 km.

---

## P3 - Kapton ram erosion at 450 km - *fully by hand*

Erosion depth is yield times fluence, $d = E_{\text{Kapton}}\,\Phi$, with
$\Phi = n\,v\,t$. **Work in CGS.** Ram speed at 450 km is $v = 7640.4$ m/s
$= 7.640\times10^{5}$ cm/s; $t = 3.156\times10^{7}$ s.

Factor out the part common to all three cases, $E\,v\,t$:

$$E\,v\,t = (3.0\times10^{-24})(7.640\times10^{5})(3.156\times10^{7})
= 7.234\times10^{-11}\ \text{cm}^4/\text{atom}$$

Then $d = n \times (E\,v\,t)$, and $1\ \text{cm} = 10^{4}\ \mu\text{m}$:

| Solar activity | $n$ (atoms/cm³) | $d = n\,(E v t)$ (cm) | $d$ (µm/yr) |
|:---|---:|---:|---:|
| Low | $6\times10^{6}$ | $4.34\times10^{-4}$ | $4.34$ |
| Medium | $2\times10^{7}$ | $1.447\times10^{-3}$ | $14.5$ |
| High | $1\times10^{8}$ | $7.234\times10^{-3}$ | $72.3$ |

$$\boxed{\;d_{\text{low}} = 4.34\ \mu\text{m},\quad
d_{\text{med}} = 14.5\ \mu\text{m},\quad
d_{\text{high}} = 72.3\ \mu\text{m}\ \ (\text{per year})\;}$$

> **Targets:** `4.34 / 14.47 / 72.33 µm`. Sanity check: the three scale exactly
> with $n$ (high is $16.7\times$ low, matching $10^{8}/6\times10^{6}$). At high
> activity the loss beats the 50 µm reference panel thickness, so a bare ram
> panel gets eaten through in a year.

---

## P4 - Apollo command module atmosphere

### (a) Mass of oxygen - *fully by hand*

Ideal gas, $m = PVM/(RT)$. Convert pressure first:
$P = 5\ \text{psia} = 5\times6894.757 = 34{,}473.8$ Pa; $T = 21^\circ\text{C} = 294.15$ K;
$V = 5.9$ m³.

| Step | Work |
|---|---|
| 1. $PV$ | $34{,}473.8 \times 5.9 = 2.034\times10^{5}\ \text{J}$ |
| 2. $RT$ | $8.314 \times 294.15 = 2445.6\ \text{J/mol}$ |
| 3. Moles | $n = PV/RT = 2.034\times10^{5}/2445.6 = 83.16\ \text{mol}$ |
| 4. Mass | $m = nM = 83.16 \times 0.0319988 = 2.66\ \text{kg}$ |

$$\boxed{\;m_{O_2} = 2.66\ \text{kg}\;}$$

> **Target:** `2.66 kg`. Sanity check: $m/V = 0.45$ kg/m³, about a third of
> sea-level air density (1.2 kg/m³), which fits a cabin at a third of an atmosphere.

### (b) Recommendation - *written answer, no arithmetic*

No: pure O₂ at 5 psia is the Apollo 1 fire atmosphere. Recommend a two-gas mix
(O₂ plus an inert diluent) with the O₂ partial pressure kept near the sea-level
normoxic value (~3 psia O₂), for example a near-sea-level ~14.7 psia mixed
atmosphere, or NASA's ~8.2 psia / 34% O₂ exploration atmosphere for a
lower-pressure compromise. Write this out; there is nothing to compute.

---

## P6 - Kapton on the ISS

### (a) What Kapton is used for - *written answer, no arithmetic*

Thermal control blankets / multilayer insulation (aluminized Kapton), component
and harness thermal insulation, and electrical / flex-circuit insulation. No
calculation.

### (b) One-year ISS erosion - *fully by hand*

Same model as P3, $d = E_{\text{Kapton}}\,\Phi$, but anchor the fluence to the
measured MISSE-2 value: $8.43\times10^{21}$ atoms/cm² over 3.95 years.

| Step | Work |
|---|---|
| 1. Annual fluence | $\Phi_{\text{yr}} = 8.43\times10^{21}/3.95 = 2.134\times10^{21}\ \text{atoms/cm}^2/\text{yr}$ |
| 2. Erosion | $d = (3.0\times10^{-24})(2.134\times10^{21}) = 6.40\times10^{-3}\ \text{cm}$ |
| 3. To µm | $6.40\times10^{-3}\ \text{cm} \times 10^{4} = 64\ \mu\text{m}$ |

$$\boxed{\;d_{\text{ISS}} \approx 64\ \mu\text{m of bare Kapton per year (ram face)}\;}$$

> **Target:** `64 µm`. Sits between the P3 medium and high cases, which fits: the
> ISS (~400 km) is lower and denser than the 450 km of P3, and MISSE-2 spanned
> active solar years. This is the *bare* rate; real ISS blankets are coated,
> which is why 64 µm/yr does not shred them.

---

## Quick answer key (cover until you have worked them)

| Problem | Quantity | By-hand answer | Script target |
|---|---|---|---|
| P1 | Decay law | $\dot a = -\rho(C_DA/m)\sqrt{\mu a}$ | (derivation) |
| P1 | Initial decay at 400 km | $\approx 0.22$ km/day | (order-of-magnitude) |
| P1 | Lifetime 400 to 150 km | (numerical) | `223.7 days` |
| P2 | $\Delta v$ over one year | $45.35$ m/s | `45.35 m/s` |
| P2 | Makeup fuel | $2.29$ kg | `2.29 kg` |
| P3 | Erosion low / med / high | $4.34 / 14.5 / 72.3$ µm | `4.34 / 14.47 / 72.33 µm` |
| P4a | O₂ mass | $2.66$ kg | `2.66 kg` |
| P6b | ISS erosion, 1 yr | $64$ µm | `64.0 µm` |

**Unit discipline reminder:** P1/P2/P4a/P6b in SI (m, s, kg, Pa); P3 in CGS
(cm, atoms/cm³). The density formula always takes **h in km** and returns
**kg/m³**, so plug altitude in km even while the rest of P1/P2 is in meters.
Mixing the two systems is the single most likely way to blow one of these.
